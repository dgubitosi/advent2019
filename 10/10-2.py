#!/usr/bin/env python3

import sys
import math
import pprint

try:
    file = sys.argv[1]
except:
    file = "input"

asteroids = {}
with open(file) as f:
    row = 0
    for line in f:
        for i, c in enumerate(line.strip()):
            if c == '#':
                pos = (i, row)
                asteroids.setdefault(pos,1)
        row += 1

pprint.pprint(asteroids)

targets = {}
precision = 3
best = None
count = 0
for b in asteroids:
    angles = {}
    for a in asteroids:
        if a == b: continue
        angle = math.atan2(a[1]-b[1], a[0]-b[0])
        angle = math.degrees(angle)

        # adjust angles so that
        # 0 is north, 90 is east, 180 is south, 270 is west
        angle += 90
        if angle < 0: angle += 360
        angle = round(angle, precision)

        distance = math.sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2))
        distance = round(distance, precision)

        angles.setdefault(angle,{})
        angles[angle][distance] = a

    if len(angles) > count:
        count = len(angles)
        best = b
        targets = angles

print(best, count, len(asteroids))
pprint.pprint(targets)

steps = 10**(precision)
r = 0
count = 0
bet = 0
asteroids.pop(best)
while len(asteroids.keys()):
    r += 1
    print(r, "targets","=",len(asteroids))
    for a in range(360):
        for decimal in range(steps):
            angle = a + decimal/steps
            angle = round(angle, precision)
            try:
                t = targets[angle]
                d = sorted(t.keys())[0]
                t = targets[angle].pop(d)
                asteroids.pop(t)
                count += 1
                print(r, angle, count, d, t)
                if count == 200:
                    bet = t[0]*100 + t[1]
            except:
                #print(r, angle)
                pass

print("bet",bet) 
