from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _Judged(measures.BaseMeasure):
    """
    Percentage of results in the top k (cutoff) results that have relevance judgments. Equivalent to P@k with
    a rel lower than any judgment.
    """
    __name__ = 'Judged'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
    }


Judged = _Judged()
measures.register(Judged)
