import logging
from PIL import Image
from functools import reduce
from xml.etree import ElementTree as ET
import json
from datetime import datetime

import matplotlib
import mpl_scatter_density
import matplotlib.pyplot as plt
import netCDF4
import numpy as np

from kadlu.geospatial.data_sources.data_util import (
        database_cfg,
        dt_2_epoch,
        epoch_2_dt,
        index,
        storage_cfg,
    )


def load_raster(filepath, plot=False, cmap=None, **kwargs):
    """ load data from raster file 

        args:
            filepath: string
                complete filepath descriptor of netcdf file to be read
            plot: boolean
                if True, a plot will be displayed using the qt5agg backend
            cmap: matplotlib colormap
                the full list of available colormaps can be viewed with:
                print(matplotlib.pyplot.colormaps())
                if None is supplied, pyplot will default to 
                matplotlib.pyplot.cm.cividis

        returns:
            values: numpy 2D array
            lats:   numpy 1D array
            lons:   numpy 1D array
    """
    if kwargs == {}: kwargs.update(dict(south=-90,west=-180,north=90,east=180))

    # load raster
    Image.MAX_IMAGE_PIXELS = 500000000
    #im = Image.open(filepath)

    with Image.open(filepath) as im:
        # GDAL raster format
        # http://duff.ess.washington.edu/data/raster/drg/docs/geotiff.txt
        if 33922 in im.tag.tagdata.keys():
            i,j,k,x,y,z = im.tag_v2[33922]  # ModelTiepointTag
            dx, dy, dz  = im.tag_v2[33550]  # ModelPixelScaleTag
            meta        = im.tag_v2[42112]  # GdalMetadata
            xml         = ET.fromstring(meta)
            params      = {tag.attrib['name'] : tag.text for tag in xml}
            lon = np.arange(x, x + (dx * im.size[0]), dx)
            lat = np.arange(y, y + (dy * im.size[1]), dy)[ :: -1] -90
            rng_lon = index(kwargs['west'], lon), index(kwargs['east'], lon)
            rng_lat = (abs(index(kwargs['north'], lat[::-1])-len(lat)), 
                       abs(index(kwargs['south'], lat[::-1])-len(lat)))
            logging.debug(f'{xml.tag}\nraster coordinate system: {im.tag_v2[34737]}'
                          f'\n{json.dumps(params, indent=2, sort_keys=True)}')

        # NASA / jet propulsion labs raster format (page 27)
        # https://landsat.usgs.gov/sites/default/files/documents/geotiff_spec.pdf
        elif 34264 in im.tag.tagdata.keys():
            dx,_,_,x,_,dy,_,y,_,_,dz,z,_,_,_,_ = im.tag_v2[34264]  # ModelTransformationTag
            lon = np.arange(x, x + (dx * im.size[0]), dx)
            lat = np.arange(y, y + (dy * im.size[1]), dy)
            rng_lon = index(kwargs['west'], lon), index(kwargs['east'], lon)
            rng_lat = index(kwargs['south'], -lat),  index(kwargs['north'], -lat)

        else: assert False, f'error {filepath}: unknown metadata tag encoding'
        assert not (z or dz), f'error {filepath}: 3D rasters not supported yet'

        aoi = im.crop((rng_lon[0], rng_lat[0], rng_lon[1], rng_lat[1])).load()
        grid = np.ndarray((len(range(*rng_lon)), len(range(*rng_lat))))

    if (n := reduce(np.multiply, (rng_lon[1] - rng_lon[0], rng_lat[1] - rng_lat[0]))) > 10000000: 
        logging.info(f'this could take a few moments ({n} points)...')

    for xi in np.arange(rng_lon[0], rng_lon[1]) -rng_lon[0]:
        for yi in np.arange(rng_lat[0], rng_lat[1]) -rng_lat[0]: 
            grid[xi][yi] = aoi[int(xi),int(yi)]

    mask = grid == float(im.tag_v2[42113])
    val = np.ma.MaskedArray(grid, mask=mask)

    # plot the data
    if plot:
        x1, y1 = np.meshgrid(lon[rng_lon[0]:rng_lon[1]], lat[rng_lat[0]:rng_lat[1]], indexing='ij')
        fig = plt.figure()
        if (rng_lon[1]-rng_lon[0]) * (rng_lat[1]-rng_lat[0]) >= 100000:
            ax = fig.add_subplot(1,1,1, projection='scatter_density')
            plt.axis('scaled')
            raster = ax.scatter_density(x1, y1, c=val, cmap=cmap)
            plt.tight_layout()
        else:
            ax = fig.add_subplot(1,1,1)
            ax.scatter(x1, y1, c=val, cmap=cmap)
        plt.show()

    return val.data, lat[rng_lat[0]:rng_lat[1]], lon[rng_lon[0]:rng_lon[1]]


def load_netcdf(filename, var=None, plot=False, cmap=None, **kwargs):
    """ read environmental data from netcdf and output to gridded numpy array

        args:
            filename: string
                complete filepath descriptor of netcdf file to be read
            var: string (optional)
                the netcdf attribute to be read as the values.
                by default, a guess will be made based on the file metadata
            plot: boolean
                if True, a plot will be displayed using the qt5agg backend
            cmap: matplotlib colormap
                the full list of available colormaps can be viewed with:
                print(matplotlib.pyplot.colormaps())
                if None is supplied, pyplot will default to 
                matplotlib.pyplot.cm.cividis

        returns:
            values: numpy 2D array
            lats:   numpy 1D array
            lons:   numpy 1D array
    """
    if kwargs == {}: kwargs.update(dict(south=-90,west=-180,north=90,east=180,
            start=datetime(1,1,1), end=datetime.now(), top=0, bottom=9999))
    ncfile = netCDF4.Dataset(filename)

    varmap = dict(
            MAPSTA      =   'f',  # ifremer tag: appears to be a land mask
            #hs             'v',
            lat         =   'y',
            latitude    =   'y',
            lon         =   'x',
            longitude   =   'x',
            time        =   't',
            epoch       =   't',
            depth       =   'z',
            elevation   =   'z',
        )

    axes = dict([(varmap[var][0], var) for var in ncfile.variables.keys() if var in varmap.keys()])
    uvars = [_ for _ in ncfile.variables.keys() if _ not in varmap.keys()]
    if len(uvars) > 0 or var: axes.update({'v': var or uvars[0]})
    if not var: var = 'z' if uvars == [] and var == None else uvars[0]

    assert 'x' in axes.keys(), f'missing x axis: {uvars = }'
    assert 'y' in axes.keys(), f'missing y axis: {uvars = }'
    assert len(axes) >= len(ncfile.variables.keys()), f'missing axis from: {uvars = }'
    assert sum(key in varmap.keys() for key in ncfile.variables.keys()) >= len(axes)-1, 'not all vars match'
    assert len(uvars) <= 1, f'more than one unknown variable: {uvars = }'

    logging.info(f'loading data from {ncfile.getncattr("title")}')

    rng_lat = index(kwargs['west'],  ncfile[axes['y']][:].data), index(kwargs['east'],  ncfile[axes['y']][:].data)
    rng_lon = index(kwargs['south'], ncfile[axes['x']][:].data), index(kwargs['north'], ncfile[axes['x']][:].data)

    out = {} if not 'v' in axes.keys() else dict(val=ncfile[axes['v']][:].data[rng_lat[0]:rng_lat[1], rng_lon[0]:rng_lon[1]])
    out.update(dict(lat=ncfile[axes['y']][:].data[rng_lat[0]:rng_lat[1]], lon=ncfile[axes['x']][:].data[rng_lon[0]:rng_lon[1]]))

    # temporal index range
    if 't' in axes.keys(): 
        if ncfile.variables[axes['t']].units == 'days since 1990-01-01T00:00:00Z':
            t0 = datetime(1990,1,1)
            rng_t = (index(dt_2_epoch(kwargs['start'], t0), ncfile[axes['t']][:].data * 24), 
                     index(dt_2_epoch(kwargs['end'], t0), ncfile[axes['t']][:].data * 24))
            out['time'] = epoch_2_dt(ncfile[axes['t']][:].data[rng_t[0]:rng_t[1]] * 24, t0)
        else:
            assert False, 'unknown time unit'

    # vertical index range
    if 'z' in axes.keys() and 'v' in axes.keys(): 
        assert axes['z'] != 'elevation', 'netcdf indexing error'
        rng_z = (index(kwargs['top'], ncfile[axes['z']][:].data),
                 index(kwargs['bottom'], ncfile[axes['z']][:].data))
        out['depth'] = ncfile[axes['z']][:].data[rng_z[0]:rng_z[1]]
    elif 'z' in axes.keys() and not 'v' in axes.keys() and len(axes.keys()) == 3:
        # when loading bathymetry, z-axis are the intended first column values
        out = dict(val=ncfile[axes['z']][:].data[rng_lat[0]:rng_lat[1], rng_lon[0]:rng_lon[1]], lat=out['lat'].copy(), lon=out['lon'].copy())
        if axes['z'] == 'elevation': out['val'] *= -1
    else: assert 'v' in axes.keys(), 'something may have gone wrong here...'

    # assert 'f' not in axes.keys(), 'functions axis not yet supported'

    # plot the data
    if plot and len(out.keys()) == 3:
        x1, y1 = np.meshgrid(out['lon'][rng_lon[0]:rng_lon[1]], out['lat'][rng_lat[0]:rng_lat[1]], indexing='ij')
        fig = plt.figure()
        if (rng_lon[1]-rng_lon[0]) * (rng_lat[1]-rng_lat[0]) >= 100000:
            ax = fig.add_subplot(1,1,1, projection='scatter_density')
            plt.axis('scaled')
            raster = ax.scatter_density(x1, y1, c=val, cmap=cmap)
            plt.tight_layout()
        else:
            ax = fig.add_subplot(1,1,1)
            ax.scatter(x1, y1, c=val, cmap=cmap)
        plt.show()

    return list(out.values())

