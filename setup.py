from pathlib import Path
from setuptools import setup

_README = Path(__file__).parent / 'README.md'


def long_description() -> str:
    with _README.open(encoding='utf-8') as readme:
        long_descript = readme.read()
    return long_descript


setup(
    name='geopandas-postgis',
    version='0.1.1',
    packages=['geopandas_postgis', 'geopandas_postgis.tests'],
    install_requires=['SQLAlchemy', 'GeoAlchemy2', 'geopandas', 'psycopg2-binary'],
    url='',
    license='MIT License',
    author='Aaron Burgess',
    author_email='geoburge@gmail.com',
    description='Adds additional postgis functionality to GeoPandas',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
