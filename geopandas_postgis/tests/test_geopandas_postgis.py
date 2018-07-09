"""
Tests for geopandas_postgis custom accessor
"""
import pytest
import typing
from pathlib import Path
import geopandas as gpd

from sqlalchemy import create_engine

import geopandas_postgis.tests.config as config
from geopandas_postgis import geopandas_postgis as GPOST

_RESOURCES = Path(__file__).parent / 'resources'


@pytest.fixture(scope='session')
def dummy_dataframe() -> str:
    """
    Creates a string reference to shp file for testing

    Returns:
        GeoDataframe for test purposes (uses Census U.S. State Cartographic Boundary Files 1:500,000)
    """
    return (_RESOURCES / 'cb_2017_us_state_500k.shp').as_posix()


def test_extract_srid_int_from_crs(dummy_dataframe: gpd.GeoDataFrame) -> typing.NoReturn:
    """
    Test that PostGIS._extract_srid_int_from_crs() returns the integer representation
    of the epsg id.

    Args:
        dummy_dataframe: Test fixture to allow all test functions to access the same object

    Returns:
        None

    """
    test_gdf = gpd.read_file(dummy_dataframe)
    assert test_gdf.postgis._extract_srid_int_from_crs() == 4269


def test_to_postgis(dummy_dataframe: gpd.GeoDataFrame) -> typing.NoReturn:
    """
    Assert that GeoDataframe is loaded to PostGIS

    Args:
        dummy_dataframe: Test fixture to allow all test functions to access the same object

    Returns:
        None

    """
    engine = create_engine(config.POSTGRES_ENGINE_STRING)

    test_gdf = gpd.read_file(dummy_dataframe)

    test_gdf.postgis.to_postgis(engine, 'test', 'MULTIPOLYGON')

    postgis_count = engine.execute("""SELECT COUNT(*) as test_cnt FROM test""").fetchone().test_cnt

    assert postgis_count == test_gdf.shape[0]
