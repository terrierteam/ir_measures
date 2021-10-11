registry = {}
def register(measure, aliases=[], name=None):
    if name is None:
        name = measure.__name__
    assert name not in registry
    registry[name] = measure
    for alias in aliases:
        assert alias not in registry
        registry[alias] = measure
    return registry

from .base import Measure, BaseMeasure, ParamInfo, MultiMeasures, MeanAgg, SumAgg
from .ap import AP, MAP, _AP
from .bpm import BPM, _BPM
from .bpref import Bpref, BPref, _Bpref
from .compat import Compat, _Compat
from .diversity import ERR_IA, _ERR_IA, nERR_IA, _nERR_IA, alpha_DCG, α_DCG, _alpha_DCG, alpha_nDCG, α_nDCG, _alpha_nDCG, NRBP, _NRBP, nNRBP, _nNRBP, AP_IA, MAP_IA, _AP_IA, P_IA, _P_IA, StRecall, _StRecall
from .err import ERR, _ERR
from .inst import INST, _INST, INSQ, _INSQ
from .infap import infAP, _infAP
from .iprec import IPrec, _IPrec
from .judged import Judged, _Judged
from .ndcg import nDCG, NDCG, _nDCG
from .nerr import NERR8, NERR9, NERR10, NERR11, _NERR8, _NERR9, _NERR10, _NERR11
from .numq import NumQ, _NumQ
from .numrel import NumRel, _NumRel
from .numret import NumRet, NumRelRet, _NumRet
from .p import P, Precision, _P
from .r import R, Recall, _R
from .rbp import RBP, _RBP
from .rprec import Rprec, RPrec, _Rprec
from .rr import RR, MRR, _RR
from .sdcg import SDCG, _SDCG
from .set_measures import SetP, SetRelP, _SetP, SetR, _SetR, SetF, _SetF, SetAP, _SetAP
from .success import Success, _Success

# enable from "ir_measures.measures import *" --- on purpuse, do not include _-prefixed versions,
# as these are intended for internal use
__all__ = list(registry.keys())
