#!/usr/bin/env python3

import sys
import re
import itertools
import math

file = "input.txt"
if len(sys.argv) > 1:
    file = sys.argv[1]

moons = []
velocity = []
regexp = r"<x=(?P<x>[\-0-9]+), y=(?P<y>[\-0-9]+), z=(?P<z>[\-0-9]+)>"
with open(file) as f:
    for line in f:
        m = re.search(regexp, line)
        moon = [ int(m.group('x')),
                 int(m.group('y')),
                 int(m.group('z')) ]
        moons.append(moon)
        v = [ 0, 0, 0 ]
        velocity.append(v)

#print(0, "M", moons)
#print(0, "V", velocity)

state = []
for m in moons:
    state.append(m.copy())
print(state)

pos = 'xyz'
first = [ 0, 0, 0 ]

combos = list(itertools.combinations(range(len(moons)),2))
step = 0
done = 0
while done < 3:
    step += 1
    for c in combos:
        for j in range(3):
            # velocity is cumulative
            if moons[c[0]][j] < moons[c[1]][j]:
                velocity[c[0]][j] += 1
                velocity[c[1]][j] += -1
            elif moons[c[0]][j] > moons[c[1]][j]:
                velocity[c[0]][j] += -1
                velocity[c[1]][j] += 1
    p = [ 0, 0, 0 ]
    v = [ 0, 0, 0 ]
    for i in range(len(moons)):
        for j in range(3):
            moons[i][j] += velocity[i][j]
            if moons[i][j] == state[i][j]: p[j] += 1
            if velocity[i][j] == 0: v[j] += 1
    c = 0
    for i in range(3):
        if p[i] == len(moons) and v[i] == len(moons):
            print(step, pos[i])
            c += 1
            if first[i] == 0:
                first[i] = step
                done += 1

print(first)
# lcm(x,y,x) = lcm(lcm(x,y),z)
# lcm(x,y) = x*y / gcd(x,y)
xy = (first[0]*first[1]) // math.gcd(first[0],first[1])
xyz = (xy*first[2]) // math.gcd(xy,first[2])
print(xyz)

 
