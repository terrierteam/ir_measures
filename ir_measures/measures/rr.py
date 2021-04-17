from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _RR(measures.BaseMeasure):
    NAME = 'RR'
    DESC = '''
<p>
The [Mean] Reciprocal Rank ([M]RR) is a precision-focused measure that scores based on the reciprocal of the rank of the
highest-scoring relevance document. An optional <span class="param">cutoff</span> can be provided to limit the
depth explored. <span class="param">rel</span> (default 1) controls which relevance level is considered relevant.
</p>
'''
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


RR = _RR()
measures.register(RR)
