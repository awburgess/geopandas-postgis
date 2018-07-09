"""
Tests for geopandas_postgis custom accessor
"""
import pytest
import typing
from pathlib import Path
import geopandas as gpd

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
        dummy_dataframe: Text fixture to allow all test functions to access the same object

    Returns:
        None
    """
    test_gdf = gpd.read_file(dummy_dataframe)
    assert test_gdf.postgis._extract_srid_int_from_crs() == 4269
