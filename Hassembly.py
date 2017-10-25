import sys

tape = [['HLT', ' ']]
cell = 0

nirvana = {'EQ': 0, 'RV': 1, 'RA': 2, 'TMP': 3}

reservedWords = ['HLT', 'MV' 'CMP', 'ADD', 'SUB', 'OUT', 'IN', 'RD', 'WRT', 'JMP', 'JE', 'STO']

def execute(t=tape):
    tape = t

    cell = 0
    while tape[cell][0] != 'HLT':
        cellHasNotChanged = True

        cmd = tape[cell][0]
        if cmd in reservedWords:
            if tape[cell][1] == 'RV':
                data = nirvana['RV']
            elif tape[cell][1] == 'RA':
                data = nirvana['RA']
            elif tape[cell][1] == 'TMP':
                data = nirvana['TMP']
            else:
                data = tape[cell][1]

            if type(data) == str and data[0] == '&':
                data = tape[int(data[1:])][1]   # Handles pointers
            if cell == len(tape) - 1:
                tape.append(0)
                tape.append(0)
            elif cell == len(tape) - 2:
                tape.append(0)


            if cmd == 'MV':
                nirvana['RA'] = cell
                cell = data
                cellHasNotChanged = False
            elif cmd == 'CMP':
                if nirvana['RV'] == data:
                    nirvana['EQ'] = 1
                else:
                    nirvana['EQ'] = 0
            elif cmd == 'ADD':
                nirvana['RV'] = nirvana['RV'] + data
            elif cmd == 'SUB':
                nirvana['RV'] = nirvana['RV'] - data
            elif cmd == 'OUT':  # may want to change this eventually
                print(str(data), end='')
            elif cmd == 'IN':
                nirvana['RV'] = input()
            elif cmd == 'RD':
                nirvana['RV'] = tape[data][1]
            elif cmd == 'WRT':
                tape[data] = nirvana['RV']
            elif cmd == 'JMP':
                cell = data 
                cellHasNotChanged = False
            elif cmd =='JE':
                if nirvana['EQ'] == 1:
                    cell = data
                    cellHasNotChanged = False
            elif cmd == 'STO':
                nirvana['TMP'] = data

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