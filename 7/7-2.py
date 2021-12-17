#!/usr/bin/env python3

class IntCodeProcessor(object):

    def __init__(self, inputs = [], interactive = False, debug = False, file = None):

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
            '99': self.opcode99
        }

        # state
        self.memory = []
        self.status = None
        self.current = None
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
                for i in line.strip().split(','):
                    self.memory.append(int(i))


    def setModePositional(self, n):
        self.mode &= ~(1<<n)


    def setModeImmediate(self, n):
        self.mode |= (1<<n)


    def getMode(self, n):
        return (self.mode & (1<<n))


    def isModeImmediate(self, n):
        if self.getMode(n) == 1: return True
        return False


    def isModePositional(self, n):
        if self.getMode(n) == 0: return True
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
            if (i == wr):
                instruction += "@"
            if positional and self.isModePositional(i):
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
        mask = "{:0{w}b}".format(self.mode, w=np)
        mask = mask[::-1]
        self.printDebug(["*",self.pc,":",self.opcode,mask,p])

        self.printInstruction(True)

        resolved = False
        for i in range(np):
            if self.isModePositional(i):
                resolved = True
                p[i] = self.memory[p[i]]

        if resolved:
            self.printInstruction(False)

        self.parameters = p


    def opcode0102(self):
        # opcode01 = add
        # opcode02 = multiply
        # three parameters
        # last is write position

        wr = self.table[self.opcode][-1]
        pos = self.parameters[wr]
        self.printDebug(["*","@",pos,"=",self.memory[pos]])

        # add
        if self.opcode == '01':
            self.memory[pos] = int(self.parameters[0])
            self.memory[pos] += int(self.parameters[1])

        # multiply
        if self.opcode == '02':
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
        pos = self.parameters[wr]
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
        if self.interactive:
            print("OUTPUT:", self.output)


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
        if self.opcode == '06':
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
        pos = self.parameters[wr]
        self.printDebug(["*","@",pos,"=",self.memory[pos]])

        evaluatedTrue = False

        # less than
        if self.opcode == '07':
            evaluatedTrue = (self.parameters[0] < self.parameters[1])

        # equal
        if self.opcode == '08':
            evaluatedTrue = (self.parameters[0] == self.parameters[1])

        if evaluatedTrue:
            self.memory[pos] = 1
        else:
            self.memory[pos] = 0

        self.printDebug(["*",evaluatedTrue])
        self.printDebug(["*","@", pos,"=",self.memory[pos]])


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

            # get addressing mode as 8 bit mask
            # 0 = positional
            # 1 = immediate
            self.mode = integer // 100
            self.mode = "{:08d}".format(self.mode)
            self.mode = int(self.mode, 2)

            # apply opcode write mask
            # write position is treated as immediate
            wr = self.table[self.opcode][-1]
            if wr is not None:
                self.setModeImmediate(wr)
            #print("*", pc, ":", opcode, "{:08b}".format(mode))

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
        file = sys.argv[1]
    except:
        file = "test.8"
        file = "test.9"
        file = "input.txt"
    
    def permute(s):
        if (len(s)==0): return [ ]
        if (len(s)==1): return [ s ]
        permutations = [ ]
        for i, c in enumerate(s):
            permutations += [ c + p for p in permute(s[:i]+s[i+1:]) ]
        return permutations

    permutations = [ "98765" ] # test.8 = "98765"
    permutations = [ "97856" ] # test.9 = "97856"

    st = '56789'
    permutations = permute(st)

    test = {}
    for p in permutations:

        # initialize thrusters
        thrusters = []
        for i, n in enumerate(p):
            thrusters.append(IntCodeProcessor(file=file, inputs=[n]))
            thrusters[i].run()

        # all thrusters are now waiting for feedback
        # feedback 0 starts the loop
        feedback = 0
        done = 0
        while (done < len(thrusters)):

            for i, n in enumerate(p):
                thrusters[i].queueInput([feedback])
                thrusters[i].unpause()
                feedback = thrusters[i].getOutput()
                print(p,i,n,feedback)

            done = sum(1 for t in thrusters if t.isStopped())
            
        test[p] = feedback

    for t in sorted(test.items(), key=lambda x:x[1]):
        print(t)

