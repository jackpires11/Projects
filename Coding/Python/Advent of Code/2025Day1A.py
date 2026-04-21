#The number the safe dial starts at.
INITIAL_NUMBER = 50
INITIAL_PASSWORD = 0
FILE_NAME = '2025Day1AInputs.txt'

#Initialises the starting number the dial is on for performing inputs.
current = INITIAL_NUMBER

#Initialises the password at 0.
password = INITIAL_PASSWORD

#Open the inputs file for reading.
f = open(FILE_NAME)

#For each step of the sequence:
for step in f:

    #If the start of the input is to turn left:
    if step[0] == 'L':
        current -= int(step[1:])
        current = current % 100
    #If the start of the input is to turn right:
    else:
        current += (int(step[1:]))
        current = current % 100

    #If the dial is at zero:
    if current == 0:
        #Increment the password.
        password += 1
        
f.close()
print(password)
