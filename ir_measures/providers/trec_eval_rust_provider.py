from .pytrec_eval_provider import PytrecEvalProvider
from ir_measures import providers

class TeRustProvider(PytrecEvalProvider):

    NAME = 'trec_eval'
    
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        try:
            import trec_eval.compat.pytrec_eval as pytrec_eval
            self.pytrec_eval = pytrec_eval
        except ImportError as ex:
            raise RuntimeError('trec_eval not available', ex)

    def install_instructions(self):
        return "pip install --upgrade 'git+https://github.com/usnistgov/trec_eval.git@trec_eval_v11#subdirectory=te-python'"

providers.register(TeRustProvider())
