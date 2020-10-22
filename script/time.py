import os, sys, json
from pprint import pprint
from data import match, jsonFiles


users = set()
times = list()

if len(sys.argv) <= 1:
    print('Usage: python {} [nameRegex | "#tripcodeRegex"]'.format(sys.argv[0]))
    print('Example: python {} "#.*cat"'.format(sys.argv[0]))
    print('Example: python {} lambda'.format(sys.argv[0]))
    exit(0)

for fn in jsonFiles:
    rooms = json.loads(open(fn).read())
    for room in rooms:
        for u in room['users']:
            for p in sys.argv[1:]:
                if match(u, p):
                    times.append(fn)
                    users.add((u['name'] + '#' + u.get('tripcode', '')))

times.sort()
pprint(times)
pprint(users)
