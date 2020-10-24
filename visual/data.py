import os, re

DATA_DIR = os.path.join('..', 'lounge')

def isTarget(u, name, tripcode, fuzzy = True):
    utrip = (lambda x: str(x) if x else x)(u.get('tripcode'))
    if fuzzy:
        if name: return re.match(re.compile(name, re.IGNORECASE), u['name'])
        if utrip and tripcode:
            return re.match(re.compile(tripcode, re.IGNORECASE), utrip)
    else:
        if name: return u['name'] == name
        if utrip and tripcode:
            return tripcode == utrip


def match(u, rule, fuzzy = True):
    return isTarget(u, None, rule[1:], fuzzy) \
            if rule.startswith('#') \
            else isTarget(u, rule, None, fuzzy)

jsonFiles = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f)) and '.json' in f]
