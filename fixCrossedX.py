from PIL import Image
import numpy as np

imgArr = np.array(Image.open('provinces.bmp'))#.reshape(512, 512, 3)
xmax = 5632
ymax = 2048

def unique(arr1,arr2):
    if all(arr1 == arr2) or np.all(arr1 == arr2):
        return False
    else:
        return True
#------------------------------------------------------------------------------------------------------------

def changeCol(x, y):
    colour = imgArr[x][y]
    imgArr[x+1][y] = colour
    imgArr[x][y+1] = colour
    imgArr[x+1][y+1] = colour
#------------------------------------------------------------------------------------------------------------

def overlap(first, second):
    x1 = first[0]
    x2 = first[0]
    y1 = second[0]
    y2 = second[1]

    if any([(y1 > x1 and y1 < x2), (x1 > y1 and x1 < y2), x1 == y1, x1 == y2, x2 == y1, x2 == y2]):
        return True
    else:
        return False
#------------------------------------------------------------------------------------------------------------

def edgeLines():
    #get all [255,255,255] pixels that are the edge
    edgeArr = []
    for i in range(0,ymax-2):
        for r in range(0,xmax-2):
            if all(imgArr[i][r] == col):
                pix = imgArr[i][r]
                colArr.append([i,r])
                ul = imgArr[i-1][r-1]
                uu = imgArr[i-1][r]
                ur = imgArr[i-1][r+1]
                ll = imgArr[i][r-1]
                rr = imgArr[i][r+1]
                dl = imgArr[i+1][r-1]
                dd = imgArr[i+1][r]
                dr = imgArr[i+1][r+1]
                fourSquare = [ul, uu, ur, ll, rr, dl, dd, dr]
                sameArr = []
                for sqr in fourSquare:
                    sameArr.append(unique(pix, sqr))
                if (any(sameArr)):
                    edgeArr.append([i,r])

    fileWriter = open("edgeArr.txt", "w")
    for edge in edgeArr:
        fileWriter.write(str(edge) + "/n")
    fileWriter.close
#------------------------------------------------------------------------------------------------------------

def getHLines():
    col = np.array([255,255,255]).astype('uint8')

    #get all pixels that are [255,255,255]
    colArr = []
    #get all [255,255,255] pixels that are the edge
    edgeArr = []
    for i in range(0,ymax-2):
        for r in range(0,xmax-2):
            if all(imgArr[i][r] == col):
                pix = imgArr[i][r]
                colArr.append([i,r])
                ul = imgArr[i-1][r-1]
                uu = imgArr[i-1][r]
                ur = imgArr[i-1][r+1]
                ll = imgArr[i][r-1]
                rr = imgArr[i][r+1]
                dl = imgArr[i+1][r-1]
                dd = imgArr[i+1][r]
                dr = imgArr[i+1][r+1]
                fourSquare = [ul, uu, ur, ll, rr, dl, dd, dr]
                sameArr = []
                for sqr in fourSquare:
                    sameArr.append(unique(pix, sqr))
                if (any(sameArr)):
                    edgeArr.append([i,r])

    #define horizontal lines
    hLines = []
    tempLine = []
    for first in colArr:
        second = colArr[colArr.index(first) + 1]
        if first[1] + 1 == second[1]:
            tempLine.append(first)
            if colArr.index(second) + 1 == len(colArr):
                tempLine.append(second)
                hLines.append(tempLine)
                break
        else:
            if(len(tempLine) > 0):
                hLines.append(tempLine)
            else:
                hLines.append([first])
            if colArr.index(second) + 1 == len(colArr):
                break
            tempLine = []


    fileWriter = open("hlines.txt", "w")
    for line in hLines:
        fileWriter.write(str(line) + "/n")
    fileWriter.close
    fileWriter = open("edgeArr.txt", "w")
    for edge in edgeArr:
        fileWriter.write(str(edge) + "/n")
    fileWriter.close
    print("finished writing")
    #------------------------------------------------------------------------------------------------------------
def getVLines():
    col = np.array([255,255,255]).astype('uint8')

    #get all pixels that are [255,255,255]
    colArr = []
    for r in range(0,xmax-2):
        for i in range(0,ymax-2):
            if all(imgArr[i][r] == col):
                colArr.append([i,r])

    #define verticle lines
    vLines = []
    tempLine = []
    for first in colArr:
        second = colArr[colArr.index(first) + 1]
        if first[0] + 1 == second[0]:
            tempLine.append(first)
            if colArr.index(second) + 1 == len(colArr):
                tempLine.append(second)
                vLines.append(tempLine)
                break
        else:
            if(len(tempLine) > 0):
                vLines.append(tempLine)
            else:
                vLines.append([first])
            if colArr.index(second) + 1 == len(colArr):
                break
            tempLine = []


    fileWriter = open("vlines.txt", "w")
    for line in vLines:
        fileWriter.write(str(line) + "/n")
    fileWriter.close

    print("finished writing")
#------------------------------------------------------------------------------------------------------------



def fixX():
    file1 = open('crossedX.txt', 'r')
    Lines = file1.readlines()


    coords = []

    strCoord = ''
    for line in Lines:
        strCoord = line.split(":")[-1].strip()
        x = int(strCoord.split(',')[0])
        y = int(strCoord.split(',')[1])
        coords.append([x,y])
        if y > 2048 or x > 5632:
            print("x is " + str(x) + " and y is " + str(y) + " overflow")





    for coord in coords:
        x = coord[0]
        y = coord[1]
        sideLength = 25 # half the size of search box for crosses

        lenMod = False
        if (x - sideLength) < 0:
            print('1')
            sideLength = 25 + (x - sideLength) - 1
            lenMod = True
        elif (x + sideLength - 1) > xmax:
            if not lenMod or (lenMod and ((x + sideLength - 1) > ((x - sidelength) * -1))):
                print('2')
                sidelength  = 25 - ((x + sideLength - 1) % xmax)
                lenMod = True
        elif (y - sideLength) < 0:
            if not lenMod or (lenMod and ((y - sideLength < 0) > (x + sideLength - 1))):
                print('3')
                sideLength = 25 + (y - sideLength) - 1
                lenMod = True
        elif (y + sideLength - 1) > ymax:
            if not lenMod or (lenMod and ((y + sideLength) > ((y - sideLength < 0) * -1))):
                print('4')
                sideLength = 25 - ((y + sideLength - 1) % ymax)

        if sideLength != 25:
            print("len " + str(sideLength))
        #smImg = imgArr[list(range(x-sideLength),(x+sideLength-1)))][list(range((y-sideLength),(y+sideLength-1)))]
        #smImgTemp = imgArr[(x-sideLength):(x+sideLength-1)]     #[(y-sideLength):(y+sideLength-1)]
        smImg = []
        for i in range(0,sideLength * 2):
            smImg.append(imgArr[i][(y-sideLength):(y+sideLength-1)])


        #(n-1)^2 vertices length with 4 depth each with 4 RGB tuplets (primary and 3 comparasins)
        #if 3 comparasins are unique and none the same as primary then change all 4 RGB tuplets
        #to primary
        for i in range(0, (sideLength * 2)):
            if (i + 1) % (sideLength * 2) == 0:
                continue
            for r in range(0, (sideLength * 2) - 2):
                #print(i)
                #print(r)

                fourSquare = [smImg[i][r], smImg[i+1][r], smImg[i][r+1], smImg[i+1][r+1]]

                prim = fourSquare[0]
                sec1 = fourSquare[1]
                sec2 = fourSquare[2]
                sec3 = fourSquare[3]
                if(unique(sec1, sec2) and unique(sec1, sec3) and unique(sec2, sec3) and unique(prim, sec1) and unique(prim, sec2) and unique(prim, sec3)):
                    xpos = y - sideLength + (i % (sideLength * 2))
                    ypos = x - sideLength + (int(i / (sideLength * 2)))
                    changeCol(xpos, ypos)
                    print("\n[" + str(xpos) + "," + str(ypos) + "]\n")





#need to change each shape of [255,255,255] into a random RGB colour and fix the border
def replaceCol():





    #indexed array [x,yStart, yEnd, yAvg]
    posArr = []
    for line in hLines:
        yRange = [10000000000,0]
        for coord in line:
            if coord[1] < yRange[0]:
                yRange[0] = coord[1]
            if coord[1] > yRange[1]:
                yRange[1] = coord[1]
        x = line[0][0]
        y = int((yRange[0] + yRange[1]) / 2)
        posArr.append([x,yRange[0], yRange[1], y])

    #seperate horizontal flat edges from verticle edges


    #need to seperate shapes from Lines
    posArrCopy = posArr
    shapes = [[]]
    midShape = False
    firstLine = []
    tempShape = []
    i = 0


    #print(hLines[0:25])
    print(posArr[0:25])

    while len(posArrCopy) > 1:
        posArrCopy.sort(key = lambda x: (x[0],x[1]))
        if midShape == False:
            firstLine = posArrCopy[0]
        possibleSecond = []
        for line in posArrCopy:
            if line[0] - 1 == firstLine[0]:
                possibleSecond.append(line)
        secondLine = possibleSecond[0]
        for line in possibleSecond:
            if abs(secondLine[3] - firstLine[3]) > abs(line[3] - firstLine[3]):
                secondLine = line
        print(firstLine)
        print(secondLine)
        if overlap([firstLine[1], firstLine[2]], [secondLine[1], secondLine[2]]) == False:
            shapes.append(tempShape)
            tempShape = []
        elif overlap([firstLine[1], firstLine[2]], [secondLine[1], secondLine[2]]):
            print("/n/ninside/n/n")
            midShape = True
            index = posArrCopy.index(firstLine)
            posArrCopy = posArrCopy[0:index] + posArrCopy[index+1:]
            firstLine = secondLine
        i += 1
        if i == 25:
            break
        print(len(posArrCopy))




    #for i in range(0,ymax-2):
    #    for r in range(0,xmax-2):
    #        if all(imgArr[i][r] == col):
    #            if not all((imgArr[i-1][r]) == col):
    #                imgArr[i-1][r] = col
    #            if not all((imgArr[i][r-1]) == col):
    #                imgArr[i][r-1] = col
    #        if not(all(imgArr[i][r] == col)):
    #            if all(imgArr[i+1][r] == col):
    #                imgArr[i+1][r] = col
    #            if all(imgArr[i][r+1] == col):
    #                imgArr[i][r+1] = col


def saveImg():

    finalImg = Image.fromarray(imgArr, 'RGB')

    finalImg.save('preovincesAltered.bmp')


#replaceCol()
getVLines()
