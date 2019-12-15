#!/usr/bin/env python3

# state
memory = []
pc = 0
opcode = 0
mode = []
halt = False

import sys
try:
    file = sys.argv[1]
except:
    file = "input"

# read program into memory as integers
with open(file) as F:
    for line in F:
        for i in line.strip().split(','):
            memory.append(int(i))


def getParams(n):

    global memory
    global pc
    global opcode
    global mode
    global halt

    if n == 0:
        return None

    p = []
    for i in range(n):
        p.insert(i, memory[pc+1+i])

    print("*", pc, ":", opcode, mode[:n], "->", p)

    # resolve addressing mode
    for i in range(n):
        # positional
        if mode[i] == 0:
            p[i] = memory[p[i]]

    print("*", pc, ":", opcode, mode[:n], "->", p)

    return p


def opcode0102():
    # opcode01 = add
    # opcode02 = multiply
    # three parameters

    global memory
    global pc
    global opcode
    global mode
    global halt

    params = 3
    mode[params-1] = 1
    p = getParams(params)
    pos = p[params-1]
    pc += params + 1

    print("* [", pos, "] =", memory[pos])

    # add
    if opcode == '01':
        print("* ADD",p[0],p[1],"> [", pos, "]")
        memory[pos] = int(p[0] + p[1])

    # multiply
    if opcode == '02':
        print("* MULT",p[0],p[1],"> [", pos, "]")
        memory[pos] = int(p[0] * p[1])

    print("* [", pos, "] =", memory[pos])


def opcode03():
    # opcode03 = input
    # one parameter

    global memory
    global pc
    global opcode
    global mode
    global halt

    params = 1
    mode[params-1] = 1
    p = getParams(params)
    pos = p[params-1]
    pc += params + 1

    print("* [", pos, "] =", memory[pos])

    value = input("input? ")
    memory[pos] = int(value)

    print("* [", pos, "] =", memory[pos])


def opcode04():
    # opcode04 = output
    # one parameter

    global memory
    global pc
    global opcode
    global mode
    global halt

    params = 1
    p = getParams(params)
    pc += params + 1

    print("output:", p[0])


def opcode0506():
    # opcode05 = jump if true
    # opcode06 = jump if false 
    # two parameters

    global memory
    global pc
    global opcode
    global mode
    global halt

    params = 2
    p = getParams(params)
    pc += params + 1

    # jump if true
    if opcode == '05':
        print("* JNZ",p[0],p[1])
        if p[0] != 0: pc = p[1]

    # jump if false
    if opcode == '06':
        print("* JZ",p[0],p[1])
        if p[0] == 0: pc = p[1]



def opcode0708():
    # opcode07 = less than
    # opcode08 = equals
    # three parameters

    global memory
    global pc
    global opcode
    global mode
    global halt

    params = 3
    mode[params-1] = 1
    p = getParams(params)
    pos = p[params-1]
    pc += params + 1

    print("* [", pos, "] =", memory[pos])

    # less than
    if opcode == '07':
        print("* LT",p[0],p[1],">",p[2])
        if p[0] < p[1]:
            memory[pos] = 1
        else:
            memory[pos] = 0

    # equal
    if opcode == '08':
        print("* EQ",p[0],p[1],">",p[2])
        if p[0] == p[1]:
            memory[pos] = 1
        else:
            memory[pos] = 0

    print("* [", pos, "] =", memory[pos])


def opcode99():
    # opcode99 = halt
    # no parameters

    global memory
    global pc
    global opcode
    global mode
    global halt

    params = 0
    p = getParams(params)
    print("*", "HALT")

    halt = True


execute = {
    '01': opcode0102,
    '02': opcode0102,
    '03': opcode03,
    '04': opcode04,
    '05': opcode0506,
    '06': opcode0506,
    '07': opcode0708,
    '08': opcode0708,
    '99': opcode99
}


while not halt:
    instruction = memory[pc]
    print("*", pc, ":", instruction)

    opcode = instruction % 100
    opcode = "{:02d}".format(opcode)

    mode = instruction // 100
    mode = "{:03d}".format(mode)
    mode = mode[::-1]

    print("*", pc, ":", opcode, mode)
    mode = [ int(n) for n in mode ]

    execute[opcode]()

