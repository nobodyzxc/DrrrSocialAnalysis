import os, sys, json
from pprint import pprint
from data import match, jsonFiles

if len(sys.argv) <= 2:
    print('Usage: python {} [name | "#tripcode"] [name | "#tripcode"]'.format(sys.argv[0]))
    print('Example: python {} "#.*cat" "lambda"'.format(sys.argv[0]))
    print('Example: python {} lambda'.format(sys.argv[0]))
    exit(0)

manA, manB = sys.argv[1:]

record = []
for fn in jsonFiles:
    rooms = json.loads(open(fn).read())
    for room in rooms:
        cnt, us = 0, []
        for u in room['users']:
            if match(u, manA) or match(u, manB):
                us.append(u['name'] + '#' + u.get('tripcode', ''))
                cnt += 1
        if cnt >= 2:
            record.append((os.path.splitext(fn)[0], us))

record.sort()

for r in record:
    pprint(r)
