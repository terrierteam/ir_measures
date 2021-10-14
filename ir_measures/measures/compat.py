from ir_measures import measures
from .base import Measure, ParamInfo


class _Compat(measures.Measure):
    """
    Compatibility measure desribed in:

::

    @article{10.1145/3451161,
      author = {Clarke, Charles L. A. and Vtyurina, Alexandra and Smucker, Mark D.},
      title = {Assessing Top-k Preferences},
      journal = {ACM Transactions on Information Systems},
      volume = {39},
      number = {3},
      articleno = {33},
      numpages = {21},
      year = {2021},
      url = {https://doi.org/10.1145/3451161},
    }
    """
    __name__ = 'Compat'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'p': measures.ParamInfo(dtype=float, default=0.95, desc='persistence'),
        'normalize': measures.ParamInfo(dtype=bool, default=True, desc='apply normalization for finite ideal rankings'),
    }


Compat = _Compat()
measures.register(Compat)
