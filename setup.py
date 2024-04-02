import os

from setuptools import setup, find_packages

setup(
    name='corpora-analyzer',
    version=os.getenv('PACKAGE_VERSION', '0.0.1'),
    packages=find_packages(include=[
            'corpora_analyzer*'
        ]),
    description='Tool to build indexes from text corpora'
                ' and work with it.',
    python_requires='>=3.8',
    install_requires=[
        'tqdm',
        'nltk',
        'matplotlib',
        'aiofiles'
    ]
)
