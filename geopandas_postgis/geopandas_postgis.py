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

    def _extract_srid_int_from_crs(self):
        """
        Extracts EPSG Integer from GeoDataframe crs property dictionary

        Returns:
            EPSG integer
        """
        try:
            # old way of specifying crs = {'init': 'epsg:4326'}, prior to geopandas 0.7.0
            return int(self._obj.crs['init'].replace('epsg:', ''))
        except TypeError:
            # new pyproj way of specifiying crs = 'epsg:4326', from geopandas 0.7.0 onwards
            # ref: https://geopandas.org/projections.html#upgrading-to-geopandas-0-7-with-pyproj-2-2-and-proj-6
            return self._obj.crs.to_epsg()

    def to_postgis(self, con: _sqlalchemy_engine, table_name: str,
                   geometry: str, schema: typing.Union[str, None]=None,
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
            **kwargs: Keyword args for to_sql method on Dataframe object

        Returns:
            None
        """
        gpd_copy = self._obj.copy()
        if transform_crs:
            gpd_copy = gpd_copy.to_crs({'init': 'epsg:{}'.format(srid)})

        gdf_srid = self._extract_srid_int_from_crs()

        gpd_copy[self._obj.geometry.name] = gpd_copy.geometry.apply(lambda geom: WKTElement(geom.wkt, srid=gdf_srid))

        gpd_copy.to_sql(name=table_name, con=con,
                        schema=schema, dtype={self._obj.geometry.name: Geometry(geometry_type=geometry.upper(),
                                                               srid=gdf_srid)}, **kwargs)
