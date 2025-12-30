"""Bounding box for all data.

|       boundary |              value | 
|----------------|--------------------|
| West longitude | -85.94712712079293 |
| East longitide | -85.3443621648922  |
| South_latitude | 37.99712528351634  |
| North_latitude | 38.38023822809115  |

Span for each dimension. 
Distance was estimated with the distance tool on Google Maps. Not precise!

|             |         difference | approximate distance | 
|-------------|--------------------|----------------------|
| ∆ longitude | 0.6027649559007244 |             30 miles |
| ∆ latitude  | 0.3831129445748118 |             26 miles |

* notes
feet_in_a_mile = 5280 
I can never remember this. It'll come in handy.

* Code for finding the boundaries can be found in
    new/00_data_discovery/county_boundaries.ipynb
"""

west_longitude = -85.94712712079293
east_longitude = -85.3443621648922
south_latitude = 37.99712528351634
north_latitude = 38.38023822809115

delta_longitude = east_longitude - west_longitude
delta_latitude = north_latitude - south_latitude