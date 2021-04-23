import ir_measures

def main():
    for file in ['README.md', 'docs/index.md']:
        with open(file, 'wt') as f:
            if file == 'README.md':
                f.write('''
[![Python package](https://github.com/terrierteam/ir_measures/actions/workflows/push.yml/badge.svg)](https://github.com/terrierteam/ir_measures/actions/workflows/push.yml)

# ir_measures

Check out our documentation website: [ir-measur.es](https://ir-measur.es/)

''')
            f.write('''
Provides a common interface to many IR measure tools.

Provided by the [Terrier Team @ Glasgow](http://terrierteam.dcs.gla.ac.uk/). Find us at [terrierteam/ir_measures](https://github.com/terrierteam/ir_measures).

## Getting Started

Install via pip

```bash
pip install ir-measures
```

## Python API

```python
from ir_measures import iter_calc, calc_aggregate
from ir_measures import AP, nDCG, RR, P

qrels = {
    'Q0': {"D0": 0, "D1": 1},
    "Q1": {"D0": 0, "D3": 2}
}
run = {
    'Q0': {"D0": 1.2, "D1": 1.0},
    "Q1": {"D0": 2.4, "D3": 3.6}
}

# aggregated results
calc_aggregate([AP, nDCG, RR, nDCG@10, P(rel=2)@10], qrels, run)
# {AP: 0.75, nDCG: 0.8154648767857288, RR: 0.75, nDCG@10: 0.8154648767857288, P(rel=2)@10: 0.05}

# by query
for metric in iter_calc([AP, nDCG, RR, nDCG@10, P(rel=2)@10], qrels, run):
    print(x)
# Metric(query_id='Q0', measure=AP, value=0.5)
# Metric(query_id='Q0', measure=RR, value=0.5)
# Metric(query_id='Q0', measure=nDCG, value=0.6309297535714575)
# Metric(query_id='Q0', measure=nDCG@10, value=0.6309297535714575)
# Metric(query_id='Q1', measure=AP, value=1.0)
# Metric(query_id='Q1', measure=RR, value=1.0)
# Metric(query_id='Q1', measure=nDCG, value=1.0)
# Metric(query_id='Q1', measure=nDCG@10, value=1.0)
# Metric(query_id='Q0', measure=P(rel=2)@10, value=0.0)
# Metric(query_id='Q1', measure=P(rel=2)@10, value=0.1)
```

Qrels can be provided in the following formats:

```python
# dict of dict
qrels = {
    'Q0': {
        "D0": 1,
        "D1": 0,
    },
    "Q1": {
        "D0": 0,
        "D3": 2
    }
}

# dataframe
qrels = pd.DataFrame([
    {'query_id': "Q0", 'doc_id': "D0", 'relevance': 1},
    {'query_id': "Q0", 'doc_id': "D1", 'relevance': 0},
    {'query_id': "Q1", 'doc_id': "D0", 'relevance': 0},
    {'query_id': "Q1", 'doc_id': "D3", 'relevance': 2},
])

# any iterable of namedtuples (e.g., list, generator, etc)
from ir_measurs.util import GenericQrel
qrels = [
    GenericQrel("Q0", "D0", 1),
    GenericQrel("Q0", "D1", 0),
    GenericQrel("Q1", "D0", 0),
    GenericQrel("Q1", "D3", 2),
]
```

Runs can be provided in the following formats:

```python
# dict of dict
run = {
    'Q0': {
        "D0": 1.2,
        "D1": 1.0,
    },
    "Q1": {
        "D0": 2.4,
        "D3": 3.6
    }
}

# dataframe
run = pd.DataFrame([
    {'query_id': "Q0", 'doc_id': "D0", 'score': 1.2},
    {'query_id': "Q0", 'doc_id': "D1", 'score': 1.0},
    {'query_id': "Q1", 'doc_id': "D0", 'score': 2.4},
    {'query_id': "Q1", 'doc_id': "D3", 'score': 3.6},
])

# any iterable of namedtuples (e.g., list, generator, etc)
from ir_measurs.util import GenericScoredDoc
run = [
    GenericScoredDoc("Q0", "D0", 1.2),
    GenericScoredDoc("Q0", "D1", 1.0),
    GenericScoredDoc("Q1", "D0", 2.4),
    GenericScoredDoc("Q1", "D3", 3.6),
]
```


''')
            measures, aliases = [], []
            for name, val in ir_measures.measures.registry.items():
                if name == val.NAME:
                    measures.append((name, val))
                else:
                    aliases.append((name, val))
            measures = sorted(measures)
            aliases = sorted(aliases)
            f.write('''
## Measures
''')
            for name, val in measures:
                f.write(f'''
### `{name}`

{val.__doc__.replace('    ', ' ')}
''')
                if val.SUPPORTED_PARAMS:
                    f.write('''**Parameters:**\n\n''')
                    for p, param in val.SUPPORTED_PARAMS.items():
                        f.write(f' - `{p}` ({param.dtype.__name__}) - {param.desc}\n')
                    f.write('\n\n')
            f.write('''
## Aliases
''')
            for name, val in aliases:
                f.write(f'- `{name}` &rarr; `{val}`\n')

            f.write('''
## Providers
''')
            for name, val in sorted(ir_measures.providers.registry.items()):
                f.write(f'''
### `{name}`

{val.__doc__.replace('    ', ' ')}
''')
                f.write('''**Supported Measures:**\n\n''')
                for measure in val.SUPPORTED_MEASURES:
                    f.write(f' - `{measure.NAME}`\n')
                f.write('\n\n')

            f.write('''
## Credits

 - Sean MacAvaney, University of Glasgow
 - Craig Macdonald, University of Glasgow

''')

if __name__ == '__main__':
    main()
