import io
import contextlib
import itertools
import tempfile
from collections import namedtuple
import ir_measures


GenericQrel = namedtuple('GenericQrel', ['query_id', 'doc_id', 'relevance'])
GenericScoredDoc = namedtuple('GenericScoredDoc', ['query_id', 'doc_id', 'score'])


class QrelsConverter:
    def __init__(self, qrels):
        self.qrels = qrels
        self._predicted_format = None

    def tee(self, count):
        t = self.predict_type()
        if t == 'namedtuple_iter':
            teed_qrels = itertools.tee(self.qrels, count)
            return [QrelsConverter(qrels) for qrels in teed_qrels]
        return [self for _ in range(count)]

    def predict_type(self):
        if self._predicted_format:
            return self._predicted_format
        result = 'UNKNOWN'
        if isinstance(self.qrels, dict):
            result = 'dict_of_dict'
        elif hasattr(self.qrels, 'itertuples'):
            cols = self.qrels.columns
            if all(i in columns for i in GenericQrel._fields):
                result = 'pd_dataframe'
        elif hasattr(self.qrels, '__iter__'):
            # peek
            # TODO: is this an OK approach?
            self.qrels, peek_qrels = itertools.tee(self.qrels, 2)
            sentinal = object()
            item = next(peek_qrels, sentinal)
            if isinstance(item, tuple) and hasattr(item, '_fields'):
                if all(i in item._fields for i in GenericQrel._fields):
                    result = 'namedtuple_iter'
            elif item is sentinal:
                result = 'namedtuple_iter'
        self._predicted_format = result
        return result

    def as_dict_of_dict(self):
        t = self.predict_type()
        if t == 'dict_of_dict':
            return self.qrels
        else:
            result = {}
            for qrel in self.as_namedtuple_iter():
                if qrel.query_id not in result:
                    result[qrel.query_id] = {}
                result[qrel.query_id][qrel.doc_id] = qrel.relevance
            return result

    def as_namedtuple_iter(self):
        t = self.predict_type()
        if t == 'namedtuple_iter':
            yield from self.qrels
        if t == 'dict_of_dict':
            for query_id, docs in self.qrels.items():
                for doc_id, relevance in docs.items():
                    yield GenericQrel(query_id=query_id, doc_id=doc_id, relevance=relevance)
        if t == 'pd_dataframe':
            yield from self.qrels.itertuples()
        if t == 'UNKNOWN':
            raise ValueError('unknown qrels format')

    def as_pd_dataframe(self):
        t = self.predict_type()
        if t == 'pd_dataframe':
            return self.qrels
        else:
            pd = ir_measures.lazylibs.pandas()
            return pd.DataFrame(self.as_namedtuple_iter())

    @contextlib.contextmanager
    def as_tmp_file(self):
        with tempfile.NamedTemporaryFile(mode='w+t') as f:
            for qrel in self.as_namedtuple_iter():
                f.write('{query_id} 0 {doc_id} {relevance}\n'.format(**qrel._asdict()))
            f.flush()
            f.seek(0)
            yield f




class RunConverter:
    def __init__(self, run):
        self.run = run

    def tee(self, count):
        t = self.predict_type()
        if t == 'namedtuple_iter':
            teed_run = itertools.tee(self.run, count)
            return [RunConverter(run) for run in teed_run]
        return [self for _ in range(count)]

    def predict_type(self):
        if isinstance(self.run, dict):
            return 'dict_of_dict'
        if hasattr(self.run, 'itertuples'):
            cols = self.run.columns
            if all(i in cols for i in GenericScoredDoc._fields):
                return 'pd_dataframe'
        if hasattr(self.run, '__iter__'):
            # peek
            # TODO: is this an OK approach?
            self.run, peek_run = itertools.tee(self.run, 2)
            sentinal = object()
            item = next(peek_run, sentinal)
            if isinstance(item, tuple) and hasattr(item, '_fields'):
                if all(i in item._fields for i in GenericScoredDoc._fields):
                    return 'namedtuple_iter'
            if item is sentinal:
                return 'namedtuple_iter'
        return 'UNKNOWN'

    def as_dict_of_dict(self):
        t = self.predict_type()
        if t == 'dict_of_dict':
            return self.run
        else:
            result = {}
            for scored_doc in self.as_namedtuple_iter():
                if scored_doc.query_id not in result:
                    result[scored_doc.query_id] = {}
                result[scored_doc.query_id][scored_doc.doc_id] = scored_doc.score
            return result

    def as_namedtuple_iter(self):
        t = self.predict_type()
        if t == 'namedtuple_iter':
            yield from self.run
        if t == 'dict_of_dict':
            for query_id, docs in self.run.items():
                for doc_id, score in docs.items():
                    yield GenericScoredDoc(query_id=query_id, doc_id=doc_id, score=score)
        if t == 'pd_dataframe':
            yield from self.run.itertuples()
        if t == 'UNKNOWN':
            raise ValueError('unknown run format')

    def as_pd_dataframe(self):
        t = self.predict_type()
        if t == 'pd_dataframe':
            return self.run
        else:
            pd = ir_measures.lazylibs.pandas()
            return pd.DataFrame(self.as_namedtuple_iter())

    @contextlib.contextmanager
    def as_tmp_file(self):
        with tempfile.NamedTemporaryFile(mode='w+t') as f:
            ranks = {}
            for scoreddoc in self.as_namedtuple_iter():
                key = scoreddoc.query_id
                rank = ranks.setdefault(key, 0)
                f.write('{query_id} Q0 {doc_id} {rank} {score} run\n'.format(**scoreddoc._asdict(), rank=rank))
                ranks[key] += 1
            f.flush()
            f.seek(0)
            yield f


def parse_trec_qrels(file):
    if hasattr(file, 'read'):
        for line in file:
            if line.strip():
                query_id, iteration, doc_id, relevance = line.split()
                yield GenericQrel(query_id=query_id, doc_id=doc_id, relevance=int(relevance))
    elif isinstance(file, str):
        if '\n' in file:
            yield from parse_trec_qrels(io.StringIO(file))
        else:
            with open(file, 'rt') as f:
                yield from parse_trec_qrels(f)


def parse_trec_run(file):
    if hasattr(file, 'read'):
        for line in file:
            if line.strip():
                query_id, iteration, doc_id, rank, score, tag = line.split()
                yield GenericScoredDoc(query_id=query_id, doc_id=doc_id, score=float(score))
    elif isinstance(file, str):
        if '\n' in file:
            yield from parse_trec_run(io.StringIO(file))
        else:
            with open(file, 'rt') as f:
                yield from parse_trec_run(f)

def flatten_measures(measures):
    result = set()
    for measure in measures:
        if isinstance(measure, ir_measures.measures.MultiMeasures):
            result = result | measure.measures
        else:
            result.add(measure)
    return result
