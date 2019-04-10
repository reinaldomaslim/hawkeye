#! /usr/bin/python

###################
##### HAWKEYE #####
###################

import json

with open('./data/station/android/20190410.geojson') as f:
    data = json.load(f)

for feature in data['features']:
    print feature['geometry']['type']
    print feature['geometry']['coordinates']