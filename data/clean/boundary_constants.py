"""Boundary information for Jefferson County, KY, USA

Proof on file."""

LONGITUDES = LONG_MIN, LONG_MAX = -85.94712712079293, -85.3474509339146
LATITUDES = LAT_MIN, LAT_MAX = 37.99712528351634, 38.38023822809115

DELTA_LONG = LONG_MAX - LONG_MIN  # == 0.5422052813680125
DELTA_LAT = LAT_MAX - LAT_MIN  # == 0.3831129445748118

def norm_long(longitude):
    return (longitude - LONG_MIN)/DELTA_LONG

def norm_lat(latitude):
    return (latitude - LAT_MIN)/DELTA_LAT

def norm_point(point):
    return (norm_long(point[0]), norm_lat(point[1]))