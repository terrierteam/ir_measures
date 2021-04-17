from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _AP(measures.BaseMeasure):
    NAME = 'AP'
    DESC = '''
<p>
The [Mean] Average Precision ([M]AP).
TODO: finish
</p>
'''
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


AP = _AP()
measures.register(AP)
