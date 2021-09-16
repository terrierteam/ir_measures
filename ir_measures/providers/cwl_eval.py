import logging
import sys
from typing import NamedTuple, Union
from cwl.cwl_eval import TrecQrelHandler, RankingMaker
from cwl.ruler.cwl_ruler import CWLRuler, PrecisionCWLMetric, RRCWLMetric, APCWLMetric, RBPCWLMetric, BPMCWLMetric, NDCGCWLMetric, NERReq8CWLMetric, NERReq9CWLMetric, NERReq10CWLMetric, NERReq11CWLMetric, INSTCWLMetric, INSQCWLMetric
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.providers.base import Any, Choices, NOT_PROVIDED
import logging

logger = logging.getLogger('ir_measures.cwl_eval')
logger.setLevel('WARNING')


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
    cwl_eval, providing C/W/L ("cool") framework measures.

    https://github.com/ireval/cwl

::

    @inproceedings{azzopardi2019cwl,
      author = {Azzopardi, Leif and Thomas, Paul and Moffat, Alistair},
      title = {cwl\\_eval: An Evaluation Tool for Information Retrieval},
      booktitle = {SIGIR},
      year = {2019}
    }
    """
    NAME = 'cwl_eval'
    SUPPORTED_MEASURES = [
        measures._P(cutoff=Any(), rel=Any()),
        measures._RR(cutoff=Choices(NOT_PROVIDED), rel=Any()),
        measures._AP(cutoff=Choices(NOT_PROVIDED), rel=Any()),
        measures._RBP(cutoff=Choices(NOT_PROVIDED), rel=Any(required=True), p=Any()),
        measures._BPM(cutoff=Any(), T=Any(), min_rel=Any(), max_rel=Any(required=True)),
        measures._SDCG(cutoff=Any(required=True), dcg=Choices('log2'), min_rel=Any(), max_rel=Any(required=True)),
        measures._NERR8(cutoff=Any(required=True), min_rel=Any(), max_rel=Any(required=True)),
        measures._NERR9(cutoff=Any(required=True), min_rel=Any(), max_rel=Any(required=True)),
        measures._NERR10(p=Any(), min_rel=Any(), max_rel=Any(required=True)),
        measures._NERR11(T=Any(), min_rel=Any(), max_rel=Any(required=True)),
        measures._INST(T=Any(), min_rel=Any(), max_rel=Any(required=True)),
        measures._INSQ(T=Any(), min_rel=Any(), max_rel=Any(required=True)),
    ]

    def _evaluator(self, measures, qrels):
        invocations = {}
        measures = ir_measures.util.flatten_measures(measures)
        for measure in measures:
            if measure.NAME in ('P', 'RR', 'AP', 'RBP'):
                inv_key = (measure['rel'], None, None)
            elif measure.NAME in ('BPM', 'SDCG', 'NERR8', 'NERR9', 'NERR10', 'NERR11', 'INST', 'INSQ'):
                inv_key = (None, measure['min_rel'], measure['max_rel'])
            if inv_key not in invocations:
                invocations[inv_key] = []
            invocations[inv_key].append(measure)
        return CwlEvaluator(measures, qrels, invocations)

    def initialize(self):
        # disable the cwl logger (which writes to cwl.log)
        cwl_logger = logging.getLogger('cwl')
        cwl_logger.disabled = True


class IrmQrelHandler(TrecQrelHandler):
    def __init__(self, bin_rel_cutoff, min_rel, max_rel):
        super().__init__(None) # file name = None
        self.bin_rel_cutoff = bin_rel_cutoff
        self.min_rel = min_rel
        self.max_rel = max_rel
        if self.bin_rel_cutoff is None:
            assert self.min_rel is not None and self.max_rel is not None, "must provide either bin_rel_cutoff xor (BOTH min_rel and max_rel)"
            assert self.min_rel < self.max_rel, "min_rel must be less than max_rel"
        else:
            assert self.min_rel is None and self.max_rel is None, "must provide either bin_rel_cutoff xor (BOTH min_rel and max_rel)"
        self._min_observed_rel = float('inf')
        self._max_observed_rel = float('-inf')

    def read_file(self, qrels):
        pass # disable reading from file, we build these below

    def put_value(self, query_id, doc_id, relevance):
        if self.bin_rel_cutoff is not None:
            relevance = 1 if relevance >= self.bin_rel_cutoff else 0
        else:
            self._min_observed_rel = min(self._min_observed_rel, relevance)
            self._max_observed_rel = max(self._max_observed_rel, relevance)
            # clip value to range [min_rel, max_rel]
            relevance = min(max(relevance, self.min_rel), self.max_rel)
            # scale to be between [0, 1], based on the min_rel, max_rel range
            relevance = (relevance - self.min_rel) / (self.max_rel - self.min_rel)
        super().put_value(query_id, doc_id, relevance)

    def verify_gains(self):
        if self.bin_rel_cutoff is None:
            if self._min_observed_rel < self.min_rel:
                is_typical = self.min_rel == 0 and self._min_observed_rel < 0
                typical_message = ' This is typical and the desired behaviour in most TREC collections (where negative relevance scores are treated equally).' if is_typical else ''
                logger.warning(f'min_rel={self.min_rel} but at least one relevance score of {self._min_observed_rel} was observed. Scores less than {self.min_rel} were treated as {self.min_rel}.{typical_message}')
            if self._min_observed_rel > self.min_rel:
                logger.warning(f'min_rel={self.min_rel} but the lowest relevance score observed was {self._min_observed_rel}.')
            if self._max_observed_rel > self.max_rel:
                logger.warning(f'max_rel={self.max_rel} but at least one relevance score of {self._max_observed_rel} was observed. Scores greater than {self.max_rel} were treated as {self.max_rel}.')
            if self._max_observed_rel < self.max_rel:
                logger.warning(f'max_rel={self.max_rel} but at the highest relevance score observed was {self._max_observed_rel}. This is sometimes expected, e.g., if annotated on a scale up to {self._max_observed_rel} but no such documents were found.')


class CwlEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels, invocations):
        self.qrhs = {}
        for inv_key in invocations.keys():
            self.qrhs[inv_key] = IrmQrelHandler(*inv_key)
        qids = set()
        for qrel in ir_measures.util.QrelsConverter(qrels).as_namedtuple_iter():
            qids.add(qrel.query_id)
            rel = max(qrel.relevance, 0) # clip all negative scores to 0, following trec_eval convention
            for qrh in self.qrhs.values():
                qrh.put_value(qrel.query_id, qrel.doc_id, rel)
        for qrh in self.qrhs.values():
            qrh.verify_gains()
        self.invocations = invocations
        super().__init__(measures, qids)

    def _iter_calc(self, run):
        # adapted from cwl_eval's main() method
        ranking_makers = None
        curr_qid = None
        for item in ir_measures.util.RunConverter(run).as_sorted_namedtuple_iter():
            if item.query_id not in self.qrel_qids:
                continue # skip queries not found in qrels; handled by base
            if item.query_id != curr_qid:
                if curr_qid is not None:
                    yield from self.flush(curr_qid, ranking_makers)
                curr_qid = item.query_id
                ranking_makers = {}
                for inv_key in self.invocations.keys():
                    ranking_makers[inv_key] = RankingMaker(curr_qid, self.qrhs[inv_key], min_gain=0., max_gain=1., cost_dict=None, max_cost=1.0, min_cost=1.0, max_n=1000) # max_n=1000 from cwl_eval default
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
        if measure.NAME == 'BPM':
            return BPMCWLMetric(measure['T'], measure['cutoff'])
        if measure.NAME == 'NERR8':
            return NERReq8CWLMetric(measure['cutoff'])
        if measure.NAME == 'NERR9':
            return NERReq9CWLMetric(measure['cutoff'])
        if measure.NAME == 'NERR10':
            return NERReq10CWLMetric(measure['p'])
        if measure.NAME == 'NERR11':
            return NERReq11CWLMetric(measure['T'])
        if measure.NAME == 'SDCG':
            return NDCGCWLMetric(measure['cutoff'])
        if measure.NAME == 'INST':
            return INSTCWLMetric(measure['T'])
        if measure.NAME == 'INSQ':
            return INSQCWLMetric(measure['T'])
        raise KeyError(f'measure {measure} not supported')


providers.register(CwlEvalProvider())
