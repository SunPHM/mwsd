import os
import sys
from sklearn import linear_model

a = 0.8

def readResults(filename):
    	res_map = {}
	ls = []
	ps = []
	ts = []
    	f = open(filename,"r+")
        for line in f:
        	tup = []
		es = line.split();
	       	tup.append(int(es[1]))
		tup.append(float(es[2]))
		tup.append(float(es[3]))
		tup.append(int(es[4]))
		res_map[es[0]] = tup
	f.close()
	return res_map
	
def getCMatrix(rmap):
	m00, m01, m10, m11 = 0, 0, 0, 0
	for k in rmap:
		tup = rmap[k]
		if tup[3] == 1:
			if tup[0] == tup[3]:
				m00 += 1
			else:
				m01 += 1
		else:
			if tup[0] == tup[3]:
				m11 += 1
			else:
				m10 += 1
	print m00, m01, m10, m11
	return m00, m01, m10, m11

def maxfusion(imap, tmap):
	mmap = {}
	for k in imap:
		if k not in tmap:
			continue
		it = imap[k]
		tt = tmap[k]
		p1 = it[it[0]]
		p2 = 0.0
		if tt[0] != 0:
			p2 = tt[tt[0]]
		if p1 > p2:
			mmap[k] = it
		else:
			mmap[k] = tt
	return mmap

def linearfusion(imap, tmap):
	lmap = {}
        for k in imap:
                if k not in tmap:
                        continue
                it = imap[k]
                tt = tmap[k]
                s1 = a * it[1] + (1 - a) * tt[1]
                s2 = a * it[2] + (1 - a) * tt[2]
		p1 = s1 / (s1 + s2)
		p2 = 1 - p1
                lt = []
		if p1 > p2:
			lt.append(1)
		else:
			lt.append(2)
		lt.append(p1)
		lt.append(p2)
		lt.append(it[3])
		lmap[k] = lt
		#print it[3], it[0], tt[0], lt[0], it[1], it[2], tt[1], tt[2]
        return lmap


def logfusion():
	print ""


print "image"
imap = readResults(sys.argv[1])
getCMatrix(imap)
print "text"
tmap = readResults(sys.argv[2])
getCMatrix(tmap)
print "max-rule fusion"
mmap = maxfusion(imap, tmap)
getCMatrix(mmap)
print "linear-rule fusion"
lmap = linearfusion(imap, tmap)
getCMatrix(lmap)
