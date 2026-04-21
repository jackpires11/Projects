#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day6AInputs.txt'
#Used for testing inputs.
#FILE_NAME = 'Test5a.txt'

#A function for splitting apart numbers separated by bllank spaces.
def parse(symbols):
    #A flag representing whether or not the next number has been parsed.
    flag = False
    #Stores the string currently being parsed.
    temp = ''
    #Collects all of the parsed strings
    collection = []

    #For every symbols in the string:
    for x in range(len(symbols)):
        #If we have parsed a number and reached an empty space:
        if (symbols[x] == ' ') and (flag == True):
            #Set the flag to false to start parsing a new number.
            flag = False
            #Add this parsed string to the collection of parsed strings.
            collection.append(temp)
            #Set the temporary parsed value to '' for parsing the next string.
            temp = ''

        #If this symbol is not a blank space or end of line character:
        elif symbols[x] != ' ' and symbols[x] != '\n':
            #We have started parsing a number
            flag = True
            temp += symbols[x]

    #If we haven't parsed the last value in the string:
    if temp != '':
        collection.append(temp)
            
    #Return the lower and upper bounds of the range.
    return(collection)

#Used to store the amount of fresh ingredients found.
answer = 0
#Open the inputs file for reading.
with open(FILE_NAME) as problems:
    #Stores the list of horizontal strings
    strings = []
    
    #For every range and ID in the ingredients list:
    for problem in problems:         
        #Temporarily stores this ID range to be sorted into the full list.
        strings.append(parse(problem))

#For every vertical problem in the list of strings:
for problem in range(len(strings[0])):
    #If this is an addition problem:
    if strings[len(strings) - 1][problem] == '+':
        #Contains the answer being calculated for the current vertical problem.
        temp_answer = 0
    
        #For every number within the problem:
        for number in range(len(strings) -2, -1, -1):
            #Calculate the total of this vertical problem.
            temp_answer += int(strings[number][problem])
            
    #This is a multiplication problem:
    else:
        #Stores the currently being calculated answer for the vertical row being checked.
        #1 as multiplying by 0 would invalidate the question.
        temp_answer = 1

        #Multiply every number in the vertical problem (ignoring the mathematical operation):
        for number in range(len(strings) -2, -1, -1):
            #Multiplies to the answer being calculated.
            temp_answer = temp_answer * int(strings[number][problem])

    #Total the answers for each vertical problem
    answer += temp_answer

#Output the answer
print(answer)
