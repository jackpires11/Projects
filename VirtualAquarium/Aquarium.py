import math
import time
import random
import os
import sys
from enum import Enum

#The class for deciding what word to use to describe how your new fish has been integrated into the squarium!
class Placement(Enum):
        plopped = 0
        placed = 1
        dropped = 2
        thrown = 3
        chucked = 4
        lowered = 5
        yeeted = 6
        plunked = 7
        jerked = 8
        dangled = 9
        hurled = 10
        directed = 11
        lobbed = 12
        catapulted = 13
        projected = 14
        launched = 15
        heaved = 16
        propelled = 17
        slung = 18
        slammed = 19
        thrust = 20
        flung = 21
        shot = 22
        delivered = 23
        put = 24
        brought = 25
        tossed = 26
        positioned = 27
        planted = 28
        swung = 29
        dumped = 30
        deposited = 31
        bunged = 32
        plonked = 33
        popped = 34
        stuck = 35
        integrated = 36

        #The (fish_name) was (Placement) into the aquarium!

#The function for deciding where food falls.
def food_Fall(size, food):
        #The list of new food positions.
        new_pos = [food[0]]
        
        #Obtains the list of positions for editting.
        for i in range(1, len(food)):
                #If the food is at the edge of the tank:
                if (food[i] == (size[0] - 1)) or (food[i] == 0):
                        #The rates at which food can fall in set directions[down, left/right].
                        rates = [60, 20]
                        #The total of the rates, used to generate a number to see where the food falls.
                        total = 80
                else:
                        #The rates at which food can fall in set directions[down, left, right].
                        rates = [60, 20, 20]
                        #The total of the rates, used to generate a number to see where the food falls.
                        total= 100
                #Picks a random number to see where the food falls.
                position = random.randint(1, total)
                
                #Over all the rates:
                for j in range(len(rates)):
                        #If the position the food is falling is not this one:
                        if position > rates[j]:
                                #Update the value of position to see if it's the next one.
                                position -= rates[j]
                        #If the food is falling here:
                        else:
                                #If it's the first position:
                                if (j == 0):
                                        #It falls down.
                                        new_pos.append(food[i])
                                        #Break out of the loop as this food has fallen.
                                        break
                                #If it's the last position:
                                elif (j == 2):
                                        #It falls right.
                                        new_pos.append(food[i] + 1)
                                        #Break out of the loop as this food has fallen.
                                        break
                                #If it's the second position:
                                else:
                                        #If the pellet is not at the edge:
                                        if (len(rates) == 3):
                                                #Fall left.
                                                new_pos.append(food[i] - 1)
                                                #Break out of the loop as this food has fallen.
                                                break
                                        #If the pellet is on the left side of the tank:
                                        elif (food[i] == 0):
                                                #The food moves right.
                                                new_pos.append(food[i] + 1)
                                                #Break out of the loop as this food has fallen.
                                                break
                                        #Otherwise, the pellet is on the right side of the tank:
                                        else:
                                                #The food moves left:
                                                new_pos.append(food[i] - 1)
                                                #Break out of the loop as this food has fallen.
                                                break
        return(new_pos)

#The function for deciding where food is initially placed.
def gen_Food(size):
        places = [x for x in range(size[0])]
        chosen = [0]
        for i in range(5):
                next_pos = random.randint(0, (len(places) - 1) - i)
                chosen.append(places[next_pos])
                places.pop(next_pos)
        return(chosen)

#Function used to see if a fish has been overfed.
def overfed(pet):

        #Used as the index in the catalogue matching the provided fish.
        index = 0
        #For every fish in the list of known fish:
        for fish in range(len(fish_list)):
                #If the fish in the catalogue matches that of the one being checked:
                if (fish_list[fish][0] == pet[0]):
                        #This is the matching fish in the catalogue.
                        index = fish
                        #Can break as the fish has been found.
                        break
        #If the fish has been overfed:
        if pet[3] >= (fish_list[index][3] * 2):
                #It has been overfed.
                return(True)
        #It has not been overfed.
        else:
                return(False)

#The function for calculating the manhattan distance of two points
def manhattan(point_a, point_b):
        #The length difference of the two points.
        length_dif = abs(point_a[0] - point_b[0])
        #The height difference of the fish and the current food pellet.
        height_dif = abs(point_a[1] - point_b[1])
        return(length_dif + height_dif)

#The function which determines the probability that a fish will eat some food based on its distance away.
def food_Eat_Chance(pet, distance, relation):
        #The chance that a fish will eat food in optimal conditions (if the food shares the column) - used as a constant for calculating chance of a fish eating some food.
        feed_chance = 90

        #The following is the formula calculated for the chance a fish will eat some food.
        midpoint = feed_chance/(pet[5] + 1)
        side_midpoint = (feed_chance - midpoint) / 2
        side_midpoint_pos = (pet[5] + 1)/2
        side_average = side_midpoint / pet[5]
        #Used as a constant for making the probability list.
        step = side_average / side_midpoint_pos

        #The list of probabilities to be created from the step calculated.
        chances = []
        #Used to know the probability at the current distance from the fish.
        current_step = 0
        #For the length of the list of probabilites about to be creates:
        for probabilities in range((pet[5] * 2) + 1):
                #If there are no probabilities yet:
                if chances == []:
                        current_fail = 1
                #Otherwise, calculate the new current_fail rate.
                else:
                        current_fail = current_fail * (1 - (chances[probabilities - 1]/ 100))

                #If we're still increasing in probability:
                if probabilities <= (pet[5]):
                        current_step += step
                        chances.append(current_step / current_fail)
                #Otherwise, we're decreasing:
                else:
                        current_step -= step
                        chances.append(current_step/current_fail)

        #If the food is above:
        if relation == 'Up':
                #Return the corresponding probability.
                return(chances[((pet[5]) - distance)])
        #Otherwise, the food is below:
        else:
                #Return the corresponding probability.
                return(chances[((pet[5]) + distance)])
        
#The function for eating nearby food.
def eat_Food(pets, food):
        
        #For every pellet in the tank:
        for pellet in range((len(food) - 1), 0, -1):
                #If all of the fish have been overfed:
                if (len(pets) == 0):
                        #Exit out of the for loop, as there are no fish left to feed.
                        break
                
                #For every fish in the tank:
                for fishies in range(0, len(pets)):
                        #The manhattan distance of the food from the fish.
                        manhat = manhattan(pets[fishies][len(pets[fishies]) - 1], [food[pellet], food[0]])
                        #If the pellet is within range of a fish:
                        if (manhat <= pets[fishies][5]):
                                #If the food is above the fish:
                                if (food[0] >= pets[fishies][len(pets[fishies]) - 1][1]): 
                                        chance = food_Eat_Chance(pets[fishies], manhat, 'Up')
                                #The food is below the fish:
                                else:
                                        chance = food_Eat_Chance(pets[fishies], manhat, 'Down')
                                success = random.uniform(0, 100)
                                #If the fish succeeds in eating the pellet:
                                if success <= chance:
                                        #Increases the hunger state of the fish by 1.
                                        pets[fishies][3] += 1
                                        #If the fish was overfed:
                                        if (overfed(pets[fishies])):
                                                pets.pop(fishies)
                                        #Remove the pellet from the list of pellets.
                                        food.pop(pellet)
                                        #Make sure not to check this same pellet for other fish:
                                        break
        return(pets, food)

#The function which returns the probabilty that a fish will eat another (based on movement).
def fish_Eat_Chance(pet, distance):
        #A constant used to define the probability of eating a fish at the maximum range of a fish's movement.
        max_distance = 10
        #If the fish is a beta:
        if pet[0] == 'beta':
                eat_chance = 40
        #If the fish is a shark
        elif pet[0] == 'shark':
                eat_chance = 75
        #If the fish type is unknown:
        else:
                print('Error!, consult the maker of the game!')
                return(max_distance)
        #Calculate the step.
        remaining = eat_chance - max_distance
        step = remaining / (pet[5] - 1)

        #The list appended to for all of the chances of the fish eating another.
        chances = [max_distance]

        #For each step needed to complete:
        for steps in range(pet[5] - 1):
                #Append the chance of a fish being eaten.
                chances.append(chances[steps] + step)

        #Used for indexing the list of chances.
        distance = pet[5] - distance
        return(chances[distance])

#The function for eating nearby fish.
def eat_Fish(pets):
        
        #The fish needs to be a carnivore to eat other fish, so:
        #Sets a variable for looping over the whole list of fish.
        i = (len(pets) - 1)
        while i >= 0:
                #If the fish is a carnivore:
                if (pets[i][2] == 'c'):

                        #Sets a variable for looping over the whole list of fish - the eatee.
                        j = (len(pets) - 1)
                        #For every fish owned: (Backwards as fish are popped if eaten).
                        while j >= 0:
                                #If the fish being checked is not the fish eating:
                                if (i != j):
                                        #Calculate the manhattan distance of the fish from each other.
                                        manhat = manhattan(pets[i][len(pets[i]) - 1], pets[j][len(pets[j]) - 1])
                                        #If the fish is within range:
                                        if (manhat <= pets[i][5]):
                                                #Finds the probability that a fish is eaten.
                                                chance = fish_Eat_Chance(pets[i], manhat)
                                                #Generate a random number to see if the fish is eaten.
                                                eaten = random.uniform(0, 100)
                                                #If the fish is eaten:
                                                if (eaten <= chance):
                                                        print('Oh no! Your', pets[i][0], 'has eaten your', pets[j][0] + '!')
                                                        #Increment their hunger status.
                                                        pets[i][3] += 1
                                                        #If the fish is overfed:
                                                        if (overfed(pets[i])):
                                                                #If the fish overfed is indexed later than the fish eaten:
                                                                if j < i:
                                                                        #Remove the overfed fish from your owned fish.
                                                                        pets.pop(i)
                                                                        #Remove the fish eaten from the list of fish owned.
                                                                        pets.pop(j)
                                                                        #Lower i by 1 as the list has moved down by two.
                                                                        i -= 1
                                                                else:
                                                                        #Removed the fish eaten from the list of owned fish.
                                                                        pets.pop(j)
                                                                        #Remove the overfed fish from the list of fish owned.
                                                                        pets.pop(i)
                                                                        #Lower j by 1 as the list has moved down by two.
                                                                        j -= 1
                                                                
                                                                #Need to break out of the for loop as it cannot eat anymore fish
                                                                break
                                                        #The fish is not overfed:
                                                        else:
                                                                #Remove the fish eaten from the list of fish owned.
                                                                pets.pop(j)
                                                                #If this fish was indexed before i,
                                                                if j < i:
                                                                        #Lower i by 1 as its index has shifted down.
                                                                        i -= 1
                                                                else:
                                                                        #Lower by 1 as its index has shifted down.
                                                                        j -= 1
                                #Decrements the fish being checked to be eaten by one.
                                j -= 1
                #Decrements the fish to eat being checked by one.
                i -= 1
        #Return the newly eaten list of pets.
        return(pets)

#The function used to calculate the chance of a pet moving in any cardinal direction.
def direction_Chances(pet):
        #If the fish is an air lover:
        if pet[6] == 'a':
                #Calculate the chance of the fish moving up.
                up_chance = (45 / (size[1] / (pet[len(pet) - 1][1] + 1))) + 25
                #Calculate the chance of the fish moving down.
                down_chance = 100 - (up_chance + 30)
                #Return the list of probabilities.
                return([up_chance, 15, 15, down_chance])
        
        #If the fish is a bottom feeder.
        elif pet[6] == 'b':
                #Calculate the chance of the fish moving down.
                down_chance = (45 / (size[1] / (size[1] - pet[len(pet) - 1][1]))) + 25
                #Calculate the chance of the fish moving up.
                up_chance = 100 - (down_chance + 30)
                #Return the list of probabilities.
                return([up_chance, 15, 15, down_chance])
        
        #The fish is a drifter.
        elif pet[6] == 'd':
                #Return a list of equal probabilities.
                return([25, 25, 25, 25])

        #The fish is an unknown type!
        else:
                #Print an error statement.
                print('This fish type is unknown!')
                #Return that of a drifter so that the program does not crash.
                return([25, 25, 25, 25])

#The function used to calculate the chances of a fish using each amount of its movement.
def move_Chances(pet):
        #Used to store the probabilities for each movement
        chances = []
        #If the pet has balanced movement:
        if (pet[7] == 'balanced'):
                #For each movement amount:
                for moves in range(pet[5]):
                        #Appends an equal chance for each movement amount
                        chances.append(100/(pet[5] + 1))
                #Return the decided possibilities.
                return(chances)

        #The pet does not have balanced movement:
        else:
                #For each movement amount:
                for moves in range(pet[5]):
                        #Follow the formula, (5/movement)x^2 + 0x + 5 = chance
                        #A scalar is:
                        A = 5/pet[5]
                        #Append the next value according to the formula.
                        chances.append((A*(moves**2)) + 5)
                #If the pet is a slow type:
                if pet[7] == 'slow':
                        #Reverse the list.
                        chances.reverse()
                return(chances)
        
#The function used to decide where fish move.
def move_Fish(pets, dimensions, checking):

        #If the checking list is empty, moving has just begun:
        if checking == []:
                #Instantiate the checking list
                checking = [x for x in range(len(pets))]

        #Instantiates a list of trapped pets for checking against and checking later. Becomes checking when running the function again.
        trapped_pets = []
        
        #For each fish:
        for pet in range((len(checking) - 1), -1, -1):
                #Used to see if a fish succeeds a probability check.
                chance = random.uniform(0, 100)
                #If the fish is a quick type:
                if(pets[checking[pet]][7] == 'quick'):
                        #Initially, test to see if the fish does not move at all:        
                        #If the fish doesn't move at all:
                        if (chance <= 1):
                                #Skip this fish as it does nothing.
                                continue                                                            
                        
                #If the fish is a slow type:
                elif(pets[checking[pet]][7] == 'slow'):
                        #Initially, test to see if the fish does not move at all:
                        #If the fish doesn't move at all:
                        if (chance <= 40):
                                #Skip this fish as it does nothing.
                                continue
                        
                #The fish is a balanced type:
                else:
                        #Initially, test to see if the fish does not move at all:
                        #If the fish doesn't move at all:
                        if (chance <= (100/(pets[checking[pet]][5] + 1))):
                                #Skip this fish as it does nothing.
                                continue
                        
                #Calculate the chances for a fish to use each amount of its movement.
                chances = move_Chances(pets[checking[pet]])
                #Used to sum up the chances provided.
                sum_up = 0
                #For every probability in the list:
                for chance in range(len(chances)):
                        #Calculate the sum of the list of probabilities.
                        sum_up += chances[chance]
                #Used to see what amount of movement the fish will use.
                amount = random.uniform(0, sum_up)         
                #For every probability, see if this one is the amount of movement used.
                for chance in range(len(chances)):
                        #If this is the amount of movement decided on:
                        if (amount <= chances[chance]):
                                #The amount of movement the fish uses (-1, but this works for indexing the chance list as 1 starts at 0.)
                                moves = chance
                                #Break out of the for loop as the amount of movement used has been found.
                                break
                        #This isn't the amount of movement decided upon.
                        else:
                                #Lower the amount for the next check.
                                amount -= chances[chance]

                #You now have the amount of movement used, time to move the fish!
                #For each one of its movement:
                for move in range(moves + 1):
                        #Used for knowing which way the fish moves:
                        direction = ['up', 'left', 'right', 'down']
                        #Calculate the list of probabilities per movement.
                        chances = direction_Chances(pets[checking[pet]])

                        #Time to remove options that are unable to be obtained.
                        #If a fish is at the top of the tank:
                        if pets[checking[pet]][len(pets[checking[pet]]) - 1][1] == 0:
                                #Remove the ability to go up.
                                direction.remove('up')
                                #This only works as this is the first part of the list checked.
                                chances.pop(0)
                        #If a fish is above you:
                        elif colliding([(pets[checking[pet]][len(pets[checking[pet]]) - 1][0]), (pets[checking[pet]][len(pets[checking[pet]]) - 1][1] - 1)], pets):
                                #Remove the ability to go up.
                                direction.remove('up')
                                #This only works as this is the first part of the list checked.
                                chances.pop(0)

                        #If a fish is at the left side of the tank:
                        if pets[checking[pet]][len(pets[checking[pet]]) - 1][0] == 0:
                                #Obtain the index for moving left.
                                index = direction.index('left')
                                #Remove the ability to go left.
                                direction.pop(index)
                                #Remove the chance of going left.
                                chances.pop(index)
                        #If a fish is to the left of you:
                        elif colliding([(pets[checking[pet]][len(pets[checking[pet]]) - 1][0] - 1), (pets[checking[pet]][len(pets[checking[pet]]) - 1][1])], pets):
                                #Obtain the index for moving left.
                                index = direction.index('left')
                                #Remove the ability to go left.
                                direction.pop(index)
                                #Remove the chance of going left.
                                chances.pop(index)

                        #If a fish is at the right side of the tank:
                        if pets[checking[pet]][len(pets[checking[pet]]) - 1][0] == (size[0] - 1):
                                #Obtain the index for moving right.
                                index = direction.index('right')
                                #Remove the ability to go right.
                                direction.pop(index)
                                #Remove the chance of going right.
                                chances.pop(index)
                        #If a fish is to the right of you:
                        elif colliding([(pets[checking[pet]][len(pets[checking[pet]]) - 1][0] + 1), (pets[checking[pet]][len(pets[checking[pet]]) - 1][1])], pets):
                                #Obtain the index for moving right.
                                index = direction.index('right')
                                #Remove the ability to go right.
                                direction.pop(index)
                                #Remove the chance of going right.
                                chances.pop(index)

                        #If a fish is at the bottom of the tank:
                        if pets[checking[pet]][len(pets[checking[pet]]) - 1][1] == (size[1] - 1):
                                #Obtain the index for moving down.
                                index = direction.index('down')
                                #Remove the ability to go down.
                                direction.pop(index)
                                #Remove the chance of going down.
                                chances.pop(index)
                        #If a fish is beneath you:
                        elif colliding([(pets[checking[pet]][len(pets[checking[pet]]) - 1][0]), (pets[checking[pet]][len(pets[checking[pet]]) - 1][1] + 1)], pets):
                                #Obtain the index for moving down.
                                index = direction.index('down')
                                #Remove the ability to go down.
                                direction.pop(index)
                                #Remove the chance of going down.
                                chances.pop(index)
                                
                        #If the fish cannot move:
                        if direction == []:
                                
                                #Add to trapped pets.
                                trapped_pets.append(checking[pet])
                                
                                #Break out of the loop as this pet is stuck.
                                break

                        #The fish can move:
                        else:
                                
                                #For every probability in the list:
                                for chance in range(len(chances)):
                                        #Calculate the sum of the list of probabilities.
                                        sum_up += chances[chance]
                                #Used to see which way the fish will decide to swim.
                                way = random.uniform(0, sum_up)

                                #For every probability, see if this one is the way the fish will go.
                                for chance in range(len(chances)):
                                        #If this is the way the fish will move:
                                        if (way <= chances[chance]):

                                                #Time to move the fish.
                                                #Used to make the code easier to read - it is the current location of the fish moving.
                                                location = pets[checking[pet]][len(pets[checking[pet]]) - 1]
                                                
                                                #If the direction is up:
                                                if direction[chance] == 'up':
                                                        #The fish moves up.
                                                        pets[checking[pet]][len(pets[checking[pet]]) - 1] = [location[0], (location[1] - 1)]

                                                #If the direction is left:
                                                elif direction[chance] == 'left':
                                                        #The fish moves left.
                                                        pets[checking[pet]][len(pets[checking[pet]]) - 1] = [(location[0] - 1), location[1]]

                                                #If the direction is right:
                                                elif direction[chance] == 'right':
                                                        #The fish moves right.
                                                        pets[checking[pet]][len(pets[checking[pet]]) - 1] = [(location[0] + 1), location[1]]

                                                #If the direction is down:
                                                elif direction[chance] == 'down':
                                                        #The fish moves down.
                                                        pets[checking[pet]][len(pets[checking[pet]]) - 1] = [location[0], (location[1] + 1)]

                                                #Break out of the for loop as the fish has now moved.
                                                break
                                        #This isn't the way the fish moves.
                                        else:
                                                #Lower the amount for the next check.
                                                way -= chances[chance]  

        #If any of the fish were trapped:
        if len(trapped_pets) > 0:
                #If the length of the trapped pets is not equal to all of those being checked:AssertionError
                if (len(trapped_pets) != len(checking)):
                        #Some fish have moved, so see if any of the trapped fish can now move:
                        move_Fish(pets, dimensions, trapped_pets)
        #Otherwise, all of the fish are still trapped, so return as they cannot move this turn.
        #Or, none of the fish were trapped so they have now all moved, so return.
        return(pets)

#Reduce the hunger of all fish by their hunger constant:
def hunger(pets):
        for i in range(len(pets)):
                pets[i][3] -= pets[i][4]
        return(pets)

#The function to check if a fish has died:
def starved(pets):
        if pets[3] < 0:
                return(True)
        else:
                return(False)

#The function for adding food to the tank.
def feed_Fish(size, pets, turn, food):
        #Involves, where the food is first put in, where it falls, and what fish
        #eat it. It will also display updates of the aquarium after each time the
        #food falls, so you can visualise the fish eating the food.
        food_pos = gen_Food(size)
        gen_Board(size, turn, pets, food, food_pos)
        #See if the fish eat any of the pellets.
        pets, food_pos = eat_Food(pets, food_pos)

        #One row of food passed, now to do the rest:
        #For the height of the tank - 1, since the very top has already been checked:
        for rows in range(size[1] - 1):
                #If all of the food was eaten, or all of the fish were overfed:
                if (len(food_pos) == 1) or (len(pets) == 0):
                        gen_Board(size, turn, pets, food, food_pos)
                        return(pets)
                #Otherwise, continue to let the food fall:
                else:
                        #Increment the row of the board being worked on.
                        food_pos[0] += 1
                        #Make the food fall down a row.
                        food_pos = food_Fall(size, food_pos)
                        #Display the new state of the board
                        gen_Board(size, turn, pets, food, food_pos)
                        #See if any fish eat the pellets in their new locations.
                        pets, food_pos = eat_Food(pets, food_pos)

        gen_Board(size, turn, pets, food, food_pos)
        return(pets)

#Used to update the positions of fish between rounds, as well as if they die/eat each other.
def update(pets, space):

        #First, check to see if they eat other fish:
        pets = eat_Fish(pets)

        #If there are still fish in the aquarium:
        if (pets != []):

                #Then move:
                pets = move_Fish(pets, space, [])



                #Then reduce hunger for the turn:
                pets = hunger(pets)

                #Did any fish starve?
                for i in range(len(pets) - 1, -1, -1):
                        if starved(pets[i]) == True:
                                print('A', pets[i][0], 'has died!')
                                pets.pop(i)

        return(pets)

#A function to decide how your fish is placed into its new home.
def gen_Verb():
        return(Placement(random.randint(0, 36)).name)
               
#Generate the position for a new fish
def gen_Pos():
        width = random.randint(0, (size[0] - 1))
        height = random.randint(0, (size[1] - 1))
        return(list([width, height]))

#The function for seeing if a position collides with those currently known.
def colliding(checking, positions):

        #For every position in the list:
        for i in range(len(positions)):
                #If checking matches the position:
                if checking == positions[i][len(positions[i]) - 1]:
                        #There has been a collision
                        return(True)

        #If no collision was found, return False:
        return(False)

#A function which returns whether or not the tank is full
def is_Tank_Full(pets):
        #If there are as many fish as there are spaces in the tank:
        if (len(pets) == (size[0] * size[1])):
                #Return true.
                return(True)
        #Otherwise, there is still space left:
        else:
                #Return false.
                return(False)
 
#The function to decide what the player is trying to buy!
def sale(choice, pets, options, coin, pellets):

        #Set the input to all lower case for generalisation.
        choice = choice.lower()
        
        #Time for case statements (basically)!

        #If you're buying food:
        if choice == 'food':
                #If you can't afford it:
                if (coin - 50) < 0:
                        print('You can\'t afford to buy that!')
                        return(pellets, pets, coin)
                else:
                        pellets += 1
                        coin -= 50
                        print('You bought some fish pellets!')
                        return(pellets, pets, coin)
        
        #If you're buying a fish:
        else:
                #If the tank is not full:
                if not is_Tank_Full(pets):        
                        #Find and add the fish.
                        for x in range(len(options)):
                                #If the fish in the catalogue matches the one chosen:
                                if options[x][0] == choice:
                                        #If you can't afford it:
                                        if (coin - options[x][1]) < 0:
                                                print('You can\'t afford to buy that!')
                                                return(pellets, pets, coin)
                                        #Else, buy the fish:
                                        else:
                                                print('You bought a ' + choice + '!')
                                                #To make sure fish do not collide.
                                                collide = True
                                                
                                                while collide == True:
                                                        #Generate the new fish's position
                                                        position = gen_Pos()
                                                        #If it doesn't collide with the fish already in the tank:
                                                        if not colliding(position, pets):
                                                                collide = False
                                                print('It was', str(gen_Verb()), 'into the tank!')
                                                #Generate the stats for the fish and add it to the list of fish in the aquarium.
                                                stats = list(options[x])
                                                stats.append(position)
                                                pets.append(stats)
                                                coin -= options[x][1]
                                                return(pellets, pets, coin)
                        #Could not find the fish
                        print('Unfortunately, you can\'t buy that.')
                #Otherwise, the tank is full:
                else:
                        print('Your tank is at maximum capacity, so you cannot buy any more fish; sorry!') 
        return(pellets, pets, coin)

#The function for displaying the fish and food available for sale!.
def shop(options):
        
        for x in range(len(options)):
                gap = ' ' * (15 - len(options[x][0]) - len(str(options[x][1])))
                print('\n' + options[x][0].capitalize() + gap + str(options[x][1]), end='')
        gap = ' ' * 9
        print('\nFood' + gap + '50\n')
        return()

#Used to find the colour of the fish, representing its health state.
def fish_colour(pet):
        
        index = ''
        #Find the index in the fish list for the fish being colour checked.
        for x in range(len(fish_list)):
                if pet[0] == fish_list[x][0]:
                        index = x
                        break
        hunger = float(pet[3] / fish_list[index][3])

        #Assigns a colour to the fish based on how hungry it is. Fails if no colour could be decided.
        for i in range(5):
                #I would do 0.0, but floating point errors mean it would fail due to being minutely small instead of 0. This encompasses that.
                if ((hunger - float(0.2)) <= float(0.1)):
                        return('\033[38;5;' + str(17+i) + 'm' + pet[0][0])
                else:
                        hunger -= float(0.2)
        return('\033[38;5;23m' + pet[0][0])

#Checks if their is a fish at the given coordinate.
def fish_Pos(fishies, x_pos, y_pos):
        
        #Checking if any of the fish are here.
        for z in range(len(fishies)):
                #If the width and height match the position of the fish:
                if (x_pos == fishies[z][len(fishies[z]) - 1][0]) and  (y_pos == (fishies[z][len(fishies[z]) - 1][1] + 1)):
                        return(fish_colour(fishies[z]))
        #If there aren't any fish here:
        return(' ')

#Initially generates the frame of the aquarium, based on the size.
def gen_Board(size, turn, pets, food, pellets):        
        #Generating the top of the HUD
        print()
        gap = str(' ') * ((math.floor(size[0]/2) - 3))
        print(gap + 'Round ' + str(turn) + '\n')
        gap = str(' ') * ((size[0] - 2) - len(str(food)))
        print('Food' + gap + str(food))

        #Generating the layout of the aquarium.
        #For the height of the aquarium...
        for x in range(size[1] + 2):
                row = ''
                if (x != 0):
                        row += '|'
                else:
                        row += ' '
                #For the width of the aquarium...
                for y in range(size[0]):
                        #If it's the top or bottom of the aquarium:
                        if (x == 0) or (x == size[1] + 1):
                                row += '_'
                        #If this is the food row:
                        elif ((x - 1) == pellets[0]):
                                #If this cell contains food:
                                if (y in pellets[1:]):
                                        row += 'f'
                                #In case a fish is there:
                                else:
                                        row += fish_Pos(pets, y, x)
                                        #If a coloured fish was returned:
                                        if row[len(row) - 1] != ' ':
                                                #Reset the colour of the row.
                                                row += '\033[0m'
                        else:
                                row += fish_Pos(pets, y, x)
                                #If a coloured fish was returned:
                                if row[len(row) - 1] != ' ':
                                        #Reset the colour of the row.
                                        row += '\033[0m'
                if (x != 0):
                        row += '|'
                print(row)

        #Generating the bottom of the HUD
        gap = str(' ') * ((size[0] - 2) - len(str(money)))
        print('\nShop' + gap + str(money))
        gap = str(' ') * (((round(size[0] / 2)) - 3) - len(str(score)))
        print(gap + 'Score: ' + str(score))
        return()

#Used to explain the game to the player!
def description():
        print('\nEach round you gain money for each fish within the tank. Money is displayed to the bottom right of the tank. You may spend money each turn to buy more food or fish and you may also feed your fish. The amount of food you have is shown to the top right of the tank and you may feed your fish by typing \'feed\'. In order to access the shop, type \'shop\'. In order to buy some fish or food, just type \'buy (fish name)\' or \'buy food\'.')
        print('\nYour score for this game is equal to the amount of money you earn while playing and is displayed beneath the centre of the aquarium. If you want to see how many points each fish type is worth, type \'fish\'.')
        print('\nIf you want to end the round and earn more money to spend, just type \'next\'. Or you can end the game by typing \'end\'. You can lose by running out of fish and not having any money to buy more, so be careful not to choose the wrong fish to put in your tank or forgetting to feed them!')
        print('\nIf you type too many commands or want to see your updated tank, simply type \'display\'. And if you want to see this explanation again, just type \'help\'!\n')
        return()

#Calculates the diet modifier for the chosen fish.
def diet_Mod(diet):
        if diet == 'c':
                return(2)
        else:
                return(1)

#Calculates the movetype modifier for the chosen fish.
def movetype_Mod(movetype):
        if movetype == 'd':
                return(2)
        else:
                return(1)

#Calculates the movespeed modifier for the chosen fish
def movespeed_Mod(movespeed):
        if movespeed == 'balanced':
                return(2)
        else:
                return(1)

#A function for calculating the points for the provided fish type.
def calc_Points(fish):
        #A constant used to balance the scores
        constant = 8
        score = (constant - math.ceil((fish[3] + 1) / fish[4])) * (constant - (fish[5] - (movetype_Mod(fish[6]) + movespeed_Mod(fish[7])))) * diet_Mod(fish[2])
        return(score)

#Used to explain the points obtained by each type of fish.
def fish_Desc():
        #Iterate over all of the fish
        for x in range(len(fish_list)):
                points = calc_Points(fish_list[x])        
                gap = ' ' * (15 - len(fish_list[x][0]) - len(str(points)))
                print(fish_list[x][0].capitalize() + gap + str(points))

#Checks to see if you have lost the game.
def game_Lost(funds, pets):
        if (len(pets) == 0) and (funds < 50):
                return(True)
        else:
                return(False)

#A function to match an owned fish to a fish in the catalogue and check how many points it is worth.
def fish_Find(pet, catalogue):
        for j in range(len(catalogue)):
                if pet == catalogue[j][0]:
                        return(calc_Points(catalogue[j]))
        #This should never be reached.
        return(print('AN ERROR HAS OCCURRED. CONTACT THE CREATOR IMMEDIATELY!'))

#The function used to see if a score is a highscore. If so, it updates the
#highscores text file.
def is_Highscore(points):
        try:
                #Used as a flag to say whether or not a new highscore was found.
                position = 10
                
                #Opens the list of highscores for reading and writing.
                scores = open('highscores.txt', 'r')
                
                #For all of the highscores in the text file (this is always 10!):
                for i in range(10):
                        current = scores.readline()
                        #For every letter in the current line:
                        for j in range(len(current)):
                                #If the letter is a space
                                if (current[j] == ' '):
                                        #Current becomes equal to the remaining text in the line.
                                        current = current[(j + 1):]
                                        #Break out of the for loop as the score has been obtained.
                                        break
                        #For the letters in the reamainder of the score:
                        for j in range(len(current)):
                                #If the letter is a \:
                                if (current[j] == '\\'):
                                        #Current becomes equal to everything before the \.
                                        current = current[:j]
                                        #Break out of the loop as the score has been obtained.
                                        break
                        #Now that we have the score,
                        #If the new points are greater than this old score:
                        if (points > int(current)):
                                #Obtains the index which needs to be implemented with this score.
                                position = i
                                #Break out of the loop as the new position of the score has been found.
                                break

                #If this is not a new highscore:
                if (position == 10):
                        #Closes the highscore file as it may be referenced later.
                        scores.close()
                        #Return that this is not a new highscore.
                        return(False)
                
                #Otherwise, this is a new highscore:
                else:
                        #Asks the player for their name for entering on the highscores page.
                        print('New High Score!')
                        name = input('\nPlease enter your name!\n\n')
                        #Generates their line in the highscores text file.
                        line = name + ' ' + str(points) + '\n'
                                
                        #Moves the file pointer to the beginning of the file.
                        scores.seek(0)
                        #Obtains the list of all lines in the file.
                        scores_list = scores.readlines()
                        #Inserts the user's name and score into the correct position in the list.
                        scores_list.insert(position, line)
                        #Removes the last element in the list as we are limited the highscores page to 10 users.
                        scores_list = scores_list[:10]

                        #Close the file and reopen in write mode to erase the contents.
                        scores.close()
                        scores = open('highscores.txt', 'w')
                        
                        #For every value in the list of scores:
                        for i in range(len(scores_list)):
                                #If it is not the last line in the file.
                                if i != 9:
                                        #Overwrite the highscores text file.
                                        scores.write(scores_list[i])
                                #It is the last line in the file:
                                else:
                                        #Writes everything but the \n.
                                        scores.write(scores_list[i].strip())
                                
                        #Closes the file for later use.
                        scores.close()
                        #Returns that this is a highscore.
                        return(True)

        #Incase the player has omitted their highscores file / installed incorrectly.
        except:
                #Prints a wholesome could not find message.
                print('Unfortunately you are unable to access the highscores for now.\nPlease make sure your highscores text file is in the folder where this executable is located!\n')
                return(False)

#The function for printing out the highscores text file.
def print_Highscores():
        try:
                #Adds a blank line to separate from input.
                print()
                #Open the high scores text file.
                with open('highscores.txt', 'r') as scores:
                        #Print the entirety of the highscores file.
                        print(scores.read())
                        #Close the highscores file as it may be needed later.
                        scores.close()
                #Adds a blank line to separate from output.
                print()
                #Means that the highscores won't immediately be overwritten by
                #the title screen; it requires input from the player first.
                input('Press any key to return to the title screen.')
                return()

        #Incase the player has omitted their highscores file / installed incorrectly.
        except:
                #Prints a wholesome could not find message.
                print('Unfortunately you are unable to access the highscores for now.\nPlease make sure your highscores text file is in the folder where this executable is located!\n')
                input('Press any key to return to the title screen.')
                return()

#The function used to load the title screen of the game.
def load_Title():
        
        for i in range(50):
                #Generate blank space; works as a way of clearing the screen.
                print()

                
        #Generate the list of options.
        #Starts a new game.
        print('1: Start Game')

        #Prints the list of known high scores.
        print('2: High Scores')

        #Exits the game.
        print('3: Quit')
        print()
        return()

        

##### START OF CODE #####



#Will repeatedly generate the loading screen when breaking out of any of the
#other 3 game modes.
while True:

        #Obtains the file path to the currently executing file.
        PATH = sys.argv[0]
        #Obtains the name of the file.
        file_name = os.path.basename(PATH)
        #Obtains the file path to the directory containing the file.
        PATH = PATH[:(len(PATH) - len(file_name))]

        #Changes the current working directory for the game, for accessing the high scores file!
        os.chdir(PATH)
        #Generate the title screen of the game.
        load_Title()
        #Asks the user to select what to do.
        option = input('Please select an option:\n\n')
        #If they have chosen to play a new game:
        if option == '1':


        
                ##### START OF GAME #####



                print('\nHello and welcome to your very own virtual Aquarium!\n')
                #Instantiating parameters.
                #Allows coloured text to work on windows.
                os.system('color')
                #The size of the aquarium, width x height.
                size = list([7, 4])
                #What round of the game the player is on.
                turn = 1
                #What score the player has.
                score = 0
                #How much food the player has.
                food = 5
                #Have you lost the game?
                lost = False
                #What fish do you own?
                fish = list([])
                #What fish exist?
                #Fish stats are ordered by: [species, price, diet, max hunger, hunger drain, movement, movement type, movement speed, position (added when a fish is bought)]
                fish_list = list([['beta', 100, 'c', 2, 1, 4, 'a', 'quick'], ['shark', 200, 'c', 4, 2, 3, 'd', 'slow'], ['molly', 50, 'h', 1, 1, 5, 'a', 'balanced'], ['tetra', 75, 'h', 2, 1, 4, 'd', 'quick'], ['catfish', 150, 'h', 3, 2, 2, 'b', 'slow'], ['goby', 100, 'h', 2, 1, 3, 'b', 'balanced']])

                #Asking the player what size aquarium they would like to have.
                print('What size aquarium would you like to play with?\n')
                print('(The width can be from size 7 - 40 and the height can be from size 4 - 20)\n')
                while True:
                        try:
                                size[0] = int(input('Start with the width!\n'))
                                size[1] = int(input('And now the height!\n'))
                                if (size[0] >= 7) and (size[0] <= 40) and (size[1] >= 4) and (size[1] <= 20):
                                        break
                                else:
                                        print('\nYou didn\'t read the parameters, did you? Try again...\n')
                        except:
                                print('\nThat input is not a size, please try again:\n')
                                
                #Assigning money based on the size of the tank.
                money = 1000 - (size[0] * size[1])
                gen_Board(size, turn, fish, food, [99])

                #Explanation of the game
                description()

                #Used by the player to select what to do within the current round.
                action = ''
                #Time for the game loop:
                while not lost:
                        #What would the player like to do?
                        action = input()
                        
                        #Remind the player how to play the game
                        if action == 'help':
                                description()

                        #Feed your fish!
                        elif action == 'feed':
                                #If you do not have any fish:
                                if fish == []:
                                        print('\nYou have no fish to feed!\n')
                                #If you have no food:
                                if food == 0:
                                        print('\nYou do not have any food!\n')
                                #Otherwise:
                                else:
                                        #Attempt to feed the fish:
                                        food -= 1
                                        fish = feed_Fish(size, fish, turn, food)
                                        print('\nYou fed your fish!\n')
                                        #This is needed as fish may be overfed and die!
                                        if game_Lost(money, fish):
                                                lost = True

                        #Check the shop!
                        elif action == 'shop':
                                shop(fish_list)

                        #Check the points gained for your current fish!
                        elif action == 'fish':
                                print()
                                fish_Desc()
                                print()

                        #Attempt to buy a fish or food!
                        elif action[0:3] == 'buy':
                                print()
                                food, fish, money = sale(action[4:], fish, fish_list, money, food)
                                #You could have used the last of your money to buy food and have no fish in the tank:
                                if game_Lost(money, fish):
                                        lost = True
                                print()

                        #Re-display the board. (Used for if too many inputs have been made and it's been pushed back up the screen.)
                        elif action == 'display':
                                gen_Board(size, turn, fish, food, [99])
                                print()
                                
                        #Advance the turn and gain more money!
                        elif action == 'next':
                                print()

                                #Calculate the points earned this round.
                                #Used to see how many points you've earned this turn
                                new_points = 0
                                #Time to find the corresponding fish in the catalogue for each fish and see how many points they're worth.
                                for i in range(len(fish)):
                                        new_points += fish_Find(fish[i][0], fish_list)
                                score += new_points
                                #Don't forget that your points are equal to your money!
                                money += new_points

                                #If there are fish in the tank:
                                if len(fish) != 0:
                                        #Update the status of the fish
                                        fish = update(fish, size)
                                
                                #If all of the fish have died...
                                if game_Lost(money, fish):
                                        lost = True
                                #Otherwise, increment the turn and display the board.
                                else:   
                                        turn += 1
                                        #Print the new state of the board.
                                        gen_Board(size, turn, fish, food, [99])
                                print()
                                
                        #End the game!
                        elif action == 'end':
                                lost = True
                                print()
                        else:
                                print('\nThat input is unrecognised, please try again.\n')

                print('Game Over!\n')
                #If the score the user attained is a high score:
                if (is_Highscore(score)):
                        print_Highscores()

                #The user did not obtain a high score.
                else:
                        #Print ending text.
                        print('You obtained a score of ' + str(score) + '!')
                        input('Press any key to return to the title screen.')


                        
                ##### END OF GAME #####

                

        #If they have chosen to view the high scores:
        elif option == '2':
                #Call the function to print the highscores text file.
                print_Highscores()

        #If they have chosen to exit the game:
        elif option == '3':
                #Breaks out of the overarching while loop and exits the game.
                break

        #The option is not recognised; skip:
        else:
                #Pass over this option.
                pass
