#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day6AInputs.txt'
#Used for testing inputs.
#FILE_NAME = 'Test6a.txt'

#A function for splitting apart numbers separated by bllank spaces.
def parse(symbols):
    #Collects all of the parsed strings
    collection = [[] for i in range(len(symbols))]
    #Keeps track of where the last string ended.
    start = 0

    #For every symbol in the string (ignoring the return character):
    for x in range(len(symbols[0])):
        #A flag for keeping track of empty space
        clear = True

        #If this is not the last character in the string:
        #- 1 to account for the return character at the end.
        if (x != (len(symbols[0]) - 1)):
            #For every string in the list:
            for y in range(len(symbols)):
                #If this character is not empty
                if symbols[y][x] != ' ':
                    #This is not the empty column.
                    clear = False
                    #Skip to the next column.
                    break

        #If this was an empty column:
        if clear == True:
            #For every string in the list:
            for y in range(len(symbols)):
                #Append the current string to the collection
                collection[y].append(symbols[y][start:x])
                #Change the starting point for the next string

            start = x + 1

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
        strings.append(problem)

    #Vertically split the strings into their columns of problems.
    strings = parse(strings)

#For every vertical problem in the list of strings:
for problem in range(len(strings[0])):
    #Stores the currently being calculated numbers per column for the vertical row.
    temp_numbers = [''] * len(strings[0][problem])

    #Add every number in the vertical problem (ignoring the mathematical operation):
    for number in range(len(strings) - 1):
        #For every digit in the number:
        for digit in range(len(strings[number][problem])):
            #If this part of the string is a number:
            if strings[number][problem][digit] != ' ':
                #Add this digit to the end of the number
                temp_numbers[digit] += strings[number][problem][digit]

    #If this is an addition problem:
    if ('+' in strings[len(strings) - 1][problem]):
        temp_answer = 0
        
        #For every vertical number calculated:
        for number in temp_numbers:
            #Calculate the total of this vertical problem.
            temp_answer += int(number)
            
    #This is a multiplication problem:
    else:
        #Stores the currently being calculated answer for the vertical row being checked.
        #1 as multiplying by 0 would invalidate the question.
        temp_answer = 1

        #Multiply every number in the vertical problem (ignoring the mathematical operation):
        for number in temp_numbers:
            #Multiplies to the answer being calculated.
            temp_answer = temp_answer * int(number)

    #Total the answers for each vertical problem
    answer += temp_answer

#Output the answer
print(answer)
