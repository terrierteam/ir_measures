import os
import re
import sys
import argparse
import json
import ir_measures
from ir_measures.util import ScoredDoc, Qrel, Metric

DEFAULT_PLACES = 4
SUMMARY_QID = 'all'


def tsv_output(args):
    if args.places == -1:
        place_format = '' # --places -1 indicates no format string (show all places, exp notation, etc.)
    else:
        place_format = f'.{args.places}f'
    def wrapped(result):
        if args.by_query:
            print(f'{result.query_id}\t{result.measure}\t{result.value:{place_format}}')
        else:
            print(f'{result.measure}\t{result.value:{place_format}}')
    return wrapped


def jsonl_output(args):
    if args.places != DEFAULT_PLACES:
        sys.stderr.write('--places is ignored when using --output jsonl\n')
    def wrapped(result):
        result = result._replace(measure=str(result.measure))._asdict()
        if not args.by_query:
            del result['query_id']
        print(json.dumps(result))
    return wrapped


OUTPUT_FORMATS = {
    'tsv': tsv_output,
    'jsonl': jsonl_output,
}


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('qrels')
    parser.add_argument('run')
    parser.add_argument('measures', nargs='+')
    parser.add_argument('--places', '-p', type=int, default=DEFAULT_PLACES)
    parser.add_argument('--by_query', '-q', action='store_true')
    parser.add_argument('--no_summary', '-n', action='store_true')
    parser.add_argument('--output_format', '-o', choices=OUTPUT_FORMATS.keys(), default='tsv')
    parser.add_argument('--provider', choices=ir_measures.providers.registry.keys())
    args = parser.parse_args()
    qrels = _get_qrels(args)
    run = ir_measures.read_trec_run(args.run)
    measures = _get_measures(args)
    calc_obj = ir_measures
    if args.provider:
        calc_obj = ir_measures.providers.registry[args.provider]
    output = OUTPUT_FORMATS[args.output_format](args)
    if args.by_query:
        aggs = {m: m.aggregator() for m in measures} if not args.no_summary else None
        for result in calc_obj.iter_calc(measures, qrels, run):
            output(result)
            if aggs:
                aggs[result.measure].add(result.value)
        if aggs:
            for measure in measures:
                output(Metric(query_id=SUMMARY_QID, measure=measure, value=aggs[measure].result()))
    else:
        assert not args.no_summary, "--no_summary (-n) only supported with --by_query (-q)"
        results = calc_obj.calc_aggregate(measures, qrels, run)
        for measure in measures:
            output(Metric(query_id=SUMMARY_QID, measure=measure, value=results[measure]))


def _get_qrels(args):
    # gets the qrels, either from a file (priority) or from ir_datasets (if installed)
    if os.path.exists(args.qrels):
        return ir_measures.read_trec_qrels(args.qrels)
    irds_available = False
    try:
        import ir_datasets
        irds_available = True
    except ImportError:
        sys.stderr.write(f'Skipping ir_datasets lookup. To use this feature, install ir_datasets.\n')
    if irds_available:
        try:
            ds = ir_datasets.load(args.qrels)
            if ds.has_qrels():
                return ds.qrels_iter()
            sys.stderr.write(f'ir_datasets ID {args.qrels} found but does not provide qrels.\n')
            sys.exit(-1)
        except KeyError:
            sys.stderr.write(f'{args.qrels} not found. (checked file and ir_datasets)\n')
            sys.exit(-1)
    sys.stderr.write(f'{args.qrels} not found.\n')
    sys.exit(-1)


def _get_measures(args):
    measures, errors = [], []
    for mstr in args.measures:
        for m in mstr.split():
            try:
                measure = ir_measures.parse_measure(m)
                if measure not in measures:
                    measures.append(measure)
            except ValueError:
                errors.append(f'syntax error: {m}')
            except NameError:
                errors.append(f'unknown measure: {m}')
    if errors:
        sys.stderr.write('\n'.join(['error parsing measures'] + errors + ['']))
        sys.exit(-1)
    return measures


if __name__ == '__main__':
    try:
        main_cli()
    except BrokenPipeError:
        sys.stderr.write('BrokenPipe\n')
    except KeyboardInterrupt:
        sys.stderr.write('KeyboardInterrupt\n')
