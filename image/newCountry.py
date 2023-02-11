import csv
import array as arr
import string

file1 = open('needHx.txt', 'r')
needLines = file1.readlines()
file1.close
file2 = open('00_countries.txt', 'r')
baseLines = file2.readlines()

keyedCodes = []

needCodes = []

for line in needLines:
    code = line.split('-')[0].split(':')[-1].strip()
    needCodes.append(code)


for line in baseLines:
    code = line.split('=')[0].strip()
    if code in needCodes:
        country = line.split('.txt')[0].split('/')[1]
        keyedCodes.append([code, country])

    
for pair in keyedCodes:
    code = pair[0]
    name = pair[1]
    file3 = open(code + " - " + name + '.txt', 'w')
    file3.write('capital=1')
    file3.close
