import ir_measures

def main():
	with open('docs/index.md', 'wt') as f:
		f.write('''
# ir-measures

Provides a common interface to many IR measure tools.

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
### {name}

{val.__doc__}
''')
		f.write('''
## Aliases
''')
		for name, val in aliases:
			f.write(f'- {name} &rarr; {val.NAME}\n')

if __name__ == '__main__':
	main()
