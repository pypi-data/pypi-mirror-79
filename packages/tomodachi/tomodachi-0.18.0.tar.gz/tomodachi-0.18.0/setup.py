#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup

import tomodachi.__version__

install_requires = [
    'pycparser>=2.18',
    'aioamqp>=0.10.0, <0.15.0',
    'uvloop>=0.8.1',
    'aiobotocore>=0.6.0, <=0.12.0',
    'tzlocal>=1.4',
    'aiohttp>=3.0.5, <3.6.0',
    'yarl>=1.1.0',
    'colorama>=0.3.9, <0.5.0'
]

PY_VER = sys.version_info

if not PY_VER >= (3, 6, 1):
    raise RuntimeError("tomodachi doesn't support Python earlier than 3.6.1")


def read(f: str) -> str:
    return str(open(os.path.join(os.path.dirname(__file__), f), 'rb').read().decode().strip())


classifiers = [
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 4 - Beta',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Typing :: Typed'
]

setup(name='tomodachi',
      version=tomodachi.__version__,
      description=('Python 3 microservice library on asyncio with HTTP, '
                   'websockets, RabbitMQ and AWS SNS+SQS.'),
      long_description='\n\n'.join((read('README.rst'), read('CHANGES.rst'))),
      classifiers=classifiers,
      author='Carl Oscar Aaro',
      author_email='hello@carloscar.com',
      url='https://github.com/kalaspuff/tomodachi',
      download_url='https://pypi.python.org/pypi/tomodachi',
      license='MIT',
      entry_points={
          'console_scripts': [
              'tomodachi = tomodachi.cli:cli_entrypoint'
          ]
      },
      install_requires=install_requires,
      keywords=('tomodachi, microservice, microservices, framework, library, asyncio, '
                'aws, sns, sqs, amqp, rabbitmq, http, websockets, easy, fast, python 3'),
      zip_safe=False,
      packages=find_packages(),
      platforms='any',
      include_package_data=True
      )
