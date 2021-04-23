from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _nDCG(measures.BaseMeasure):
    """
    The normalized Discounted Cumulative Gain (nDCG).
    TODO: finish
    """
    __name__ = 'nDCG'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'dcg': measures.ParamInfo(dtype=str, choices=['log2', 'exp-log2'], default='log2', desc='DCG formulation')
    }


nDCG = _nDCG()
NDCG = nDCG
measures.register(nDCG, ['NDCG'])
