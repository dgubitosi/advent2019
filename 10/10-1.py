#!/usr/bin/env python3

import sys
import math

try:
    file = sys.argv[1]
except:
    file = "input.txt"

asteroids = []
with open(file) as f:
    row = 0
    for line in f:
        for i, c in enumerate(line.strip()):
            if c == '#':
                pos = (i, row)
                asteroids.append(pos)
        row += 1

#print(asteroids)
table = {}
best = None
count = 0
for i, b in enumerate(asteroids):
    angles = {}
    for j, a in enumerate(asteroids):
        if i == j: continue
        angle = str(round(math.atan2(b[0]-a[0], b[1]-a[1]),6))
        #print(i,j,b,a,angle)
        angles.setdefault(angle,0)
        angles[angle] += 1
    if len(angles) > count:
        count = len(angles)
        best = b
    table.setdefault(b,{})
    table[b]=angles

print(table[best])
print(best, count)
