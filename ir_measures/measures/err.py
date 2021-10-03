from ir_measures import measures
from .base import Measure, ParamInfo


class _ERR(measures.Measure):
    """
    The Expected Reciprocal Rank (ERR) is a precision-focused measure.
    In essence, an extension of reciprocal rank that encapsulates both graded relevance and
    a more realistic cascade-based user model of how users brwose a ranking.
    """
    __name__ = 'ERR'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
    }


ERR = _ERR()
measures.register(ERR)
