from ir_measures import measures
from .base import Measure, ParamInfo


class _NERR8(measures.Measure):
    """
    Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (8) of the the following paper.

::

     @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
       author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
       title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
       booktitle = {ICTIR},
       year = {2021},
       url = {https://doi.org/10.1145/3471158.3472239}
     }
    """
    __name__ = 'NERR8'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }

class _NERR9(measures.Measure):
    """
    Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (9) of the the following paper.

::

     @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
       author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
       title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
       booktitle = {ICTIR},
       year = {2021},
       url = {https://doi.org/10.1145/3471158.3472239}
     }
    """
    __name__ = 'NERR9'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }

class _NERR10(measures.Measure):
    """
    Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (10) of the the following paper.

::

     @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
       author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
       title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
       booktitle = {ICTIR},
       year = {2021},
       url = {https://doi.org/10.1145/3471158.3472239}
     }
    """
    __name__ = 'NERR10'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'p': measures.ParamInfo(dtype=float, default=0.9, desc='persistence'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }

class _NERR11(measures.Measure):
    """
    Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (12) of the the following paper.

::

     @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
       author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
       title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
       booktitle = {ICTIR},
       year = {2021},
       url = {https://doi.org/10.1145/3471158.3472239}
     }
    """
    __name__ = 'NERR11'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'T': measures.ParamInfo(dtype=float, default=1.0, desc='total desired gain (normalized)'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


NERR8 = _NERR8()
measures.register(NERR8)
NERR9 = _NERR9()
measures.register(NERR9)
NERR10 = _NERR10()
measures.register(NERR10)
NERR11 = _NERR11()
measures.register(NERR11)
