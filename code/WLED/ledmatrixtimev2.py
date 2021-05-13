from ledmatrixtimeutil2 import slanted
from time import localtime
import numpy as np
import sacn

ROWS = 7
COLS = 20

colors = [
    (158,194,230), #Blue10
    (104,222,124), #Green10
    (0,186,55), #Green30
    (242,214,117), #Yellow10
    (255, 165,0), #Orange
    (255,127,80), #Peach
    (255,0,255), #fuchsia
    (148,0,211), #dark violet
    (19,94,150), #blue
    (158,194,230), #Blue10
    (255,255,255), #white
    (0,0,0) #black
]

mapping = [
[9,10,23,24,34,38,51,52,65,66,79,80,93,94,107,108,121,128,129,130],
[8,11,22,25,36,39,50,53,64,67,78,81,92,95,106,109,120,122,131,132],
[0,7,12,21,26,35,40,49,54,63,68,77,82,91,96,105,110,119,123,133],
[1,6,13,20,27,34,41,48,55,62,69,76,83,90,97,104,111,118,124,127],
[134,2,5,14,19,28,33,42,47,56,61,70,75,84,89,98,103,112,117,125],
[135,136,4,15,18,29,32,43,46,57,60,71,74,85,88,99,102,113,116,126],
[137,138,139,3,16,17,30,31,44,45,58,59,72,73,86,87,100,101,114,115]
]

def printCharMatrix(m):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in m]))


def printLEDMatrix(l):
    m = l.tolist()
    #m.reverse()
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in m]))

def setupBackground(l):
    for i in range(ROWS):
        colorIndex = 0;
        for j in range(COLS):
            if j % 2 == 1:
                colorIndex = colorIndex + 1
            l[i][j] = colorIndex

def setPixel(x, y , colorIndex=11):
    ledmatrixNumpy[x][y] = colorIndex
    #ledmatrixNumpy[ROWS - 1 - x][y] = colorIndex

def printTime(h, m):
    # print colon first
    matrixColon = slanted[ord(':')]
    matrixColonNumpy = np.array(matrixColon)
    #ledmatrixNumpy[1:5, 1:3] = matrixColonNumpy
    ledmatrixNumpy[2:6, 9:11] = matrixColonNumpy

    # print one if hour greater than or equal to 10
    if h >= 10:
        matrixOne = slanted[ord('1')]
        matrixOneNumpy = np.array(matrixOne)
        ledmatrixNumpy[1:6, 0:4] = matrixOneNumpy
        h = h % 10

    matrixH = slanted[ord(str(h))]
    matrixHNumpy = np.array(matrixH)
    ledmatrixNumpy[1:6, 5:9] = matrixHNumpy   

    mm = m // 10
    mmm = m % 10
    
    matrixMM = slanted[ord(str(mm))]
    matrixMMNumpy = np.array(matrixMM)
    ledmatrixNumpy[1:6, 12:16] = matrixMMNumpy   

    matrixMMM = slanted[ord(str(mmm))]
    matrixMMMNumpy = np.array(matrixMMM)
    ledmatrixNumpy[1:6, 16:20] = matrixMMMNumpy       

def prepareMessage():
    row = 0
    col = 0
    dmxMessage = [0]*512

    for i in mapping:
        for j in i:
            #print(f"i:{i} j:{j} col: {ledmatrixNumpy[row][col]}")
            red,green,blue = colors[ledmatrixNumpy[row][col]]
            index = 3*mapping[row][col]
            dmxMessage[index] = red
            dmxMessage[index + 1] = green
            dmxMessage[index + 2] = blue
            col = col + 1
        row = row + 1
        col = 0

    print(dmxMessage)
    return dmxMessage

def sendMessage(msg):
    sender = sacn.sACNsender()  # provide an IP-Address to bind to if you are using Windows and want to use multicast
    sender.start()  # start the sending thread
    sender.activate_output(1)  # start sending out data in the 1st universe

    sender[1].multicast = False  # set multicast to True
    sender[1].destination = "192.168.20.45"  # or provide unicast information.
    sender.manual_flush = True
    sender[1].dmx_data = msg
    #time.sleep(1)
    sender.flush()
    sender.manual_flush = False
    sender.stop()

    
ledmatrix = [ [-1] * COLS for _ in range(ROWS)]
ledmatrixNumpy = np.array(ledmatrix)
setupBackground(ledmatrixNumpy)
#setPixel(1,1)
#printLEDMatrix(ledmatrixNumpy)
#print()
#for i in range(10):
#    print("------{}------".format(i))
#    printCharMatrix(slanted[ord(str(i))])

currentTime = localtime()
hour = currentTime.tm_hour
minute = currentTime.tm_min

printTime(hour, minute)
print()
printLEDMatrix(ledmatrixNumpy)
print(f"pixel value at (1,6): {ledmatrixNumpy[1][6]}")

dmxMessage = prepareMessage()
sendMessage(dmxMessage)

