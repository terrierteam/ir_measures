from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _RBP(measures.BaseMeasure):
    """
    The Rank-Biased Precision (RBP)
    TODO: write
    """
    __name__ = 'RBP'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'p': measures.ParamInfo(dtype=float, default=0.8, desc='persistence'),
        'rel': measures.ParamInfo(dtype=int, required=False, desc='minimum relevance score to be considered relevant (inclusive), or NOT_PROVIDED to use graded relevance')
    }


RBP = _RBP()
measures.register(RBP)
