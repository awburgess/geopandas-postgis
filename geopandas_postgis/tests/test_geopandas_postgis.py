"""
Tests for geopandas_postgis custom accessor
"""
import pytest
from pathlib import Path

from geopandas_postgis import geopandas_postgis as GPOST

_RESOURCES = Path(__file__).parent / 'resources'


@pytest.fixture(scope='session')
def dummy_dataframe():
    """
    Creates a GeoDataframe for testing from resource file

    Returns:
        GeoDataframe for test purposes (uses Census U.S. State Cartographic Boundary Files 1:500,000)
    """
    state_shp = _RESOURCES / 'cb_2017_us_state_500k.shp'
