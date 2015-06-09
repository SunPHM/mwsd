import nltk, re, pprint
import os
import sys
import codecs

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
		#ns = nltk.ne_chunk(ps, binary=True)
		#print ps
		#print ns
		for x in ps:
			print x
		#	if type(x) is nltk.tree.Tree:
		#		print s, x
		#		print ps	

def main(filename):
	docs = read_file(filename)
	extractNE(docs)
	
if __name__ == "__main__":
	main("../data/ed/bass/train/info.txt")
