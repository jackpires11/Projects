#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day8AInputs.txt'
#Used for testing inputs.
#FILE_NAME = 'Test8a.txt'
#A constant used to check how many shortest paths to calculate.
AMOUNT = 1000
#A constant used to calculate how many lengths of circuit to multiply together.
CIRCUITS = 3

#Separates coordinates into x, y and z via comma separated values:
def parse(coordinates):
    #Keeps track of the coordinate so far
    coordinate = ''
    #Stores the three obtained coordinates.
    coordinate_list = []
    
    #For every character in the string:
    for x in coordinates:
        #If this is not the end of the coordinate:
        if x != ',' and x != '\n':
            coordinate += x

        #If this is the end of the coordinate
        else:
            #Add this coordinate to the list
            coordinate_list.append(int(coordinate))
            #Reset the coordinate to obtain the next one.
            coordinate = ''

    #If this is the last entry in the file, and so does not terminate with a \n character:
    if coordinate != '':
        #Add this coordinate to the list.
        coordinate_list.append(int(coordinate))

    #Return the list of obtained coordinates
    return(coordinate_list)

#Calculates the distance between two points
def calcDistance(first, second):
    #Keeps track of the distance so far.
    distance = 0
    #For x, y, z:
    for i in range(3):
        #Find the distance between the two points on that axis
        length = abs(first[i] - second[i])
        #Multiply them together and add them to the total distance.
        distance += length * length

    #Works under the formular that the distance between two 3D points is:

    #x^2 + z^2 + y^2

    #A larger number will always square root to a larger number, so comparisons
    #can simply be made on squares of distances.
        
    #Returns the square of the distance (saves on square root calculating)
    return(distance)

#Used to store the amount of fresh ingredients found.
answer = 1
#Open the inputs file for reading.
with open(FILE_NAME) as coords:
    #Stores the list of horizontal strings
    positions = []
    
    #For every range and ID in the ingredients list:
    for coord in coords:
        #Temporarily stores this ID range to be sorted into the full list.
        positions.append(parse(coord))

#Tracks all of the distances between every point in the list.
distances = []
#Used to keep track of running through every position in the list
x = 0
#For every position in the list, except the final position.
while (x < (len(positions) - 1)):
    #Keeps track of the positions being checked against the current one.
    y = x + 1
    #For every other further position in the list of positions:
    while (y < len(positions)):
        #Calculate the distance between the two points.
        distances.append([calcDistance(positions[x], positions[y]), positions[x], positions[y]])
        #Increase the pointer to check the distance of the next point.
        y += 1

    #Increase the pointer to check the distance of positions against the next point.
    x += 1

#Sort the list of distances by distance.        
distances.sort()

#Used to keep track of the circuits calculated.
circuits = []
#A flag to keep track of the index of positions already in a circuit
index = -1
#For the first AMOUNT connections made:
for x in range(AMOUNT):
    #A flag used to check if either position is already in a circuit
    found = False
    
    #If this is the first connection:
    if circuits == []:
        #Append the coordinates to this circuit.
        circuits.append([distances[x][1]])
        circuits[0].append(distances[x][2])

    #For every circuit already made:
    for circuit in range(len(circuits)):
        #If the first coordinate is in this circuit:
        if distances[x][1] in circuits[circuit]:
            #Updates the flag as a position is in a circuit
            found = True
            
            #If the second coordinate is not also in this circuit:
            if distances[x][2] not in circuits[circuit]:
                #If this is the first coordinate to be found in a circuit:
                if index == -1:
                    #Set this circuits index as a reference for later.
                    index = circuit

                #The other coordinate is in another circuit:
                else:
                    #Connect these two circuits
                    circuits[index].extend(circuits[circuit])
                    #Remove the now duplicate circuit
                    circuits.pop(circuit)
                    #Reset the index to show that a connection has been made
                    index = -1
                    #Exit the loop and check the next connection.
                    break

            #If the second coordinate was in this circuit, the loop can be skipped as they
            #Are both already present and accounted for
            else:
                break

        #Else if the second coordinate is in this circuit:
        elif distances[x][2] in circuits[circuit]:
            found = True
            
            #If this is the first coordinate to be found in a circuit:
            if index == -1:
                #Set this circuits index as a flag for later.
                index = circuit

            #The other coordinate is in another circuit:
            else:
                #Connect these two circuits
                circuits[index].extend(circuits[circuit])
                #Remove the now duplicate circuit
                circuits.pop(circuit)
                #Reset the index to show that a connection has been made
                index = -1
                #Exit the loop to check the next connection.
                break

    #If a connection was not made and a position is already in a circuit:
    if index != -1:
        #If the first position is in this circuit:
        if distances[x][1] in circuits[index]:
            #Append the second position.
            circuits[index].append(distances[x][2])

        #The second position is in this circuit:
        else:
            #Append the first position.
            circuits[index].append(distances[x][1])

        #Reset the index for the next check.
        index = -1

    #Else if neither coordinate is in a circuit already:
    elif found == False:
        #Create a new circuit with these two positions.
        circuits.append([distances[x][1]])
        circuits[len(circuits)-1].append(distances[x][2])

#Sort the list of circuits by length of circuit in descending order.
circuits.sort(key=len, reverse=True)
#For the amount of circuits to multiply together:
for i in range(CIRCUITS):
    #Multiply the length of the circuit by the running total
    answer = answer * len(circuits[i])

#Output the answer
print(answer)
