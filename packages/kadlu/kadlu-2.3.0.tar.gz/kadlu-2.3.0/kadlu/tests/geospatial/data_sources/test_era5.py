import pytest
import kadlu
from datetime import datetime, timedelta

# gulf st lawrence
kwargs = dict(
        south=46.1, west=-64.4, north=47, east=-63.4,
        start=datetime(2016, 2, 1), end=datetime(2016, 2, 1),
        top=0, bottom=5000,
    )

def test_era5_load_windwaveswellheight():
    val, lat, lon, time = kadlu.load(source='era5', var='waveheight', **kwargs)
    assert(len(val)==len(lat)==len(lon))
    assert(len(lat) > 0)

def test_era5_load_wavedirection():
    val, lat, lon, time = kadlu.load(source='era5', var='wavedir', **kwargs)
    assert(len(val)==len(lat)==len(lon))
    assert(len(lat) > 0)

def test_era5_load_waveperiod():
    val, lat, lon, time = kadlu.load(source='era5', var='waveperiod', **kwargs)
    assert(len(val)==len(lat)==len(lon))
    assert(len(lat) > 0)

def test_era5_load_wind():
    ns_offset = 1
    ew_offset = 1

    uval,lat,lon,epoch = kadlu.load(source='era5', var='wind_u', 
                        start=datetime(2016, 3, 9) , end=datetime(2016,3,11),
                        south=44.5541333 - ns_offset, west=-64.17682 - ew_offset, 
                        north=44.5541333 + ns_offset, east=-64.17682 + ew_offset, 
                        top=0, bottom=0)
    assert(len(uval)==len(lat)==len(lon))
    assert len(uval) > 0

    vval,lat,lon,epoch = kadlu.load(source='era5', var='wind_v', 
                        start=datetime(2016, 3, 9) , end=datetime(2016,3,11),
                        south=44.5541333 - ns_offset, west=-64.17682 - ew_offset, 
                        north=44.5541333 + ns_offset, east=-64.17682 + ew_offset, 
                        top=0, bottom=0)
    assert(len(vval)==len(lat)==len(lon))
    assert len(vval) > 0

    uvval,lat,lon,epoch = kadlu.load(source='era5', var='wind_uv', 
                        start=datetime(2016, 3, 9) , end=datetime(2016,3,11),
                        south=44.5541333 - ns_offset, west=-64.17682 - ew_offset, 
                        north=44.5541333 + ns_offset, east=-64.17682 + ew_offset, 
                        top=0, bottom=0)

    assert(len(uvval)==len(lat)==len(lon))
    assert len(uvval) > 0

