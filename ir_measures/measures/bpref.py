from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _Bpref(measures.BaseMeasure):
    """
    Binary Preference (Bpref).
    TODO: write
    """
    __name__ = 'Bpref'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


Bpref = _Bpref()
BPref = Bpref
measures.register(Bpref, ['BPref'])
