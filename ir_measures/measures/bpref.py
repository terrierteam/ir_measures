from ir_measures import measures
from .base import Measure, ParamInfo


class _Bpref(measures.Measure):
    """
    Binary Preference (Bpref).
    This measure examines the relative ranks of judged relevant and non-relevant documents. Non-judged documents are not considered. 
    """
    __name__ = 'Bpref'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


Bpref = _Bpref()
BPref = Bpref
measures.register(Bpref, ['BPref'])
