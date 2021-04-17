from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _Bpref(measures.BaseMeasure):
    NAME = 'Bpref'
    DESC = '''
<p>
Binary Preference (Bpref).
TODO: write
</p>
'''
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


Bpref = _Bpref()
measures.register(Bpref)
