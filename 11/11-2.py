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
        self.write = None
        self.pc = 0
        self.opcode = None
        self.parameters = []
        self.mode = []
        self.halt = False
        self.interactive = interactive
        self.debug = debug
        self.input = inputs
        self.input_c = -1
        self.output = []
        self.output_c = -1
        self.error = "Something went wrong!"
        
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

        try:
            np = self.table[self.opcode][1]
            wr = self.table[self.opcode][-1]
        except:
            # illegal opcodes are caught here first
            message = "Illegal opcode: " + str(self.opcode)
            self.error = message

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
                    self.write = p[wr]
                else:
                    p[i] = self.memory[p[i]]
            elif self.isModeRelative(i):
                resolved = True
                if (i == wr):
                    self.write = p[wr] + self.relative_base
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

        pos = self.write
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


    def pendingInput(self):
        return len(self.input) - self.input_c -1


    def getInteractiveInput(self):
        value = input("INPUT? ")
        self.getInput(value)


    def getInput(self, value):
        self.input.append(value)


    def getInputs(self, list):
        self.input += list


    def opcode03(self):
        # opcode03 = input
        # one parameter
        # last is write position

        pos = self.write
        value = None

        if self.interactive:
            self.getInteractiveInput()

        if self.pendingInput() > 0:
            self.input_c += 1
            value = self.input[self.input_c]
        if value == None:
            # store program counter and pause execution
            self.pc = self.current
            self.pause()
            return

        self.printDebug(["*","@",pos,"=",self.memory[pos]])
        self.memory[pos] = int(value)
        self.printDebug(["*","@",pos,"=",self.memory[pos]])


    def pendingOutput(self):
        return len(self.output) - self.output_c - 1


    def getOutputs(self):
        n = self.pendingOutput()
        if n == 0:
            return []
        self.output_c = len(self.output) - 1
        return self.output[-n:]


    def getOutput(self):
        if self.pendingOutput() == 0:
            return None
        self.output_c += 1
        return self.output[self.output_c]


    def opcode04(self):
        # opcode04 = output
        # one parameter

        self.output.append(self.parameters[0])
        if self.debug:
            n = self.pendingOutput()
            print("OUTPUT:", self.output[-n:])
        if self.interactive:
            print(self.getOutput())


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

        pos = self.write
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

            try:
                # store current pc value
                self.current = self.pc

                # get integer
                integer = self.memory[self.pc]
                self.printDebug(["*",self.pc,":","INT",integer])

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

                # get parameters
                self.getParameters()

                # program counter is incremented based off
                # number of parameters for current opcode
                # jumps in execution can overwrite the program counter
                np = self.table[self.opcode][1]
                self.pc += 1 + np
                self.execute[self.opcode]()

            except:
                print("ERROR", self.error)
                self.halt = True


if __name__ == "__main__":

    import pprint

    heading = 'URDL'
    direction = {
        'U': (0,1),
        'D': (0,-1),
        'R': (1,0),
        'L': (-1,0)
    }

    # robot starts facing UP on panel(0,0)
    index = 0
    dir = heading[index]
    pos = (0,0)

    # panels are tracked by coordinates
    # and contain the color and number of visits
    panels = { pos: [ 1, 0 ] }
    path = []

    min = [ 0, 0 ]
    max = [ 0, 0 ]

    robot = IntCodeProcessor(file="input.txt", debug=False, interactive=False)
    robot.run()
    while not robot.isStopped():

        # find coordinate space
        for i in [ 0, 1 ]:
            if pos[i] < min[i]: min[i] = pos[i]
            if pos[i] > max[i]: max[i] = pos[i]

        p = panels[pos]
        color = p[0]

        print(len(path), dir, pos, p)

        robot.getInput(color)
        robot.unpause()
        outputs = robot.getOutputs()

        # paint
        color = outputs[0]
        panels[pos][0] = color
        panels[pos][1] += 1

        # list of all coordinates visited
        path.append(pos)

        # turn
        turn = outputs[1]
        # rotate left
        if turn == 0:
            index -= 1
            if index < 0:
                index = len(heading)-1
        # rotate right
        if turn == 1:
            index += 1
            if index >= len(heading):
                index = 0

        dir = heading[index]
        point = tuple(map(lambda x, y: x + y, pos, direction[dir]))
        pos = point

        try:
            p = panels[pos]
        except:
            p = { pos: [ 0, 0 ] }
            panels.update(p)


#pprint.pprint(path)
#pprint.pprint(panels)

print(min, max)
w = (max[0] - min[0]) + 1
h = (max[1] - min[1]) + 1
print(w, h, w*h)

# w x h area
area = [[' ' for i in range(w)] for j in range(h)]

# adjust relative positions
for pos in panels:
    x = pos[0]+abs(min[0])
    y = -1 * (pos[1]+abs(min[1])) - 1
    if panels[pos][0] == 1: area[y][x] = '#'

for line in range(h):
    print("".join(area[line]))
