#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day7AInputs.txt'
#Used for testing inputs.
#FILE_NAME = 'Test7a.txt'

#Calculates the total of a list:
def calc_Total(amount):
    #Used to store the running total.
    beams = 0
    #For every number in the list:
    for beam in amount:
        #Add up the total
        beams += beam

    #Return the total
    return(beams)

#Calculate the amount of splits that occur for a beam at a given location in a manfold.
def splits(row, indices, overlaps):
    #print(row, index, count)
    #If this is the first row.
    if (indices == []):
        #Find where the beam begins.
        start = row.find('S')
        #Check the following row from this position.
        return([start], [1])

    #For every beam:
    i = 0
    while i < len(indices):
        #If this is a split:
        if (row[indices[i]] == '^'):

            #If it's not at the end of the row:
            if indices[i] != (len(row) - 1):
                #Note the beam one to the right and carry on its overlap.
                indices.insert(i+1, indices[i] + 1)
                overlaps.insert(i+1, overlaps[i])
            
            #print(row, index, count)
            #If the split is not at the start of the row:
            if indices[i] != 0:
                #If a beam already exists one to the left of this index:
                if indices[i] - 1 in indices:
                    #Adds the overlaps for this beam to the already existing beam.
                    overlaps[i - 1] += overlaps[i]
                    #Remove the current beam from the list of stored beams
                    #It is already accounted for.
                    overlaps.pop(i)
                    indices.pop(i)

                #A beam does not exist one to the left:
                else:
                    #Update it to be one to the left.
                    indices[i] = indices[i] - 1
                    #The overlap remains the same; no need to update.
                    #Increase the index to skip over the created new indices.
                    i += 1

        #If this is not a split
        else:
            #If this is not the only beam and it is not the first beam
            if (len(indices) > 1) and (i != 0):
                #Check if the previous beam split to here:
                if indices[i - 1] == indices[i]:
                    #Add these beams to the beams already stored here.
                    overlaps[i - 1] += overlaps[i]
                    #Remove these beams from the list.
                    overlaps.pop(i)
                    indices.pop(i)
                    #Balance out the counter as the next beam is now at this index.
                    i -= 1

                #This is the only beam here, so do nothing
               
        #Check the next beam.
        i += 1

    return(indices, overlaps)

#Open the inputs file for reading.
with open(FILE_NAME) as manifolds:
    #Stores the list of overlaps and indices for beams
    indices = []
    overlaps = []
    
    #For every string in the manifold:
    for manifold in manifolds:
        indices, overlaps = splits(manifold, indices, overlaps) 

#Calculate the total amount of beams.
answer = calc_Total(overlaps)
#Output the answer.
print(answer)
