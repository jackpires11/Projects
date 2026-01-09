#See how many possible permutations of 3 colours, including no duplicates and only partners.
import random

#Concept art.
colours = ['R', 'O', 'Y', 'G', 'B', 'P']
valid = ['']
a = 0

#Iterate over one colour.
while (a < len(colours)):
    b = 0
    first = colours[a]
    
    #Iterate over a second colour.
    while (b < len(colours)):
        second = colours[b]
        #If the two colours are next to each other:
        if ((abs(a-b) == 1) or (abs(a-b) == 5)):
            c = 0

            #Iterate over a third colour.
            while (c < len(colours)):
                third = colours[c]
                #If the two colours are next to each other:
                if ((abs(b-c) == 1) or (abs(b-c) == 5)):
                    valid.append([first, second, third])

                #Check the next colour.
                c += 1
        #Check the next colour.
        b += 1
    #Check the next colour.
    a += 1

a = 0
#Iterate over the completed list to show valid colour combinations:
while (a < len(valid)):
    print(str(valid[a]) + '\n')
    a += 1
print(len(valid))
input()
