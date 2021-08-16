import contextlib
import sys
from typing import NamedTuple, Union
from cwl.cwl_eval import TrecQrelHandler, RankingMaker
from cwl.ruler.cwl_ruler import CWLRuler, PrecisionCWLMetric, RRCWLMetric, APCWLMetric, RBPCWLMetric, NDCGCWLMetric
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.providers.base import Any, Choices, NOT_PROVIDED


class CwlMetric(NamedTuple):
    query_id: str
    measure: 'Measure'
    value: Union[float, int] # i.e., expected_utility
    expected_total_utility: float
    expected_cost: float
    expected_total_cost: float
    expected_items: float


class CwlEvalProvider(providers.Provider):
    """
    cwl_eval, providing C/W/L ("cool") framework measures
    """
    NAME = 'cwl_eval'
    SUPPORTED_MEASURES = [
        measures._P(cutoff=Any(), rel=Any()),
        measures._RR(cutoff=Choices(NOT_PROVIDED), rel=Any()),
        measures._AP(cutoff=Choices(NOT_PROVIDED), rel=Any()),
        measures._RBP(cutoff=Choices(NOT_PROVIDED), rel=Any(), p=Any()),
        # measures._nDCG(cutoff=Any(required=True), dcg=Choices('exp-log2')),
    ]

    def _evaluator(self, measures, qrels):
        # TODO: qrh.validate_gains(min_gain=min_gain, max_gain=max_gain)?
        # How to determine minimum + maximum gains? Can these be inferred from the qrels? If so, what's the point of validating?
        # If there was a tigher coupling with ir_datasets, the dataset itself would provide this information via qrels_defs.
        invocations = {}
        measures = ir_measures.util.flatten_measures(measures)
        for measure in measures:
            if measure.NAME in ('P', 'RR', 'AP', 'RBP'):
                inv_key = (measure['rel'],)
            elif measure.NAME in ('nDCG',):
                inv_key = (None,)
            if inv_key not in invocations:
                invocations[inv_key] = []
            invocations[inv_key].append(measure)
        return CwlEvaluator(measures, qrels, invocations)


class IrmQrelHandler(TrecQrelHandler):
    def __init__(self, min_rel):
        super().__init__(None) # file name = None
        self.min_rel = min_rel

    def read_file(self, qrels):
        pass # disable reading from file, we build these below

    def put_value(self, query_id, doc_id, relevance):
        if self.min_rel is not None:
            relevance = 1 if relevance >= self.min_rel else 0
        super().put_value(query_id, doc_id, relevance)


class CwlEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels, invocations):
        super().__init__(measures)
        self.qrhs = {}
        for inv_key in invocations.keys():
            self.qrhs[inv_key] = IrmQrelHandler(*inv_key)
        for qrel in ir_measures.util.QrelsConverter(qrels).as_namedtuple_iter():
            for qrh in self.qrhs.values():
                qrh.put_value(qrel.query_id, qrel.doc_id, qrel.relevance)
        self.invocations = invocations

    def iter_calc(self, run):
        # adapted from cwl_eval's main() method
        # TODO: set these properly:
        costs = None
        max_gain = 1.0
        min_gain = 0.0
        max_cost = 1.0
        min_cost = 1.0
        max_depth = 1000
        ranking_makers = None
        curr_qid = None
        for item in ir_measures.util.RunConverter(run).as_sorted_namedtuple_iter():
            if item.query_id != curr_qid:
                if curr_qid is not None:
                    yield from self.flush(curr_qid, ranking_makers)
                curr_qid = item.query_id
                ranking_makers = {}
                for inv_key in self.invocations.keys():
                    ranking_makers[inv_key] = RankingMaker(curr_qid, self.qrhs[inv_key], costs, max_gain=max_gain, max_cost=max_cost, min_cost=min_cost, max_n=max_depth)
            for maker in ranking_makers.values():
                maker.add(item.doc_id, "_")

        if curr_qid is not None:
            yield from self.flush(curr_qid, ranking_makers)

    def flush(self, qid, ranking_makers):
        rankings = {inv_key: maker.get_ranking() for inv_key, maker in ranking_makers.items()}
        for inv_key, measures in self.invocations.items():
            for measure in measures:
                cwl_measure = self._irm_convert_to_measure(measure)
                value = cwl_measure.measure(rankings[inv_key])
                yield CwlMetric(query_id=qid, measure=measure,
                    value=value,
                    expected_total_utility=cwl_measure.expected_total_utility,
                    expected_cost=cwl_measure.expected_cost,
                    expected_total_cost=cwl_measure.expected_total_cost,
                    expected_items=cwl_measure.expected_items)

    def _irm_convert_to_measure(self, measure):
        if measure.NAME == 'P':
            return PrecisionCWLMetric(measure['cutoff'])
        if measure.NAME == 'RR':
            return RRCWLMetric()
        if measure.NAME == 'AP':
            return APCWLMetric()
        if measure.NAME == 'RBP':
            return RBPCWLMetric(measure['p'])
        if measure.NAME == 'nDCG':
            return NDCGCWLMetric(measure['cutoff'])
        raise KeyError(f'measure {measure} not supported')


providers.register(CwlEvalProvider())
