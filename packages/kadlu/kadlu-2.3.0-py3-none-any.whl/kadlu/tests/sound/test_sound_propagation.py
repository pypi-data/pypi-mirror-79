""" Unit tests for the the 'sound.sound_propagation' module in the 'kadlu' package

    Authors: Oliver Kirsebom
    contact: oliver.kirsebom@dal.ca
    Organization: MERIDIAN-Intitute for Big Data Analytics
    Team: Acoustic data Analytics, Dalhousie University
    Project: packages/kadlu
             Project goal: Tools for underwater soundscape modeling
     
    License:

"""
import pytest
import math
import numpy as np
from kadlu.sound.sound_propagation import TLCalculator, Seafloor
from kadlu.geospatial.ocean import Ocean
from kadlu.utils import XYtoLL
from datetime import datetime

start = datetime(2019, 1, 1)
end = datetime(2019, 1, 1)

def test_initialize_seafloor_with_default_args():
    s = Seafloor()
    assert s.c == 1700
    assert s.density == 1.5
    assert s.thickness == 2000
    assert s.loss == 0.5

def test_initialize_seafloor_with_user_specified_args():
    s = Seafloor(c=1555, density=0.8, thickness=1000, loss=0.8)
    assert s.c == 1555
    assert s.density == 0.8
    assert s.thickness == 1000
    assert s.loss == 0.8

def test_attempt_to_compute_nsq_gives_error():
    s = Seafloor()
    with pytest.raises(AssertionError):
        _ = s.nsq()

def test_compute_nsq():
    s = Seafloor()
    s.c0 = 1500
    s.frequency = 20
    n = s.nsq()
    assert np.real(n) == pytest.approx(0.77835066, abs=1E-6)
    assert np.imag(n) == pytest.approx(0.01426442, abs=1E-6)

def test_initialize_tlcalculator_with_default_args():
    s = Seafloor()
    tl = TLCalculator(ocean_kwargs={}, seafloor=s)
    assert tl._compute_sound_speed == True
    assert tl.steps_btw_c_updates == 1

def test_initialize_tlcalculator_with_uniform_sound_speed():
    s = Seafloor()
    tl = TLCalculator(ocean_kwargs={}, seafloor=s, sound_speed=1488)
    assert tl._compute_sound_speed == False
    assert tl.c.data == 1488
    assert tl.steps_btw_c_updates == math.inf

def test_initialize_tlcalculator_with_ssp():
    s = Seafloor()
    z = np.array([-10, -100, -250, -900])
    c = np.array([1488, 1489, 1490, 1491])
    tl = TLCalculator(ocean_kwargs={}, seafloor=s, sound_speed=(c,z))
    assert tl._compute_sound_speed == False
    assert isinstance(tl.c.data, tuple)
    assert np.all(tl.c.data[0] == c)
    assert np.all(tl.c.data[1] == z)
    assert tl.steps_btw_c_updates == math.inf
    c1 = tl.c.eval(x=0,y=0,z=z,grid=True)
    assert np.all(c1 == c)

def test_update_source_location_and_time():
    s = Seafloor()
    tl = TLCalculator(ocean_kwargs={}, seafloor=s, sound_speed=1470)
    tl._update_source_location_and_time(lat=45, lon=80, start=start, end=end)
    tl.ocean.origin[0] == 45
    tl.ocean.origin[1] == 80
    lat_max, _ = XYtoLL(x=0, y=60e3, lat_ref=45, lon_ref=80)
    assert lat_max == tl.ocean.boundaries['north']
    lat_min, _ = XYtoLL(x=0, y=-60e3, lat_ref=45, lon_ref=80)
    assert lat_min == tl.ocean.boundaries['south']
    _, lon_max = XYtoLL(x=60e3, y=0, lat_ref=45, lon_ref=80)
    assert lon_max == tl.ocean.boundaries['east']
    _, lon_min = XYtoLL(x=-60e3, y=0, lat_ref=45, lon_ref=80)
    assert lon_min == tl.ocean.boundaries['west']

def test_bounding_box():
    s = Seafloor()
    tl = TLCalculator(ocean_kwargs={}, seafloor=s)
    s,n,w,e = tl._bounding_box(lat=45, lon=80, r=60e3)
    lat_max, _ = XYtoLL(x=0, y=60e3, lat_ref=45, lon_ref=80)
    assert lat_max == n
    lat_min, _ = XYtoLL(x=0, y=-60e3, lat_ref=45, lon_ref=80)
    assert lat_min == s
    _, lon_max = XYtoLL(x=60e3, y=0, lat_ref=45, lon_ref=80)
    assert lon_max == e
    _, lon_min = XYtoLL(x=-60e3, y=0, lat_ref=45, lon_ref=80)
    assert lon_min == w

def test_create_grid():
    s = Seafloor(thickness=800)
    o = {'load_bathymetry': 1000}
    dz = 10
    tl = TLCalculator(ocean_kwargs=o, seafloor=s, absorption_layer=0.2, vertical_bin=dz)
    tl._update_source_location_and_time(lat=45, lon=80, start=start, end=end)
    g = tl._create_grid(frequency=10)
    assert g.dr == 0.5 * 1500 / 10
    assert np.max(g.z) == pytest.approx((1000 + 800) * 1.2, abs=dz/2)

def test_run_with_flat_seafloor():
    s = Seafloor(thickness=2000)
    o = {'load_bathymetry': 10000}
    tl = TLCalculator(ocean_kwargs=o, seafloor=s, sound_speed=1500,\
        radial_bin=1000, radial_range=10e3, angular_bin=45, vertical_bin=1000,\
        verbose=True, progress_bar=False)
    tl.run(frequency=10, source_depth=9900, source_lat=45, source_lon=60)
    field = tl.TL[0,0]
    expected = np.array([[-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
        [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
        [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
        [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
        [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
        [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
        [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
        [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535]])
    np.testing.assert_array_almost_equal(field, expected, decimal=3)

def test_run_with_realistic_bathymetry():
    s = Seafloor(thickness=2000)
    o = {'load_bathymetry': 'CHS'}
    # initialize calculator
    tl = TLCalculator(ocean_kwargs=o, seafloor=s, sound_speed=1500,\
        radial_bin=1000, radial_range=10e3, angular_bin=45, vertical_bin=1000,\
        verbose=True, progress_bar=False)
    # run
    tl.run(frequency=10, source_depth=60., source_lat=43.5, source_lon=-59.5)

def test_run_with_uniform_temp_and_salinity():
    s = Seafloor(thickness=2000)
    o = {'load_bathymetry':'chs', 'load_temp':4, 'load_salinity':35}
    # initialize calculator
    tl = TLCalculator(ocean_kwargs=o, seafloor=s,\
        radial_bin=1000, radial_range=10e3, angular_bin=45, vertical_bin=1000,\
        verbose=True, progress_bar=False)
    # run
    tl.run(frequency=10, source_depth=-60., source_lat=43.5, source_lon=-59.5)

def test_run_at_same_depth_twice():
    s = Seafloor(thickness=2000)
    o = {'load_bathymetry':10000}
    tl = TLCalculator(ocean_kwargs=o, seafloor=s, sound_speed=1500,\
        radial_bin=1000, radial_range=10e3, angular_bin=45, vertical_bin=1000,\
        verbose=True, progress_bar=False)
    tl.run(frequency=10, source_depth=[9900, 9900], source_lat=45, source_lon=60)
    for field in [tl.TL[0,0], tl.TL[1,0]]:
        expected = np.array([[-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
            [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
            [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
            [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
            [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
            [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
            [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535],\
            [-164.6453, -170.6553, -176.7944, -172.0352, -182.3293, -176.6379, -176.8878, -183.8019, -177.9633, -181.3535]])
        np.testing.assert_array_almost_equal(field, expected, decimal=3)

def test_run_at_multiple_source_depths():
    s = Seafloor(thickness=2000)
    o = {'load_bathymetry': 10000}
    tl = TLCalculator(ocean_kwargs=o, seafloor=s, sound_speed=1500,\
        radial_bin=1000, radial_range=10e3, angular_bin=45, vertical_bin=1000,\
        verbose=True, progress_bar=False)
    tl.run(frequency=10, source_depth=[9900], source_lat=45, source_lon=60)
    f0 = tl.TL[0,0].copy()
    tl.run(frequency=10, source_depth=[8800], source_lat=45, source_lon=60)
    f1 = tl.TL[0,0].copy()
    tl.run(frequency=10, source_depth=[9900, 8800], source_lat=45, source_lon=60)
    fields = tl.TL[:,0]
    np.testing.assert_array_almost_equal(fields[0], f0, decimal=3)
    np.testing.assert_array_almost_equal(fields[1], f1, decimal=3)
