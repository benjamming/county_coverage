"""Geometry information for Jefferson County, Kentucky and datasets.

Bounding box for all data.

|       boundary |              value |               |
|----------------|--------------------|---------------|
| West longitude | -85.94712712079293 | min longitude |
| East longitide | -85.3443621648922  | max longitude |
| South latitude | 37.99712528351634  | min latitude  |
| North latitude | 38.38023822809115  | max latitude  |

Spans for each dimension. 

|             |         difference | approximate | haversine |
|             |                    |    distance |  distance |
|-------------|--------------------|-------------|-----------|
| ∆ longitude | 0.6027649559007244 |    30 miles |  32.68 mi |
| ∆ latitude  | 0.3831129445748118 |    26 miles |  26.50 mi |

Approximate distance was gathered using Google Maps "measure distance" tool.
Pretty close for eyeballing it. 

* Code for finding/calculating these various figures can be found in
    new/00_data_discovery/county_boundaries.ipynb
"""

from numpy import radians, sin, cos, arcsin, sqrt
from numpy.linalg import norm

from pyproj import CRS
from pyproj.transformer import Transformer 

# convert coordinates from LOJIC CRS to (longitude, latitude)
# LOJIC projection: ESRI:102679
# NAD_1983_StatePlane_Kentucky_North_FIPS_1601_Feet

# Standard long, lat: epsg:4326
KY_grid_north_CRS = CRS("ESRI:102679")
standard_CRS = CRS("epsg:4326")

LL_to_KY_grid = Transformer.from_crs(
    crs_from=standard_CRS, crs_to=KY_grid_north_CRS, always_xy=True).transform

KY_grid_to_LL = Transformer.from_crs(
    crs_from=KY_grid_north_CRS, crs_to=standard_CRS, always_xy=True).transform


# Some constants
earth_radius_km = 6367
earth_radius_mi = 3956

# value for km calculated from:
# https://planetcalc.com/7721/
earth_radius_km_2 = 6370.074


mi_to_ft = 5280
earth_radius_ft = earth_radius_mi * mi_to_ft

km_to_miles = 0.6213712
km_to_ft = km_to_miles * mi_to_ft

"""
Notes on these values: 
via: https://www.themathdoctors.org/distances-on-earth-2-the-haversine-formula/

The following comes under the heading “What value should I use for the radius of 
the Earth, R?” in the GIS FAQ:

The historical definition of a "nautical mile" is "one minute of arc of a 
great circle of the earth." Since the earth is not a perfect sphere, that 
definition is ambiguous. However, the internationally accepted (SI) value for 
the length of a nautical mile is (exactly, by definition) 1.852 km or exactly 
1.852/1.609344 international miles (that is, approximately 1.15078 miles —
either "international" or "U.S. statute"). Thus, the implied "official" 
circumference is 

    360 degrees times 60 minutes/degree times 1.852 km/minute = 40003.2 km. 

The implied radius is the circumference divided by 2 pi: 

R = 6367 km = 3956 mi
"""

# More constants: Bounding box for Jefferson county
west_longitude = -85.94712712079293
east_longitude = -85.3443621648922
south_latitude = 37.99712528351634 
north_latitude = 38.38023822809115

delta_longitude = east_longitude - west_longitude
delta_latitude = north_latitude - south_latitude

# 
def scale_point(point):
    """Scale longitude, latitude to a value between 0.0 and 1.0 inclusive,
    where 0.0 represents the minimum boundary and 1.0 represents the maximum
    boundary for each dimension within the county box.
    """
    lon, lat = point
    lon -= west_longitude # min longitude
    lat -= south_latitude # min latitude
    return lon/delta_longitude, lat/delta_latitude

def scale_longitude(longitude):
    return (longitude - west_longitude)/delta_longitude

def scale_latitude(latitude):
    return (latitude - south_latitude)/delta_latitude


# euclidean functions
def euc_distance_mi(point1, point2):
    lon1, lat1 = point1
    lon2, lat2 = point2

    dlon = ((lon1 - lon2)/delta_longitude) * 32.68 # mile distance
    dlat = ((lat1 - lat2)/delta_longitude) * 26.50

    return sqrt(dlon**2 + dlat**2)

# haversine functions
def central_angle(point1, point2):
    """
    Calculate the central angle between two points on the earth 
    (specified in decimal degrees)
    
    """
    lon1, lat1 = map(radians, point1)
    lon2, lat2 = map(radians, point2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    havTheta = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2
    return 2 * arcsin(sqrt(havTheta))


def haversine_distance_mi(point1, point2):
    """Calculate distance between two points on the earth using the
    haversine formula. Returns distance in miles.
    """
    return central_angle(point1, point2) * earth_radius_mi

def haversine_distance_ft(point1, point2):
    """Calculate distance between two points on the earth using the
    haversine formula. Returns distance in feet.
    """
    return central_angle(point1, point2) * earth_radius_ft

def haversine_distance_km(point1, point2):
    """Calculate distance between two points on the earth using the
    haversine formula. Returns distance in kilometers.
    """
    return central_angle(point1, point2) * earth_radius_km


# These have really come in handy
# Determined by haversine method

#longitude_span_mi = 32.68 # distance in miles #
#latitide_span_mi = 26.50 

longitude_span_mi = haversine_distance_mi(
    (west_longitude, north_latitude), (east_longitude, north_latitude))

latitude_span_mi = haversine_distance_mi(
    (west_longitude, south_latitude), (west_longitude, north_latitude))

class converter:
    def __init__(self):
        self.KY_grid_CRS = KYCRS = CRS("ESRI:102679")
        self.long_lat_CRS = LLCRS =CRS("epsg:4326")

        to_grid = Transformer.from_crs(crs_from=LLCRS, crs_to=KYCRS, always_xy=True)
        to_ll = Transformer.from_crs(crs_from=KYCRS, crs_to=LLCRS, always_xy=True)

        self.to_grid = self.from_ll = to_grid.transform
        self.to_ll = self.from_grid = to_ll.transform

    def point_to_ll(self, point):
        return self.to_ll(*point)
    
    def point_to_grid(self, point):
        return self.to_grid(*point)

convert_points = converter()