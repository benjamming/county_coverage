"""Boundary information for Jefferson County, KY, USA"""

import shapes

SOURCE = """data/raw/Louisville_Metro_KY_County_Boundaries.geojson"""

LONG_MIN = -85.94712712079293 # derived from county data
LONG_MAX = -85.3474509339146 # derived from road data; longitude range for centerline points is slightly wider.
LAT_MIN, LAT_MAX = 37.99712528351634, 38.38023822809115 # derived from county data

DELTA_LONG = LONG_MAX - LONG_MIN  # == 0.5996761868783267
DELTA_LAT = LAT_MAX - LAT_MIN  # == 0.3831129445748118

BOX = shapes.Box(LONG_MIN, LONG_MAX, LAT_MIN, LAT_MAX)


def norm_long(longitude):
    return (longitude - LONG_MIN)/DELTA_LONG

def norm_lat(latitude):
    return (latitude - LAT_MIN)/DELTA_LAT

def norm_point(point):
    return (norm_long(point[0]), norm_lat(point[1]))


    
def validate():
    # This code will need to be fixed to cope with additional data from centerlines. 
    from readers import read_json
    from shapes import Box

    data = read_json(SOURCE)
    for feature in data['features']:
        if feature['properties']['CNTY_NAME'] == "JEFFERSON":
            shape = feature['geometry']['coordinates'][0]
            break

    box = Box.from_points(shape)
    
    if LONG_MIN == box.LONG_MIN:
        if LONG_MAX == box.LONG_MAX:
            if DELTA_LONG == box.DELTA_LONG:
                if LAT_MIN == box.LAT_MIN:
                    if LAT_MAX == box.LAT_MAX:
                        if DELTA_LAT == box.DELTA_LAT:
                            return True
    return False

"""
import shapes
import county_boundary

from os import path

CLEAN = "../../data/cleaner"
ROADS = path.join(CLEAN, 'centerlines.csv')
assert path.exists(ROADS)
COORDS = pd.read_csv(ROADS)['COORDINATES']

def generate_all_road_points(coordinates):
    for string in coordinates:
        for coord in string.split():
            x, y = coord.split(',')
            yield (float(x), float(y))

road_box = shapes.Box.from_points(generate_all_road_points(COORDS))
#road_box
for name in ("LONG_MIN", "LAT_MIN"):
    cty = getattr(county_boundary, name)
    rd = getattr(road_box, name)
    if rd < cty:
        print(name, rd)

for name in ("LONG_MAX", "LAT_MAX"):
    cty = getattr(county_boundary, name)
    rd = getattr(road_box, name)
    if rd > cty:
        print(name, rd)
"""