from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _P(measures.BaseMeasure):
    NAME = 'P'
    DESC = '''
<p>
Basic measure for that computes the percentage of documents in the top <span class="param">cutoff</span> results
that are labeled as relevant. <span class="param">cutoff</span> is a required parameter, and can be provided as
<kbd>P@cutoff</kbd>.
</p>
'''
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


P = _P()
measures.register(P)
