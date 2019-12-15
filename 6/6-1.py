#!/usr/bin/env python3

import pprint
import sys

try:
    file = sys.argv[1]
except:
    file = "input"

table = {}
with open(file) as F:
    for line in F:
        p, c = line.strip().split(")")
        table.setdefault(p, []).append(c)
        table.setdefault(c, []).append(p)

# dijkstra's algorithm
unvisited = { node: None for node in list(table.keys()) }
visited = {}
current = 'COM'
current_distance = 0
unvisited[current] = current_distance

while True:
    for neighbor in table[current]:
        if neighbor not in unvisited: continue
        new_distance = current_distance + 1
        if unvisited[neighbor] is None or unvisited[neighbor] > new_distance:
            unvisited[neighbor] = new_distance
    visited[current] = current_distance
    del unvisited[current]
    if not unvisited: break
    candidates = [ node for node in unvisited.items() if node[1] ]
    current, current_distance = sorted(candidates, key = lambda x: x[1])[0]

print(visited)
steps = 0
for k in visited:
    steps += visited[k]
print(steps)
