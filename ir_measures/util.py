import re
import io
import contextlib
import itertools
import tempfile
from typing import List
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


def convert_trec_name(measure: str) -> List['BaseMeasure']:
    TREC_NAME_MAP = {
        'ndcg': (ir_measures.nDCG, None, None),
        'P': (ir_measures.P, 'cutoff', [5, 10, 15, 20, 30, 100, 200, 500, 1000]),
        'map_cut': (ir_measures.AP, 'cutoff', [5, 10, 15, 20, 30, 100, 200, 500, 1000]),
        'Rndcg': (None, None, None),
        'num_nonrel_judged_ret': (None, None, None),
        'set_map': (None, None, None),
        '11pt_avg': (None, None, None),
        'relative_P': (None, None, None),
        'gm_map': (None, None, None),
        'binG': (None, None, None),
        'set_P': (ir_measures.SetP, None, None),
        'infAP': (ir_measures.infAP, None, None),
        'bpref': (ir_measures.Bpref, None, None),
        'num_rel_ret': (ir_measures.NumRelRet, None, None),
        'ndcg_rel': (None, None, None),
        'recip_rank': (ir_measures.RR, None, None),
        'recall': (ir_measures.R, 'cutoff', [5, 10, 15, 20, 30, 100, 200, 500, 1000]),
        'set_recall': (None, None, None),
        'utility': (None, None, None),
        'set_relative_P': (None, None, None),
        'num_ret': (ir_measures.NumRet, None, None),
        'num_rel': (ir_measures.NumRel, None, None),
        'ndcg_cut': (ir_measures.nDCG, 'cutoff', [5, 10, 15, 20, 30, 100, 200, 500, 1000]),
        'runid': (None, None, None),
        'Rprec': (ir_measures.Rprec, None, None),
        'Rprec_mult': (None, None, None),
        'relstring': (None, None, None),
        'gm_bpref': (None, None, None),
        'num_q': (ir_measures.NumQ, None, None),
        'map': (ir_measures.AP, None, None),
        'G': (None, None, None),
        'success': (ir_measures.Success, 'cutoff', [1, 5, 10]),
        'set_F': (None, None, None),
        'iprec_at_recall': (ir_measures.IPrec, 'recall', [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
    }
    import pytrec_eval
    if measure in pytrec_eval.supported_nicknames:
        result = []
        skipped = []
        for sub_name in sorted(pytrec_eval.supported_nicknames[measure]):
            try:
                result += convert_trec_name(sub_name)
            except ValueError:
                skipped.append(sub_name)
        if skipped:
            print(f'skipped {skipped}: measures not yet supported')
        return result

    # Adapted from <https://github.com/cvangysel/pytrec_eval/blob/master/py/__init__.py#L76>
    RE_BASE = r'{}[\._]([0-9]+(\.[0-9]+)?(,[0-9]+(\.[0-9]+)?)*)'

    # break apart measures in any of the following formats and combine
    #  1) meas          -> {meas: {}}  # either non-parameterized measure or use default params
    #  2) meas.p1       -> {meas: {p1}}
    #  3) meas_p1       -> {meas: {p1}}
    #  4) meas.p1,p2,p3 -> {meas: {p1, p2, p3}}
    #  5) meas_p1,p2,p3 -> {meas: {p1, p2, p3}}
    if measure in TREC_NAME_MAP:
        meas, arg_name, default_args = TREC_NAME_MAP[measure]
        if meas is None:
            raise ValueError(f'known trec name {measure}, but not yet supported')
        if arg_name is not None and default_args is not None:
            result = []
            for arg in default_args:
                result.append(meas(**{arg_name: arg}))
            return result
        return [meas]
    matches = ((m, re.match(RE_BASE.format(re.escape(m)), measure)) for m in TREC_NAME_MAP)
    match = next(filter(lambda x: x[1] is not None, matches), None)
    if match is None:
        raise ValueError('unkonwn measure {}'.format(measure))
    base_meas, meas_args = match[0], match[1].group(1)
    meas, arg_name, _ = TREC_NAME_MAP[base_meas]
    if meas is None:
        raise ValueError(f'known trec name {measure}, but not yet supported')
    if arg_name is None:
        raise ValueError(f'unknown argument for {measure}: {meas_args}')
    result = []
    dtype = meas.SUPPORTED_PARAMS[arg_name].dtype
    for arg in meas_args.split(','):
        result.append(meas(**{arg_name: dtype(arg)}))
    return result
