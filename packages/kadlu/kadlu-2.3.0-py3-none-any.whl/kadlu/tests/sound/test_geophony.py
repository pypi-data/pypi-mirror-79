""" Unit tests for the the 'sound.geophony' module in the 'kadlu' package

    Authors: Oliver Kirsebom
    contact: oliver.kirsebom@dal.ca
    Organization: MERIDIAN-Intitute for Big Data Analytics
    Team: Acoustic data Analytics, Dalhousie University
    Project: packages/kadlu
             Project goal: Tools for underwater soundscape modeling
     
    License:

"""

import pytest
import os
import numpy as np
from kadlu.sound.geophony import geophony, transmission_loss, kewley_sl_func, source_level
from kadlu.geospatial.ocean import Ocean
from kadlu.utils import R1_IUGG, deg2rad

current_dir = os.path.dirname(os.path.realpath(__file__))
path_to_assets = os.path.join(os.path.dirname(current_dir),"assets")

def test_kewley_sl_func():
    sl1 = kewley_sl_func(freq=10, wind_uv=0)
    sl2 = kewley_sl_func(freq=40, wind_uv=2.57)
    assert sl1 == sl2
    assert sl2 == 40.0
    sl3 = kewley_sl_func(freq=40, wind_uv=5.14)
    assert sl3 == 44.0
    sl4 = kewley_sl_func(freq=100, wind_uv=5.14)
    assert sl4 == 42.5

def test_source_level():
    ok = {'load_bathymetry': 10000, 'load_wind_uv': 5.14}
    o = Ocean(**ok)
    sl = source_level(freq=10, x=0, y=0, area=1, ocean=o, sl_func=kewley_sl_func)
    assert sl == 44.0
    sl = source_level(freq=100, x=[0,100], y=[0,100], area=[1,2], ocean=o, sl_func=kewley_sl_func)
    assert sl[0] == 42.5
    assert sl[1] == sl[0] + 10*np.log10(2)

def test_geophony_flat_seafloor():
    """ Check that we can execute the geophony method for a 
        flat seafloor and uniform sound speed profile"""
    kwargs = {'load_bathymetry':10000, 'load_wind_uv':1.0, 'ssp':1480, 'angular_bin':90, 'dr':1000, 'dz':1000}
    geo = geophony(freq=100, south=44, north=46, west=-60, east=-58, depth=[100, 2000], xy_res=71, **kwargs)
    spl = geo['spl']
    x = geo['x']
    y = geo['y']
    assert x.shape[0] == 3
    assert y.shape[0] == 5
    assert spl.shape[0] == 3
    assert spl.shape[1] == 5
    assert spl.shape[2] == 2
    assert np.all(np.diff(x) == 71e3)
    assert np.all(np.diff(y) == 71e3)
    # try again, but this time for specific location
    kwargs = {'load_bathymetry':10000, 'load_wind_uv':1.0, 'ssp':1480, 'angular_bin':90, 'dr':1000, 'dz':1000, 'propagation_range':50}
    geo = geophony(freq=100, lat=45, lon=-59, depth=[100, 2000], **kwargs)

def test_geophony_in_canyon(bathy_canyon):
    """ Check that we can execute the geophony method for a 
        canyon-shaped bathymetry and uniform sound speed profile"""
    kwargs = {'load_bathymetry':bathy_canyon, 'load_wind_uv':1.0, 'ssp':1480, 'angular_bin':90, 'dr':1000, 'dz':1000}
    z = [100, 1500, 3000]
    geo = geophony(freq=10, south=43, north=46, west=60, east=62, depth=z, xy_res=71, **kwargs)
    spl = geo['spl']
    x = geo['x']
    y = geo['y']
    assert spl.shape[0] == x.shape[0]
    assert spl.shape[1] == y.shape[0]
    assert spl.shape[2] == len(z)
    assert np.all(np.diff(x) == 71e3)
    assert np.all(np.diff(y) == 71e3)    
    # check that noise is NaN below seafloor and non Nan above
    bathy = np.swapaxes(np.reshape(geo['bathy'], newshape=(y.shape[0], x.shape[0])), 0, 1)
    bathy = bathy[:,:,np.newaxis]
    xyz = np.ones(shape=bathy.shape) * z
    idx = np.nonzero(xyz >= bathy)
    assert np.all(np.isnan(spl[idx]))
    idx = np.nonzero(xyz < bathy)
    assert np.all(~np.isnan(spl[idx]))

def test_transmission_loss_real_world_env():
    """ Check that we can initialize a transmission loss object 
        for a real-world environment and obtain the expected result """

    from datetime import datetime
    bounds = dict(
               start=datetime(2015,1,1), end=datetime(2015,1,2), 
               top=0, bottom=10000
             )    
    src = dict(load_bathymetry='gebco', load_temp='hycom', load_salinity='hycom')
    sound_source = {'freq': 200, 'lat': 43.8, 'lon': -59.04, 'source_depth': 12}
    seafloor = {'sound_speed':1700,'density':1.5,'attenuation':0.5}
    transm_loss = transmission_loss(seafloor=seafloor, propagation_range=20, **src, **bounds, **sound_source, dr=100, angular_bin=45, dz=50)

    tl_h, ax_h, tl_v, ax_v = transm_loss.calc(vertical=True)

    answ_h = np.array([[97.595,117.194,114.901,119.233,119.289,120.622,121.556,122.377,123.14,123.812],
                       [97.591,116.458,117.6,117.633,120.35,121.847,121.204,123.162,120.045,123.039],
                       [97.589,114.272,117.154,118.378,120.621,120.2,122.151,120.387,125.348,121.132],
                       [97.591,117.637,117.931,117.816,117.736,121.136,119.898,120.671,122.311,123.554],
                       [97.596,114.647,117.596,117.484,116.91,120.097,121.753,120.093,119.835,121.315],
                       [97.601,110.389,115.481,119.57,118.993,117.875,117.697,123.378,120.65,122.312],
                       [97.602,110.202,114.798,117.773,123.759,120.094,121.009,121.674,123.78,120.367],
                       [97.6,111.986,115.665,118.448,119.055,120.196,121.165,122.011,122.771,123.482]])

    answ_v = np.array([[31.924,65.424,68.072,70.096,71.566,72.738,73.682,74.518,75.277,75.947,76.558],
                       [53.424,147.254,144.17,147.928,155.102,150.892,151.214,150.512,150.979,151.79,152.478],
                       [59.513,164.737,161.177,164.933,172.159,167.848,168.171,167.467,167.933,168.743,169.43],
                       [63.744,175.057,171.466,175.221,182.452,178.128,178.451,177.747,178.212,179.021,179.709],
                       [67.565,182.674,179.116,182.871,190.102,185.775,186.098,185.394,185.858,186.668,187.356],
                       [71.795,189.304,185.777,189.537,196.759,192.44,192.763,192.06,192.525,193.334,194.022],
                       [77.882,194.952,193.267,197.562,201.774,201.128,201.815,202.04,202.716,203.448,204.088],
                       [98.878,213.995,214.738,219.276,223.096,223.392,224.291,225.042,225.818,226.514,227.13]])

    np.testing.assert_array_almost_equal(tl_h[0,0,:,::20], answ_h, decimal=3) 
    np.testing.assert_array_almost_equal(tl_v[0,1::10,::20,0], answ_v, decimal=3) 
    assert tl_h.shape == (1,1,8,200), f'tl_h.shape = {tl_h.shape}'
    assert tl_v.shape == (1,72,201,8), f'tl_v.shape = {tl_v.shape}'

def test_transmission_loss_flat_seafloor():
    """ Check that we can initialize a transmission loss object 
        for a flat seafloor and uniform sound speed profile """
    transm_loss = transmission_loss(freq=100, source_depth=75, propagation_range=0.5, load_bathymetry=2000, ssp=1480, angular_bin=10)
    tl_h, ax_h, tl_v, ax_v = transm_loss.calc(vertical=True)
    answ = np.genfromtxt(os.path.join(path_to_assets, 'lloyd_mirror_f100Hz_SD75m.csv'), delimiter=",")
    assert answ.shape == tl_v[0,:,:,0].shape
    np.testing.assert_array_almost_equal(-tl_v[0,1:,:,0], answ[1:,:], decimal=3) 

#def test_test():
#    from datetime import datetime
#    bounds = dict(
#               south=43.53, north=44.29, west=-59.84, east=-58.48,
#               start=datetime(2015,1,1), end=datetime(2015,1,2), 
#               top=0, bottom=10000
#             )    
#    src = dict(load_bathymetry='chs', load_temp='hycom', load_salinity='hycom')
#    sound_source = {'freq': 200, 'lat': 43.8, 'lon': -59.04, 'source_depth': 12}
#    o = Ocean(**src, **bounds)
#    seafloor = {'sound_speed':1700,'density':1.5,'attenuation':0.5}
#    transm_loss = transmission_loss(seafloor=seafloor, propagation_range=20, **src, **bounds, **sound_source, ssp=1480, dz=50)
#    transm_loss.calc(vertical=False)
