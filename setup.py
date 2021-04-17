from glob import glob
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ir_measures",
    version="0.0.1",
    author="Sean MacAvaney",
    author_email="sean.macavaney@glasgow.ac.uk",
    description="provides a common interface to many IR measure tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seanmacavaney/ir_measures",
    include_package_data = True,
    packages=setuptools.find_packages(include=['ir_measures', 'ir_measures.*']),
    install_requires=list(open('requirements.txt')),
    extras_require={
        "pytrec_eval": ["pytrec-eval==0.5"],
        "trectools": ["trectools>=0.0.44"],
    },
    classifiers=[],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['ir_measures=ir_measures:main_cli'],
    },
    package_data={
        'ir_measures': glob('bin/gdeval.pl'),
    },
)
