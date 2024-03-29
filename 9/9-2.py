#!/usr/bin/env python3

class IntCodeProcessor(object):

    def __init__(self, inputs = [], interactive = True, debug = False, file = None):

        # opcode table
        # instruction
        # number of parameters
        # write position
        self.table = {
            '01': [ 'ADD',  3, 2 ],
            '02': [ 'MULT', 3, 2 ],
            '03': [ 'IN',   1, 0 ],
            '04': [ 'OUT',  1, None ],
            '05': [ 'JNZ',  2, None ],
            '06': [ 'JZ',   2, None ],
            '07': [ 'LT',   3, 2 ],
            '08': [ 'EQ',   3, 2 ],
            '09': [ 'REL',  1, None ],
            '99': [ 'HALT', 0, None ]
        }

        # execution dispatch
        self.execute = {
            '01': self.opcode0102,
            '02': self.opcode0102,
            '03': self.opcode03,
            '04': self.opcode04,
            '05': self.opcode0506,
            '06': self.opcode0506,
            '07': self.opcode0708,
            '08': self.opcode0708,
            '09': self.opcode09,
            '99': self.opcode99
        }

        # state
        self.memory = [0]*64*1024*1024
        self.status = None
        self.current = None
        self.relative_base = 0
        self.pos = None
        self.pc = 0
        self.opcode = None
        self.parameters = []
        self.mode = []
        self.halt = False
        self.interactive = interactive
        self.debug = debug
        self.inputs = inputs
        self.input = None
        self.output = None
        if file:
            self.readProgram(file)


    def getStatus(self):
        return self.status


    def isStopped(self):
        # None = stopped
        return (self.status == None)


    def isRunning(self):
        # True = running
        return (self.status == True)


    def isWaiting(self):
        # False = waiting
        return (self.status == False)


    def readProgram(self, file):
        # read program into memory as integers
        with open(file) as F:
            for line in F:
                pos = 0
                for i in line.strip().split(','):
                    self.memory[pos] = (int(i))
                    pos += 1


    def setModePositional(self, n):
        self.mode[n] = 0


    def setModeImmediate(self, n):
        self.mode[n] = 1


    def setModeRelative(self, n):
        self.mode[n] = 2


    def getMode(self, n):
        return int(self.mode[n])


    def isModePositional(self, n):
        if self.getMode(n) == 0: return True
        return False


    def isModeImmediate(self, n):
        if self.getMode(n) == 1: return True
        return False


    def isModeRelative(self, n):
        if self.getMode(n) == 2: return True
        return False


    def printDebug(self, array):
        if self.debug:
            string = ""
            for s in array:
                string += str(s) + " "
            print(string[:-1])


    def printInstruction(self, positional = True):

        # print instruction
        instruction = self.table[self.opcode][0]
        np = self.table[self.opcode][1]
        wr = self.table[self.opcode][-1]
        for i, p in enumerate(self.parameters):
            instruction += " "
            if i == wr:
                instruction += "@"
            elif positional and not self.isModeImmediate(i):
                instruction += "@"
            instruction += str(p)
            if (i < (np - 1)): 
                instruction += ","
        self.printDebug(["*",self.pc,":",instruction])


    def getParameters(self):

        np = self.table[self.opcode][1]
        wr = self.table[self.opcode][-1]

        p = []
        for i in range(np):
            p.insert(i, self.memory[self.pc + 1 + i])
        self.parameters = p

        # resolve addressing mode
        # write position is treated as immediate
        mask = "".join([ str(c) for c in self.mode[:np] ])
        if not mask: mask = '*'
        self.printDebug(["*",self.pc,":",self.opcode,mask,p])

        self.printInstruction(True)

        resolved = False
        for i in range(np):
            #print(i, wr, p[i])
            if self.isModePositional(i):
                resolved = True
                if (i == wr):
                    self.pos = p[wr]
                else:
                    p[i] = self.memory[p[i]]
            elif self.isModeRelative(i):
                resolved = True
                if (i == wr):
                    self.pos = p[wr] + self.relative_base
                else:
                    offset = p[i] + self.relative_base
                    p[i] = self.memory[offset]

        if resolved:
            self.printInstruction(False)

        self.parameters = p


    def opcode0102(self):
        # opcode01 = add
        # opcode02 = multiply
        # three parameters
        # last is write position

        wr = self.table[self.opcode][-1]
        pos = self.pos
        self.printDebug(["*","@",pos,"=",self.memory[pos]])

        # add
        if self.opcode == '01':
            self.memory[pos] = int(self.parameters[0])
            self.memory[pos] += int(self.parameters[1])

        # multiply
        elif self.opcode == '02':
            self.memory[pos] = int(self.parameters[0])
            self.memory[pos] *= int(self.parameters[1])

        self.printDebug(["*","@",pos,"=",self.memory[pos]])


    def getInput(self):
        value = input("INPUT? ")
        self.input = value


    def queueInput(self, inputs):
        self.inputs += (inputs)


    def opcode03(self):
        # opcode03 = input
        # one parameter
        # last is write position

        if self.interactive:
            self.getInput()
        else:
            if self.inputs:
                self.input = self.inputs.pop(0)
            else:
                # store program counter and pause execution
                self.pc = self.current
                self.pause()
                return

        wr = self.table[self.opcode][-1]
        pos = self.pos
        self.printDebug(["*","@",pos,"=",self.memory[pos]])
        self.memory[pos] = int(self.input)
        self.printDebug(["*","@",pos,"=",self.memory[pos]])
        self.input = None


    def getOutput(self):
        return self.output


    def opcode04(self):
        # opcode04 = output
        # one parameter

        self.output = self.parameters[0]
        if self.debug:
            print("OUTPUT:", self.output)
        else:
            print(self.output)


    def opcode0506(self):
        # opcode05 = jump if true
        # opcode06 = jump if false 
        # two parameters

        evaluatedTrue = False

        # jump if not zero
        # aka jump if true
        if self.opcode == '05':
            evaluatedTrue = (self.parameters[0] != 0)

        # jump if zero
        # aka jump if false
        elif self.opcode == '06':
            evaluatedTrue = (self.parameters[0] == 0)

        self.printDebug(["*",evaluatedTrue]) 

        # change program counter
        if evaluatedTrue:
            self.pc = self.parameters[1]


    def opcode0708(self):
        # opcode07 = less than
        # opcode08 = equals
        # three parameters

        wr = self.table[self.opcode][-1]
        pos = self.pos
        self.printDebug(["*","@",pos,"=",self.memory[pos]])

        evaluatedTrue = False

        # less than
        if self.opcode == '07':
            evaluatedTrue = (self.parameters[0] < self.parameters[1])

        # equal
        elif self.opcode == '08':
            evaluatedTrue = (self.parameters[0] == self.parameters[1])

        if evaluatedTrue:
            self.memory[pos] = 1
        else:
            self.memory[pos] = 0

        self.printDebug(["*",evaluatedTrue])
        self.printDebug(["*","@", pos,"=",self.memory[pos]])


    def opcode09(self):
        # opcode09 = set relative base
        # one parameter

        self.relative_base += self.parameters[0]


    def opcode99(self):
        # opcode99 = halt
        # no parameters

        self.halt = True
        self.status = None


    def pause(self):
        # pause execution
        self.status = False


    def unpause(self):
        # unpause execution
        self.status = True
        self.run()


    def run(self):

        self.status = True
        while self.status and not self.halt:

            # store current pc value
            self.current = self.pc

            # get integer
            integer = self.memory[self.pc]
            self.printDebug(["*",self.pc,":",integer])

            # get opcode
            self.opcode = integer % 100
            self.opcode = "{:02d}".format(self.opcode)

            # addressing mode as 8 char string
            # 0 = positional
            # 1 = immediate
            # 2 = relative
            self.mode = integer // 100
            self.mode = "{:08d}".format(self.mode)
            self.mode = [ int(c) for c in self.mode[::-1] ]

            # apply opcode write mask
            # write position is treated as immediate
            #print("!", self.pc, ":", self.opcode, self.mode)
            #wr = self.table[self.opcode][-1]
            #if wr is not None:
            #    self.setModeImmediate(wr)
            #print("!", self.pc, ":", self.opcode, self.mode)

            # get parameters
            self.getParameters()

            # program counter is incremented based off
            # number of parameters for current opcode
            # jumps in execution can overwrite the program counter
            np = self.table[self.opcode][1]
            self.pc += 1 + np
            self.execute[self.opcode]()


if __name__ == "__main__":

    import sys

    try:
        file = sys.argv[-1]
        debug = True
        if file.startswith("test"):
            debug = False
        intcode = IntCodeProcessor(file=file, debug=debug)
    except:
        file = "input.txt"
        intcode = IntCodeProcessor(file=file, debug=False, interactive=False, inputs = [ 2 ])

    intcode.run()


