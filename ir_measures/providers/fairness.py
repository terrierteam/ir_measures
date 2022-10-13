from typing import Iterable, Iterator, Final

from pandas import DataFrame

from ir_measures.measures.fairness import FairnessMeasure, rND, rKL, rRD
from ir_measures.providers import Provider, Evaluator, register
from ir_measures.util import (
    flatten_measures, QrelsConverter, RunConverter, Metric, Run, Qrels
)


class FairnessEvaluator(Evaluator):
    _measures: Final[Iterable[FairnessMeasure]]
    _qrels: Final[DataFrame]

    def __init__(self, measures: Iterable[FairnessMeasure], qrels: DataFrame):
        super().__init__(measures, set(self._qrels["query_id"].unique()))
        self._measures = measures
        self._qrels = qrels

    def _iter_calc(self, run: Run) -> Iterator[Metric]:
        run: DataFrame = RunConverter(run).as_pd_dataframe()
        run.sort_values(
            by=["query_id", "score"],
            ascending=[True, False],
            inplace=True,
        )
        for measure in self._measures:
            yield from measure.measure(self._qrels, run)


class FairnessProvider(Provider):
    """
    Group fairness measures from the papers:

    - Measuring Fairness in Ranked Outputs:
      https://doi.org/10.1145/3085504.3085526
      https://github.com/DataResponsibly/FairRank
    - Evaluating Fairness in Argument Retrieval:
      https://doi.org/10.1145/3459637.3482099
      https://github.com/sachinpc1993/fair-arguments
    """

    NAME = "fairness"
    SUPPORTED_MEASURES = [rND, rKL, rRD]
    _is_available = True

    def _evaluator(
            self,
            measures: Iterable[FairnessMeasure],
            qrels: Qrels
    ) -> FairnessEvaluator:
        measures = flatten_measures(measures)
        qrels: DataFrame = QrelsConverter(qrels).as_pd_dataframe()
        qrels.sort_values(
            by=["query_id", "doc_id"],
            inplace=True,
        )
        return FairnessEvaluator(measures, qrels)


_provider = FairnessProvider()
register(_provider)
