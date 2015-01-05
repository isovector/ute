import json
import os.path
from ute.utils import homeDir

custom_palette = []
type_mapping = { }

def build_custom_palette():
    filename = homeDir(".ute.palette")
    if not os.path.exists(filename):
        return

    js = None
    with open(filename) as f:
        js = json.load(f)

    for name, data in js["colors"].iteritems():
        custom_palette.append((name, data[0], data[1], data[2]))

    for color, types in js["map"].iteritems():
        for type in types:
            type_mapping[type] = color

