import nltk, re, pprint
import os
import sys

def main():
	s = "On World Oceans Day, explore their beauty with Google Maps"
	ws = nltk.word_tokenize(s)
	ps = nltk.pos_tag(ws)
	#ns = nltk.ne_chunk(ps, binary=True)
	ns = nltk.ne_chunk(ps)
	print ws
	print ps
	print ns

if __name__ == "__main__":
	main()
