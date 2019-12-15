#!/usr/bin/env python3

with open("input") as F:
    pathes = F.readlines()

direction = {
    'U': (0,1),
    'D': (0,-1),
    'R': (1,0),
    'L': (-1,0)
}

wire = []
for index, path in enumerate(pathes):
    wire.append([])
    wire[index].append((0,0))
    p = path.strip().split(',')
    for pp in p:
        dir = pp[0]
        length = int(pp[1:])
        for j in range(length):
            pos = wire[index][-1]
            point = tuple(map(lambda x, y: x + y, pos, direction[dir]))
            wire[index].append(point)

intersection = list(set(wire[0]) & set(wire[1]))
distance = []
for p in intersection:
    if p == (0,0): continue
    d = abs(p[0]) + abs(p[1])
    distance.append(d)

print(min(distance))
