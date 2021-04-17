from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _R(measures.BaseMeasure):
    NAME = 'R'
    DESC = '''
<p>
Recall@k (R@k).
TODO: write
</p>
'''
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


R = _R()
measures.register(R)
