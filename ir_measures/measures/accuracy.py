from ir_measures import measures
from .base import Measure, ParamInfo

class _Accuracy(Measure):
    """Accuracy metric

    Reports the probability that a relevant document is ranked before a non relevant one.
    This metric purpose is to be used for diagnosis (checking that train/test/validation accuracy match).
    As such, it only considers relevant documents which are within the returned ones.
    """
    __name__ = 'Accuracy'
    NAME = __name__
    PRETTY_NAME = 'Accuracy'
    SHORT_DESC = 'The probability that a relevant document is ranked before a non relevant one.'
    SUPPORTED_PARAMS = {
        'cutoff': ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }

Accuracy = _Accuracy()
measures.register(Accuracy)
