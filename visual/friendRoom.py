import os, sys, json, operator
from math import log
from pprint import pprint
from data import jsonFiles, match
from service import run_http, open_web, host_timezone, fn_as_path
import threading

def keyOfMaxVal(dictionary):
    return max(dictionary.items(), key=operator.itemgetter(1))[0]

def findFriends(rule, fuzzy=True):
    friends = set()
    fnames = set()
    fcodes = set()
    roomHost = dict()
    for filename in jsonFiles:
        rooms = json.loads(open(filename).read())
        for room in rooms:
            if room['name'] not in roomHost:
                d = roomHost.setdefault(room['name'], dict())
                d[room['host']['name']] = d.get(room['host']['name'], 0) + 1
            for user in room['users']:
                if match(user, rule, fuzzy):
                    for u in room['users']:
                        fn, fc = u['name'], u.get('tripcode', '')
                        fnames.add(fn)
                        if fc: fcodes.add(fc)
                    friends.update([(u['name'], u.get('tripcode', '')) for u in room['users']])
    for roomName in roomHost:
        host = keyOfMaxVal(roomHost[roomName])
        roomHost[roomName] = host
    return friends, fnames, fcodes, roomHost

def normalize(v):
    return log(v) + 1

def count_link(friends, fnames, fcodes):
    links = dict()
    roomMap = dict()
    for filename in jsonFiles:
        rooms = json.loads(open(filename).read())
        for room in rooms:
            names = [u['name'] for u in room['users'] if u['name'] in fnames]
            names.sort()
            for name in names:
                rm = roomMap.setdefault(name, dict())
                rm[room['name']] = links.get(room['name'], 0) + 1
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    key = (names[i], names[j])
                    links[key] = links.get(key, 0) + 1
    return links, roomMap

def folding_nodes_links(fs, fns, fcs, freqs, rfreqs, hosts):

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

    names = set([fold_name(n) for n in fns])
    for roomName in hosts:
        hosts[roomName] = fold_name(hosts[roomName])

    roomMap = dict()
    for name in rfreqs:
        fn = fold_name(name)
        nd = roomMap.setdefault(fn, dict())
        for key in rfreqs[name]:
            nd[key] = nd.get(key, 0) + rfreqs[name][key]

    meetsNames = dict()
    meetsCounts = dict()
    lnames = set()
    for a, b in freqs:
        fna, fnb = fold_name(a), fold_name(b)
        lnames.add(fna); lnames.add(fnb)
        meetsNames.setdefault(fna, set()).add(fnb)
        meetsNames.setdefault(fnb, set()).add(fna)
        meetsCounts[fna] = meetsCounts.get(fna, 0) + freqs[(a, b)]
        meetsCounts[fnb] = meetsCounts.get(fnb, 0) + freqs[(a, b)]

    if len(lnames) != len(names):
        print(lnames - names)
        exit(0)

    return names, meetsNames, meetsCounts, roomMap, hosts

def strB2Q(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 32:
                inside_code = 12288
            elif (inside_code >= 33 and inside_code <= 126):
                inside_code += 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

def main(rule, fuzzy=True):
    fs, fns, fcs, hosts = findFriends(rule, fuzzy)
    freqs, rfreqs = count_link(fs, fns, fcs)
    names, meetsNames, meetsCounts, roomMap, hosts = folding_nodes_links(fs, fns, fcs, freqs, rfreqs, hosts)

    #norname = lambda name: name.replace('.', '．').replace('/', '／').replace(' ', '_').replace('+', '＋').replace('-', '—').replace(';', '；')
    norname = strB2Q
    add_room = lambda name: "flare.drrr.{}.{}".format(norname(hosts[keyOfMaxVal(roomMap[name])]), norname(name))
    data = [{"name": add_room(name), \
             "size": meetsCounts[name], \
             "imports": [add_room(n) for n in meetsNames[name]]} for name in names]

    fd = open(os.path.join(fn_as_path(), 'files', 'data.json'), 'w')
    print(json.dumps(data, indent=2), file=fd)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else "#L/CaT//Hsk")
    t = threading.Thread(target = open_web, args = ('http://localhost:8000/',))
    t.start()
    run_http()
    t.join()
