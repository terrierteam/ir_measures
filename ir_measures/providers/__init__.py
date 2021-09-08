registry = {}
def register(provider):
	registry[provider.NAME] = provider
	return provider

from .base import Provider, Evaluator
from .fallback_provider import FallbackProvider
from .cwl_eval import CwlEvalProvider, CwlMetric
from .pytrec_eval_provider import PytrecEvalProvider
from .judged_provider import JudgedProvider
from .gdeval_provider import GdevalProvider
from .trectools_provider import TrectoolsProvider
from .msmarco_provider import MsMarcoProvider
