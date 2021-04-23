from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _SetP(measures.BaseMeasure):
    """
    The Set Precision (SetP); i.e., the number of relevant docs divided by the total number retrieved
    """
    __name__ = 'SetP'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


SetP = _SetP()
measures.register(SetP)
