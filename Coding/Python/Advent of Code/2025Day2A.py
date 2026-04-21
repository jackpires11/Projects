#The library for opening .csv files.
import csv
#Used for the floor function.
import math

#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day2AInputs.txt'

#A function for splitting apart provided ranges.
def parse(ranges):    
    #Iterates over the string
    for x in range(0, len(ranges)):
        #If we have reached the hyphen:
        if ranges[x] == '-':
            #Slice the string into the two halves
            lower = ranges[:x]
            upper = ranges[(x+1):]
            return(lower, upper)

#The function used to calculate the lowest invalid value within this bounadary
def calcLower(boundary):
    #If the length of the lower bound is even:
    if ((len(boundary) % 2) == 0):
        #If the first half of the number is greater than or equal to the second half:
        if int(boundary[:len(boundary)//2]) >= int(boundary[len(boundary)//2:]):
            return(boundary[:len(boundary)//2] * 2)
        #If the second half of the number is greater than the first half:
        else:
            #Add one to that repeating number.
            return(str(int(boundary[:len(boundary)//2]) + 1) * 2)
            
    #If the length of the lower bound is odd:
    else:
        return(('1' + ('0' * (math.floor(len(boundary)/ 2)))) * 2)

#The function used to calculate the highest invalid value within this boundary.
def calcUpper(boundary):
    #If the length of the upper bound is even:
    if ((len(boundary) % 2) == 0):
        #If the first half of the number is less than or equal to the second half:
        if int(boundary[:len(boundary)//2]) <= int(boundary[len(boundary)//2:]):
            return(str(boundary[:len(boundary)//2]) * 2)
        #If the second half of the number is less than the first half:
        else:
            #Take one from that repeating number.
            return(str(int(boundary[:len(boundary)//2]) - 1) * 2)
            
    #If the length of the upper bound is odd:
    else:
        #Return 9 * one less than the current length.
        return('9' * (len(boundary) - 1))

    
#A function to calculate the invalid number boundaries and total them.
def calcBoundTotals(low, high):
    #Calculate the upper and lower boundaries respective to invalid values.
    low = calcLower(low)
    high = calcUpper(high)

    #If the range is backwards:
    if int(high) < int(low):
        #This range is invalid; add nothing. (This should NEVER be invoked!
        #We're assuming only valid inputs!)
        return(0)

    #Used in case of recursion.
    total = 0
    #If the lower boundary is a different length to the upper boundary:
    if len(low) < len(high):
        #Calculate the total of the next set based on number length.
        total += calcBoundTotals('1' + ('0' * (len(low) + 1)), high)
        #Set the upper bound to the upper bound of this number length.
        high = '9' * len(low)

    #Calculate the first repeated number + the last repeated number.
    calc = int(low) + int(high)
    
    #Used to calculate the total amount of numbers in the series.
    initial = int(low[:len(low)//2])
    final = int(high[:len(high)//2])
    #Calculate how many numbers are in the series.
    amount = (final - initial) + 1

    #print(low, high)
    #print(initial, final, amount)

    #Calculate how many times to multiply the repeated sum by.
    multiplier = amount/2
    
    #Return the total of the series according to the formula:
    #(n[0] + n[n-1]) * (n/2)
    print(int(total + (calc * multiplier)))
    return(int(total + (calc * multiplier)))    

#Used for keeping track of the total of invalid inputs.
answer = 0

#Open the inputs file for reading.
with open(FILE_NAME, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',', quotechar='|')

    #Iterates over the rows of inputs in the file.    
    for values in reader:
        #Prints the list of ranges obtained from the csv file
        print(values)

        #Iterates over each range within the selection.
        for span in values:
            #Prints the current range in the selection.
            #print(span)

            #Parse the range into its upper and lower bounds.
            lower, upper = parse(span)
            #print(lower, upper)

            #If the boundaries are both the same odd length.
            if ((len(lower) % 2) == 1) and (len(lower) == len(upper)):
                #Skip this boundary as there are no invalid values.
                continue
            
            #Calculate the boundaries of invalid numbers and total them.
            answer += calcBoundTotals(lower, upper)
          
#Close the file and print the total of invalid inputs.
csvfile.close()
print(answer)
