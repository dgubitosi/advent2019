#!/usr/bin/env python3

# state
memory = []
pc = 0
opcode = 0
modes = []
halt = False


# read program into memory as integers
with open("input") as F:
    for line in F:
        for i in line.strip().split(','):
            memory.append(int(i))


def opcode0102():
    # opcode01 = add
    # opcode02 = multiply
    # three parameters

    global memory
    global pc
    global opcode
    global modes
    global halt

    params = 3
    p = []
    for i in range(params):
        p.insert(i, memory[pc+1+i])

    print("*", pc, ":", opcode, modes, "->", p)

    # parameters 1 and 2 can be immediate or positional
    for i in [0,1]:
        # positional
        if modes[i] == 0:
            p[i] = memory[p[i]]

    print("*", pc, ":", opcode, modes, "->", p)

    # parameter 3 is always positional
    pos = p[2]
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
    pc += params + 1


def opcode03():
    # opcode03 = input
    # one parameter

    global memory
    global pc
    global opcode
    global modes
    global halt

    params = 1
    p = []
    for i in range(params):
        p.insert(i, memory[pc+1+i])

    print("*", pc, ":", opcode, modes, "->", p)

    # always positional
    pos = p[0]
    value = input("input? ")

    print("* [", pos, "] =", memory[pos])
    memory[pos] = int(value)
    print("* [", pos, "] =", memory[pos])

    pc += params + 1


def opcode04():
    # opcode04 = output
    # one parameter

    global memory
    global pc
    global opcode
    global modes
    global halt

    params = 1
    p = []
    for i in range(params):
        p.insert(i, memory[pc+1+i])

    print("*", pc, ":", opcode, modes, "->", p)

    value = p[0]
    if modes[0] == 0:
        value = memory[p[0]]
    print("output:", value)

    pc += params + 1


def opcode99():
    # opcode99 = halt
    # no parameters

    global memory
    global pc
    global opcode
    global modes
    global halt

    p = []
    print("*", pc, ":", opcode, p)

    halt = True


execute = {
    '01': opcode0102,
    '02': opcode0102,
    '03': opcode03,
    '04': opcode04,
    '99': opcode99
}


while not halt:
    instruction = memory[pc]
    print("*", pc, ":", instruction)

    opcode = instruction % 100
    opcode = "{:02d}".format(opcode)

    modes = instruction // 100
    modes = "{:03d}".format(modes)
    modes = [ int(n) for n in modes ]
    modes.reverse()

    print("*", pc, ":", opcode, modes)
    execute[opcode]()

