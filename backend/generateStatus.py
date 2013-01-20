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
    i = random.randint(1,10)
    if i==1:
        return "So excited to be on my way to " + destCity + "!"
    elif i==2:
        return "Ugh! Major delays. It will all be worth it when I get to "+ destCity
    elif i==3:
        return "I will be off facebook for a bit, I am going to "+destCity
    elif i==4:
        return "Getting away for a while! Going to: "+destCity
    elif i==5:
        return "Get ready for some awesome pics from "+destCity
    elif i==6:
        return ""+destCity+" here I come!!"
    elif i==7:
        return "Headed out to "+destCity+" today."
    elif i==8:
        return "Can anyone give me a ride to the airport? I need to catch a plane to "+destCity
    elif i==9:
        return destCity+"!!!!"
    else:
        return "Finally made it to the hotel in "+ destCity +"!"

def generateMiddleStatus(destCity):
    i = random.randint(1,10)
    if i==1:
        return "Ready for another exciting day in "+ destCity
    elif i==2:
        return "Wish you were here!"
    elif i==3:
        return destCity+" is great!"
    elif i==4:
        return "Thinking of staying in "+destCity+" forever!"
    elif i==5:
        return destCity + " is the shit"
    elif i==6:
        return "Time for "+destCity+", Part II"
    elif i==7:
        return "Keep watching my feed for pictures from "+destCity
    elif i==8:
        return "If you havent been to "+destCity+" you havent lived"
    elif i==9:
        return "Vacation is great"
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
