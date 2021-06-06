import io
import pkgutil
import subprocess
import tempfile
import contextlib
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.providers.base import Any, Choices, NOT_PROVIDED


class GdevalProvider(providers.Provider):
    """
    gdeval
    """
    NAME = 'gdeval'
    SUPPORTED_MEASURES = [
        measures._nDCG(cutoff=Any(required=True), dcg=Choices('exp-log2')),
        measures._ERR(cutoff=Any(required=True)),
    ]

    def _evaluator(self, measures, qrels):
        MEASURES = ('nDCG', 'ERR')
        cutoffs = {}
        for measure in ir_measures.util.flatten_measures(measures):
            if measure.NAME in MEASURES:
                cutoff = measure['cutoff']
                if cutoff not in cutoffs:
                    cutoffs[cutoff] = [None] * len(MEASURES)
                cutoffs[cutoff][MEASURES.index(measure.NAME)] = measure
            else:
                raise ValueError(f'unsupported measure {measure}')
        invocations = []
        for cutoff, (NDCG, ERR) in cutoffs.items():
            invocations.append((cutoff, NDCG, ERR))
        qrels = list(ir_measures.util.QrelsConverter(qrels).as_namedtuple_iter())
        return GdevalEvaluator(measures, qrels, invocations)

    def initialize(self):
        try:
            subprocess.check_output(['perl', '--version'])
        except CalledProcessError as ex:
            raise RuntimeError('perl not available', ex)


class GdevalEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels, invocations):
        super().__init__(measures, set(q.query_id for q in qrels))
        self.qrels = qrels
        self.invocations = invocations

    def _iter_calc(self, run):
        with tempfile.NamedTemporaryFile() as perlf, \
             ir_measures.util.QrelsConverter(self.qrels).as_tmp_file() as qrelsf, \
             ir_measures.util.RunConverter(run).as_tmp_file() as runf:
            perlf_contents = pkgutil.get_data('ir_measures', 'bin/gdeval.pl')
            perlf.write(perlf_contents)
            perlf.flush()
            for cutoff, nDCG_measure, ERR_measure in self.invocations:
                cmd = ['perl', perlf.name, qrelsf.name, runf.name, str(cutoff)]
                output = subprocess.check_output(cmd)
                output = output.decode().replace('\t', ' ').split('\n')
                for i, s in enumerate(output):
                    if s == '' or i == 0:
                        continue
                    arr = s.split(',')
                    assert len(arr) == 4
                    _, qid, ndcg, err = arr
                    if nDCG_measure is not None:
                        yield Metric(query_id=qid, measure=nDCG_measure, value=float(ndcg))
                    if ERR_measure is not None:
                        yield Metric(query_id=qid, measure=ERR_measure, value=float(err))


providers.register(GdevalProvider())
