import re
import ir_measures

project = 'ir-measures'
copyright = '2021'
author = 'Sean MacAvaney'

extensions = ['sphinx.ext.autodoc', 'sphinx_tabs.tabs']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'furo'
html_static_path = ['_static']
sphinx_tabs_disable_tab_closing = True

def setup(app):
    app.add_css_file('main.css')

def docstring2rst(docstring):
    indent = re.search(r' +', docstring.split('\n')[:2][-1], flags=re.M | re.S)
    if indent:
        docstring = re.sub('\n' + indent.group(), '\n', docstring)
    return docstring

with open('measures.rst', 'wt') as f:
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

:class:`~ir_measures.measures.Measure` objects speficy the measure to calculate, along with any
parameters they have. (They do not define the implementation --- that's the job of a
:class:`~ir_measures.providers.Provider`.)

This page provides a list of the Measures that are available in this package.

''')
    for name, val in measures:
        f.write(f'''
.. _measures.{name}:

``{name}``
-------------------------

{docstring2rst(val.__doc__)}
''')
        if val.SUPPORTED_PARAMS:
            f.write('''**Parameters:**\n\n''')
            for p, param in val.SUPPORTED_PARAMS.items():
                f.write(f'- ``{p}`` ({param.dtype.__name__}) - {param.desc}\n')
            f.write('\n\n')
        measure_providers = [(n, [m for m in p.SUPPORTED_MEASURES if m.__name__ == val.__name__]) for n, p in ir_measures.providers.registry.items()]
        measure_providers = [(n, m) for n, m in measure_providers if m]
        f.write('''**Supported by:**\n\n''')
        if measure_providers:
            for p, ms in measure_providers:
                ms = ', '.join(f'``{m}``' for m in ms)
                f.write(f'- :ref:`{p} <providers.{p}>`: {ms}\n')
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
        ref = str(val).split('(')[0]
        f.write(f'- ``{name}`` → :ref:`{val} <measures.{ref}>`\n')

with open('providers.rst', 'wt') as f:
    f.write('''
Providers
=========================

A :class:`~ir_measures.providers.Provider` implements the calculation logic for one or more
:class:`~ir_measures.measures.Measure`.

This page provides a list of the Providers that are available in this package.

''')
    for name, val in sorted(ir_measures.providers.registry.items()):
        f.write(f'''
.. _providers.{name}:

``{name}``
-------------------------

{docstring2rst(val.__doc__)}

''')
        inst = val.install_instructions()
        if inst:
            f.write(f'''**Installation:**\n\n.. code-block::\n\n    {inst}\n\n''')
        f.write('''**Supported Measures:**\n\n''')
        for measure in val.SUPPORTED_MEASURES:
            f.write(f'- ``{measure}``\n')
        f.write('\n\n')
