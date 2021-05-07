__version__ = "0.1.4"
from . import util
from .util import parse_measure, convert_trec_name
from . import measures
from .measures import P, RR, MRR, Rprec, AP, nDCG, R, Bpref, Judged, ERR, RBP, NumRet, NumRelRet, NumQ, NumRel, SetP, Success, IPrec, infAP
from . import providers


DefaultPipeline = providers.FallbackProvider([
	providers.PytrecEvalProvider(),
	# providers.TrectoolsProvider(),  # buggy; will add back later
	providers.JudgedProvider(),
	providers.MsMarcoProvider(),
	providers.GdevalProvider(),  # doesn't work when installed from package #9
])
calc_ctxt = DefaultPipeline.calc_ctxt
iter_calc = DefaultPipeline.iter_calc
calc_aggregate = DefaultPipeline.calc_aggregate
