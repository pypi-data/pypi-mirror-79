import os
import logging
import zipfile
import requests
import subprocess
from functools import reduce
import json

import numpy as np
from tqdm import tqdm

import kadlu
from kadlu import Spinbin
from kadlu.geospatial.data_sources.data_util import (
        Boundary,
        database_cfg,
        ext, 
        fmt_coords,
        logmsg,
        logmsg_nodata,
        storage_cfg,
    )


conn, db = database_cfg()
db.execute('CREATE TABLE IF NOT EXISTS gebco' 
            '(   val     REAL    NOT NULL,  ' 
            '    lat     REAL    NOT NULL,  ' 
            '    lon     REAL    NOT NULL,  ' 
            '    source  TEXT    NOT NULL)  ') 
db.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_gebco on gebco(lon, lat, val, source)')


class Gebco():

    def fetch_bathymetry(self, *, south, north, west, east):
        """ download geotiff zip archive, decompress it, and log values from .tif files as needed """
        zipf = os.path.join(storage_cfg(), "gebco_2020_geotiff.zip")

        if not os.path.isfile(zipf):
            logging.info('downloading and decompressing gebco bathymetry (geotiff ~8GB)... ')
            url = 'https://www.bodc.ac.uk/data/open_download/gebco/gebco_2020/geotiff/'
            with requests.get(url, stream=True) as payload_netcdf:
                assert payload_netcdf.status_code == 200, 'error fetching file'
                with open(zipf, 'wb') as f:
                    with tqdm(total=3730631664, desc='gebco_2020_geotiff.zip', ascii=True, unit='MB', unit_divisor=1000000) as t:
                        for chunk in payload_netcdf.iter_content(chunk_size=8192): 
                            t.update(f.write(chunk))

        if not os.path.isfile(os.path.join(storage_cfg(), 'GEBCO_2020_Grid.pdf')) and os.name == 'nt': 
            raise NotImplementedError('no windows support for GEBCO\'s zip format. ' 
                'manually unzip file f{storage_cfg()}/gebco_2020_geotiff.zip and run function again')
        elif os.name != 'posix': logging.warning('untested on this platform!')
        with Spinbin(storagedir=storage_cfg(), bins=False) as unzipper: 
            unzipper(callback=subprocess.run, args=(f'unzip -D -n {os.path.join(storage_cfg(), "gebco_2020_geotiff.zip")} -d {storage_cfg()}'.split()))

        for fname in [f for f in (zipfile.ZipFile(zipf, "r").namelist()) if (tif := ext(f, ('.tif',)))]:
            n,s,w,e = [float(f[1:]) for f in fname.split('_',2)[-1].rsplit('.', 1)[0].split('_')]
            if Boundary(s,n,w,e).intersects(Boundary(south=south, north=north, west=west, east=east)):
                with Spinbin(storagedir=storage_cfg(), south=south, north=north, west=west, east=east) as fetchmap:
                    fetchmap(callback=self.callback, fname=fname)
        return


    def callback(self, *, fname, south, north, west, east, **_):
        """ build data grid and insert into the database """
        logging.info(f'GEBCO BATHYMETRY  scanning {fname} for new data...')
        val, lat, lon = kadlu.load_file(os.path.join(storage_cfg(), fname), south=south, north=north, west=west, east=east)
        grid = list(map(tuple, np.vstack((
            val.flatten() * -1, 
            reduce(np.append, (lat for _ in range(val.flatten().shape[0] // len(lat)))),
            reduce(np.append, (lon[i // len(lon)] for i in range(val.flatten().shape[0]))), 
            ['gebco' for _ in range(val.flatten().shape[0])])).T))
        n1 = db.execute(f"SELECT COUNT(*) FROM gebco ").fetchall()[0][0]
        db.executemany(f"INSERT OR IGNORE INTO gebco VALUES (?,?,?,?)", grid)
        n2 = db.execute(f"SELECT COUNT(*) FROM gebco ").fetchall()[0][0]
        logmsg('gebco', 'bathymetry', (n1, n2), south=south, west=west, north=north, east=east)
        conn.commit()


    def load_bathymetry(self, *, south, north, west, east, **_):
        """ load gebco bathymetry data """
        self.fetch_bathymetry(south=south, north=north, west=west, east=east)
        db.execute(' AND '.join([f'SELECT * FROM gebco WHERE lat >= ?','lat <= ?','lon >= ?','lon <= ?']), tuple(map(str, [south, north, west, east])))
        res = np.array(db.fetchall()).T[:-1].astype(float)
        if len(res) == 0: 
            logmsg_nodata('gebco', 'bathymetry', south=south, north=north, west=west, east=east)
            return np.array([[],[],[]])
        return res

