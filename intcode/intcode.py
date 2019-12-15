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


def setModePositional(n):
    global mode
    mode &= ~(1<<n)


def setModeImmediate(n):
    global mode
    mode |= (1<<n)


def getMode(n):
    global mode
    return (mode & (1<<n))


def isModeImmediate(n):
    global mode
    if getMode(n) == 1: return True
    return False


def isModePositional(n):
    global mode
    if getMode(n) == 0: return True
    return False


def printInstruction(parameters, positional = True):
    global table
    global pc

    np = table[opcode][1]
    wr = table[opcode][-1]

    # print instruction
    instruction = table[opcode][0]
    for i, p in enumerate(parameters):
        instruction += " "
        if (i == wr):
            instruction += "@"
        if positional and isModePositional(i):
            instruction += "@"
        instruction += str(p)
        if (i < (np - 1)): 
            instruction += ","
    print("*",pc,":",instruction)


def getParams():
    global table
    global memory
    global pc
    global opcode
    global mode
    global halt

    np = table[opcode][1]
    wr = table[opcode][-1]

    p = []
    for i in range(np):
        p.insert(i, memory[pc+1+i])

    # resolve addressing mode
    # write position is treated as immediate
    mask = "{:0{w}b}".format(mode, w=np)
    mask = mask[::-1]
    print("*",pc,":",opcode,mask,p)

    printInstruction(p)

    resolved = False
    for i in range(np):
        if isModePositional(i):
            resolved = True
            p[i] = memory[p[i]]

    if resolved:
        printInstruction(p, False)

    return p


def opcode0102(p, wr):
    # opcode01 = add
    # opcode02 = multiply
    # three parameters
    # last is write position

    global memory
    global pc
    global opcode
    global mode
    global halt

    pos = p[wr]
    print("*","@",pos,"=",memory[pos])

    # add
    if opcode == '01':
        memory[pos] = int(p[0] + p[1])

    # multiply
    if opcode == '02':
        memory[pos] = int(p[0] * p[1])

    print("*","@",pos,"=",memory[pos])


def opcode03(p, wr):
    # opcode03 = input
    # one parameter
    # last is write position

    global memory
    global pc
    global opcode
    global mode
    global halt

    pos = p[wr]

    print("*","@",pos,"=",memory[pos])

    value = input("INPUT? ")
    memory[pos] = int(value)

    print("*","@",pos,"=",memory[pos])


def opcode04(p, wr):
    # opcode04 = output
    # one parameter

    global memory
    global pc
    global opcode
    global mode
    global halt

    print("OUTPUT:", p[0])


def opcode0506(p, wr):
    # opcode05 = jump if true
    # opcode06 = jump if false 
    # two parameters

    global memory
    global pc
    global opcode
    global mode
    global halt

    # jump if true
    if opcode == '05':
        if p[0] != 0: pc = p[1]

    # jump if false
    if opcode == '06':
        if p[0] == 0: pc = p[1]


def opcode0708(p, wr):
    # opcode07 = less than
    # opcode08 = equals
    # three parameters

    global memory
    global pc
    global opcode
    global mode
    global halt

    pos = p[wr]

    print("*","@",pos,"=",memory[pos])

    # less than
    if opcode == '07':
        if p[0] < p[1]:
            memory[pos] = 1
        else:
            memory[pos] = 0

    # equal
    if opcode == '08':
        if p[0] == p[1]:
            memory[pos] = 1
        else:
            memory[pos] = 0

    print("*","@", pos,"=",memory[pos])


def opcode99(p, wr):
    # opcode99 = halt
    # no parameters

    global memory
    global pc
    global opcode
    global mode
    global halt

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

# opcode,
# instruction,
# number of parameters,
# write position
table = {
    '01': [ 'ADD',  3, 2 ],
    '02': [ 'MULT', 3, 2 ],
    '03': [ 'IN',   1, 0 ],
    '04': [ 'OUT',  1, None ],
    '05': [ 'JNZ',  2, None ],
    '06': [ 'JZ',   2, None ],
    '07': [ 'LT',   3, 2 ],
    '08': [ 'EQ',   3, 2 ],
    '99': [ 'HALT', 0, None ]
}

while not halt:
    integer = memory[pc]
    print("*", pc, ":", integer)

    opcode = integer % 100
    opcode = "{:02d}".format(opcode)

    # addressing mode as 8 bit mask
    # 0 = positional
    # 1 = immediate

    mode = integer // 100
    mode = "{:08d}".format(mode)
    mode = int(mode, 2)

    # apply opcode write mask
    # write position is treated as immediate
    wr = table[opcode][-1]
    if wr is not None:
        setModeImmediate(wr)
    #print("*", pc, ":", opcode, "{:08b}".format(mode))

    # get parameters
    np = table[opcode][1]
    parameters = getParams()

    # incrememnt program counter
    # jumps in execution can overwrite the program counter
    pc += np + 1
    execute[opcode](parameters, wr)

