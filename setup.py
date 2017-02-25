import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
    name='permutation',
    version='0',
    packages=find_packages(),
    # url='private',
    license='MIT Licence',
    author='Martino Salvetti',
    author_email='tldr@inbitcoin.it',
    description='Command line tool that provide plausible deniability for '
                'bitcoin wallets seeds encoding them to deck of cards '
                'orderings',
    long_description=README,
    test_suite='permutation.tests',
    package_dir={
        'permutation': 'lib',
    },
    scripts=['permutation'],
    package_data={
        'permutation': [
            'data/ordering.json',
            'data/tests.json',
            'data/wordlist/*.txt'
        ]
    },
)
