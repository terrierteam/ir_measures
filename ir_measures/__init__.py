__version__ = "0.4.2"
import sys
import logging
from ir_measures import util
from ir_measures import lazylibs
from ir_measures.util import (
    parse_measure, parse_trec_measure, read_trec_qrels, read_trec_run,
    Qrel, ScoredDoc, Metric, CalcResults,
    GenericQrel, # deprecated; replaced with Qrel
    GenericScoredDoc, # deprecated; replaced with ScoredDoc
    convert_trec_name, # deprecated; replaced with parse_trec_measure
    parse_trec_qrels, # deprecated; replaced with read_trec_qrels
    parse_trec_run, # deprecated; replaced with read_trec_run
)
from ir_measures import measures
from ir_measures.measures import (
    Accuracy, alpha_DCG, alpha_nDCG, AP, AP_IA, BaseMeasure, BPM, Bpref, BPref, Compat, ERR, ERR_IA, infAP, INSQ, INST,
    IPrec, Judged, MAP, MAP_IA, MeanAgg, Measure, MRR, nDCG, NDCG, NERR10, NERR11, NERR8, NERR9, nERR_IA, nNRBP, NRBP,
    NumQ, NumRel, NumRelRet, NumRet, P, P_IA, ParamInfo, Precision, R, RBP, Recall, Rprec, RPrec, RR, SDCG, SetAP, SetF,
    SetP, SetR, SetRelP, StRecall, Success, SumAgg, α_DCG, α_nDCG
)
from ir_measures import providers
from ir_measures.providers import Provider, Evaluator



logger = logging.getLogger('ir_measures')
logger.setLevel('WARNING')
log_handler = logging.StreamHandler(sys.stderr)
log_handler.setFormatter(logging.Formatter('[%(name)s] [%(levelname)s] %(message)s'))
logger.addHandler(log_handler)

# providers
accuracy = providers.registry['accuracy']
cwl_eval = providers.registry['cwl_eval']
compat = providers.registry['compat']
gdeval = providers.registry['gdeval']
pytrec_eval = providers.registry['pytrec_eval']
trectools = providers.registry['trectools']
judged = providers.registry['judged']
msmarco = providers.registry['msmarco']
pyndeval = providers.registry['pyndeval']
ranx = providers.registry['ranx']
runtime = providers.registry['runtime']

define = providers.define
define_byquery = providers.define_byquery

CwlMetric = providers.CwlMetric

DefaultPipeline = providers.FallbackProvider([
    runtime,
    pytrec_eval,
    cwl_eval,
    compat,
    pyndeval,
    # trectools,  # buggy; will add back later
    judged,
    msmarco,
    gdeval,  # doesn't work when installed from package #9
    accuracy,
    ranx,
])
evaluator = DefaultPipeline.evaluator
calc_ctxt = DefaultPipeline.calc_ctxt # deprecated; replaced with evaluator
iter_calc = DefaultPipeline.iter_calc
calc_aggregate = DefaultPipeline.calc_aggregate
calc = DefaultPipeline.calc
run_inputs = DefaultPipeline.run_inputs
qrel_inputs = DefaultPipeline.qrel_inputs

__all__ = [
    'accuracy', 'cwl_eval', 'compat', 'gdeval', 'pytrec_eval', 'trectools', 'judged', 'msmarco', 'pyndeval', 'ranx',
    'runtime',
    'define', 'define_byquery',
    'CwlMetric',
    'DefaultPipeline',
    'evaluator', 'calc_ctxt', 'iter_calc', 'calc_aggregate', 'calc',
    'Accuracy', 'alpha_DCG', 'alpha_nDCG', 'AP', 'AP_IA', 'BaseMeasure', 'BPM', 'Bpref', 'BPref', 'Compat', 'ERR',
    'ERR_IA', 'infAP', 'INSQ', 'INST', 'IPrec', 'Judged', 'MAP', 'MAP_IA', 'MeanAgg', 'Measure', 'MRR', 'nDCG', 'NDCG',
    'NERR10', 'NERR11', 'NERR8', 'NERR9', 'nERR_IA', 'nNRBP', 'NRBP', 'NumQ', 'NumRel', 'NumRelRet', 'NumRet', 'P',
    'P_IA', 'ParamInfo', 'Precision', 'R', 'RBP', 'Recall', 'Rprec', 'RPrec', 'RR', 'SDCG', 'SetAP', 'SetF', 'SetP',
    'SetR', 'SetRelP', 'StRecall', 'Success', 'SumAgg', 'α_DCG', 'α_nDCG',
    'Measure',
    'Provider', 'Evaluator',
    'Qrel', 'ScoredDoc', 'Metric', 'CalcResults',
    'GenericQrel', 'GenericScoredDoc',
    'convert_trec_name', 'parse_trec_measure',
    'read_trec_qrels', 'read_trec_run',
    'parse_measure', 'parse_trec_qrels', 'parse_trec_run',
    'util',
    'measures',
    'providers',
    'lazylibs',
    '__version__',
]
