import os, sys, json, csv
from pprint import pprint
from data import match, jsonFiles
from datetime import datetime
from service import run_http, open_web, host_timezone, fn_as_path
import threading


def findTimes(rule, fuzzy = True):
    users = set()
    times = list()
    for fn in jsonFiles:
        rooms = json.loads(open(fn).read())
        for room in rooms:
            for u in room['users']:
                if match(u, rule, fuzzy):
                    times.append(fn)
                    users.add((u['name'] + '#' + u.get('tripcode', '')))
    times.sort()
    return times, users

beg = '/lounge/'
end = '.json'

def parseTime(s):
    day, time = s.split('@')
    weekday = datetime.strptime(day, '%m_%d_%Y').weekday()
    return weekday, int(time.split(':')[0])


def main(rule, fuzzy = True):
    times, names = findTimes(rule, fuzzy)
    times = [s[s.index(beg) + len(beg):s.index(end)] for s in times]
    times = [parseTime(t) for t in times]
    counts = [[0 for j in range(7)] for i in range(24)]
    fd = open(os.path.join(fn_as_path(), 'files', 'data.csv'), 'w')
    htz = int(host_timezone())
    for d, h in times:
        counts[h - 8 + htz][d] += int(5)
    print('State,Sun (UTC{}{}),Mon,Tue,Wed,Thu,Fri,Sat'.format('+' if htz > 0 else '', htz), file=fd)
    for h, days in enumerate(counts):
        print("{},{}".format(h, ','.join([str(d) for d in days])), file=fd)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else "#L/CaT//Hsk")
    t = threading.Thread(target = open_web, args = ('http://localhost:8000/',))
    t.start()
    run_http()
    t.join()
