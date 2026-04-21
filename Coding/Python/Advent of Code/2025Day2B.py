
#The library for opening .csv files.
import csv
#Used for the floor function.
import math

#The constant for the name of the file of inputs we need to parse.
FILE_NAME = '2025Day2AInputs.txt'
#FILE_NAME = 'Test.txt'

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

#Calculates the factors of a length of number, excluding n.
def factor(number):
    i = 2
    factors = [1]
    pairs = []
    
    #While the factor being checked is less than  or equal to the square of the number:
    while (i * i) <= number:
        #If this is a factor of the number:
        if (number % i) == 0:
            #Add the factor to the list and its pair to the front of the pairs list.
            #This allows the factors to be concatenated in ascending order later.
            factors.append(i)

            #If this is not a square number:
            if (number // i) != i:
                #Append its multiplicative pair to the list.
                pairs.append(number // i)
        #Increment the factor being checked.
        i += 1

    #If the number is not prime:
    if pairs != []:
        #Reverse the pairs list to be in ascending order.
        pairs.reverse()
        #Extends the list of factors by their pairs in ascending order.
        factors.extend(pairs)
        
    #Return the list of factors, excluding n.
    return(factors)

#A function to calculate which numbers are not factors of the rest in a list.
def non_factors(numbers):
    #Stores the list of indivisible factors.
    not_factors = []

    #For every number in the list:
    for number in numbers:
        #Adds the number to the list of indivisibles, until proven otherwise.
        not_factors.append(number)
        
        #For every number after this in the list.
        for n in range(numbers.index(number) + 1, len(numbers)):
            #If the number being checked is a factor of a later number in the list:
            if numbers[n] % number == 0:
                #Remove it from the list of indivisibles.
                not_factors.pop()
                #Skip to check the next number.
                break

    #Return the list of factors which aren't factors of the others.
    return(not_factors)

#Counts how many times a number is a factor of a list of numbers.
def count_factors(numbers):
    #Initialise the dictionary for storing the count of factors.
    f_count = []
    
    #For every factor in the cut-down list of factors:
    for number in numbers:
        #Stores the factors of the current non_factor factor.
        temp_factors = factor(number)

        #For each factor of this number:
        for tf in temp_factors:
            #If this is the first factor to be added to the list:
            if f_count == []:
                f_count.append([tf, 1])

            else:
                #Flag used for if this factor has been counted before.
                flag = False
                #For every counted factor:
                for f_c in f_count:
                    #If this factor is a factor of another number in the list:
                    if tf == f_c[0]:
                        #Increment how many times it is a factor of the numbers.
                        f_count[f_count.index(f_c)][1] += 1
                        #This factor is already in the list.
                        flag = True
                        break

                #If this factor is not already in the list:
                if flag == False:
                    #Initialise this factor and its count in the list.
                    f_count.append([tf, 1])

    #Returns the dictionary of the count of factors for the numbers in the list.
    return(f_count)

#The function used to calculate the lowest invalid value within this bounadary and length.
def calcLower(boundary, length):
    #Splits the boundary into the number of desired repeated length.
    invalid = boundary[:length]
    #How many times the repeated number will fit into the length fo the boundary.    
    divisor = len(boundary) // length
    #Holds the current boundary's invalid ID.
    checking = invalid * divisor

    #If the current boundary works:
    if (int(boundary) <= int(checking)):
        #Return this as the starting invalid ID.
        return(checking)
    
    #If the current boundary does not work:
    else:
        #Return the next invalid ID.
        return((str(int(invalid) + 1)) * divisor)     

#The function used to calculate the highest invalid value within this boundary.
def calcUpper(boundary, length):
    #If the upper boundary is not divisible by the current length being checked:
    if ((len(boundary) % length) != 0):
        #Obtain the amount of times the length divides into the boundary length.
        divisor = len(boundary) // length
        #Return the final invalid ID of a length divisible by the currently being checked length of invalid ID.
        return('9' * divisor)
    
    else:
        #Splits the boundary into the number of desired repeated length.
        invalid = boundary[:length]
        #How many times the repeated number will fit into the length fo the boundary.
        divisor = len(boundary) // length
        #Holds the current boundary's invalid ID.
        checking = invalid * divisor
        
        #If the current boundary works:
        if (int(boundary) >= int(checking)):
            #Return this as the starting invalid ID.
            return(checking)
        #If the current boundary does not work:
        else:
            #Return the next invalid ID down.
            return((str(int(invalid) - 1)) * divisor) 
    
#A function to calculate the invalid number boundaries and total them.
def calcBoundTotals(low, high, divisor):
    
    #print(low, high, divisor)
    #Calculate the upper and lower boundaries respective to invalid values.
    low = calcLower(low, divisor)
    #If the higher bound is a different length to the lower bound:
    if len(high) > len(low):
        high = '9' * len(low)
    else:
        high = calcUpper(high, divisor)

    #If the range contains no invalid IDs:
    if int(low) > int(high):
        #Return 0.
        return(0)
                    
    #Calculate the first repeated number + the last repeated number.
    calc = int(low) + int(high)
    
    #Used to calculate the total amount of numbers in the series.
    initial = int(low[:divisor])
    final = int(high[:divisor])

    #Calculate how many numbers are in the series.
    amount = (final - initial) + 1

    #print(low, high)
    #print(initial, final, amount)

    #Calculate how many times to multiply the repeated sum by.
    multiplier = amount/2
    
    #Return the total of the series according to the formula:
    #(n[0] + n[n-1]) * (n/2)
    #print(calc * multiplier)
    return(calc * multiplier)    

#Used for keeping track of the total of invalid inputs.
answer = 0

#Open the inputs file for reading.
with open(FILE_NAME, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',', quotechar='|')

    #Iterates over the rows of inputs in the file.    
    for values in reader:
        #Prints the list of ranges obtained from the csv file
        #print(values)

        #Iterates over each range within the selection.
        for span in values:
            #Prints the current range in the selection.
            #print(span)

            #Parse the range into its upper and lower bounds.
            lower, upper = parse(span)
            #print(lower, upper)

            #For every length this invalid ID could be:
            #Range is exclusive of the upper bound, so + 1 is needed.
            for length in range(len(lower), len(upper) + 1):

                #If the length of number currently being checked is 1:
                if length == 1:
                    #Skip this check as no 1 length IDs are invalid.
                    continue
                
                #If the lower boundary is a different length to the length currently being checked:
                if len(lower) < length:
                    #Increase the lower bound to the minimum of the next length.
                    lower = ('1' + ('0' * (length - 1)))

                #If the range is backwards:
                if int(upper) < int(lower):
                    #This range is invalid; add nothing.
                    break
            
                #Calculate the factors of the length of the lower bound.
                factors = factor(len(lower))
                #Removes factors which are contained within other factors.
                factors = non_factors(factors)

                #For every non_factor factor of the length:
                for f in factors:
                    #Calculate the boundaries of invalid numbers and total them.
                    answer += calcBoundTotals(lower, upper, f)
                    #print(answer)

                #print(factors)
                #If the length is non-prime:
                if factors[0] != 1:
                    #A list storing the count of factors of the non_factor factors in descending order.
                    factor_count = sorted(count_factors(factors), key=lambda x: x[0], reverse=True)       
                    #For every factor of these non-factor factors:
                    #Works backwards to avoid having to run through the list again
                    #Looking for discrepencies.
                    for f in factor_count:
                        #If the factor appears more than once:
                        if f[1] > 1:
                            #print(factor_count)
                            #How many times this factor has been over-calculated.
                            overcount = f[1] - 1
                            #print(overcount, answer)
                            #Remove this factor's total from the answer however many times it has been overused.
                            answer -= (calcBoundTotals(lower, upper, f[0]) * overcount)
                            #print(answer)
                            #Lower this factor's count to 1.
                            factor_count[factor_count.index(f)][1] -= overcount

                            #If the factor being checked isn't 1:
                            if f[0] != 1:  
                                #Calculate the factors of this factor
                                temp_factors = factor(f[0])
                                #For every factor of this factor:
                                for tf in temp_factors:
                                    #For every factor and count in the count of factors:
                                    for counts in factor_count:
                                        if tf == counts:
                                            #Reduce the amount of times it has been counted by the overcount.
                                            factor_count[factor_count.index(counts)][1] -= overcount

                        #If the factor has been removed too many times:
                        elif f[1] < 1:                           
                            #How many times the factor has been over-removed.
                            undercount = abs(f[1] - 1)
                            #Adds this factor's total back on to the answer however many times it has been underused.
                            answer += (calcBoundTotals(lower, upper, f[0]) * undercount)
                            #Increase this factor's count back to 1.
                            factors_count[factor_count.index(f)[1]] += undercount

                            #If the factor being checked isn't 1:
                            if f[0] != 1:       
                                #Calculate the factors of this factor
                                temp_factors = factor(f[0])
                                #For every factor of this factor:
                                for tf in temp_factors:
                                    #Increase the amount of times it has been counted by the undercount.
                                    factor_count[factor_count.index(tf)[1]] += undercount

                        #Do nothing if it has been counted exactly once.
                        else:
                            
                            #Redundant as the for loop ends here anyway, but thought it looked nice.
                            continue
              
#Close the file and print the total of invalid inputs.
csvfile.close()
print(int(answer))
