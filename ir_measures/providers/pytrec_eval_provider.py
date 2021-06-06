import contextlib
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.providers.base import Any, Choices, NOT_PROVIDED


class PytrecEvalProvider(providers.Provider):
    """
    pytrec_eval

    https://github.com/cvangysel/pytrec_eval

::

    @inproceedings{VanGysel2018pytreceval,
        title={Pytrec\\_eval: An Extremely Fast Python Interface to trec\\_eval},
        author={Van Gysel, Christophe and de Rijke, Maarten},
        publisher={ACM},
        booktitle={SIGIR},
        year={2018},
    }

    """
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
        measures._NumQ(),
        measures._NumRel(rel=Choices(1)), # for some reason, relevance_level doesn't flow through to num_rel, so can only support rel=1
        measures._SetAP(rel=Any()),
        measures._SetF(rel=Any(), beta=Any()),
        measures._SetP(rel=Any(), relative=Any()),
        measures._SetR(rel=Any()),
        measures._Success(rel=Any(), cutoff=Any()),
        measures._IPrec(recall=Any()),
        measures._infAP(rel=Any()),
        # Cannot support Judged because software doesn't support negative relevance levels: <https://github.com/cvangysel/pytrec_eval/blob/2362660e02c324df281932cc23ad7efd31cd3957/src/pytrec_eval.cpp#L354>
    ]

    def __init__(self):
        super().__init__()
        self.pytrec_eval = None

    def _evaluator(self, measures, qrels):
        measures = ir_measures.util.flatten_measures(measures)
        # Convert qrels to dict_of_dict (input format used by pytrec_eval)
        qrels = ir_measures.util.QrelsConverter(qrels).as_dict_of_dict()

        # Depending on the measure params, we may need multiple invocations of pytrec_eval
        # (e.g., with different rel_level, since it only supports running with 1 rel_level at a time)
        invokers = self._build_invokers(measures, qrels)
        return PytrecEvalEvaluator(measures, invokers, qrels)

    def _build_invokers(self, measures, qrels):
        invocations = {}
        setf_count = 0
        for measure in measures:
            match_str = None
            if measure.NAME == 'P':
                invocation_key = (measure['rel'], 0)
                measure_str = f'P_{measure["cutoff"]}'
            elif measure.NAME == 'RR':
                invocation_key = (measure['rel'], 0)
                measure_str = f'recip_rank'
            elif measure.NAME == 'Rprec':
                invocation_key = (measure['rel'], 0)
                measure_str = f'Rprec'
            elif measure.NAME == 'AP':
                invocation_key = (measure['rel'], 0)
                if measure['cutoff'] is NOT_PROVIDED:
                    measure_str = f'map'
                else:
                    measure_str = f'map_cut_{measure["cutoff"]}'
            elif measure.NAME == 'infAP':
                invocation_key = (measure['rel'], 0)
                measure_str = f'infAP'
            elif measure.NAME == 'nDCG':
                # Doesn't matter where this goes... Put it in an existing invocation, or just (1,) if none yet exist
                if invocations:
                    invocation_key = next(iter(invocations))
                else:
                    invocation_key = (1, 0)
                if measure['cutoff'] is NOT_PROVIDED:
                    measure_str = f'ndcg'
                else:
                    measure_str = f'ndcg_cut_{measure["cutoff"]}'
            elif measure.NAME == 'R':
                invocation_key = (measure['rel'], 0)
                measure_str = f'recall_{measure["cutoff"]}'
            elif measure.NAME == 'Bpref':
                invocation_key = (measure['rel'], 0)
                measure_str = f'bpref'
            elif measure.NAME == 'NumRet':
                if measure['rel'] is NOT_PROVIDED:
                    # Doesn't matter where this goes... Put it in an existing invocation, or just (1,) if none yet exist
                    if invocations:
                        invocation_key = next(iter(invocations))
                    else:
                        invocation_key = (1, 0)
                    measure_str = 'num_ret'
                else:
                    invocation_key = (measure['rel'], 0)
                    measure_str = 'num_rel_ret'
            elif measure.NAME == 'NumQ':
                # Doesn't matter where this goes... Put it in an existing invocation, or just (1,) if none yet exist
                if invocations:
                    invocation_key = next(iter(invocations))
                else:
                    invocation_key = (1, 0)
                measure_str = 'num_q'
            elif measure.NAME == 'NumRel':
                invocation_key = (measure['rel'], 0)
                measure_str = 'num_rel'
            elif measure.NAME == 'SetAP':
                invocation_key = (measure['rel'], 0)
                measure_str = f'set_map'
            elif measure.NAME == 'SetF':
                # set_F is strange (or buggy?) in both trec_eval and pytrec_eval. It only accepts
                # the first beta argument it's given, which is why we use the setf_count approach
                # to handle multiple invocations. It also is always reported as the name set_F by
                # pytrec_eval, so we need different measure_str and match_str here.
                invocation_key = (measure['rel'], setf_count)
                setf_count += 1
                measure_str = f'set_F_{measure["beta"]}'
                match_str = 'set_F'
                if measure['beta'] == 1.:
                    measure_str = f'set_F'
                else:
                    measure_str = f'set_F_{measure["beta"]}'
            elif measure.NAME == 'SetP':
                if measure['relative']:
                    invocation_key = (measure['rel'], 0)
                    measure_str = f'set_relative_P'
                else:
                    invocation_key = (measure['rel'], 0)
                    measure_str = f'set_P'
            elif measure.NAME == 'SetR':
                invocation_key = (measure['rel'], 0)
                measure_str = f'set_recall'
            elif measure.NAME == 'Success':
                invocation_key = (measure['rel'], 0)
                measure_str = f'success_{measure["cutoff"]}'
            elif measure.NAME == 'IPrec':
                invocation_key = (measure['rel'], 0)
                measure_str = f'iprec_at_recall_{measure["recall"]:.2f}'
            else:
                raise ValueError(f'unsupported measure {measure}')

            if match_str is None:
                match_str = measure_str

            if invocation_key not in invocations:
                invocations[invocation_key] = {}
            invocations[invocation_key][match_str] = (measure, measure_str)

        invokers = []
        for (rel_level, it), measure_map in invocations.items():
            invokers.append(PytrecEvalInvoker(self.pytrec_eval, qrels, measure_map, rel_level))

        return invokers

    def initialize(self):
        try:
            import pytrec_eval
            self.pytrec_eval = pytrec_eval
        except ImportError as ex:
            raise RuntimeError('pytrec_eval not available', ex)


class PytrecEvalEvaluator(providers.Evaluator):
    def __init__(self, measures, invokers, qrels):
        super().__init__(measures, set(qrels.keys()))
        self.invokers = invokers

    def _iter_calc(self, run):
        # Convert qrels to dict_of_dict (input format used by pytrec_eval)
        run = ir_measures.util.RunConverter(run).as_dict_of_dict()
        for invoker in self.invokers:
            yield from invoker.iter_calc(run)


class PytrecEvalInvoker:
    def __init__(self, pte, qrels, measure_map, rel_level):
        self.evaluator = pte.RelevanceEvaluator(qrels, [m for _, m in measure_map.values()], relevance_level=rel_level)
        self.measure_map = measure_map

    def iter_calc(self, run):
        result = self.evaluator.evaluate(run)
        for query_id, measures in result.items():
            for measure_str, value in measures.items():
                yield Metric(query_id=query_id, measure=self.measure_map[measure_str][0], value=value)


providers.register(PytrecEvalProvider())
