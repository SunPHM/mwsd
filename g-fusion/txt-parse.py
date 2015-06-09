import nltk, re, pprint
import os
import sys

def main():
	s = "On World Oceans Day, explore their beauty with Google Maps"
	ws = nltk.word_tokenize(s)
	ps = nltk.pos_tag(ws)
	print ws
	print ps

if __name__ == "__main__":
	main()
