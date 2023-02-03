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

def changeCol(x, y):
    colour = imgArr[x][y]
    imgArr[x+1][y] = colour
    imgArr[x][y+1] = colour
    imgArr[x+1][y+1] = colour


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

    #define horizontal lines
    hLines = []
    tempLine = []
    while(len(edgeArr) > 1):
        first = edgeArr[0]
        second = edgeArr[1]
        if first[1] + 1 == second[1]:
            tempLine.append(first)
            if len(edgeArr) == 1:
                tempLine.append(second)
            edgeArr = edgeArr[1:]


        else:
            if(len(tempLine) > 0):
                hLines.append(tempLine)
            else:
                hLines.append([first])
            tempLine = []
            edgeArr = edgeArr[1:]



    #indexed array [x,yAvg]
    posArr = []
    for line in hLines:
        yRange = [10000000000,0]
        for coord in line:
            if coord[1] < yRange[0]:
                yRange[0] = coord
            if coord[1] > yRange[1]:
                yRange[1] = coord
        x = line[0][0]
        y = (yRange[0] + yRange[1]) / 2
        posArr.append([x,y])



    #need to seperate shapes from Lines
    posArrCopy = posArr
    while len(posArr) > 1:









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


replaceCol()
