from ir_measures import measures


class _ERR_IA(measures.BaseMeasure):
    """
    Intent-Aware Expected Reciprocal Rank with collection-independent normalisation.


    .. cite.dblp:: conf/cikm/ChapelleMZG09
    """
    __name__ = 'ERR_IA'
    NAME = __name__
    PRETTY_NAME = 'Intent-Aware Expected Reciprocal Rank'
    SHORT_DESC = 'A version of ERR that accounts for multiple possible query intents.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _nERR_IA(measures.BaseMeasure):
    """
    Intent-Aware Expected Reciprocal Rank with collection-dependent normalisation.


    .. cite.dblp:: conf/cikm/ChapelleMZG09
    """
    __name__ = 'nERR_IA'
    NAME = __name__
    PRETTY_NAME = 'Intent-Aware Normalised Expected Reciprocal Rank'
    SHORT_DESC = 'A normalised version of ERR that accounts for multiple possible query intents.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _alpha_DCG(measures.BaseMeasure):
    """
    A version of DCG that accounts for multiple possible query intents.


    .. cite.dblp:: conf/sigir/ClarkeKCVABM08
    """
    __name__ = 'alpha_DCG'
    NAME = __name__
    PRETTY_NAME = 'Alpha Discounted Cumulative Gain'
    SHORT_DESC = 'A version of DCG that accounts for multiple possible query intents.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'alpha': measures.ParamInfo(dtype=float, default=0.5, desc='Redundancy intolerance'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _alpha_nDCG(measures.BaseMeasure):
    """
    A version of nDCG that accounts for multiple possible query intents.


    .. cite.dblp:: conf/sigir/ClarkeKCVABM08
    """
    __name__ = 'alpha_nDCG'
    NAME = __name__
    PRETTY_NAME = 'Alpha Normalised Discounted Cumulative Gain'
    SHORT_DESC = 'A version of nDCG that accounts for multiple possible query intents.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'alpha': measures.ParamInfo(dtype=float, default=0.5, desc='Redundancy intolerance'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _NRBP(measures.BaseMeasure):
    """
    Novelty- and Rank-Biased Precision with collection-independent normalisation.


    .. cite.dblp:: conf/ictir/ClarkeKV09
    """
    __name__ = 'NRBP'
    NAME = __name__
    PRETTY_NAME = 'Novelty- and Rank-Biased Precision'
    SHORT_DESC = 'A version of RBP that accounts for multiple possible query intents.'
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'alpha': measures.ParamInfo(dtype=float, default=0.5, desc='Redundancy intolerance'),
        'beta': measures.ParamInfo(dtype=float, default=0.5, desc='Patience'),
    }

class _nNRBP(measures.BaseMeasure):
    """
    Novelty- and Rank-Biased Precision with collection-dependent normalisation.


    .. cite.dblp:: conf/ictir/ClarkeKV09
    """
    __name__ = 'nNRBP'
    NAME = __name__
    PRETTY_NAME = 'Normalised Novelty- and Rank-Biased Precision'
    SHORT_DESC = 'A normalised version of RBP that accounts for multiple possible query intents.'
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'alpha': measures.ParamInfo(dtype=float, default=0.5, desc='Redundancy intolerance'),
        'beta': measures.ParamInfo(dtype=float, default=0.5, desc='Patience'),
    }

class _AP_IA(measures.BaseMeasure):
    """
    Intent-aware (Mean) Average Precision
    """
    __name__ = 'AP_IA'
    NAME = __name__
    PRETTY_NAME = 'Intent-Aware (Mean) Average Precision'
    SHORT_DESC = 'A version of AP that accounts for multiple possible query intents.'
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _P_IA(measures.BaseMeasure):
    """
    Intent-aware Precision@k.
    """
    __name__ = 'P_IA'
    NAME = __name__
    PRETTY_NAME = 'Intent-Aware Precision@k'
    SHORT_DESC = 'A version of P@k that accounts for multiple possible query intents.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='calculate measure using only judged documents (i.e., discard unjudged documents)'),
    }

class _StRecall(measures.BaseMeasure):
    """
    Subtopic recall (the number of subtopics covered by the top k docs)
    """
    __name__ = 'StRecall'
    NAME = __name__
    PRETTY_NAME = 'Subtopic Recall at k'
    SHORT_DESC = 'The percentage of subtopics covered by the top k documents.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
    }



ERR_IA = _ERR_IA()
nERR_IA = _nERR_IA()
alpha_DCG = _alpha_DCG()
α_DCG = alpha_DCG
alpha_nDCG = _alpha_nDCG()
α_nDCG = alpha_nDCG
NRBP = _NRBP()
nNRBP = _nNRBP()
AP_IA = _AP_IA()
MAP_IA = AP_IA
P_IA = _P_IA()
StRecall = _StRecall()

measures.register(ERR_IA)
measures.register(nERR_IA)
measures.register(alpha_DCG, aliases=['α_DCG'])
measures.register(alpha_nDCG, aliases=['α_nDCG'])
measures.register(NRBP)
measures.register(nNRBP)
measures.register(AP_IA, aliases=['MAP_IA'])
measures.register(P_IA)
measures.register(StRecall)
