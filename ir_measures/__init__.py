__version__ = "0.1.4"
from . import util
from . import lazylibs
from .util import (parse_measure, parse_trec_measure,
	               read_trec_qrels, read_trec_run,
	               Qrel, ScoredDoc, Metric,
	               GenericQrel, # deprecated; replaced with Qrel
	               GenericScoredDoc, # deprecated; replaced with ScoredDoc
	               convert_trec_name, # deprecated; replaced with parse_trec_measure
	               parse_trec_qrels, # deprecated; replaced with read_trec_qrels
	               parse_trec_run, # deprecated; replaced with read_trec_run
	              )
from . import measures
from .measures import *
from . import providers

# providers
cwl_eval = providers.registry['cwl_eval']
gdeval = providers.registry['gdeval']
pytrec_eval = providers.registry['pytrec_eval']
trectools = providers.registry['trectools']
judged = providers.registry['judged']
msmarco = providers.registry['msmarco']

DefaultPipeline = providers.FallbackProvider([
	pytrec_eval,
	cwl_eval,
	# trectools,  # buggy; will add back later
	judged,
	msmarco,
	gdeval,  # doesn't work when installed from package #9
])
evaluator = DefaultPipeline.evaluator
calc_ctxt = DefaultPipeline.calc_ctxt # deprecated; replaced with evaluator
iter_calc = DefaultPipeline.iter_calc
calc_aggregate = DefaultPipeline.calc_aggregate

__all__ = measures.__all__
