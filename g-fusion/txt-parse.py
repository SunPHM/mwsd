import nltk, re, pprint
import os
import sys
import codecs
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import PorterStemmer

concepts_1 = {}
concepts_2 = {}
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
		docs.append(unicode(line, errors="ignore"))
		# i += 1
	return docs	

def extract(docs):# extract named entities and noun phrases
	print "extracting ne and np"
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
					concepts_1[x] = 1
				else:
					concepts_1[x] += 1
		else:
			for x in al:
				if x not in concepts_2:
					concepts_2[x] = 1
				else:
					concepts_2[x] += 1 

def extNP(ps): # extract NP
	nps = []
	i = 0
	while i < len(ps):
		x = ps[i]
		if x[1] == 'NN' or x[1] == 'NNS':
			y = wnl.lemmatize(x[0])
			nps.append(y)
			i += 1
		elif x[1] == 'NNP' or x[1] == 'NNPS':	
			np = ''
			while i < len(ps) and (ps[i][1] == 'NNP' or ps[i][1] == 'NNPS'):
				np += wnl.lemmatize(ps[i][0]) + " "
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
	c1 = sorted(concepts_1, concepts_1.get)
	c2 = sorted(concepts_2, concepts_2.get)
	for i in range(min(10, len(c1))):
		print c1[i], 
	print ""
	for i in range(min(10, len(c2))):
		print c2[i],
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
