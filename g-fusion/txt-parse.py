import nltk, re, pprint
import os
import sys
import codecs
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import PorterStemmer

entities = []
wnl = WordNetLemmatizer() # lemmatizer
st = PorterStemmer()

def read_file(filename):
	print "reading file"
	f = open(filename,'r')
	docs = []
	for line in f:
		#print line
		docs.append(unicode(line, errors="ignore"))
	return docs	

def extractNE(docs):# extract named entities
	for s in docs:
		ws = nltk.word_tokenize(s)
		ps = nltk.pos_tag(ws)
		ns = nltk.ne_chunk(ps)
		# output named entity and NP with size <= 2
		ns = nltk.ne_chunk(ps, binary=True)
		print ps
		for i in range(len(ps)):
			x = ps[i]
			#TODO pos tagging, NN, NNP, NNS, NNPS
			if x[1] == 'NN':
				y = wnl.lemmatize(x[0])
				entities.append(y)
				if i > 0 and ps[i - 1][1] == 'NN':
					z = wnl.lemmatize(ps[i - 1][0])
					entities.append(z + " " + y)
						
		for x in ns:
			# print x
			# print type(x)
			if type(x) is nltk.tree.Tree:
				# print x
				# print x.label()
				# entities.append(x)
				et = ''
				for y in x:
					et += y[0] + ' '
				entities.append(et)
		
		for x in entities:
			print x

def count(entities):
	print "N.A."
	# lemmatization
	# hashmap count


def main(filename):
	docs = read_file(filename)
	extractNE(docs)
	
if __name__ == "__main__":
	# main("../data/ed/bass/train/info.txt")
	print wnl.lemmatize('feet')
	docs = []
	docs.append("big turtle lake - a premier minnesota smallmouth bass fishery - John Green")
	extractNE(docs)
