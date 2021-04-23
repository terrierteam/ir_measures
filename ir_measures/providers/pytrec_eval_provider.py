import contextlib
import ir_measures
from ir_measures import providers, measures
from ir_measures.providers.base import Any, Choices, Metric, NOT_PROVIDED


class PytrecEvalProvider(providers.MeasureProvider):
    NAME = 'pytrec_eval'
    SUPPORTED_MEASURES = [
        measures._P(cutoff=Any(), rel=Any()),
        measures._RR(cutoff=Choices(NOT_PROVIDED), rel=Any()),
        measures._Rprec(rel=Any()),
        measures._AP(cutoff=Any(), rel=Any()),
        measures._nDCG(cutoff=Any(), dcg=Choices('log2')),
        measures._R(cutoff=Any()),
        measures._Bpref(rel=Any()),
        measures._NumRet(rel=Any()),
        measures._NumQ(rel=Any()),
        measures._NumRel(rel=1), # for some reason, relevance_level doesn't flow through to num_rel, so can only support rel=1
        measures._SetP(rel=Any()),
        measures._Success(rel=Any(), cutoff=Any()),
        measures._IPrec(recall=Any()),
        measures._infAP(rel=Any()),
        # Cannot support Judged because software doesn't support negative relevance levels: <https://github.com/cvangysel/pytrec_eval/blob/2362660e02c324df281932cc23ad7efd31cd3957/src/pytrec_eval.cpp#L354>
    ]

    def __init__(self):
        super().__init__()
        self.pytrec_eval = None

    @contextlib.contextmanager
    def _calc_ctxt(self, measures, qrels):
        # Convert qrels to dict_of_dict (input format used by pytrec_eval)
        qrels = ir_measures.util.QrelsConverter(qrels).as_dict_of_dict()

        # Depending on the measure params, we may need multiple invocations of pytrec_eval
        # (e.g., with different rel_level, since it only supports running with 1 rel_level at a time)
        invokers = self._build_invokers(measures, qrels)

        def _iter_calc(run):
            # Convert qrels to dict_of_dict (input format used by pytrec_eval)
            run = ir_measures.util.RunConverter(run).as_dict_of_dict()
            for invoker in invokers:
                yield from invoker.iter_calc(run)

        yield _iter_calc
        del invokers

    def _build_invokers(self, measures, qrels):
        invocations = {}
        for measure in ir_measures.util.flatten_measures(measures):
            if measure.NAME == 'P':
                invocation_key = (measure['rel'],)
                measure_str = f'P_{measure["cutoff"]}'
            elif measure.NAME == 'RR':
                invocation_key = (measure['rel'],)
                measure_str = f'recip_rank'
            elif measure.NAME == 'Rprec':
                invocation_key = (measure['rel'],)
                measure_str = f'Rprec'
            elif measure.NAME == 'AP':
                invocation_key = (measure['rel'],)
                if measure['cutoff'] is NOT_PROVIDED:
                    measure_str = f'map'
                else:
                    measure_str = f'map_cut_{measure["cutoff"]}'
            elif measure.NAME == 'infAP':
                invocation_key = (measure['rel'],)
                measure_str = f'infAP'
            elif measure.NAME == 'nDCG':
                # Doesn't matter where this goes... Put it in an existing invocation, or just (1,) if none yet exist
                if invocations:
                    invocation_key = next(iter(invocations))
                else:
                    invocation_key = (1,)
                if measure['cutoff'] is NOT_PROVIDED:
                    measure_str = f'ndcg'
                else:
                    measure_str = f'ndcg_cut_{measure["cutoff"]}'
            elif measure.NAME == 'R':
                invocation_key = (measure['rel'],)
                measure_str = f'recall_{measure["cutoff"]}'
            elif measure.NAME == 'Bpref':
                invocation_key = (measure['rel'],)
                measure_str = f'bpref'
            elif measure.NAME == 'NumRet':
                if measure['rel'] is NOT_PROVIDED:
                    # Doesn't matter where this goes... Put it in an existing invocation, or just (1,) if none yet exist
                    if invocations:
                        invocation_key = next(iter(invocations))
                    else:
                        invocation_key = (1,)
                    measure_str = 'num_ret'
                else:
                    invocation_key = (measure['rel'],)
                    measure_str = 'num_rel_ret'
            elif measure.NAME == 'NumQ':
                # Doesn't matter where this goes... Put it in an existing invocation, or just (1,) if none yet exist
                if invocations:
                    invocation_key = next(iter(invocations))
                else:
                    invocation_key = (1,)
                measure_str = 'num_q'
            elif measure.NAME == 'NumRel':
                invocation_key = (measure['rel'],)
                measure_str = 'num_rel'
            elif measure.NAME == 'SetP':
                invocation_key = (measure['rel'],)
                measure_str = f'set_P'
            elif measure.NAME == 'Success':
                invocation_key = (measure['rel'],)
                measure_str = f'success_{measure["cutoff"]}'
            elif measure.NAME == 'IPrec':
                invocation_key = (measure['rel'],)
                measure_str = f'iprec_at_recall_{measure["recall"]:.2f}'
            else:
                raise ValueError(f'unsupported measure {measure}')

            if invocation_key not in invocations:
                invocations[invocation_key] = {}
            invocations[invocation_key][measure_str] = measure

        invokers = []
        for (rel_level, ), measure_map in invocations.items():
            invokers.append(PytrecEvalInvoker(self.pytrec_eval, qrels, measure_map, rel_level))

        return invokers

    def initialize(self):
        try:
            import pytrec_eval
            self.pytrec_eval = pytrec_eval
        except ImportError as ex:
            raise RuntimeError('pytrec_eval not available', ex)


class PytrecEvalInvoker:
    def __init__(self, pte, qrels, measure_map, rel_level):
        self.evaluator = pte.RelevanceEvaluator(qrels, measure_map.keys(), relevance_level=rel_level)
        self.measure_map = measure_map

    def iter_calc(self, run):
        result = self.evaluator.evaluate(run)
        for query_id, measures in result.items():
            for measure_str, value in measures.items():
                yield Metric(query_id=query_id, measure=self.measure_map[measure_str], value=value)

    def __del__(self):
        del self.evaluator


providers.register(PytrecEvalProvider())
