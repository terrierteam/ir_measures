from ir_measures import measures
from .base import Measure, ParamInfo


class _RBP(measures.Measure):
    """
    The Rank-Biased Precision (RBP).

::

     @article{Moffat:2008:RPM:1416950.1416952,
       author = {Moffat, Alistair and Zobel, Justin},
       title = {Rank-biased Precision for Measurement of Retrieval Effectiveness},
       journal = {ACM Trans. Inf. Syst.},
       year = {2008},
       url = {http://doi.acm.org/10.1145/1416950.1416952}
     }
    """
    __name__ = 'RBP'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'p': measures.ParamInfo(dtype=float, default=0.8, desc='persistence'),
        'rel': measures.ParamInfo(dtype=int, required=False, desc='minimum relevance score to be considered relevant (inclusive), or NOT_PROVIDED to use graded relevance')
    }


RBP = _RBP()
measures.register(RBP)
