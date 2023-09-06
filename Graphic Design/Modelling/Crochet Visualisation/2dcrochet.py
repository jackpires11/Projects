def row_Parser(pattern):
        new_pattern = ''
        current_row = ''
        for symbol in pattern:
                if symbol != str('\n'):
                        current_row += symbol
                else:
                        new_pattern += current_row[::-1] + '\n'
                        current_row = ''
        return(new_pattern)

def crochet_Parser(old_crochets, crochets, done):
        new_crochets = str('')
        while len(crochets) > 0:
                concat_string = str(crochets[0])
                if concat_string == 'c':
                        new_crochets += '_'
                        crochets = crochets[1:]
                else:
                        concat_string += str(crochets[1])
                        if concat_string == 'dc':
                                new_crochets += '#'
                                crochets = crochets[2:]
                        elif concat_string == 'tc':
                                new_crochets += '||'
                                crochets = crochets[2:]
                        else:
                                concat_string += str(crochets[2])
                                if concat_string == 'end':
                                        done = True
                                        crochets = ''
                                else:
                                        concat_string += str(crochets[3])
                                        if concat_string == 'turn':
                                                old_crochets += new_crochets + '\n'
                                                old_crochets = row_Parser(old_crochets)
                                                new_crochets = ''
                                                crochets = crochets[4:]
        old_crochets += new_crochets                                        
        return(old_crochets, done)

finished = False
current = str('')
while finished == False:
        next_crochets = input('Please input the next row: \n')
        (current, finished) = crochet_Parser(current, next_crochets, finished)
        print(current, '\n')
