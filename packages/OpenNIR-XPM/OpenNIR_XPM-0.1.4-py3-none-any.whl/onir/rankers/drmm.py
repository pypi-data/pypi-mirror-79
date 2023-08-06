
from experimaestro import param, config, Choices
import torch
from torch import nn
from onir import rankers, modules, vocab, log

@param("nbins", default=29, help="number of bins in matching histogram")
@param(
    "hidden", default=5, help="hidden layer dimension for feed forward matching network"
)
@param(
    "histType", default="logcount", help="histogram type",
    checker=Choices(['count', 'norm', 'logcount'])
)
@param("combine", default="idf", checker=Choices(["idf", "sum"]), help="term gate type")
@config()
class Drmm(rankers.Ranker):
    """
    Implementation of the DRMM model from:
      > Jiafeng Guo, Yixing Fan, Qingyao Ai, and William Bruce Croft. 2016. A Deep Relevance
      > Matching Model for Ad-hoc Retrieval. In CIKM.
    """
    def initialize(self, random):
        super().initialize(random)
        self.encoder = self.vocab.encoder()
        if not self.encoder.static():
            self.logger.warn('In most cases, using vocab.train=True will not have an effect on DRMM '
                        'because the histogram is not differentiable. An exception might be if '
                        'the gradient is proped back by another means, e.g. BERT [CLS] token.')
        self.simmat = modules.InteractionMatrix()
        self.histogram = {
            'count': CountHistogram,
            'norm': NormalizedHistogram,
            'logcount': LogCountHistogram
        }[self.histType](self.nbins)
        channels = self.encoder.emb_views()
        self.hidden_1 = nn.Linear(self.nbins * channels, self.hidden)
        self.hidden_2 = nn.Linear(self.hidden, 1)
        self.combine = {
            'idf': IdfCombination,
            'sum': SumCombination
        }[self.combine]()

    def input_spec(self):
        result = super().input_spec()
        result['fields'].update({'query_tok', 'doc_tok', 'query_len', 'doc_len', 'query_idf'})
        result['qlen_mode'] = 'max'
        result['dlen_mode'] = 'max'
        return result

    def _forward(self, **inputs):
        simmat = self.simmat.encode_query_doc(self.encoder, **inputs)
        qterm_features = self.histogram_pool(simmat, inputs)
        BAT, QLEN, _ = qterm_features.shape
        qterm_scores = self.hidden_2(torch.relu(self.hidden_1(qterm_features))).reshape(BAT, QLEN)
        return self.combine(qterm_scores, inputs['query_idf'])

    def histogram_pool(self, simmat, inputs):
        histogram = self.histogram(simmat, inputs['doc_len'], inputs['doc_tok'], inputs['query_tok'])
        BATCH, CHANNELS, QLEN, BINS = histogram.shape
        histogram = histogram.permute(0, 2, 3, 1)
        histogram = histogram.reshape(BATCH, QLEN, BINS * CHANNELS)
        return histogram


class CountHistogram(nn.Module):
    def __init__(self, bins):
        super().__init__()
        self.bins = bins

    def forward(self, simmat, dlens, dtoks, qtoks):
        BATCH, CHANNELS, QLEN, DLEN = simmat.shape

        # +1e-5 to nudge scores of 1 to above threshold
        bins = ((simmat + 1.00001) / 2. * (self.bins - 1)).int()
        weights = ((dtoks != -1).reshape(BATCH, 1, DLEN).expand(BATCH, QLEN, DLEN) * \
                      (qtoks != -1).reshape(BATCH, QLEN, 1).expand(BATCH, QLEN, DLEN)).float()
        # apparently no way to batch this... https://discuss.pytorch.org/t/histogram-function-in-pytorch/5350
        bins, weights = bins.cpu(), weights.cpu() # WARNING: this line (and the similar line below) improve performance tenfold when on GPU
        histogram = []
        for superbins, w in zip(bins, weights):
            result = []
            for b in superbins:
                result.append(torch.stack([torch.bincount(q, x, self.bins) for q, x in zip(b, w)], dim=0))
            result = torch.stack(result, dim=0)
            histogram.append(result)
        histogram = torch.stack(histogram, dim=0)
        histogram = histogram.to(simmat.device) # WARNING: this line (and the similar line above) improve performance tenfold when on GPU
        return histogram


class NormalizedHistogram(CountHistogram):
    def forward(self, simmat, dlens, dtoks, qtoks):
        result = super().forward(simmat, dlens, dtoks, qtoks)
        BATCH, QLEN, _ = simmat.shape
        return result / dlens.reshape(BATCH, 1).expand(BATCH, QLEN)


class LogCountHistogram(CountHistogram):
    def forward(self, simmat, dlens, dtoks, qtoks):
        result = super().forward(simmat, dlens, dtoks, qtoks)
        return (result.float() + 1e-5).log()


class SumCombination(nn.Module):
    def forward(self, scores, idf):
        return scores.sum(dim=1)


class IdfCombination(nn.Module):
    def forward(self, scores, idf):
        idf = idf.softmax(dim=1)
        return (scores * idf).sum(dim=1)
