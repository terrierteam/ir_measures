from ir_measures import measures
from .base import Measure, ParamInfo


class _SetP(measures.Measure):
    """
    The Set Precision (SetP); i.e., the number of relevant docs divided by the total number retrieved
    """
    __name__ = 'SetP'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'relative': measures.ParamInfo(dtype=bool, default=False, desc='calculate the measure using the maximum possible SetP for the provided result size'),
    }

SetP = _SetP()
SetRelP = _SetP(relative=True)
measures.register(SetP)
measures.register(SetRelP, name='SetRelP')


class _SetR(measures.Measure):
    """
    The Set Recall (SetR); i.e., the number of relevant docs divided by the total number of relevant documents
    """
    __name__ = 'SetR'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }

SetR = _SetR()
measures.register(SetR)

class _SetF(measures.Measure):
    """
    The Set F measure (SetF); i.e., the harmonic mean of SetP and SetR
    """
    __name__ = 'SetF'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'beta': measures.ParamInfo(dtype=float, default=1., desc='relative importance of R to P in the harmonic mean'),
    }

SetF = _SetF()
measures.register(SetF)

class _SetAP(measures.Measure):
    """
    The unranked Set AP (SetAP); i.e., SetP * SetR
    """
    __name__ = 'SetAP'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
    }

SetAP = _SetAP()
measures.register(SetAP)
