import pkgutil
import subprocess
import tempfile
import contextlib
import ir_measures
from ir_measures import providers, measures
from ir_measures.providers.base import Any, Choices, Metric, NOT_PROVIDED


class GdevalProvider(providers.MeasureProvider):
    NAME = 'gdeval'
    SUPPORTED_MEASURES = [
        measures._nDCG(cutoff=Any(required=True), dcg=Choices('exp-log2')),
        measures._ERR(cutoff=Any(required=True)),
    ]

    def __init__(self):
        super().__init__()
        self._perlf = None

    @contextlib.contextmanager
    def _calc_ctxt(self, measures, qrels):
        cutoffs = {}
        for measure in ir_measures.util.flatten_measures(measures):
            if measure.NAME in ('nDCG', 'ERR'):
                cutoff = measure['cutoff']
                if cutoff not in cutoffs:
                    cutoffs[cutoff] = []
                cutoffs[cutoff].append(measure)
            else:
                raise ValueError(f'unsupported measure {measure}')

        # Convert qrels to file
        with ir_measures.util.QrelsConverter(qrels).as_tmp_file() as f_qrels:
            def _iter_calc(run):
                # Convert run to file
                with ir_measures.util.RunConverter(run).as_tmp_file() as f_run:
                    for cutoff, measures in cutoffs.items():
                        yield from self._invoke_iter(f_qrels.name, f_run.name, cutoff, measures)

            yield _iter_calc

    def _invoke_iter(self, qrelsf, runf, cutoff, measures):
        """
        Runs gdeval.pl on the given run/qrels pair
        """
        # adapted from searchivarius/AccurateLuceneBM25/scripts/eval_output_gdeval.py
        nDCG_measure, ERR_measure = None, None
        for measure in measures:
            if measure.NAME == 'nDCG':
                nDCG_measure = measure
            elif measure.NAME == 'ERR':
                ERR_measure = measure

        cmd = ['perl', self._perlf.name, qrelsf, runf, str(cutoff)]
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

    def initialize(self):
        try:
            subprocess.check_output(['perl', '--version'])
        except CalledProcessError as ex:
            raise RuntimeError('perl not available', ex)
        perlf_contents = pkgutil.get_data('ir_measures', 'bin/gdeval.pl')
        self._perlf = tempfile.NamedTemporaryFile()
        self._perlf.write(perlf_contents)
        self._perlf.flush()


providers.register(GdevalProvider())
