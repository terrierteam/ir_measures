from ir_measures.measures.base import Measure, BaseMeasure, ParamInfo, MeanAgg, SumAgg, registry, register
from ir_measures.measures.accuracy import Accuracy, _Accuracy
from ir_measures.measures.ap import AP, MAP, _AP
from ir_measures.measures.bpm import BPM, _BPM
from ir_measures.measures.bpref import Bpref, BPref, _Bpref
from ir_measures.measures.compat import Compat, _Compat
from ir_measures.measures.diversity import ERR_IA, _ERR_IA, nERR_IA, _nERR_IA, alpha_DCG, α_DCG, _alpha_DCG, alpha_nDCG, α_nDCG, _alpha_nDCG, NRBP, _NRBP, nNRBP, _nNRBP, AP_IA, MAP_IA, _AP_IA, P_IA, _P_IA, StRecall, _StRecall
from ir_measures.measures.err import ERR, _ERR
from ir_measures.measures.inst import INST, _INST, INSQ, _INSQ
from ir_measures.measures.infap import infAP, _infAP
from ir_measures.measures.iprec import IPrec, _IPrec
from ir_measures.measures.judged import Judged, _Judged
from ir_measures.measures.ndcg import nDCG, NDCG, _nDCG
from ir_measures.measures.nerr import NERR8, NERR9, NERR10, NERR11, _NERR8, _NERR9, _NERR10, _NERR11
from ir_measures.measures.numq import NumQ, _NumQ
from ir_measures.measures.numrel import NumRel, _NumRel
from ir_measures.measures.numret import NumRet, NumRelRet, _NumRet
from ir_measures.measures.p import P, Precision, _P
from ir_measures.measures.r import R, Recall, _R
from ir_measures.measures.rbp import RBP, _RBP
from ir_measures.measures.rprec import Rprec, RPrec, _Rprec
from ir_measures.measures.rr import RR, MRR, _RR
from ir_measures.measures.sdcg import SDCG, _SDCG
from ir_measures.measures.set_measures import SetP, SetRelP, _SetP, SetR, _SetR, SetF, _SetF, SetAP, _SetAP
from ir_measures.measures.success import Success, _Success

# include all (to make ruff happy)
__all__ = [
    'Measure', 'BaseMeasure', 'ParamInfo', 'MeanAgg', 'SumAgg', 'registry', 'register',
    'Accuracy', '_Accuracy', 'AP', 'MAP', '_AP', 'BPM', '_BPM', 'Bpref', 'BPref', '_Bpref', 'Compat', '_Compat',
    'ERR', '_ERR', 'ERR_IA', '_ERR_IA', 'nERR_IA', '_nERR_IA', 'alpha_DCG', 'α_DCG', '_alpha_DCG', 'alpha_nDCG', 'α_nDCG', '_alpha_nDCG',
    'NRBP', '_NRBP', 'nNRBP', '_nNRBP', 'AP_IA', 'MAP_IA', '_AP_IA', 'P_IA', '_P_IA', 'StRecall', '_StRecall',
    'INST', '_INST', 'INSQ', '_INSQ', 'infAP', '_infAP', 'IPrec', '_IPrec', 'Judged', '_Judged', 'nDCG', 'NDCG', '_nDCG',
    'NERR8', 'NERR9', 'NERR10', 'NERR11', '_NERR8', '_NERR9', '_NERR10', '_NERR11', 'NumQ', '_NumQ', 'NumRel', '_NumRel',
    'NumRet', 'NumRelRet', '_NumRet', 'P', 'Precision', '_P', 'R', 'Recall', '_R', 'RBP', '_RBP', 'Rprec', 'RPrec', '_Rprec',
    'RR', 'MRR', '_RR', 'SDCG', '_SDCG', 'SetP', 'SetRelP', '_SetP', 'SetR', '_SetR', 'SetF', '_SetF', 'SetAP', '_SetAP',
    'Success', '_Success'
]

# enable "from ir_measures.measures import *" --- on purpuse, do not include _-prefixed versions,
# as these are intended for internal use
__all__ = [
    'Measure', 'BaseMeasure', 'ParamInfo', 'MeanAgg', 'SumAgg', 'registry', 'register',
    'Accuracy', 'AP', 'MAP', 'BPM', 'Bpref', 'BPref', 'Compat', 'ERR_IA', 'nERR_IA', 'alpha_DCG', 'α_DCG', 'alpha_nDCG', 'α_nDCG', 'NRBP', 'nNRBP', 'AP_IA', 'MAP_IA', 'P_IA', 'StRecall', 'ERR', 'INST', 'INSQ', 'infAP', 'IPrec', 'Judged', 'nDCG', 'NDCG', 'NERR8', 'NERR9', 'NERR10', 'NERR11', 'NumQ', 'NumRel', 'NumRet', 'NumRelRet', 'P', 'Precision', 'R', 'Recall', 'RBP', 'Rprec', 'RPrec', 'RR', 'MRR', 'SDCG', 'SetP', 'SetRelP', 'SetR', 'SetF', 'SetAP', 'Success'
]
