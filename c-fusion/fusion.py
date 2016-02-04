import os
import sys
from sklearn import linear_model

word = "bass"
a = 0.6

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
	m00, m01, m10, m11, m02, m03, m12, m13 = 0, 0, 0, 0, 0, 0, 0, 0
	for k in rmap:
		tup = rmap[k]
		if tup[3] == 1:
			if tup[0] == tup[3]:
				m00 += 1
			else:
				m01 += 1
				if tup[0] == 0:
					m02 += 1
				else:
					m03 += 1
		else:
			if tup[0] == tup[3]:
				m11 += 1
			else:
				m10 += 1
				if tup[0] == 0:
					m12 += 1
				else:
					m13 += 1
	#print m00, m01, m02, m03
	#print m10, m11, m12, m13
	print 'coverage = ' + str(1 - float(m12 + m02) / (m00 + m01 + m10 + m11)) 
	print 'average precision = ' + str((float(m00) / (m00 + m03) + float(m11) / (m11 + m13)) / 2)
	print 'average recall = ' + str((float(m00) / (m00 + m01) + float(m11) / (m11 + m10)) / 2)
	return m00, m01, m10, m11

def compute_weight(vimap, vtmap):
	a1 = 0
	a2 = 0
	s = 0
	for k in vimap:
		if k not in vtmap: continue
		s += 1
		if vimap[k][0] == vimap[k][3]:
			a1 += 1
		if vtmap[k][0] == vtmap[k][3]:
			a2 += 1
	p1 = float(a1) / float(s)
	p2 = float(a2) / float(s)
	return p1 / (p1 + p2) 

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


def logfusion(vimap, vtmap, imap, tmap):
	lr = linear_model.LogisticRegression()
	# read features and labels
	X = []
	y = []
	for k in vimap:
		if k not in vtmap: continue
		p = []
		p.append(vimap[k][0])
		p.append(vimap[k][1])
		p.append(vimap[k][2])
		p.append(vtmap[k][0])
		p.append(vtmap[k][1])
		p.append(vtmap[k][2])
		X.append(p)
		y.append(vimap[k][3])
	# train logistic regression
	lr.fit(X, y)
	# run the lr classifier on testing data and store the results		
	rmap = {}
	keys = []
	features = []
	truth = []
	for k in imap:
		if k not in tmap: continue
		feature = []
		feature.append(imap[k][0])
		feature.append(imap[k][1])
		feature.append(imap[k][2])
		feature.append(tmap[k][0])
		feature.append(tmap[k][1])
		feature.append(tmap[k][2])
		features.append(feature)
		keys.append(k)
		truth.append(imap[k][3])
	
	labels = lr.predict(features)
	probs = lr.predict_proba(features)
	for i in range(len(keys)):
		tup = []
		tup.append(labels[i])
		tup.append(probs[i][0])
		tup.append(probs[i][1])
		tup.append(truth[i])
		rmap[keys[i]] = tup
			
	#getCMatrix(rmap)
	#print "logistic regression is done"
	return rmap 

def printResults(word, imap, tmap, lmap, mmap, rmap):
	txtfile = open(word + "-raw-results.txt", 'w')
	txtfile.write('results for each method are shown as [sense label, confidence score for sense 1, confidence score for sense 2]\n')
	txtfile.write('1 for sense 1, 2 for sense 2, 0 for the undetermined sense\n')
	txtfile.write('true-sense\timage\ttext\tlinear\tmax\tlog-reg\n')
	for k in imap:
		txtfile.write(str(imap[k][3]) + '\t')
		txtfile.write(str(imap[k][0:3]) + '\t')
		txtfile.write(str(tmap[k][0:3]) + '\t')
		txtfile.write(str(lmap[k][0:3]) + '\t')
		txtfile.write(str(mmap[k][0:3]) + '\t')
		txtfile.write(str(rmap[k][0:3]) + '\t')
		txtfile.write('\n')
	txtfile.close()

if len(sys.argv) > 1:
	word = sys.argv[1]
if len(sys.argv) > 2:
	a = float(sys.argv[2])
print "processing word", word
img_test = "../data/ed/" + word + "/img_test_results.txt"
txt_test = "../data/ed/" + word + "/txt_test_results.txt"
img_valid = "../data/ed/" + word + "/img_valid_results.txt"
txt_valid = "../data/ed/" + word + "/txt_valid_results.txt"

print "loading files"
vimap = readResults(img_valid)
vtmap = readResults(txt_valid)
imap = readResults(img_test)
tmap = readResults(txt_test)

a = compute_weight(vimap, vtmap)
print "weight = ", a

print "image"
getCMatrix(imap)
print "text"
getCMatrix(tmap)
print "max-rule fusion"
mmap = maxfusion(imap, tmap)
getCMatrix(mmap)
print "linear-rule fusion"
lmap = linearfusion(imap, tmap)
getCMatrix(lmap)
print "logistice regression fusion"
lrmap = logfusion(vimap, vtmap, imap, tmap)
getCMatrix(lrmap)
printResults(word, imap, tmap, lmap, mmap, lrmap)
