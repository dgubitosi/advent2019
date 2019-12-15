#!/usr/bin/env python3

import sys

try:
    file = sys.argv[1]
except:
    file = "input"

w = 25
h = 6
size = 25 * 6

data = []
with open(file) as f:
    data = f.read().strip()

nlayers = len(data) // size
checksum = len(data) % size
assert checksum == 0, "oops"

layers = []
occurances = []
n = 0
z = size
best = None
while len(data) >= size:
    slice, data = data[:size], data[size:]
    layers.append(slice)
    o = [ 0,0,0 ]
    for c in slice:
        o[int(c)] += 1
    if o[0] < z:
        z = o[0]
        best = n
    occurances.append(o)
    n += 1

print(best,occurances[best],occurances[best][1] * occurances[best][2])
