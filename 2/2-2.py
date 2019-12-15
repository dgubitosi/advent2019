#!/usr/bin/env python3

with open("input") as F:
    memory = []
    for line in F:
        memory.extend(line.split(','))

stop = False
for noun in range(0, 99):
    if stop: break
    for verb in range(0, 99):
        if stop: break
        print(noun, verb)
        m = []
        m.extend(memory)
        m[1] = noun
        m[2] = verb
        pc = 0
        halt = False
        while not halt:
            opcode = int(m[pc])
            addr_x = int(m[pc+1])
            addr_y = int(m[pc+2])
            addr_z = int(m[pc+3])
            pc += 4
            if opcode == 1:
               m[addr_z] = int(m[addr_x]) + int(m[addr_y])
            if opcode == 2:
               m[addr_z] = int(m[addr_x]) * int(m[addr_y])
            if opcode == 99:
                halt = True
        if m[0] == 19690720:
            stop = True

