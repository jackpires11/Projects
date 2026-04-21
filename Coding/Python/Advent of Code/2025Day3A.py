#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day3AInputs.txt'
#FILE_NAME = 'Test.txt'

#Open the inputs file for reading.
with open(FILE_NAME) as banks:
    #Stores the joltage as lines are read.
    answer = 0
    
    #For every bank in the set of banks:
    for bank in banks:
        #Stores the highest digit found in the bank.
        tens = 1
        #Stores the position of the highest digit found in the bank.
        position = -1
        #For every single digit number backwards:
        for i in range(9, 1, -1):
            #If this single digit is in this bank (excluding the last digit and the return character):
            if str(i) in bank[:len(bank)-2]:
                #Store this digit as the tens digit in this bank
                tens = i
                #Stores the position of this digit within the bank
                position = bank.index(str(i))
                #print(position)
                #Break out of the loop as the highest digit and position has been found.
                break

        #print(tens)
        #For every single digit number backwards:
        for i in range(9, 0, -1):
            #If this single digit is in the digits remaining from the current found highest digit:
            if str(i) in bank[position + 1:]:
                #Add the combined digits to our final joltage.
                answer += int(str(tens) + str(i))
                #print(answer, i)
                #Break out of the loop as our highest joltage has been found.
                break

#Close the opened file of banks
banks.close()
#Output the answer
print(answer)
