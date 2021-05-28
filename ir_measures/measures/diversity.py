from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _ERR_IA(measures.BaseMeasure):
    """
    TODO
    """
    __name__ = 'ERR_IA'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _nERR_IA(measures.BaseMeasure):
    """
    TODO
    """
    __name__ = 'nERR_IA'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _alpha_DCG(measures.BaseMeasure):
    """
    TODO
    """
    __name__ = 'alpha_DCG'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'alpha': measures.ParamInfo(dtype=float, default=0.5, desc='Redundancy intolerance'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _alpha_nDCG(measures.BaseMeasure):
    """
    TODO
    """
    __name__ = 'alpha_nDCG'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'alpha': measures.ParamInfo(dtype=float, default=0.5, desc='Redundancy intolerance'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _NRBP(measures.BaseMeasure):
    """
    TODO
    """
    __name__ = 'NRBP'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'alpha': measures.ParamInfo(dtype=float, default=0.5, desc='Redundancy intolerance'),
        'beta': measures.ParamInfo(dtype=float, default=0.5, desc='Patience'),
    }

class _nNRBP(measures.BaseMeasure):
    """
    TODO
    """
    __name__ = 'nNRBP'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'alpha': measures.ParamInfo(dtype=float, default=0.5, desc='Redundancy intolerance'),
        'beta': measures.ParamInfo(dtype=float, default=0.5, desc='Patience'),
    }

class _AP_IA(measures.BaseMeasure):
    """
    TODO
    """
    __name__ = 'AP_IA'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _P_IA(measures.BaseMeasure):
    """
    TODO
    """
    __name__ = 'P_IA'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _STREC(measures.BaseMeasure):
    """
    TODO
    """
    __name__ = 'STREC'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
    }



ERR_IA = _ERR_IA()
nERR_IA = _nERR_IA()
alpha_DCG = _alpha_DCG()
α_DCG = alpha_DCG
alpha_nDCG = _alpha_nDCG()
α_nDCG = alpha_nDCG
NRBP = _NRBP()
nNRBP = _nNRBP()
AP_IA = _AP_IA()
P_IA = _P_IA()
STREC = _STREC()

measures.register(ERR_IA)
measures.register(nERR_IA)
measures.register(alpha_DCG, aliases=['α_DCG'])
measures.register(alpha_nDCG, aliases=['α_nDCG'])
measures.register(NRBP)
measures.register(nNRBP)
measures.register(AP_IA)
measures.register(P_IA)
measures.register(STREC)
