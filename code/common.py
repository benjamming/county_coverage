def get_long_lat_ranges(points):
    longitudes, latitudes = set(), set()
    for long, lat in points:
        longitudes.add(long)
        latitudes.add(lat)
    return ((min(longitudes), max(longitudes)), (min(latitudes), max(latitudes)))

