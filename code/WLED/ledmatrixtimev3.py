from ledmatrixtimeutil2 import slanted
from time import localtime, sleep
import numpy as np
import sacn


class LEDMatrix:
    ROWS = 7
    COLS = 20
    WLED_ADDRESS = "192.168.20.45"

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


    def __init__(self):
        self.LEDMatrix = np.array([ [-1] * LEDMatrix.COLS for _ in range(LEDMatrix.ROWS)])

    def drawBackground(self):
        for i in range(LEDMatrix.ROWS):
            colorIndex = 0;
            for j in range(LEDMatrix.COLS):
                if j % 2 == 1:
                    colorIndex = colorIndex + 1
                self.LEDMatrix[i][j] = colorIndex        

    def drawTime(self, h, m):
        # print colon first
        matrixColon = slanted[ord(':')]
        matrixColonNumpy = np.array(matrixColon)
        #LEDMatrixNumpy[1:5, 1:3] = matrixColonNumpy
        self.LEDMatrix[2:6, 9:11] = matrixColonNumpy

        # print one if hour greater than or equal to 10
        if h >= 10:
            matrixOne = slanted[ord('1')]
            matrixOneNumpy = np.array(matrixOne)
            self.LEDMatrix[1:6, 0:4] = matrixOneNumpy
            h = h % 10

        matrixH = slanted[ord(str(h))]
        matrixHNumpy = np.array(matrixH)
        self.LEDMatrix[1:6, 5:9] = matrixHNumpy   

        mm = m // 10
        mmm = m % 10
        
        matrixMM = slanted[ord(str(mm))]
        matrixMMNumpy = np.array(matrixMM)
        self.LEDMatrix[1:6, 12:16] = matrixMMNumpy   

        matrixMMM = slanted[ord(str(mmm))]
        matrixMMMNumpy = np.array(matrixMMM)
        self.LEDMatrix[1:6, 16:20] = matrixMMMNumpy         

    def prepareMessage(self):
        row = 0
        col = 0
        dmxMessage = [0]*512

        for i in LEDMatrix.mapping:
            for j in i:
                #print(f"i:{i} j:{j} col: {LEDMatrixNumpy[row][col]}")
                red,green,blue = LEDMatrix.colors[self.LEDMatrix[row][col]]
                index = 3*LEDMatrix.mapping[row][col]
                dmxMessage[index] = red
                dmxMessage[index + 1] = green
                dmxMessage[index + 2] = blue
                col = col + 1
            row = row + 1
            col = 0

        print(dmxMessage)
        return dmxMessage        


    def sendMessage(self, msg):
        sender = sacn.sACNsender() 
        sender.start() 
        sender.activate_output(1) # Universe 1

        sender[1].multicast = False  # Unicast
        sender[1].destination = LEDMatrix.WLED_ADDRESS 
        sender.manual_flush = True
        sender[1].dmx_data = msg
        #sleep(1)
        sender.flush()
        sender.manual_flush = False
        sender.stop()        

    def sendUpdate(self):
        message = self.prepareMessage()
        self.sendMessage(message)


def main():
    matrix = LEDMatrix()
    oldHour=None
    oldMinute=None
    while True:
        currentTime = localtime()
        hour = currentTime.tm_hour
        minute = currentTime.tm_min
        if oldHour != hour and oldMinute != minute:

            matrix.drawBackground()
            h = hour - 12 if hour > 12 else hour 
            matrix.drawTime(h, minute)
            matrix.sendUpdate()
            oldHour = hour
            oldMinute = minute
        sleep(1)


if __name__ == '__main__':
    main()

