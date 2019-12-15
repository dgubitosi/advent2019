#!/usr/bin/env python3

with open("input") as F:
    memory = []
    for line in F:
        memory.extend(line.split(','))
    memory[1] = 12
    memory[2] = 2
    pc = 0
    halt = False
    while not halt:
        opcode = int(memory[pc])
        addr_x = int(memory[pc+1])
        addr_y = int(memory[pc+2])
        addr_z = int(memory[pc+3])
        pc += 4
        if opcode == 1:
           memory[addr_z] = int(memory[addr_x]) + int(memory[addr_y])
        if opcode == 2:
           memory[addr_z] = int(memory[addr_x]) * int(memory[addr_y])
        if opcode == 99:
            halt = True

print(memory[0])
