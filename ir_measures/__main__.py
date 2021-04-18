import argparse
import ir_measures
from ir_measures.util import GenericScoredDoc, GenericQrel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('qrels')
    parser.add_argument('run')
    args = parser.parse_args()
    run = (l.split() for l in open(args.run))
    run = (GenericScoredDoc(cols[0], cols[2], float(cols[4])) for cols in run)
    qrels = (l.split() for l in open(args.qrels))
    qrels = (GenericQrel(cols[0], cols[2], int(cols[3])) for cols in qrels)
    s, c = 0, 0
    for result in (ir_measures.Judged@5).iter_calc(qrels, run):
        s += result.value
        c += 1
    print(s/c)


if __name__ == '__main__':
    main()
