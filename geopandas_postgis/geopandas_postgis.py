"""
Custom Accessor for GeoPandas that adds enhanced PostGIS read/write and PostGIS functionality
"""
import typing

import geopandas as gpd
from geoalchemy2 import WKTElement, Geometry


_sqlalchemy_engine = typing.TypeVar('SQLAlchemy engine')


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

    @classmethod
    def to_postgis(cls, con: _sqlalchemy_engine, table_name: str, geometry: str, schema: str=typing.Union[str, None],
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
        gpd_copy =  cls._obj.copy()
        if transform_crs:
            gpd_copy = gpd_copy.to_crs({'init': 'epsg:{}'.format(srid)})

        gdf_srid = cls._extract_srid_int_from_crs()

        gpd_copy['geom'] = gpd_copy.geometry.apply(lambda geom: WKTElement(geom.wkt, srid=gdf_srid))
        gpd_copy.drop('geometry', 1, inplace=True)

        cls.to_sql(name=table_name, con=con, schema=schema, dtype={'geom': Geometry(geometry_type=geometry.upper(),
                                                                                    srid=gdf_srid)}, **kwargs)
