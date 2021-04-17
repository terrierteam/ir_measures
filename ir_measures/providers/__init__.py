reigistry = {}
def register(provider):
	reigistry[provider.NAME] = provider
	return provider

from .base import MeasureProvider
from .fallback_provider import FallbackProvider
from .pytrec_eval_provider import PytrecEvalProvider
from .judged_provider import JudgedProvider
from .gdeval_provider import GdevalProvider
from .trectools_provider import TrectoolsProvider
from .msmarco_provider import MsMarcoProvider
