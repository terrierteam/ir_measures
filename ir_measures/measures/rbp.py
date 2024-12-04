from ir_measures import measures


class _RBP(measures.Measure):
    """
    The Rank-Biased Precision (RBP).


    .. cite.dblp:: journals/tois/MoffatZ08
    """
    __name__ = 'RBP'
    NAME = __name__
    PRETTY_NAME = 'Rank-Biased Precision'
    SHORT_DESC = 'A measure of the rate at which utility is gained as a user traverses a result list with a degree of persistence.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'p': measures.ParamInfo(dtype=float, default=0.8, desc='persistence'),
        'rel': measures.ParamInfo(dtype=int, required=False, desc='minimum relevance score to be considered relevant (inclusive), or NOT_PROVIDED to use graded relevance')
    }


RBP = _RBP()
measures.register(RBP)
