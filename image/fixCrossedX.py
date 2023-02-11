from PIL import Image
import numpy as np

imgArr = np.array(Image.open('provinces2.bmp'))#.reshape(512, 512, 3)
xmax = 2056#xmax = 5632
ymax = 873 #ymax = 2048
col = np.array([255,255,255]).astype('uint8')

numShapes = 0

whitePixels = []

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

def getEdgeArr():
    print("started edgeArr()")
    col = np.array([255,255,255]).astype('uint8')

    #get all [255,255,255] pixels that are the edge
    edgeArr = []
    for i in range(0,ymax-2):
        for r in range(0,xmax-2):
            if all(imgArr[i][r] == col):
                pix = imgArr[i][r]
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
    print("finished edgeArr()")
    return edgeArr
    #fileWriter = open("edgeArr.txt", "w")
    #for edge in edgeArr:
    #    fileWriter.write(str(edge) + "/n")
    #fileWriter.close
#------------------------------------------------------------------------------------------------------------

def getHLines(edgeArr):
    print("started hLines()")
    colArr = sorted(edgeArr, key = lambda x: (x[1], x[0]))

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
                hLines.append(first)
            if colArr.index(second) + 1 == len(colArr):
                break
            tempLine = []


    print("finished hLines()")

    return hLines
#------------------------------------------------------------------------------------------------------------
def getVLines(edgeArr):
    print("started vLines()")
    colArr = sorted(edgeArr, key = lambda x: (x[0], x[1]))

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
                vLines.append(first)
            if colArr.index(second) + 1 == len(colArr):
                break
            tempLine = []

    print("finsished vLines")
    return vLines
    #fileWriter = open("vlines.txt", "w")
    #for line in vLines:
    #    fileWriter.write(str(line) + "/n")
    #fileWriter.close

    print("finished writing")
#------------------------------------------------------------------------------------------------------------
def cleanLines(hLines, vLines):
    for line in hLines:
        if (len(line) == 1) and (line in vLines == False):
            hLines.pop(hLines.index(line))
    for line in vLines:
        if(len(line) == 1) and (line in hLines == False):
            vLines.pop(vLines.index(line))
    return [hLines, vLines]
#------------------------------------------------------------------------------------------------------------

def checkAdjacentBootstrap(x, y):
    if(notInArr(x, y)):
        # numShapes = numShapes + 1
        checkAdjacent(x, y)

def findNumShapes():
    for i in range(0, xmax - 1):
        for j in range(0, ymax - 1):
            checkAdjacentBootstrap(i, j)
    # print(numShapes)

def notInArr(x, y):
    for subArr in whitePixels:
        if subArr[0] == x and subArr[1] == y:
            return False
    return True
num = 0
def checkAdjacent(x, y):
    global num
    num += 1
    print(num)
    if(all(imgArr[x + 1][y] == col) and notInArr(x + 1, y)):
        # I think there is a better way to store this data
        # shrug
        whitePixels.append([x, y])
        checkAdjacent(x + 1, y)
    if(all(imgArr[x - 1][y] == col) and notInArr(x - 1, y)):
        # I think there is a better way to store this data
        # shrug
        whitePixels.append([x, y])
        checkAdjacent(x - 1, y)
    if(all(imgArr[x][y + 1] == col) and notInArr(x, y + 1)):
        # I think there is a better way to store this data
        # shrug
        whitePixels.append([x, y])
        checkAdjacent(x, y + 1)
    if(all(imgArr[x][y - 1] == col) and notInArr(x, y - 1)):
        # I think there is a better way to store this data
        # shrug
        whitePixels.append([x, y])
        checkAdjacent(x, y - 1)

def getShapes():
    print("started shapes")
    edgeArr = getEdgeArr()
    hLines = getHLines(edgeArr)
    vLines = getVLines(edgeArr)

    print("cleanLines")
    temp = cleanLines(hLines, vLines)
    hLines = temp[0]
    vLines = temp[1]


    #create indexed arr [hlineIndex, [vlineIndices . . .]]]
    hIndexedArr = []
    hShort = []
    h = 0
    for hLine in hLines:
        v = -1
        hIndexedArr.append([h,[]])
        hShort.append(h)
        for pix in hLine:
            for vLine in vLines:
                v += 1
                if pix in vLine:
                    hIndexedArr[h][1].append(v)
        h += 1

    vIndexedArr = []
    vShort = []
    v = 0
    for vLine in vLines:
        h = -1
        vIndexedArr.append([v,[]])
        vShort.append(v)
        for pix in vLine:
            for hLine in hLines:
                h += 1
                if pix in hLine:
                    vIndexedArr[v][1].append(h)
        v += 1
    print("\nindexedArr horizontal")
    print(hIndexedArr[0:10])
    print("\nhLines")
    print(hLines[0:10])
    shapes = []
    done = False
    index = 0
    while (len(shapes) < 5):
        print("inside while < 5")
        tempShapeH = []
        tempShapeV = []
        hs = [hIndexedArr[index]]
        vs = []

        #ensure horizontal line isnt already apart of a shape
        #change done to true to exit loop
        newH = False
        while newH == False:
            newH = True
            for shape in shapes:
                if hs[0][0] in shapes[0]:
                    index += 1
                    newH = False
                    if index < len(hIndexedArr):
                        hs[0] = hIndexedArr[index]
                    else:
                        done = True
        if done:
            print("done")
            break

        for v in hIndexedArr[0][1]:
            vs.append(vIndexedArr[v])

        #find all horizontal and vertical lines attached to each other
        new = True
        print("inside While new():")

        while new:
            for h in hs:
                tempShapeH.append(h[0])
            for v in vs:
                tempShapeV.append(v[0])
            #add new verticle and horizontal lines
            for h in hs:
                for v in h[1]:
                    vs.append(vIndexedArr[v])
            for v in vs:
                for h in v[1]:
                    hs.append(hIndexedArr[h])
            #remove overlap already in temp arrays
            hstemp = hs
            for h in hstemp:
                if h[0] in tempShapeH:
                    hs.pop(h[0])
            vstemp = vs
            for v in vstemp:
                if v[0] in tempShapeV:
                    vs.pop(v[0])
            print(len(shapes))
            #all iterations ran through
            if(len(hs) == 0) and (len(vs) == 0):
                new = False
                print("hlines")
                print(tempShapeH)
                shapes.append([tempShapeH,tempShapeV])

    print(shapes)

    #get actual lines, not vlineIndices
    for shape in shapes:
        for h in shape[0]:
            shape[0][h] = [hLines[h][0],hLines[h][-1]]
        for v in shape[1]:
            shape[1][v] = [vLines[v][0],vLines[v][-1]]

    print(shapes)

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
#------------------------------------------------------------------------------------------------------------





#need to change each shape of [255,255,255] into a random RGB colour and fix the border
def replaceCol(shape):
    #help





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
#------------------------------------------------------------------------------------------------------------




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
#------------------------------------------------------------------------------------------------------------

# getShapes()
findNumShapes()
