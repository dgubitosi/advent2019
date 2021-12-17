#!/usr/bin/env python3

fuel = 0
with open("input.txt") as F:
    for number in F:
        fuel += int(int(number) / 3) - 2

print(fuel)
