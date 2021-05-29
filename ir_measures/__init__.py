__version__ = "0.1.4"
from . import util
from .util import parse_measure, convert_trec_name, read_trec_qrels, read_trec_run, GenericQrel, GenericScoredDoc
from . import measures
from .measures import *
from . import providers

# providers
gdeval = providers.registry['gdeval']
pytrec_eval = providers.registry['pytrec_eval']
trectools = providers.registry['trectools']
judged = providers.registry['judged']
msmarco = providers.registry['msmarco']

DefaultPipeline = providers.FallbackProvider([
	pytrec_eval,
	# trectools,  # buggy; will add back later
	judged,
	msmarco,
	gdeval,  # doesn't work when installed from package #9
])
evaluator = DefaultPipeline.evaluator
calc_ctxt = DefaultPipeline.calc_ctxt # deprecated
iter_calc = DefaultPipeline.iter_calc
calc_aggregate = DefaultPipeline.calc_aggregate

__all__ = measures.__all__
