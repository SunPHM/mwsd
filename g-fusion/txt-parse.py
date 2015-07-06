import nltk, re, pprint
import os
import sys
import codecs
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import PorterStemmer

concepts_1 = {}
concepts_2 = {}
x = 0.0
y = 0.0
wnl = WordNetLemmatizer() # lemmatizer
st = PorterStemmer()

def read_file(filename):
	print "reading file"
	f = open(filename,'r')
	docs = []
	# i = 0
	for line in f:
		# if i > 100: break
		#print line
		if line[0] == '1':
			#print n1
			x += 1.0
		else:
			y += 1.0
		docs.append(unicode(line, errors="ignore"))
		# i += 1
	return docs	

def extract(docs):# extract named entities and noun phrases
	print "extracting noun phrases"
	for s in docs:
		# tokenization, pos tagging, named entity extraction
		ws = nltk.word_tokenize(s)
		ps = nltk.pos_tag(ws)
		ns = nltk.ne_chunk(ps)
		ns = nltk.ne_chunk(ps, binary=True)
		# extract noun phrases and entities
		nps = extNP(ps)
		ents = []
		# ents = extNE(ns)
		al = nps + ents
		#print ps 
		#print nps
		#print ents
		if ws[0][0] == '1':
			for x in al:
				if x not in concepts_1:
					concepts_1[x] = 1.0
				else:
					concepts_1[x] += 1.0
		else:
			for x in al:
				if x not in concepts_2:
					concepts_2[x] = 1.0
				else:
					concepts_2[x] += 1.0 

def extNP(ps): # extract NP
	nps = []
	i = 0
	while i < len(ps):
		x = ps[i]
		if x[1] == 'NN' or x[1] == 'NNS':
			y = wnl.lemmatize(x[0])
			nps.append(y)
			#nps.append(x[0])
			i += 1
		elif x[1] == 'NNP' or x[1] == 'NNPS':	
			np = ''
			while i < len(ps) and (ps[i][1] == 'NNP' or ps[i][1] == 'NNPS'):
				np += wnl.lemmatize(ps[i][0]) + " "
				#np += ps[i][0] + " "
				i += 1
			nps.append(np[:len(np) - 1])

		else:
			i += 1
	return nps
				
def extNE(ns): # extract Named Entity
	ents = []
	for x in ns:
		if type(x) is nltk.tree.Tree:
			et = ''
			for y in x:
				et += y[0] + ' '
			ents.append(et[:len(et) - 1])
	return ents


def output():
	print "output"
	for k in concepts_1.keys():
		concepts_1[k] /= n1
	for k in concepts_2.keys():
		concepts_2[k] /= n2
	cc1 = {}
	cc2 = {}
	for k in concepts_1.keys():
		if k in concepts_2.keys():
			#print k, concepts_1[k], concepts_2[k]
			cc1[k] = concepts_1[k] / concepts_2[k]
		else:
			cc1[k] = concepts_1[k]
	for k in concepts_2.keys():
		if k in concepts_1.keys():
			#print k, concepts_1[k], concepts_2[k]
			cc2[k] = concepts_2[k] / concepts_1[k]	
		else:
			cc2[k] = concepts_2[k]
	c1 = sorted(cc1.items(), key = lambda t : t[1])
	c2 = sorted(cc2.items(), key = lambda t : t[1])
	#print c1
	#print c2
	for i in range(min(10, len(c1))):
		print c1[len(c1) - 1 - i], 
	print ""
	for i in range(min(10, len(c2))):
		print c2[len(c2) - 1 - i],
	print ""

def main(filename):
	docs = read_file(filename)
	extract(docs)
	output()	

if __name__ == "__main__":
	main("../data/ed/squash/train/info.txt")
	# docs = []
	# docs.append("big turtle lake - a premier minnesota smallmouth bass fishery - John Green")
	# extract(docs)
