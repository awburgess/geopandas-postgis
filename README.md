# GeoPandas-Postgis

Utilities oriented to using PostGIS features.

## Install

```python
python setup.py install
```

## Requirements

* GeoPandas
* GeoAlchemy2
* SQLAlchemy
* psycopg2

## Usage

Currently, the ```postgis``` accessor only features a ```to_postgis``` method.

```python
import geopandas as gpd
from sqlalchemy import create_engine

from geopandas_postgis import PostGIS

engine = create_engine("postgresql+psycopg2://postgres:postgres/localhost:test")
my_gdf = geopandas.read_file("my_shp.shp")
my_gdf.postgis.to_postgis(con=engine, table_name='test', geometry='Polygon')
```

The ```to_postgis``` method will accept any keyword argument in the to_sql method in ```pandas```

## Testing

Postgres needs to be running on your local machine with a postgres user (that has write access.)  This will be moved to Docker over time.

## License

MIT License

Copyright (c) 2018 Aaron Burgess

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
