from ledmatrixtimeutil import slanted
from time import localtime
import numpy as np

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

]




def printMatrix(m):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in m]))


def setupBackground(l):
    for i in range(ROWS):
        colorIndex = 0;
        for j in range(COLS):
            if j % 2 == 1:
                colorIndex = colorIndex + 1
            l[i][j] = colorIndex

def setPixel(x, y , colorIndex=11):
    ledmatrix[ROWS - 1 - x][y] = colorIndex

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

    
ledmatrix = [ [-1] * COLS for _ in range(ROWS)]
ledmatrixNumpy = np.array(ledmatrix)
setupBackground(ledmatrixNumpy)
#setPixel(1,1)
printMatrix(ledmatrixNumpy)
print()
for i in range(10):
    print("------{}------".format(i))
    printMatrix(slanted[ord(str(i))])

currentTime = localtime()
hour = currentTime.tm_hour
minute = currentTime.tm_min

printTime(hour, minute)
print()
printMatrix(ledmatrixNumpy)



