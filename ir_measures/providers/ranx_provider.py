import contextlib
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.providers.base import Any, Choices, NOT_PROVIDED


class RanxProvider(providers.Provider):
    """
    ranx

    https://amenra.github.io/ranx/

::

    @misc{ranx2021,
      title = {ranx: A Blazing-Fast Python Library for Ranking Evaluation and Comparison},
      author = {Bassani, Elias},
      year = {2021},
      publisher = {GitHub},
      howpublished = {\\url{https://github.com/AmenRa/ranx}},
    }

    """
    NAME = 'ranx'
    SUPPORTED_MEASURES = [
        measures._P(cutoff=Any(), rel=Any()),
        measures._SetP(rel=Any()),
        measures._RR(cutoff=Choices(NOT_PROVIDED), rel=Any()),
        measures._Rprec(rel=Any()),
        measures._AP(cutoff=Any(), rel=Any()),
        measures._nDCG(cutoff=Any(), dcg=Choices('log2', 'exp-log2'), gains=Choices(NOT_PROVIDED)),
        measures._R(cutoff=Any()),
        measures._SetR(rel=Any()),
        measures._NumRet(rel=Any(required=True)),
        measures._Success(cutoff=Any(required=True), rel=Any()),
    ]

    def __init__(self):
        super().__init__()
        self.ranx = None

    def _evaluator(self, measures, qrels):
        measures = ir_measures.util.flatten_measures(measures)
        # Convert qrels to dict_of_dict (input format used by pytrec_eval)
        qrels = ir_measures.util.QrelsConverter(qrels).as_pd_dataframe()
        qids = set(qrels['query_id'].unique())

        # Depending on the measure params, we may need multiple invocations of ranx
        # (e.g., with different rel_level, since it only supports running with 1 rel_level at a time)
        invokers = self._build_invokers(measures, qrels)
        return RanxEvaluator(self.ranx, measures, invokers, qrels, qids=qids)

    def _build_invokers(self, measures, qrels):
        invocations = {}
        setf_count = 0
        for measure in measures:
            match_str = None
            if measure.NAME == 'P':
                invocation_key = (measure['rel'], 0)
                measure_str = f'precision@{measure["cutoff"]}'
            elif measure.NAME == 'SetP':
                invocation_key = (measure['rel'], 0)
                measure_str = f'precision'
            elif measure.NAME == 'R':
                invocation_key = (measure['rel'], 0)
                measure_str = f'recall@{measure["cutoff"]}'
            elif measure.NAME == 'SetR':
                invocation_key = (measure['rel'], 0)
                measure_str = f'recall'
            elif measure.NAME == 'RR':
                invocation_key = (measure['rel'], 0)
                if 'cutoff' in measure.params:
                    measure_str = f'mrr@{measure["cutoff"]}'
                else:
                    measure_str = f'mrr'
            elif measure.NAME == 'AP':
                invocation_key = (measure['rel'], 0)
                if 'cutoff' in measure.params:
                    measure_str = f'map@{measure["cutoff"]}'
                else:
                    measure_str = f'map'
            elif measure.NAME == 'Success':
                invocation_key = (measure['rel'], 0)
                measure_str = f'hit_rate@{measure["cutoff"]}'
            elif measure.NAME == 'NumRet':
                invocation_key = (measure['rel'], 0)
                measure_str = f'hits'
            elif measure.NAME == 'nDCG':
                invocation_key = (None, 0)
                name = 'ndcg_burges' if measure.params.get('dcg', measure.SUPPORTED_PARAMS['dcg'].default) == 'exp-log2' else 'ndcg'
                if 'cutoff' in measure.params:
                    measure_str = f'{name}@{measure["cutoff"]}'
                else:
                    measure_str = name
            elif measure.NAME == 'Rprec':
                invocation_key = (measure['rel'], 0)
                measure_str = f'r-precision'
            else:
                raise ValueError(f'unsupported measure {measure}')

            if match_str is None:
                match_str = measure_str

            if invocation_key not in invocations:
                invocations[invocation_key] = {}
            invocations[invocation_key][match_str] = (measure, measure_str)

        invokers = []
        for (rel_level, it), measure_map in invocations.items():
            if rel_level is not None:
                these_qrels = qrels.assign(relevance=(qrels['relevance']>=rel_level).astype(int))
            else:
                these_qrels = qrels
            these_qrels = self.ranx.Qrels.from_df(these_qrels, q_id_col='query_id', doc_id_col='doc_id', score_col='relevance')
            invokers.append(RanxInvoker(self.ranx, these_qrels, measure_map))

        return invokers

    def initialize(self):
        try:
            import ranx
            self.ranx = ranx
        except ImportError as ex:
            raise RuntimeError('ranx not available (do you need to `pip install ranx`?)', ex)


class RanxEvaluator(providers.Evaluator):
    def __init__(self, ranx, measures, invokers, qrels, qids):
        super().__init__(measures, qids)
        self.ranx = ranx
        self.invokers = invokers

    def _iter_calc(self, run):
        run = self.ranx.Run.from_df(ir_measures.util.RunConverter(run).as_pd_dataframe(), q_id_col='query_id', doc_id_col='doc_id', score_col='score')
        for invoker in self.invokers:
            yield from invoker.iter_calc(run)


class RanxInvoker:
    def __init__(self, ranx, qrels, measure_map):
        self.ranx = ranx
        self.qrels = qrels
        self.measure_map = measure_map

    def iter_calc(self, run):
        self.ranx.evaluate(self.qrels, run, list(self.measure_map))
        for measure, qid_value_map in run.scores.items():
            for query_id, value in qid_value_map.items():
                yield Metric(query_id=query_id, measure=self.measure_map[measure][0], value=value)
        run.scores.clear()


providers.register(RanxProvider())
