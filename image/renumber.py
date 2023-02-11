import csv
import array as arr

file1 = open('definition.csv', 'r')
Lines = csv.reader(file1)

newArr = []

num2 = 0
for line in Lines:
    #print(line)
    num = int(line[0].split(';', 1)[0])

              

    if num > 3271 and num < 3275:
        print(num)
    else:
        tempArr = line[0].split(';')
        tempArr[0] = str(num2)
        if 'ocean' in tempArr:
            tempArr[-1] = '0\n'
        else:
            tempArr[-1] = '1\n'
        
        newArr.append(';'.join(tempArr))
        num2 += 1

file1.close()
file2 = open('test.csv', 'w')
file2.writelines(newArr)
file2.close()

print(newArr[3273])
