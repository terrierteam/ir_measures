from ir_measures import measures
from .base import Measure, ParamInfo


class _BPM(measures.Measure):
    """
    The Bejeweled Player Model (BPM).

::

     @inproceedings{Zhang:2017:EWS:3077136.3080841,
       author = {Zhang, Fan and Liu, Yiqun and Li, Xin and Zhang, Min and Xu, Yinghui and Ma, Shaoping},
       title = {Evaluating Web Search with a Bejeweled Player Model},
       booktitle = {SIGIR},
       year = {2017},
       url = {http://doi.acm.org/10.1145/3077136.3080841}
     }
    """
    __name__ = 'BPM'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'T': measures.ParamInfo(dtype=float, default=1., desc='total desired gain (normalized)'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


BPM = _BPM()
measures.register(BPM)
