import os
from distutils.core import setup

from setuptools import find_packages

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    # Name of the package
    name='django-postgres-product',
    # Packages to include into the distribution
    packages=[
        'postgres_product',
    ],
    # Start with a small number and increase it with
    # every change you make https://semver.org
    version='1.0',
    # Chose a license from here: https: //
    # help.github.com / articles / licensing - a -
    # repository. For example: MIT
    license='MIT',
    # Short description of your library
    description='A product aggregation function to a postgres database and makes it available with django',
    # Long description of your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Your name
    author='Axel Wegener',
    # Your email
    author_email='development@sparse-space.de',
    # Either the link to your github or to your website
    url='https://github.com/awmath/django-postgres-product',
    # Link from which the project can be downloaded
    download_url='https://github.com/awmath/django-postgres-product',
    # List of keywords
    keywords=['django'],
    # List of packages to install with this one
    install_requires=['psycopg2', 'django>2'],
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ])
