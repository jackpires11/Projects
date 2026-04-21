#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day5AInputs.txt'
#Used for testing inputs.
#FILE_NAME = 'Test5a.txt'

#A function for splitting apart provided ranges.
def parse(ranges):    
    #Iterates over the string
    for x in range(0, len(ranges)):
        #If we have reached the hyphen:
        if ranges[x] == '-':
            #Slice the string into the two halves
            lower = int(ranges[:x])
            #If this is not the last range:
            if ranges[len(ranges)-1] == '\n':
                #Set the upper range - the \n character.
                upper = int(ranges[(x+1):len(ranges) - 1])

            #If this is the last range
            else:
                #Set the upper range to the end of the string
                upper = int(ranges[(x+1):])

            #Return the lower and upper bounds of the range.
            return([lower, upper])

    #Return a 0.
    #THIS SHOULD NOT BE REACHED AS WE ASSUME VALID INPUTS ONLY.
    return(0)

#A recursive function for inserting a list into another list sorted by lower bound.
def insertSorted(perm, temp):
    #print(perm, temp)
    #Base case. If the main list is empty, send back the temporary list to be inserted.
    if len(perm) == 0:
        return([temp])

    #Used to store the new, sorted list.
    #If the middle of the list is less than the temporary list.
    if perm[len(perm)//2][0] < temp[0]:
        #Retry to insert the new list into the later half of the list.
        #Append this to the first half of the list.
        new_list = perm[:(len(perm) // 2) + 1]
        #print(new_list)
        new_list.extend(insertSorted(perm[(len(perm) // 2) + 1:], temp))
        #+ 1 to make sure the middle of the list is not included in the next check.
        #Return this newly sorted list.
        return(new_list)

    #If the middle of the list is greater than the temporary list:
    elif perm[len(perm)//2][0] > temp[0]:
        #Retry to insert the new list into the first half of the list.
        #Append the second half of the list to this.
        new_list = insertSorted(perm[:(len(perm)//2)], temp)
        new_list.extend(perm[(len(perm)//2):])
        return(new_list)

    #If the middle of the list is equal to the temporary list:
    else:
        #Generates a new list and extends it to contain the temporary list in the center.
        new_list = perm[:len(perm) // 2]
        new_list.extend([temp])
        new_list.extend(perm[len(perm) // 2:])
        #Returns the list with the temporary list in the middle.
        return(new_list)

#Optimise the ranges with a list by condensing overlap:
def optimiseRanges(ranges):
    #Counter for running through the list of ranges
    i = 0
    #For every range in the range (ignoring the last value as it has no following ranges):
    while i < (len(ranges) - 1):
        #A flag used to check whether or not the list of ranges has been condensed this check.
        condensed = False
        
        #If the upper range of the first is greater than, equal to
        #or consecutive to the lower range of the following:
        if ranges[i][1] >= (ranges[i+1][0] - 1):
            #If the upper range of the following range is greater than the current upper range:
            if ranges[i][1] < ranges[i+1][1]:
                #Set the upper bound of this range to the upper bound of the following range.
                ranges[i][1] = ranges[i+1][1]
                #Remove the following range - it is now included in the previous range.
                ranges.pop(i+1)

            #If the upper range of this range is greater than or equal to
            #the following upper range:
            else:
                #The following range is already encompassed by the current one - remove it.
                ranges.pop(i+1)

            #A range has been removed this check.
            condensed = True

        #If a range was not condensed this check:
        if condensed == False:
            #Start condensing the following range.
            i += 1

    #Return the condensed set of ranges.
    return(ranges)

#Checks if a number is within a set of ranges:
def checkFresh(number, ranges):
    #For every range of ids in the range:
    for valid_ids in ranges:
        #print(number, valid_ids)
        #If the number is within the range:
        if (number > valid_ids[0]) and (number < valid_ids[1]):
            #Return True
            return(True)

    #Return False
    return(False)

#Used to store the amount of fresh ingredients found.
answer = 0
#Open the inputs file for reading.
with open(FILE_NAME) as ingredients:
    #Stores the valid ID ranges.
    valid_ranges = []
    #Stores the list of IDs on hand.
    ingredient_IDs = []

    #A flag used to check when the file switches from valid_id ranges to ingredient IDs.
    v_ranges = True
    #For every range and ID in the ingredients list:
    for IDs in ingredients:
        #If we are parsing the ID ranges:
        if v_ranges == True:
            #If we have reached the end of the valid ID ranges:
            if IDs == '\n':
                #Optimise the ranges for overlap
                valid_ranges = optimiseRanges(valid_ranges)
                #The ranges have been found and parsed; add the remaining IDs to the
                #range needing to be checked.
                v_ranges = False
                continue
            
            #Temporarily stores this ID range to be sorted into the full list.
            temp_range = parse(IDs)
            #If there are no ranges in the list yet:
            if len(valid_ranges) == 0:
                #Initialise the list.
                valid_ranges.append(temp_range)

            #If there are ranges in the list:
            else:
                #Inserts the range into the list sorted from lowest to highest lower bound.
                valid_ranges = insertSorted(valid_ranges, temp_range)

        #If we are parsing the ingredient IDs on hand:
        else:
            #If this is not the last entry:
            if IDs[len(IDs) - 1] == '\n':
                #Add this ID to the list of available IDs to be checked, - the \n character.
                ingredient_IDs.append(int(IDs[:len(IDs)-1]))

            #If this is the last entry:
            else:
                ingredient_IDs.append(int(IDs))

#Close the opened file of ingredients IDs.
ingredients.close()

#print(valid_ranges)

#For every ingredient ID in the list:
for ID in ingredient_IDs:
    #If the ID is in the list of valid ranges:
    if checkFresh(ID, valid_ranges):
        answer += 1

#Output the answer
print(answer)
