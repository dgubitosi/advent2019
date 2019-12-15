#!/usr/bin/env python3

def isValid(n):
    k = str(n)

    dup = {}
    for i in range(1, len(k)):
        if k[i] < k[i-1]:
            return False
        if k[i] == k[i-1]:
            dup[k[i]] = dup.setdefault(k[i],0) + 1

    for k in dup:
        if dup[k] == 1: return True
    return False

with open("input") as F:
    start, end = F.readline().strip().split('-',2)

c = 0
n = int(start)
while n <= int(end):
    if isValid(n):
        print(n)
        c += 1
    n += 1

print("Total",c)
