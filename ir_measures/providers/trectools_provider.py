import sys
import contextlib
import functools
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.providers.base import Any, Choices, NOT_PROVIDED


class TrectoolsProvider(providers.Provider):
    """
    trectools

    https://github.com/joaopalotti/trectools

::

    @inproceedings{palotti2019,
       author = {Palotti, Joao and Scells, Harrisen and Zuccon, Guido},
       title = {TrecTools: an open-source Python library for Information Retrieval practitioners involved in TREC-like campaigns},
       series = {SIGIR'19},
       year = {2019},
       location = {Paris, France},
       publisher = {ACM}
    }

    """
    NAME = 'trectools'
    SUPPORTED_MEASURES = [
        measures._P(cutoff=Any(), rel=Choices(1)),
        measures._RR(cutoff=Choices(NOT_PROVIDED), rel=Choices(1)),
        measures._Rprec(rel=Choices(1)),
        measures._AP(cutoff=Any(), rel=Choices(1)),
        measures._nDCG(cutoff=Any(), dcg=Any()),
        measures._Bpref(rel=Choices(1)),
        measures._RBP(cutoff=Any(), p=Any(), rel=Any()),
        # Other supported metrics: urbp, ubpref, alpha_urbp, geometric_map, unjudged
    ]

    def __init__(self):
        super().__init__()
        self.trectools = None

    def _evaluator(self, measures, qrels):
        import pandas as pd
        measures = ir_measures.util.flatten_measures(measures)
        # Convert qrels to dict_of_dict (input format used by pytrec_eval)
        tmp_qrels = ir_measures.util.QrelsConverter(qrels).as_namedtuple_iter()
        tmp_qrels = pd.DataFrame(tmp_qrels)
        if len(tmp_qrels) == 0:
            tmp_qrels = pd.DataFrame(columns=['query', 'docid', 'rel'], dtype='object')
        else:
            tmp_qrels = tmp_qrels.rename(columns={'query_id': 'query', 'doc_id': 'docid', 'relevance': 'rel'})
        qrels = self.trectools.TrecQrel()
        qrels.qrels_data = tmp_qrels

        invocations = self._build_invocations(measures)

        return TrectoolsEvaluator(measures, qrels, invocations, self.trectools)

    def _build_invocations(self, measures):
        invocations = []
        for measure in measures:
            def depth():
                try:
                    cutoff = measure['cutoff']
                except KeyError:
                    cutoff = NOT_PROVIDED
                if cutoff is NOT_PROVIDED:
                    cutoff = sys.maxsize
                return cutoff
            if measure.NAME == 'P':
                fn = functools.partial(self.trectools.TrecEval.get_precision, depth=depth(), per_query=True, trec_eval=False, removeUnjudged=False)
            elif measure.NAME == 'RR':
                fn = functools.partial(self.trectools.TrecEval.get_reciprocal_rank, depth=depth(), per_query=True, trec_eval=False, removeUnjudged=False)
            elif measure.NAME == 'Rprec':
                fn = functools.partial(self.trectools.TrecEval.get_rprec, depth=depth(), per_query=True, trec_eval=False, removeUnjudged=False)
            elif measure.NAME == 'AP':
                fn = functools.partial(self.trectools.TrecEval.get_map, depth=depth(), per_query=True, trec_eval=False)
            elif measure.NAME == 'nDCG':
                te_mode = {
                    'log2': True,
                    'exp-log2': False
                }[measure['dcg']]
                # trec_eval has other side-effects; namely ordering by score instead of rank.
                # But in our setting, those are always the same so no difference.
                fn = functools.partial(self.trectools.TrecEval.get_ndcg, depth=depth(), per_query=True, trec_eval=te_mode, removeUnjudged=False)
            elif measure.NAME == 'Bpref':
                fn = functools.partial(self.trectools.TrecEval.get_bpref, depth=depth(), per_query=True, trec_eval=False)
            elif measure.NAME == 'RBP':
                rel = measure['rel']
                if rel is not NOT_PROVIDED:
                    # TODO: how to handle different relevance levels? I think the only way is to modify
                    # the dataframe.
                    raise RuntimeError('unsupported')
                    fn = lambda ev: self.trectools.TrecEval.get_rbp(ev, p=measure['p'], depth=depth(), per_query=True, binary_topical_relevance=True, average_ties=True, removeUnjudged=False)[0]
                else:
                    fn = lambda ev: self.trectools.TrecEval.get_rbp(ev, p=measure['p'], depth=depth(), per_query=True, binary_topical_relevance=False, average_ties=True, removeUnjudged=False)[0]
            else:
                raise ValueError(f'unsupported measure {measure}')

            invocations.append((fn, measure))

        return invocations
 
    def initialize(self):
        try:
            import trectools
            self.trectools = trectools
        except ImportError as ex:
            raise RuntimeError('trectools not available', ex)


class TrectoolsEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels, invocations, trectools):
        super().__init__(measures, qrels.qrels_data['query'].unique())
        self.qrels = qrels
        self.invocations = invocations
        self.trectools = trectools

    def _iter_calc(self, run):
        import pandas as pd
        available_qids = set(self.qrels.qrels_data['query'].unique())
        tmp_run = ir_measures.util.RunConverter(run).as_namedtuple_iter()
        tmp_run = pd.DataFrame(tmp_run)
        if len(tmp_run) == 0:
            tmp_run = pd.DataFrame(columns=['query', 'docid', 'score'], dtype='object')
        else:
            tmp_run = tmp_run.rename(columns={'query_id': 'query', 'doc_id': 'docid', 'score': 'score'})
        tmp_run.sort_values(['query', 'score'], ascending=[True, False], inplace=True)
        run = self.trectools.TrecRun()
        run.run_data = tmp_run
        evaluator = self.trectools.TrecEval(run, self.qrels)
        for invocation, measure in self.invocations:
            for query_id, value in invocation(evaluator).itertuples():
                if query_id in available_qids:
                    yield Metric(query_id=query_id, measure=measure, value=value)



providers.register(TrectoolsProvider())
