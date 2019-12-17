#!/usr/bin/env python3

import sys
import re
import itertools
import hashlib

file = "input"
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

states = {}
state = [ moons, velocity ]
state = hashlib.sha256("{}".format(state).encode()).hexdigest()
states[state] = 0

combos = list(itertools.combinations(range(len(moons)),2))
step = 0
while True:
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
    for i in range(len(moons)):
        for j in range(3):
            moons[i][j] += velocity[i][j]
    state = [ moons, velocity ]
    print(step, state)
    state = hashlib.sha256("{}".format(state).encode()).hexdigest()

    try:
        states[state] += 0
    except:
        states[state] = step
    else:
        # found the first duplicate state
        print("Repeats the state at step:",states[state])
        break


