registry = {}
def register(provider):
	registry[provider.NAME] = provider
	return provider

from .base import Provider, Evaluator
from .accuracy_provider import AccuracyProvider
from .fallback_provider import FallbackProvider
from .compat_provider import CompatProvider
from .cwl_eval import CwlEvalProvider, CwlMetric
from .pyndeval_provider import PyNdEvalProvider
from .pytrec_eval_provider import PytrecEvalProvider
from .judged_provider import JudgedProvider
from .gdeval_provider import GdevalProvider
from .trectools_provider import TrectoolsProvider
from .msmarco_provider import MsMarcoProvider
from .ranx_provider import RanxProvider
from .runtime_provider import RuntimeProvider, define, define_byquery
