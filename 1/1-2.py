#!/usr/bin/env python3

fuel = 0
with open("input") as F:
    for number in F:
        n = int(number)
        f = []
        f.append(n)
        while f[-1] > 0:
            fx = int(f[-1] / 3) - 2
            if fx < 0: fx = 0
            f.append(fx)
        f.pop(0)
        ff = sum(f)
        fuel += ff
        print(n, ff, f)

print(fuel)
