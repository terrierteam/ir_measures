import ir_measures

def main():
    with open('docs/measures.rst', 'wt') as f:
        measures, aliases = [], []
        for name, val in ir_measures.measures.registry.items():
            if name == val.NAME:
                measures.append((name, val))
            else:
                aliases.append((name, val))
        measures = sorted(measures)
        aliases = sorted(aliases)
        f.write('''
Measures
=========================
''')
        for name, val in measures:
            f.write(f'''
``{name}``
-------------------------

{val.__doc__.replace('    ', ' ')}
''')
            if val.SUPPORTED_PARAMS:
                f.write('''**Parameters:**\n\n''')
                for p, param in val.SUPPORTED_PARAMS.items():
                    f.write(f' - ``{p}`` ({param.dtype.__name__}) - {param.desc}\n')
                f.write('\n\n')
        f.write('''
Aliases
-------------------------
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
                f.write(f' - ``{measure.NAME}``\n')
            f.write('\n\n')

if __name__ == '__main__':
    main()
