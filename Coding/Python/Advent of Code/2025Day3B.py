#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day4AInputs.txt'
#FILE_NAME = 'Test.txt'

#Open the inputs file for reading.
with open(FILE_NAME) as room:
    #Stores the rows of coordinates for the room.
    row = []
    
    #For every bank in the set of banks:
    for positions in room:
        #Add this row of positions to the overall row layout of the room.
        row += positions

    print(row)

#Close the opened file of banks
room.close()

#Stores how many rolls of paper the forklifts can reach.
answer = 0
#Output the answer
print(answer)
