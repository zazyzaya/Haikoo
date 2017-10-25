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
                    isNum = False
                else:
                    isNum = True

                if isNum:
                    value = wordsToNum(words[i:]) # only assigns last number / simplifies expressions
                else:                             # that aren't strings
                    while (i < len(words)):
                        value += words[i] + ' '
                        i += 1
                    value = value[1:-1]
                i += 1

                if not isNum:
                    value = value[:-1]

                varNames.append(varName.upper())
                varAddresses.append(len(cmds))
                cmds.append(['VAR', value])

            elif words[i].upper in varNames:
                name = words[i].upper()
                address = varNames.index(words[j].upper())
                cmds.append(['RD', varAddresses[varNames.index(words[j].upper())]])
                
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

def wordsToNum(words):
    currentVal = 0

    subtracting = False
    for word in words:
        word = word.upper()
        if word in wordsForSubtracting:
            subtracting = True
        else:
            subtracting = False

        if word in wordsForValues:
            if subtracting:
                currentVal -= int(wordsForValues.index(word)/2)
            else:
                currentVal += int(wordsForValues.index(word)/2)

        #if word in varNames:   TODO
         #   if subtracting:
                

    return currentVal

code = readFile('helloworld.hai') # sys.argv[1])
haisembly = compile(code)

toStr = ''
for cmd in haisembly:
    toStr += (cmd[0] + '~' + str(cmd[1]) + '`')

with open('out.koo', 'w+') as f:
    f.write(toStr[:-1])