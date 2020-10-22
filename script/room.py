import os, sys, json
from pprint import pprint
from data import jsonFiles, match

if len(sys.argv) <= 1:
    print('Usage: python {} [name | "#tripcode"]'.format(sys.argv[0]))
    print('Example: python {} "#.*cat"'.format(sys.argv[0]))
    print('Example: python {} lambda'.format(sys.argv[0]))
    exit(0)

place = set()
for fn in jsonFiles:
    rooms = json.loads(open(fn).read())
    for room in rooms:
        for u in room['users']:
            for p in sys.argv[1:]:
                if match(u, p):
                    place.add((room['name'], u['name']))
pprint(place)
