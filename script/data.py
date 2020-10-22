import os, re

DATA_DIR = os.path.join('..', 'lounge')

def isTarget(u, name, tripcode):
    utrip = (lambda x: str(x) if x else x)(u.get('tripcode'))
    if name: return re.match(re.compile(name, re.IGNORECASE), u['name'])
    if utrip and tripcode:
        return re.match(re.compile(tripcode, re.IGNORECASE), utrip)

def match(u, rule):
    return isTarget(u, None, rule[1:]) \
            if rule.startswith('#') \
            else isTarget(u, rule, None)

jsonFiles = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f)) and '.json' in f]
