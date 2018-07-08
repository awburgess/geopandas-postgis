"""
Custom Accessor for GeoPandas that adds enhanced PostGIS read/write and PostGIS functionality
"""
import typing

from sqlalchemy.engine import en
import geopandas as gpd


_sqlalchemy_engine = typing.TypeVar['SQLAlchemy engine']

@gpd.tools.util.pd.api.extensions.register_dataframe_accessor('postgis')
class PostGIS:
    def __init__(self, geopandas_obj: gpd.GeoDataFrame):
        self._obj = geopandas_obj

    @classmethod
    def _extract_srid_int_from_crs(cls):
        """
        Extracts EPSG Integer from GeoDataframe crs property dictionary

        Returns:
            EPSG integer
        """
        return cls._obj.crs['init'].replace('epsg:', '')

    def to_postgis(self, con: _sqlalchemy_engine, table_name: str, geometry: str, schema: str=typing.Union[str, None],
                   transform_crs: bool=False, srid: int=4326, **kwargs) -> typing.NoReturn:
        """
        Loads a GeoDataframe to PostGIS

        Args:
            con: SQLAlchemy engine connection
            table_name: Name of table as desired in the db
            geometry: Type of geometry; ['POINT', 'POLYGON', 'LINESTRING', 'MULTIPOINT',
                                         'MULTIPOLYGON', 'MULTILINESTRING']

        Keyword Args:
            schema: Name of schema if any, default None
            transform_crs: Boolean indicating whether GeoDataframe needs transformed
            srid: Projection system by EPSG as integer
            **kwargs:

        Returns:
            None
        """
