# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()

requires = [
    'geoalchemy2',
    # see https://github.com/OnroerendErfgoed/oe_geoutils/issues/93
    'geojson < 2.5.0',
    'Shapely',
    'colander',
    'pyramid',
    'requests',
    'pycountry <= 18.5.26',
    'crabpy',
    'crabpy_pyramid',
    'pyproj',
    'oe_utils >= 1.5.0'
]

setup(
    name='oe_geoutils',
    version='1.7.5',
    description='Utility Library',
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/OnroerendErfgoed/oe_geoutils',
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='geoloc',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = oe_geoutils:main
      """,
)
