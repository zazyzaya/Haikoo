import sys

tape = [['HLT', ' ']]
cell = 0

nirvanaDict = {'EQ': 0, 'RV': 1, 'RA': 2}
nirvana = [0, 0, 0]

reservedWords = ['HLT', 'MV' 'CMP', 'ADD', 'SUB', 'OUT', 'IN', 'RD', 'WRT', 'JMP', 'JE', 'VAR']

def execute(t=tape):
    tape = t

    cell = 0
    while tape[cell][0] != 'HLT':
        cellHasNotChanged = True

        cmd = tape[cell][0]
        if tape[cell][1] == 'RV':
            data = nirvana[nirvanaDict['RV']]
        elif tape[cell][1] == 'RA':
            data = nirvana[nirvanaDict['RA']]
        else:
            data = tape[cell][1]

        if cell == len(tape) - 1:
            tape.append(0)
            tape.append(0)
        elif cell == len(tape) - 2:
            tape.append(0)


        if cmd == 'MV':
            nirvana[nirvanaDict['RA']] = cell
            cell = data
            cellHasNotChanged = False
        elif cmd == 'CMP':
            if tape[cell + 1][1] == data:
                nirvana[nirvanaDict['EQ']] = 1
            else:
                nirvana[nirvanaDict['EQ']] = 0
        elif cmd == 'ADD':
            nirvana[nirvanaDict['RV']] = tape[cell + 1][1] + data
        elif cmd == 'SUB':
            nirvana[nirvanaDict['RV']] = tape[cell + 1][1] + data
        elif cmd == 'OUT':  # may want to change this eventually
            print(str(data), end='')
        elif cmd == 'IN':
            nirvana[nirvanaDict['RV']] = input()
        elif cmd == 'RD':
            nirvana[nirvanaDict['RV']] = tape[int(data)]
        elif cmd == 'WRT':
            tape[data] = nirvana[nirvanaDict['RV']]
        elif cmd == 'JMP':
            cell = data 
            cellHasNotChanged = False
        elif cmd =='JE':
            if tape[nirvana[nirvanaDict['EQ']]] == 1:
                cell = data
                cellHasNotChanged = False
        elif cmd == 'VAR':
            tape[nirvana[nirvanaDict['RV']]] = data
        if cellHasNotChanged:
            cell += 1

def readIn():
    global tape
    rawFile = 'out.koo' #sys.argv[0]
    with open(rawFile, 'r') as f:
        rawText = f.read()

    lines = rawText.split('`')
    tape = []
    for line in lines:
        tape.append([line.split('~')[0], line.split('~')[1]])

    return tape

readIn()
execute(tape)