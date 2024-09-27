"""Boundary information for Jefferson County, KY, USA"""



LONGITUDES = LONG_MIN, LONG_MAX = -85.94712712079293, -85.40492183942492
LATITUDES = LAT_MIN, LAT_MAX = 37.99712528351634, 38.38023822809115

DELTA_LONG = LONG_MAX - LONG_MIN  # == 0.5422052813680125
DELTA_LAT = LAT_MAX - LAT_MIN  # == 0.3831129445748118

def norm_long(longitude):
    return (longitude - LONG_MIN)/DELTA_LONG

def norm_lat(latitude):
    return (latitude - LAT_MIN)/DELTA_LAT

def norm_point(point):
    return (norm_long(point[0]), norm_lat(point[1]))


"""
To validate, run:
SOURCE = "/data/raw/Louisville_Metro_KY_County_Boundaries.geojson"
COUNTY = "JEFFERSON"

import json
import os

try:
    assert os.path.exists(SOURCE)
except:
    os.chdir('../..')
    assert os.path.exists(SOURCE)
# Not sure this test works yet. 
# Figure out the filesystem quirk here when running files vs. notebooks.

with open(file, 'r') as file:
    data = json.load(file)

for feature in data['features']:
    if feature['properties']['CNTY_NAME'] == COUNTY:
        shape = feature['geometry']['coordinates'][0]
        break

longitudes, latitudes = set(), set()
for long, lat in shape:
    longitudes.add(long)
    latitudes.add(lat)

LONG_MIN = min(longitudes)
LONG_MAX = max(longitudes)
#etc.
"""