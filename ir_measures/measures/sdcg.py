from ir_measures import measures
from .base import Measure, ParamInfo


class _SDCG(measures.Measure):
    """
    The Scaled Discounted Cumulative Gain (SDCG), a variant of nDCG that assumes more
    fully-relevant documents exist but are not labeled.

::

     @inproceedings{Moffat:2015:IAM:2838931.2838938,
       author = {Moffat, Alistair and Bailey, Peter and Scholer, Falk and Thomas, Paul},
       title = {INST: An Adaptive Metric for Information Retrieval Evaluation},
       booktitle = {Proceedings of the 20th Australasian Document Computing Symposium},
       year = {2015},
       url = {http://doi.acm.org/10.1145/2838931.2838938}
     }
    """
    __name__ = 'SDCG'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'dcg': measures.ParamInfo(dtype=str, choices=['log2'], default='log2', desc='DCG formulation'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


SDCG = _SDCG()
measures.register(SDCG)
