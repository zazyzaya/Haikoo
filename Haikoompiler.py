import sys

global lines

varAddresses = []
varNames = []

fluff =             ['THE', 'A', 'AN', 'MAY', 'YOUR', 'MY', 'HIS', 'HER', 'HE', 'SHE', 'IT', 'MUST']
wordsForOut =       ['SPAKE', 'SPOKE', 'SPEAK', 'SAID', 'BELLOWED', 'ANNOUNCED', 'CRIED', 'PROCLAIMED', 'SAY']
wordsForStore =     ['BECOMES', 'BECOME']
wordsForValues =    ['ZERO', 'VOID', 'ONE', 'SINGLE', 'TWO', 'TWICE', 'THREE', 'THRICE', 'FOUR', 'FOUR', 
                     'FIVE', 'FIVE', 'SIX', 'SIX', 'SEVEN', 'SEVEN', 'EIGHT', 'EIGHT', 'NINE', 'NINE'] # Need to think of more words
wordsForAdding =    ['AND', 'WITH', 'TOGETHER']
wordsForSubtracting = ['WITHOUT', 'TAKEN']

def readFile(source):
    with open(source, 'r') as f:
        whole = f.read()

    whole.replace(',', '')
    linesTmp = whole.split('\n')
    
    # TODO handle tabs / nested stuff
    return linesTmp

def compile(code):
    cmds = []
    for line in code:
        data = []
        words = line.split(' ')
        foundKeyword = False
        i = 0
        timeToBreak = False
        while (i < len(words)):
            word = words[i]
            if words[i].upper() in wordsForOut:   # OUT / PRINT
                timeToBreak = True
                inWord = False
                j = i
                while (j < len(words)):
                    if (words[j][0] == '"' and inWord == False):
                        inWord = True
                        cmds.append(['OUT', words[i]])
                    elif (words[j][-1] == '"' and inWord == True):
                        inWord = False
                        cmds.append(['OUT', words[i]])
                        cmds.append(['OUT', '\n'])
                        break
                    elif (inWord):
                        cmds.append(['OUT', words[i]])
                    elif words[j].upper() in varNames:
                        cmds.append(['RD', varAddresses[varNames.index(words[j].upper())]])
                        cmds.append(['OUT', 'RV'])
                        cmds.append(['OUT', '\n'])
                    j += 1
            
            elif words[i].upper() in wordsForStore:   # Declare a variable

                varName = ''
                j = 0
                while(j < len(words) and words[j].upper() not in wordsForStore):
                    if words[j].upper() not in fluff:
                        varName += words[j] + ' '
                    j += 1
                varName = varName[:-1] # trim trailing space

                i += 1
                value = '' 
                if words[i][0] == '"':
                    isStr = True
                else:
                    isStr = False

                if not isStr:
                    commands = getValueOf(words[i:], varName) 
                else:                             
                    while (i < len(words)):
                        value += words[i] + ' '
                        i += 1
                    value = value[1:-1]
                i += 1

                if isStr:
                    value = value[:-1]

                if varName not in varNames:
                    if isStr:
                        cmds.append(['RD', value])
                        varNames.append(varName.upper())
                        varAddresses.append(len(cmds))
                        cmds.append(['WRT', len(cmds)])
                    else:
                        varNames.append(varName.upper())
                        addr = len(cmds)
                        varAddresses.append(addr)
                        cmds.append('WRT', addr)
                        cmds += commands
                
                else:
                    if isStr:
                        cmds.append(['RD', value])
                        cmds.append(['WRT', addressOf(varName)])
                    else:
                        cmds += commands
                        
            elif words[i].upper in varNames:    # If a variable is in the line
                name = words[i].upper()
                address = varNames.index(words[j].upper())
                cmds.append(['RD', addressOf(name)])
                
                i += 1
                while (i < len(words)):
                    if words[i] in wordsForStore:   # assign new value
                        value = '' 
                        isNum = not words[i][0] == '"'
                        #if isNum:  TODO
                        #    value = 
                        
            i += 1
    cmds.append(['HLT', ' '])
    return cmds

def addressOf(varName):
    global varAddresses, varNames
    return varAddresses[varNames.index(varName.upper())]

def getValueOf(words, varName):
    commands = []
    addr = addressOf(varName)
    global varNames

    subtracting = False
    for word in words:
        word = word.upper()
        if word in wordsForSubtracting:
            subtracting = True
        else:
            subtracting = False

        if word in wordsForValues:
            commands.append(['RD', addr])
            if subtracting:
                commands.append('SUB', int(wordsForValues.index(word)/2))
            else:
                commands.append('ADD', int(wordsForValues.index(word)/2))
            commands.append('WRT', addr)

        if word in varNames:
            commands.append(['RD', addr])
            if subtracting:
                commands.append(['SUB', '&' + addressOf(word)])
            else:
                commands.append(['ADD', '&' + addressOf(word)])
                
            commands.append(['WRT', addr])
            
    return commands

code = readFile('helloworld.hai') # sys.argv[1])
haisembly = compile(code)

toStr = ''
for cmd in haisembly:
    toStr += (cmd[0] + '~' + str(cmd[1]) + '`')

with open('out.koo', 'w+') as f:
    f.write(toStr[:-1])