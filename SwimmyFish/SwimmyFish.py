import sys
import os
import xml.etree.ElementTree as ET
#Used for running the game and handling the graphics.
import pygame

#Function for updating all of the UI elements.
#Fonts are stored as [ID, font style, colour, location, text]
def update_UI(fonts, screen):
    #For every font in the UI:
    for i in range(len(fonts)):
        fonts[i][1].render_to(screen, fonts[i][3], fonts[i][4], fonts[i][2])
    return(screen)

#Initialises the fonts for the current screen.
def initialise_Fonts():
    #Used for storing all of the initialised fonts.
    font_list = []

    #Initialises the xml file of font data.
    font_xml = ET.parse('resources/text_data.xml')
    #Obtains the root of the xml file.
    font_root = font_xml.getroot()

    #For every child node of the root node:
    for child in font_root:
        #Obtain the id of the font; used for obtaining the correct font later when rendering.
        ID = child.get('id')
        #Initialises the font.
        font = pygame.freetype.SysFont(child.find('font').text, int(child.find('size').text))
        #Obtains the font's colour.
        colour = child.find('colour').text
        #Obtains the font's location and store it correctly as a list of int.
        location = (child.find('location').text).split(",")
        location = [int(i) for i in location]
        text = child.find('text').text
        #Store all of the required data in the list of fonts for use later.
        font_list.append([ID, font, colour, location, text])
    
    #Returns the list of initialised fonts.
    return(font_list)

#The function for updating the score.
#[ID, font style, colour, location, text]
def update_Score(score):
    #Adds 1 to the current score.
    score[4] = str(int(score[4]) + 1)
    return(score)

#The function used to rotate the original image by the required amount.
def rotate(image, degree):
    #Sets the image to be equal to a rotation of the pure-uneditted image
    #To prevent against cumulative distortion.
    image = pygame.transform.rotate(pure_fish, degree)
    return(image)

#Used for spawning a rock just off the screen.
def spawn_rock(x, y):
    #Loads in the rock image and gets the rect position for collisions.
    new_rock = pygame.image.load("assets/rock.png")
    new_rock_rect = new_rock.get_rect()
    #Moves the rock to a position just off the screen.
    new_rock_rect = new_rock_rect.move(x, (y - new_rock_rect.height))
    return([new_rock, new_rock_rect])

#Initialises pygame.
pygame.init()

#Obtains the file path to the currently executing file.
PATH = sys.argv[0]
print(PATH)

#Sets the size of the game window.
size = width, height = 1280, 640

#Sets the colour of the game background.
background = 100, 100, 255

#Sets the initial and maximum movement speed of the fish.
speed = 0
max_speed = 2

#Sets the cumulative speed of the fish - used to make the fish move even when
#speed is less than 1 or greater than -1; helps with small increments.
cumulative_speed = 0

#Instantiates the screen.
screen = pygame.display.set_mode(size)

#Test.
screen.fill(background)

#Initilises and stores a list of all of the text element fonts contained within the current screen.
fonts_list = initialise_Fonts()

#Test.
pygame.display.flip()

input()

#Loads the fish into the game at the required position.
fish = pygame.image.load("assets/fish.png")
fish = pygame.transform.scale(fish, (200, 80))
#Used for rotations and other destructive transformations.
pure_fish = fish.copy()
fishrect = fish.get_rect()
fishrect = fishrect.move([width/5, height/2])

#Sets the initial rotation of the fish and is used to keep track throughout.
rotation = 0
#Sets the initial rotation acceleration of the fish.
rotation_acceleration = 0
#Flag used to see if the fish is moving up; initially set to move down.
upwards = False

#Used to store the rocks and their positions.
rocks = []
#Temporary counter
counter = 0

while True:

    #Check to see if spawns a rock:
    #Waits to spawn a rock
    counter += 1
    #If it has been 100 frames:
    if counter > 200:
        #Spawn a rock with related rect.
        rocks.append(spawn_rock(width, height))
        #Resets the counter for spawning rocks.
        counter = 0
    #If there are rocks:
    if (len(rocks) != 0):
        #Counter used to scan through the list of rocks.
        i = 0
        #Checking through the list of rocks:
        while i < len(rocks):
            #If the rock has now moved off the screen:
            if rocks[i][1].x < -rocks[i][1].width:
                #Remove the rock from the list.
                rocks.pop(i)
            #Otherwise, move the rock:
            else:
                #If the rock is in line with the fish:
                if rocks[i][1].x == fishrect.x:
                    #For every font:
                    for j in range(len(fonts_list)):
                        #If the font is for the score:
                        if fonts_list[j][0] == 'SCORE':
                            #Update the score.
                            fonts_list[j] = update_Score(fonts_list[j])
                #Move the rock one pixel to the left.
                rocks[i][1] = rocks[i][1].move([-1, 0])
            #Increase the counter.
            i += 1

    #Event handling.
    #For all of the events caused this frame:
    for event in pygame.event.get():
        #If the user has called to quit the game, safely terminate.
        if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_q)):
            pygame.quit()
            sys.exit()
        #If the user has pressed the space bar:
        elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
            #The fish is now moving up.
            upwards = True
        #If the user has stopped pressing the space bar:
        elif (event.type == pygame.KEYUP) and (event.key == pygame.K_SPACE):
            #The fish is no longer moving up.
            upwards = False

    #Speed handling.
    #If the player is trying to move the fish up:
    if (upwards == True):
        #If the fish is not yet at top speed:
        if speed > -max_speed:
            speed += -0.02
        #Otherwise:
        else:
            #Set for floating point error.
            speed = -max_speed
        #Set the new cumulative speed of the fish.
        cumulative_speed += speed
    #The fish is not being moved up:
    else:
        #If the fish is not yet at top speed:
        if (speed < max_speed):
            #Pull the fish down more.
            speed += 0.02    
        #Otherwise:
        else:
            #Set for floating point error.
            speed = max_speed
        #Set the new cumulative speed of the fish.
        cumulative_speed += speed

    #Fish movement handling.
    #If the cumulative speed is enough to make the fish move:
    if (cumulative_speed>1) or (cumulative_speed<-1):
        #Move the fish.
        fishrect = fishrect.move([0, cumulative_speed])

        #Rotation Handling
        #Use the speed to calculate what the angle of the fish should be.
        #Speed ranges from -2 to 2 and angle from -20 to 20, so it is a
        #fairly straight-forward calculation.
        #Rotation is simply negative ten times speed.
        rotation = speed * -10
        #Apply the rotation.
        fish = rotate(fish, rotation)
        #Update the hitbox for the fish.
        fishrect = fish.get_rect(center=fishrect.center)

        #The speed needs to be reset to below these threshholds as the movement
        #Has now been used.
        #While the cumulative_speed is still enough to move:
        while (cumulative_speed>1) or (cumulative_speed<-1):
            #If the fish is moving down:
            if (cumulative_speed>1):
                #Lower the cumulative speed by 1
                cumulative_speed -= 1
            #The fish is moving up:
            else:
                #Increase the cumulative speed by 1.
                cumulative_speed += 1

    if fishrect.bottom > height:
        speed = -speed
        rotation += 3
        fish = rotate(fish, rotation)
        fishrect = fish.get_rect(left=fishrect.left)

    #Paint in the sea.
    screen.fill(background)

    #Update the UI of fonts.
    screen = update_UI(fonts_list, screen)
    
    screen.blit(fish, fishrect)
    #If there are rocks:
    if (len(rocks) != 0):
        #For every rock:
        for i in range(len(rocks)):
            screen.blit(rocks[i][0], rocks[i][1])
    pygame.display.flip()
