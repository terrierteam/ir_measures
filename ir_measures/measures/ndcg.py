from ir_measures import measures
from .base import Measure, ParamInfo


class _nDCG(measures.Measure):
    """
    The normalized Discounted Cumulative Gain (nDCG).
    Uses graded labels - systems that put the highest graded documents at the top of the ranking.
    It is normalized wrt. the Ideal NDCG, i.e. documents ranked in descending order of graded label.

::

    @article{Jarvelin:2002:CGE:582415.582418,
      author = {J\"{a}rvelin, Kalervo and Kek\"{a}l\"{a}inen, Jaana},
      title = {Cumulated Gain-based Evaluation of IR Techniques},
      journal = {ACM Trans. Inf. Syst.},
      volume = {20},
      number = {4},
      year = {2002},
      pages = {422--446},
      numpages = {25},
      url = {http://doi.acm.org/10.1145/582415.582418},
    }
    """
    __name__ = 'nDCG'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'dcg': measures.ParamInfo(dtype=str, choices=['log2', 'exp-log2'], default='log2', desc='DCG formulation')
    }


nDCG = _nDCG()
NDCG = nDCG
measures.register(nDCG, ['NDCG'])
