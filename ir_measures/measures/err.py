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
    PRETTY_NAME = 'Expected Reciprocal Rank'
    SHORT_DESC = 'An extension of Reciprocal Rank that accounts for both graded relevance and a more realistic user model.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
    }


ERR = _ERR()
measures.register(ERR)
