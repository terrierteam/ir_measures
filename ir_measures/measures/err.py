from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _ERR(measures.BaseMeasure):
    """
    The Expected Reciprocal Rank (ERR) is a precision-focused measure.
    TODO: finish
    """
    __name__ = 'ERR'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
    }


ERR = _ERR()
measures.register(ERR)
