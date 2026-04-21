#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day4AInputs.txt'
#Used for testing inputs.
#FILE_NAME = 'Test.txt'
#Constant for how far adjacency applies to rolls of paper.
REACH = 1
#Constant for how many rolls of paper adjacent is too many.
#It is equal to 1 more than the fewer allowed to account for
#Including the roll itself in the adjacency check.
MIN = 5

#Checks if the position being checked is around the edge of the room
#And returns suitable offsets to account for it:
def check_Edges(x, y, space):
    #The default values for a position not at the edge
    x_offset = [0,1]
    y_offset = [0,1]
    
    #If the reach extends beyond the top of the room:
    if y - REACH < 0:
        #The vertical offset is correctly adjusted
        y_offset[0] = abs(y - REACH)
    #If the reach extends beyond the bottom of the room:
    if y + REACH >= len(space):
        y_offset[1] += (y + REACH) - len(space)
    #If the reach extends beyond the left of the room:
    if x - REACH < 0:
        #The horizontal offset is correctly adjusted
        x_offset[0] = abs(x - REACH)
    #If the reach extends beyond the right of the room:
    if x + REACH >= len(space[y]):
        x_offset[1] += (x + REACH) - len(space[y])

    #Returns the offsets needed for this section.
    return([x_offset, y_offset])

#Finds the section to check for adjacency
def find_Section(space, place, width):
    #print(space, place, width)
    #For every line in the space:
    for line in range(len(space)):
        #Slice the space into the correct section.
        space[line] = space[line][place - REACH + width[0]:place + REACH + width[1]]

    #Returns the section to be checked for adjacency.
    return(space)

def check_Adjacency(section):
    #Counts how many rolls of paper are in this section
    count = 0
    
    #For every row in the section:
    for x in range(len(section)):
        #For every position within the row:
        for y in range(len(section[x])):
            #If this is a roll of paper:
            if section[x][y] == '@':
                #Increment the counter
                count += 1

    #If the count is less than the amount not allowed:
    if count < MIN:
        #This roll of paper is valid
        return(True)
    #The count is more than the amount allowed:
    else:
        return(False)

#Checks the rows of a given room for rolls of paper.
def check_Rows(room):
    #The total of suitable rolls of paper
    total = 0
    #For every row in the room:
    for row in range(len(room)):
        #For every position in the row:
        for position in range(len(room[row])):
            #If there is a roll of paper at this position:
            if room[row][position] == '@':
                #Checks for edge cases.
                offsets = check_Edges(position, row, room) 
                #Obtain the section we need to check.
                section = find_Section(room[row-REACH+offsets[1][0]:row+REACH+offsets[1][1]], position, offsets[0])
                
                #If the square of adjacent positions (based on REACH constant) contains less
                #adjacent rolls than the max allowed:
                if (check_Adjacency(section)):
                    #Increment the amount of valid rolls of paper.
                    total += 1

    #Return the amount of valid rolls of paper.
    return(total)

#Open the inputs file for reading.
with open(FILE_NAME) as room:
    #Stores the rows of coordinates for the room.
    rows = []
    
    #For every bank in the set of banks:
    for positions in room:      
        #Add this row of positions to the overall row layout of the room.
        #The - 1 accounts for the return character at the end of each row.
        rows.append(positions[:len(positions) - 1])

#Close the opened file of banks
room.close()

#Checks each roll of paper in the room and adds them to a running total if they have
#less than the minimum adjacent rolls disallowed.
answer = check_Rows(rows)

#Output the answer
print(answer)
