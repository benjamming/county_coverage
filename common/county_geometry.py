"""Bounding box for all data.

|       boundary |              value |               |
|----------------|--------------------|---------------|
| West longitude | -85.94712712079293 | min longitude |
| East longitide | -85.3443621648922  | max longitude |
| South_latitude | 37.99712528351634  | min latitude  |
| North_latitude | 38.38023822809115  | max latitude  |

Span for each dimension. 
Distance was estimated with the distance tool on Google Maps. Not precise!

|             |         difference |        approximate distance |  haversine estimate |
|-------------|--------------------|-(Google maps distance tool)-|---------------------|
| ∆ longitude | 0.6027649559007244 |                    30 miles |            32.68 mi |
| ∆ latitude  | 0.3831129445748118 |                    26 miles |            26.50 mi |


* Code for finding the boundaries can be found in
    new/00_data_discovery/county_boundaries.ipynb
"""
from numpy import radians, sin, cos, arcsin, sqrt

# Some constants
earth_radius_km = 6367
earth_radius_mi = 3956

km_to_miles = 0.6213712
mi_to_ft = 5280
km_to_ft = km_to_miles * mi_to_ft

# Notes on thest values: The following comes under the heading 
# “What value should I use for the radius of the Earth, R?” in the GIS FAQ:
# via: https://www.themathdoctors.org/distances-on-earth-2-the-haversine-formula/

"""The historical definition of a "nautical mile" is "one minute of arc of a 
great circle of the earth." Since the earth is not a perfect sphere, that 
definition is ambiguous. However, the internationally accepted (SI) value for 
the length of a nautical mile is (exactly, by definition) 1.852 km or exactly 
1.852/1.609344 international miles (that is, approximately 1.15078 miles - 
either "international" or "U.S. statute"). Thus, the implied "official" 
circumference is 
360 degrees times 60 minutes/degree times 1.852 km/minute = 40003.2 km. 

The implied radius is the circumference divided by 2 pi: 

R = 6367 km = 3956 mi"""

west_longitude = -85.94712712079293 # min longitude
east_longitude = -85.3443621648922
south_latitude = 37.99712528351634 # min latitude
north_latitude = 38.38023822809115

delta_longitude = east_longitude - west_longitude
delta_latitude = north_latitude - south_latitude

def scale_point(point):
    long, lat = point
    long = (long - west_longitude)/delta_longitude
    lat = (lat - south_latitude)/delta_latitude
    return long, lat 

def haversine_km(point1, point2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Returns value in kilometers.
    
    All args must be of equal length.    

    """
    lon1, lat1 = map(radians, point1)
    lon2, lat2 = map(radians, point2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    havTheta = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2
    
    theta = 2 * arcsin(sqrt(havTheta))
    return earth_radius_km * theta


def haversine_mi(point1, point2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Returns value in miles
    
    All args must be of equal length.    
    
    """
    lon1, lat1 = map(radians, point1)
    lon2, lat2 = map(radians, point2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    havTheta = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2
    
    theta = 2 * arcsin(sqrt(havTheta))
    return earth_radius_mi * theta
