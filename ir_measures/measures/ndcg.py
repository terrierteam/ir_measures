from ir_measures import measures
from .base import Measure, ParamInfo


class _nDCG(measures.Measure):
    """
    The normalized Discounted Cumulative Gain (nDCG).
    Uses graded labels - systems that put the highest graded documents at the top of the ranking.
    It is normalized wrt. the Ideal NDCG, i.e. documents ranked in descending order of graded label.
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
