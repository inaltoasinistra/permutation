import os
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

version = 'UNDEFINED'
with open('permutation/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('= ')[1].strip("'")
            break


setup(
    name='permutation',
    version=version,
    packages=['permutation'],
    # url='private',
    license='MIT Licence',
    author='Martino Salvetti',
    author_email='tldr@inbitcoin.it',
    description='Command line tool that provide plausible deniability for '
                'bitcoin wallets seeds encoding them to deck of cards '
                'orderings',
    scripts=['scripts/permutation'],
    test_suite='permutation.tests',
    package_data={
        'permutation': [
            'data/ordering/*.txt',
            'data/wordlist/*.txt',
            'data/tests.json'
        ]
    },
)
