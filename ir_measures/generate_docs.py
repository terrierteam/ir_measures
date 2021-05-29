import ir_measures

def main():
    with open('docs/measures.rst', 'wt') as f:
        measures, aliases = [], []
        for name, val in ir_measures.measures.registry.items():
            if name == val.NAME:
                measures.append((name, val))
            else:
                aliases.append((name, val))
        measures = sorted(measures, key=lambda x: x[0].upper())
        aliases = sorted(aliases, key=lambda x: x[0].upper())
        f.write('''
Measures
=========================
''')
        for name, val in measures:
            f.write(f'''
``{name}``
-------------------------

{val.__doc__.replace('    ', '')}
''')
            if val.SUPPORTED_PARAMS:
                f.write('''**Parameters:**\n\n''')
                for p, param in val.SUPPORTED_PARAMS.items():
                    f.write(f'- ``{p}`` ({param.dtype.__name__}) - {param.desc}\n')
                f.write('\n\n')
            measure_providers = [(n, [m for m in p.SUPPORTED_MEASURES if m.__name__ == val.__name__]) for n, p in ir_measures.providers.registry.items()]
            measure_providers = [(n, m) for n, m in measure_providers if m]
            f.write('''**Provided by:**\n\n''')
            if measure_providers:
                for p, ms in measure_providers:
                    ms = ', '.join(f'``{m}``' for m in ms)
                    f.write(f'- ``{p}``: {ms}\n')
                f.write('\n\n')
            else:
                f.write('\n\n*(none yet)*\n\n')
        f.write('''
Aliases
-------------------------

These provide shortcuts to "canonical" measures, and are typically used when multiple
names or casings for the same measure exist. You can use them just like any other measure
and the identifiers are equal (e.g., ``AP == MAP``) but the names will appear in the
canonical form when printed.

''')
        for name, val in aliases:
            f.write(f'- ``{name}`` → ``{val}``\n')

    with open('docs/providers.rst', 'wt') as f:
        f.write('''
Providers
=========================
''')
        for name, val in sorted(ir_measures.providers.registry.items()):
            f.write(f'''
``{name}``
-------------------------

{val.__doc__.replace('    ', ' ')}
''')
            f.write('''**Supported Measures:**\n\n''')
            for measure in val.SUPPORTED_MEASURES:
                f.write(f' - ``{measure}``\n')
            f.write('\n\n')

if __name__ == '__main__':
    main()
