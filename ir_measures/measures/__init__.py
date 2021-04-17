registry = {}
def register(measure):
	registry[measure.NAME] = measure
	return registry

from .base import BaseMeasure, ParamInfo, MultiMeasures
from .p import P, _P
from .rr import RR, _RR
from .rprec import Rprec, _Rprec
from .ap import AP, _AP
from .ndcg import nDCG, _nDCG
from .r import R, _R
from .bpref import Bpref, _Bpref
from .judged import Judged, _Judged
from .err import ERR, _ERR
from .rbp import RBP, _RBP
