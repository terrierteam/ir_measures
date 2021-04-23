from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _R(measures.BaseMeasure):
    """
    Recall@k (R@k). The fraction of relevant documents for a query that have been retrieved by rank k.
    """
    __name__ = 'R'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


R = _R()
measures.register(R)
