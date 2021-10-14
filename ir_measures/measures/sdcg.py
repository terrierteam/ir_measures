from ir_measures import measures
from .base import Measure, ParamInfo


class _SDCG(measures.Measure):
    """
    The Scaled Discounted Cumulative Gain (SDCG), a variant of nDCG that assumes more
    fully-relevant documents exist but are not labeled.
    """
    __name__ = 'SDCG'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'dcg': measures.ParamInfo(dtype=str, choices=['log2'], default='log2', desc='DCG formulation'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


SDCG = _SDCG()
measures.register(SDCG)
