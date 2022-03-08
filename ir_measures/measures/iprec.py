from ir_measures import measures
from .base import Measure, ParamInfo


class _IPrec(measures.Measure):
    """
    Interpolated Precision at a given recall cutoff. Used for building precision-recall graphs.
    Unlike most measures, where @ indicates an absolute cutoff threshold, here @ sets the recall
    cutoff.
    """
    __name__ = 'IPrec'
    NAME = __name__
    PRETTY_NAME = 'Interpolated Precision@recall'
    SHORT_DESC = 'The interpolated precision at a given recall cutoff.'
    AT_PARAM = 'recall'
    SUPPORTED_PARAMS = {
        'recall': measures.ParamInfo(dtype=float, required=True, desc='recall threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


IPrec = _IPrec()
measures.register(IPrec)
