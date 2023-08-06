#!/usr/bin/env python3

import sys
import json

paths = sys.argv[1:]
json_paths = [x.replace(".jpeg", ".json") for x in paths]

def print_x_coords(path):
    dct = json.loads(path)
    x_coords = [x for x, y in dct['shapes'][0]['points']]
    for x in x_coords:
        print(x)

for path in json_paths:
    print_x_coords(path)
