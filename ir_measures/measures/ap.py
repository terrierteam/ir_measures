from ir_measures import measures
from .base import Measure, ParamInfo


class _AP(measures.Measure):
    """
    The [Mean] Average Precision ([M]AP). The average precision of a single query is the mean
    of the precision scores at each relevant item returned in a search results list.
    
    AP is typically used for adhoc ranking tasks where getting as many relevant items as possible is. It is commonly referred to as MAP,
    by taking the mean of AP over the query set.

::

    @article{Harman:1992:ESIR,
      author = {Donna Harman},
      title = {Evaluation Issues in Information Retrieval},
      journal = {Information Processing and Management},
      volume = {28},
      number = {4},
      pages = {439 - -440},
      year = {1992},
    }
    """
    __name__ = 'AP'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


AP = _AP()
MAP = AP
measures.register(AP, ['MAP'])
