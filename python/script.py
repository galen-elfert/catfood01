import webiopi
from webiopi.devices.serial import Serial
# import datetime

serial = Serial("ttyACM0", 9600)
catID = 0
catAte = [0.0, 0.0]
catDiet = [500, 500]
seriString = "bleh"

# setup function is automatically called at WebIOPi startup
def setup():
    # Read cat data from file

    # empty input buffer before starting
    while (serial.available() > 0):
        serial.readString()


# loop function is repeatedly called by WebIOPi 
def loop():
    # retrieve current datetime
    # now = datetime.datetime.now()
    global seriString

    if (serial.available() > 0):
        seriString = serial.readString()

    webiopi.sleep(1)

    """
    doorOpen = False
    while (not doorOpen):
        if (serial.available() > 0):
            data = serial.readString()
            seriString = data
            if (data[0] == "o"):
                catID = int(data[1])
                doorOpen = True
        webiopi.sleep(1)

    while (doorOpen):
        if (serial.available() > 0):
            data = serial.readString()
            seriString = data
            if (data[0] == "c"):
                catAte[catID] = float(data[1:])
                doorOpen = False
        webiopi.sleep(1)
    """

# destroy function is called at WebIOPi shutdown
def destroy():
    # Write cat data to file
    pass

@webiopi.macro
def getAte(ID):
    return catAte[ID]

@webiopi.macro
def setDiet(ID, food):
    catDiet[ID] = food

@webiopi.macro
def getState():
    # global seriString

    return seriString

    """
    if (doorOpen):
        return "o" + str(catID)
    else:
        return "c" + str(catID) + str(catAte[ID])
    """
