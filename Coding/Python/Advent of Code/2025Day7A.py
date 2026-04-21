#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day7AInputs.txt'
#Used for testing inputs.
#FILE_NAME = 'Test7a.txt'

#Calculate the amount of splits that occur for a beam at a given location in a manfold.
def splits(row, index, count):
    #print(row, index, count)
    #If this is the first row.
    if (row == 0):
        #Find where the beam begins.
        start = strings[row].find('S')
        #Check the following row from this position.
        count = splits(1, start, count)

    #If you have traversed all the rows:
    elif (row > len(strings) - 1):
        return(count)

    #Else if this is not a split:
    elif (strings[row][index] != '^'):
        #If this has not been traversed already:
        if (strings[row][index] != '|'):
            #Slice the string to set this as a beam
            strings[row] = strings[row][:index] + '|' + strings[row][(index + 1):]
            #Check the next row down at this index.
            count = splits(row + 1, index, count)
            #Return the counter when recursing back out.

    #If this is a split:
    else:
        #Increment the counter.
        count += 1

        #If the split is not at the start of the row:
        if index != 0:
            #If the space to the left has not been traversed:
            if strings[row][index - 1] != '|':
                #Continue checking from one to the left.
                count = splits(row, index - 1, count)

            #If this split is not at the end of the row.
            if index != (len(strings[row]) - 1):
                #If the space to the right has not been traversed:
                if strings[row][index + 1] != '|':
                    #Continue checking from one to the right.
                    count = splits(row, index + 1, count)

            #No need for an else, as the split is at the end and the left has already been
            #checked.

        #Else the split is at the start:
        else:
            #Check right.
            count = splits(row, index + 1, count)

    return(count)

#Used to store the amount of fresh ingredients found.
answer = 0
#Open the inputs file for reading.
with open(FILE_NAME) as manifolds:
    #Stores the list of horizontal strings
    strings = []
    
    #For every range and ID in the ingredients list:
    for manifold in manifolds:
        #Temporarily stores this ID range to be sorted into the full list.
        strings.append(manifold)

answer = splits(0, None, answer)
print(answer)



