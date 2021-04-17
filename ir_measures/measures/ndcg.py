from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _nDCG(measures.BaseMeasure):
    NAME = 'nDCG'
    DESC = '''
<p>
The normalized Discounted Cumulative Gain (nDCG).
TODO: finish
</p>
'''
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'dcg': measures.ParamInfo(dtype=str, choices=['log2', 'exp-log2'], default='log2', desc='DCG formulation')
    }


nDCG = _nDCG()
measures.register(nDCG)
