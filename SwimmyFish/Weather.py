from enum import enum

class Weather():
    #Stores the types of weather
    weather = None

    #Used to store the chances of advancing to other weather types
    smooth = None
    slight = None
    moderate = None
    choppy = None
    rough = None
    stormy = None

    #Used to store the current weather state
    current = None

    #An enum for the types of weather
    class Types(Enum):
        SMOOTH = 0
        SLIGHT = 1
        MODERATE = 2
        CHOPPY = 3
        ROUGH = 4
        STORMY = 5

    def __init__(self):
        #Initialises the enum for the different types of weather.
        self.weather = Enum('Types', ['SMOOTH', 'SLIGHT', 'MODERATE', 'CHOPPY', 'ROUGH', 'STORMY'])

        #Initialises all of the weather classes for probability usage.
        self.smooth = Smooth()
        self.slight = Slight()
        self.moderate = Moderate()
        self.choppy = Choppy()
        self.rough = Rough()
        self.stormy = Stormy()

        #Intialises the state of the weather to slight.
        self.current = self.weather.SLIGHT
