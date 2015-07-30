import os
import sys

# to transform the google downloaded data to usable format
txtfile1 = open('apple/1.txt', 'r')
p1 = []
for line in txtfile1:
	p1.append(line)
txtfile2 = open('apple/2.txt', 'r')
p2 = []
for line in txtfile2:
	p2.append(line)
txtfile1.close()
txtfile2.close()
#print p1
#print p2
images = os.listdir('apple/images')
output = open('apple/info.txt', 'w')
i, j, k = 0, 0, 0
p = []
while i < len(images):
	if images[i][0] == '1':
		p.append(images[i][:-4] + '\t' + p1[j].replace('_', ' '))
		j += 1
	elif images[i][0] == '2':
		p.append(images[i][:-4] + '\t' + p2[k].replace('_', ' '))
		k += 1
	i += 1
for x in p:
	output.write(x)
output.close()
