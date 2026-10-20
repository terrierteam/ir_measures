import pkgutil
import subprocess
import tempfile
import warnings
from collections import defaultdict
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.providers.base import Any, Choices, NOT_PROVIDED


MAX_JUDGMENT = 4  # hard-coded in gdeval.pl


class GdevalProvider(providers.Provider):
    """
    gdeval
    """
    NAME = 'gdeval'
    SUPPORTED_MEASURES = [
        measures._nDCG(cutoff=Any(required=True), dcg=Choices('exp-log2'), gains=Choices(NOT_PROVIDED), judged_only=Choices(False)),
        measures._ERR(cutoff=Any(required=True)),
    ]

    def _evaluator(self, measures, qrels):
        MEASURES = ('nDCG', 'ERR')
        cutoffs = {}
        for measure in measures:
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
        max_rel = max((q.relevance for q in qrels), default=0)
        if max_rel > MAX_JUDGMENT:
            raise ValueError(f'gdeval only supports relevance grades up to {MAX_JUDGMENT}, but qrels contain grade {max_rel}')
        if max_rel < MAX_JUDGMENT and any(ERR is not None for _, _, ERR in invocations):
            warnings.warn(f'gdeval computes ERR assuming a maximum relevance grade of {MAX_JUDGMENT}, but the highest grade in qrels is {max_rel}; '
                          'ERR values will differ from an ERR that uses the maximum grade in the qrels.')
        return GdevalEvaluator(measures, qrels, invocations)

    def initialize(self):
        import shutil
        if not shutil.which("perl"):
            raise RuntimeError('perl not available')

    def install_instructions(self):
        return 'Install perl, see <https://www.perl.org>'


class GdevalEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels, invocations):
        super().__init__(measures, set(q.query_id for q in qrels))
        # gdeval.pl only accepts integer query ids, so use integers internally and map back afterwards
        self.qid_map = defaultdict(lambda: len(self.qid_map))
        self.qrels = [q._replace(query_id=str(self.qid_map[q.query_id])) for q in qrels]
        self.invocations = invocations

    def _iter_calc(self, run):
        qid_map = defaultdict(lambda: len(qid_map), self.qid_map)
        def remap(run):
            for d in ir_measures.util.RunConverter(run).as_namedtuple_iter():
                yield d._replace(query_id=str(qid_map[d.query_id]))
        run = list(remap(run))
        qid_unmap = {str(v): k for k, v in qid_map.items()}
        with tempfile.NamedTemporaryFile() as perlf, \
             ir_measures.util.QrelsConverter(self.qrels).as_tmp_file() as qrelsf, \
             ir_measures.util.RunConverter(run).as_tmp_file() as runf:
            perlf_contents = pkgutil.get_data('ir_measures', 'bin/gdeval.pl')
            perlf.write(perlf_contents)
            perlf.flush()
            for cutoff, nDCG_measure, ERR_measure in self.invocations:
                cmd = ['perl', perlf.name, qrelsf.name, runf.name, str(cutoff)]
                proc = subprocess.run(cmd, capture_output=True, check=False)
                if proc.returncode != 0:
                    raise RuntimeError(f'gdeval failed with exit status {proc.returncode}: {proc.stderr.decode().strip()}')
                output = proc.stdout
                output = output.decode().replace('\t', ' ').split('\n')
                for i, s in enumerate(output):
                    if s == '' or i == 0:
                        continue
                    arr = s.split(',')
                    assert len(arr) == 4
                    _, qid, ndcg, err = arr
                    if nDCG_measure is not None:
                        yield Metric(query_id=qid_unmap[qid], measure=nDCG_measure, value=float(ndcg))
                    if ERR_measure is not None:
                        yield Metric(query_id=qid_unmap[qid], measure=ERR_measure, value=float(err))


providers.register(GdevalProvider())
