from experimaestro import config, param
from onir import log, vocab
import torch
from torch import nn

@param("qlen", default=20)
@param("dlen", default=2000)
@param("add_runscore", default=False)
@param("vocab", type=vocab.Vocab)
@config()
class Ranker(nn.Module):
    def initialize(self, random):
        nn.Module.__init__(self)
        self.random = random
        self.logger = log.easy()
        seed = self.random.randint((2**32)-1)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        if self.add_runscore:
            self.runscore_alpha = torch.nn.Parameter(torch.full((1, ), -1.))
        self.vocab.initialize()

    def input_spec(self):
        # qlen_mode and dlen_mode possible values:
        # 'strict': query/document must be exactly this length
        # 'max': query/document can be at most this length
        result = {
            'fields': set(),
            'qlen': self.qlen,
            'qlen_mode': 'strict',
            'dlen': self.dlen,
            'dlen_mode': 'strict'
        }
        if self.add_runscore:
            result['fields'].add('runscore')
        return result

    def forward(self, **inputs):
        result = self._forward(**inputs)
        if len(result.shape) == 2 and result.shape[1] == 1:
            result = result.reshape(result.shape[0])
        if self.add_runscore:
            alpha = torch.sigmoid(self.runscore_alpha)
            result = alpha * result + (1 - alpha) * inputs['runscore']
        return result

    def _forward(self, **inputs):
        raise NotImplementedError

    def save(self, path):
        state = self.state_dict(keep_vars=True)
        for key in list(state):
            if state[key].requires_grad:
                state[key] = state[key].data
            else:
                del state[key]
        torch.save(state, path)

    def load(self, path):
        self.load_state_dict(torch.load(path), strict=False)
