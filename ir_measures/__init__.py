from . import util
from . import measures
from .measures import P, RR, Rprec, AP, nDCG, R, Bpref, Judged, ERR, RBP
from . import providers


DefaultPipeline = providers.FallbackProvider([
	providers.TrectoolsProvider(),
	providers.PytrecEvalProvider(),
	providers.JudgedProvider(),
	providers.GdevalProvider(),
	providers.MsMarcoProvider(),
])
calc_ctxt = DefaultPipeline.calc_ctxt
iter_calc = DefaultPipeline.iter_calc
calc_aggregate = DefaultPipeline.calc_aggregate
# aggreage = DefaultPipeline.aggreage
