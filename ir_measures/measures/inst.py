from ir_measures import measures
from .base import Measure, ParamInfo, SumAgg


class _INST(measures.Measure):
    """
    INST, a variant of INSQ

::

     @inproceedings{10.1145/2766462.2767728,
       author = {Bailey, Peter and Moffat, Alistair and Scholer, Falk and Thomas, Paul},
       title = {User Variability and IR System Evaluation},
       year = {2015},
       booktitle = {Proceedings of the 38th International ACM SIGIR Conference on Research and Development in Information Retrieval},
       pages = {625–634},
       series = {SIGIR '15},
       url = {https://doi.org/10.1145/2766462.2767728}
     }
    """
    __name__ = 'INST'
    NAME = __name__
    PRETTY_NAME = 'INST'
    SHORT_DESC = 'An improved version of INSQ that better handles when either no documents or all retrieved documents are relevant.'
    SUPPORTED_PARAMS = {
        'T': measures.ParamInfo(dtype=float, default=1.0, desc='total desired gain (normalized)'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


class _INSQ(measures.Measure):
    """
    INSQ

::

     @inproceedings{Moffat:2012:MMI:2407085.2407092,
       author = {Moffat, Alistair and Scholer, Falk and Thomas, Paul},
       title = {Models and Metrics: IR Evaluation As a User Process},
       booktitle = {Proceedings of the Seventeenth Australasian Document Computing Symposium},
       year = {2012},
       url = {http://doi.acm.org/10.1145/2407085.2407092}
     }
    """
    __name__ = 'INSQ'
    NAME = __name__
    PRETTY_NAME = 'INSQ'
    SHORT_DESC = 'A weighted precision measure based on the conditional probability of the user continuing to the next item.'
    SUPPORTED_PARAMS = {
        'T': measures.ParamInfo(dtype=float, default=1.0, desc='total desired gain (normalized)'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


INST = _INST()
measures.register(INST)

INSQ = _INSQ()
measures.register(INSQ)
