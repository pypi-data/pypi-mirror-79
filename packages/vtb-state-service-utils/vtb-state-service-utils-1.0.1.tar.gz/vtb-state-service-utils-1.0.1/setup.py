import io
from pathlib import Path

from setuptools import setup, find_packages

REQUIRED = [
    'aiohttp>=3.6.2',
    'aio_pika>=6.6.1',
    'simplejson>=3.17.2'
]

with io.open(Path(__file__).parent / 'README.md', encoding='utf-8') as f:
    long_description = '\n' + f.read()

# python setup.py sdist bdist_wheel
# python -m twine upload --repository pypi dist/*
setup(
    name='vtb-state-service-utils',
    version='1.0.1',
    packages=find_packages(exclude=['tests']),
    url='https://bitbucket.org/Michail_Shutov/state_service_utils',
    license='',
    author=' Mikhail Shutov',
    author_email='michael-russ@yandex.ru',
    description=long_description,
    install_requires=REQUIRED,
    extras_require={
        'test': [
            'pytest',
            'pylint',
        ]
    }
)
