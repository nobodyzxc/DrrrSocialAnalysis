import os, sys, json
from math import log
from pprint import pprint
from data import jsonFiles, match
from service import run_http, open_web, host_timezone, fn_as_path
import threading

def findFriends(rule, fuzzy=True):
    friends = set()
    fnames = set()
    fcodes = set()
    target = set()
    for filename in jsonFiles:
        rooms = json.loads(open(filename).read())
        for room in rooms:
            for user in room['users']:
                if match(user, rule, fuzzy):
                    target.add((user['name'], user.get('tripcode', '')))
                    for u in room['users']:
                        fn, fc = u['name'], u.get('tripcode', '')
                        fnames.add(fn)
                        if fc: fcodes.add(fc)
                    friends.update([(u['name'], u.get('tripcode', '')) for u in room['users']])
    return friends, fnames, fcodes, target

def normalize(v):
    return log(v) + 1

def count_link(friends, fnames, fcodes):
    links = dict()
    for filename in jsonFiles:
        rooms = json.loads(open(filename).read())
        for room in rooms:
            names = [u['name'] for u in room['users'] if u['name'] in fnames]
            names.sort()
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    key = (names[i], names[j])
                    links[key] = links.get(key, 0) + 1
    return links

def folding_nodes_links(fs, fns, fcs, freqs, target):

    tc2names = {tc: set() for tc in fcs}
    name2tc = dict()

    for n, c in fs:
        if c: tc2names.setdefault(c, set()).add(n)
    for tc in tc2names:
        for name in tc2names[tc]:
            name2tc[name] = tc

    def fold_name(name):
        if name in name2tc:
            return list(tc2names[name2tc[name]])[0]
        return name

    target_name = fold_name(list(target)[0][0])

    names = set([fold_name(n) for n in fns])
    nodes = [{'id': n, 'group': i} for i, n in enumerate(names)]

    counts = dict()
    lnames = set()
    for a, b in freqs:
        key = tuple(sorted([fold_name(a), fold_name(b)]))
        lnames.add(key[0])
        lnames.add(key[1])
        counts[key] = counts.get(key, 0) + freqs[(a, b)]

    if len(lnames) != len(names):
        print(lnames - names)
        exit(0)

    uniq = lambda a, b: b if a == target_name else (a if b == target_name else None)
    links = [(uniq(*pr).replace('.', '．').replace('/', '／'), counts[pr]) for pr in counts if uniq(*pr)]
    return nodes, links


def main(rule, fuzzy=True):
    fs, fns, fcs, target = findFriends(rule, fuzzy)
    freqs = count_link(fs, fns, fcs)
    nodes, links = folding_nodes_links(fs, fns, fcs, freqs, target)
    fd = open(os.path.join(fn_as_path(), 'files', 'data.csv'), 'w')
    print('id,value', file=fd)
    for name, value in links:
        print('{},{}'.format(name, value), file=fd)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else "#L/CaT//Hsk")
    t = threading.Thread(target = open_web, args = ('http://localhost:8000/',))
    t.start()
    run_http()
    t.join()
