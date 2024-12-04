from ir_measures import measures


class _NERR8(measures.Measure):
    """
    Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (8) of the the following paper.


    .. cite.dblp:: conf/ictir/AzzopardiMM21
    """
    __name__ = 'NERR8'
    NAME = __name__
    PRETTY_NAME = 'Nearly Expected Reciprocal Rank Eq 8'
    SHORT_DESC = 'A C/W/L approximation of ERR using gain-based stopping with truncation at k.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }

class _NERR9(measures.Measure):
    """
    Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (9) of the the following paper.


    .. cite.dblp:: conf/ictir/AzzopardiMM21
    """
    __name__ = 'NERR9'
    NAME = __name__
    PRETTY_NAME = 'Nearly Expected Reciprocal Rank Eq 9'
    SHORT_DESC = 'A C/W/L approximation of ERR using gain-based stopping and discount with truncation at k.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }

class _NERR10(measures.Measure):
    """
    Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (10) of the the following paper.


    .. cite.dblp:: conf/ictir/AzzopardiMM21
    """
    __name__ = 'NERR10'
    NAME = __name__
    PRETTY_NAME = 'Nearly Expected Reciprocal Rank Eq 10'
    SHORT_DESC = 'A C/W/L approximation of ERR using gain-based stopping and RBP patience (p).'
    SUPPORTED_PARAMS = {
        'p': measures.ParamInfo(dtype=float, default=0.9, desc='persistence'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }

class _NERR11(measures.Measure):
    """
    Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (12) of the the following paper.


    .. cite.dblp:: conf/ictir/AzzopardiMM21
    """
    __name__ = 'NERR11'
    NAME = __name__
    PRETTY_NAME = 'Nearly Expected Reciprocal Rank Eq 11'
    SHORT_DESC = 'A C/W/L approximation of ERR using gain based stopping and INST Goal (T).'
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
