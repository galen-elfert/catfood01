import webiopi
from webiopi.devices.serial import Serial
# import datetime

serial = Serial("ttyACM0", 9600)
catID = 0
catAte = [0.0, 0.0]
catFull = [0, 0]
catDiet = [250, 250]
status = "c:0:0.0:0:0.0"

# setup function is automatically called at WebIOPi startup
def setup():
    # Read cat data from file
    global status, catID, catAte, catFull

    # empty input buffer before starting
    while (serial.available() > 0):
        serial.readString()


# loop function is repeatedly called by WebIOPi 
def loop():
    # retrieve current datetime
    # now = datetime.datetime.now()
    global status, catID, catAte, catFull
    doorOpen = False
    
    while (not doorOpen):
        if (serial.available() > 0):
            data = serial.readString()
            if (data[0] == "o"):
                catID = int(data[1])
                if (catAte[catID] < catDiet[catID]):
                    serial.writeString("1")
                    status = data
                    doorOpen = True
                else:
                    serial.writeString("0")
        webiopi.sleep(0.5)

    while (doorOpen):
        if (serial.available() > 0):
            data = serial.readString()
            if (data[0] == "c"):
                catAte[catID] = round((catAte[catID] + float(data[1:])), 2)
                if(catAte[catID] > catDiet[catID]):
                    catFull[catID] = 1
                else:
                    catFull[catID] = 0
                status = "c:" + str(catFull[0]) + ":" + str(catAte[0]) + ":" + str(catFull[1]) + ":"+ str(catAte[1])
                doorOpen = False
        webiopi.sleep(1)


# destroy function is called at WebIOPi shutdown
def destroy():
    # Write cat data to file
    pass

@webiopi.macro
def getDiet(ID):
    #global catDiet
    return catDiet[ID]

@webiopi.macro
def setDiet(ID, food):
    global catDiet
    catDiet[ID] = food

@webiopi.macro
def getState():
    #global status
    return status
