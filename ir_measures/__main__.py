import os
import re
import sys
import argparse
import ir_measures
from ir_measures.util import ScoredDoc, Qrel


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('qrels')
    parser.add_argument('run')
    parser.add_argument('measures', nargs='+')
    parser.add_argument('--places', '-p', type=int, default=4)
    parser.add_argument('--by_query', '-q', action='store_true')
    parser.add_argument('--no_summary', '-n', action='store_true')
    parser.add_argument('--provider', choices=ir_measures.providers.registry.keys())
    args = parser.parse_args()
    qrels = _get_qrels(args)
    run = ir_measures.read_trec_run(args.run)
    measures = _get_measures(args)
    calc_obj = ir_measures
    if args.provider:
        calc_obj = ir_measures.providers.registry[args.provider]
    if args.by_query:
        aggs = {m: m.aggregator() for m in measures} if not args.no_summary else None
        for result in calc_obj.iter_calc(measures, qrels, run):
            print(f'{result.query_id}\t{result.measure}\t{result.value:.{args.places}f}')
            if aggs:
                aggs[result.measure].add(result.value)
        if aggs:
            for measure in measures:
                print(f'all\t{measure}\t{aggs[measure].result():.{args.places}f}')
    else:
        assert not args.no_summary, "--no_summary (-n) only supported with --by_query (-q)"
        results = calc_obj.calc_aggregate(measures, qrels, run)
        for measure in measures:
            print(f'{measure}\t{results[measure]:.{args.places}f}')


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
    main_cli()
