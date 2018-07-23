from setuptools import setup

setup(
    name='geopandas-postgis',
    version='0.1.0',
    packages=['geopandas_postgis', 'geopandas_postgis.tests'],
    install_requires=['SQLAlchemy', 'GeoAlchemy2', 'geopandas', 'psycopg2'],
    url='',
    license='MIT License',
    author='Aaron Burgess',
    author_email='geoburge@gmail.com',
    description='Adds additional postgis functionality to GeoPandas'
)
