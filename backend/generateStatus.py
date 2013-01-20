import random

###########################################
#   NEED TO CHANGE TO ACTUAL DATA NAMES   #
#   NEED TO FIGURE OUT HOW TO CALL THIS   #
###########################################

#keys used
destinationCity = "destinationCity"
destinationRegion = "destinationRegion"
sourceCity = "sourceCity"
hotelName = "hotelName"


def generateFirstStatus(destCity):
    i = random.randint(1,3)
    if i==1:
        return "So excited to be on my way to " + destCity + "!"
    elif i==2:
        return "Ugh! Major delays. It will all be worth it when I get to "+ destCity
    else:
        return "Finally made it to the hotel in "+ destCity +"!"

def generateMiddleStatus(destCity):
    i = random.randint(1,3)
    if i==1:
        return "Ready for another exciting day in "+ destCity
    elif i==2:
        return "Wish you were here!"
    else:
        return "I dont think I will ever leave "+destCity

def generateEndStatus(destCity):
        return "Its been a good trip, but I am glad to be home."


def generateImageTag(destCity):
    i = random.randint(1,4)
    if i == 1:
        return "Having a great time in " +destCity+"!"
    elif i == 2:
        return "I cant believe I'm here!!!"
    elif i == 3:
        return "This one looks a little shopped..."
    else:
        return "I wonder how long I can hold this pose?"
