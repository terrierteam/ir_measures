from ir_measures import measures
from .base import Measure, ParamInfo, SumAgg


class _INST(measures.Measure):
    """
    INST

::

     @inproceedings{Moffat:2012:MMI:2407085.2407092,
       author = {Moffat, Alistair and Scholer, Falk and Thomas, Paul},
       title = {Models and Metrics: IR Evaluation As a User Process},
       booktitle = {Proceedings of the Seventeenth Australasian Document Computing Symposium},
       year = {2012},
       url = {http://doi.acm.org/10.1145/2407085.2407092}
     }
    """
    __name__ = 'INST'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'T': measures.ParamInfo(dtype=float, default=1.0, desc='TODO'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


class _INSQ(measures.Measure):
    """
    INSQ, a variant of INST

::

     @inproceedings{Moffat:2015:IAM:2838931.2838938,
       author = {Moffat, Alistair and Bailey, Peter and Scholer, Falk and Thomas, Paul},
       title = {INST: An Adaptive Metric for Information Retrieval Evaluation},
       booktitle = {Proceedings of the 20th Australasian Document Computing Symposium},
       year = {2015},
       url = {http://doi.acm.org/10.1145/2838931.2838938}
     }
    """
    __name__ = 'INSQ'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'T': measures.ParamInfo(dtype=float, default=1.0, desc='TODO'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


INST = _INST()
measures.register(INST)

INSQ = _INSQ()
measures.register(INSQ)
