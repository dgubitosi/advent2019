#!/usr/bin/env python3

import pprint
import sys

try:
    file = sys.argv[1]
except:
    file = "input"

adjacencies = {}
with open(file) as F:
    for line in F:
        p, c = line.strip().split(")")
        adjacencies.setdefault(p, []).append(c)
        adjacencies.setdefault(c, []).append(p)

# dijkstra's algorithm
unvisited = { node: None for node in list(adjacencies.keys()) }
visited = {}
current = 'COM'
current_distance = 0
unvisited[current] = current_distance

while True:
    print("V",visited)
    print("U",unvisited)
 
    print("Current:",current, adjacencies[current])
    for neighbor in adjacencies[current]:
        if neighbor not in unvisited: continue
        new_distance = current_distance + 1
        print("U:",neighbor,unvisited[neighbor],new_distance)
        if unvisited[neighbor] is None or unvisited[neighbor] > new_distance:
            unvisited[neighbor] = new_distance

    print("V",visited)
    print("U",unvisited)

    visited[current] = current_distance
    del unvisited[current]

    print("V",visited)
    print("U",unvisited)

    if not unvisited: break
    candidates = [ node for node in unvisited.items() if node[1] ]
    print("C",sorted(candidates, key = lambda x: x[1]))
    current, current_distance = sorted(candidates, key = lambda x: x[1])[0]
    print("Next:",current,current_distance)
    print()

