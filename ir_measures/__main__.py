import re
import sys
import argparse
import ir_measures
from ir_measures.util import GenericScoredDoc, GenericQrel


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('qrels')
    parser.add_argument('run')
    parser.add_argument('measures', nargs='+')
    parser.add_argument('--places', '-p', type=int, default=4)
    parser.add_argument('--by_query', '-q', action='store_true')
    parser.add_argument('--no_summary', '-n', action='store_true')
    args = parser.parse_args()
    run = (l.split() for l in open(args.run))
    run = (GenericScoredDoc(cols[0], cols[2], float(cols[4])) for cols in run)
    qrels = (l.split() for l in open(args.qrels))
    qrels = (GenericQrel(cols[0], cols[2], int(cols[3])) for cols in qrels)
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
    if args.by_query:
        aggs = {m: m.aggregator() for m in measures} if not args.no_summary else None
        for result in ir_measures.iter_calc(measures, qrels, run):
            print(f'{result.query_id}\t{result.measure}\t{result.value:.{args.places}f}')
            if aggs:
                aggs[result.measure].add(result.value)
        if aggs:
            for measure in measures:
                print(f'all\t{measure}\t{aggs[measure].result():.{args.places}f}')
    else:
        assert not args.no_summary, "--no_summary (-n) only supported with --by_query (-q)"
        results = ir_measures.calc_aggregate(measures, qrels, run)
        for measure in measures:
            print(f'{measure}\t{results[measure]:.{args.places}f}')



if __name__ == '__main__':
    ir_measures.main_cli()
