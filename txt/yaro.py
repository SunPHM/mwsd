#Usage
#	sense_dist.py word
#Author: Dihong
import sys, getopt, os, os.path
import nltk
from nltk.corpus import wordnet as wn
import subprocess
from decimal import Decimal
from numpy import zeros
import time as dt

def main(argv):
	# get all the filenames
	word = argv[1]
	folder = argv[2]
	seed = folder + "/" + word + ".seed"
	train = folder + "/train/info.txt"
	valid = folder + "/valid/info.txt"
	test = folder + "/test/info.txt"
	classifier = folder + "/" + word + ".classifier"
	testing_results = folder + "/" + word + ".txt.test"
	valid_results = folder + "/" + word + ".txt.valid"
	#print seed, train, valid, test
	#print os.path.isfile(seed), os.path.isfile(train), os.path.isfile(valid), os.path.isfile(test)

	print 'Word to be disambiguated: %s.' % word
	if os.path.isfile(seed) == False or os.path.isfile(train) == False or os.path.isfile(valid) == False or os.path.isfile(test) == False:
		print 'Error: the input file(s) does not exist.'
		sys.exit(2)
	

	#Train classifier
	n1=dt.time()
	sys.stdout.write('Training classifier ... ')
	cmd = './uwsd -train '+ train + ' '+ seed +' '+ classifier+' ' + word
	#cmd = './uwsd -train '+ test + ' '+ seed +' '+ classifier+' ' + word
	os.system(cmd)
	n2=dt.time()
	print 'done. Elapsed time is %.4f seconds.' % ((n2-n1))
	n1=dt.time()
	
	#Classify the validation text
	sys.stdout.write('Classifying validation text ... ')
	cmd = './uwsd -test '+ classifier +' '+ valid +' ' + word
	out = subprocess.check_output(cmd, shell=True)
	fd = open(valid_results, 'w');
	fd.truncate()
	fd.write(out)
	fd.close()
	n2=dt.time()
	print 'done. Elapsed time is %.4f seconds.' % ((n2-n1))

	#Classify the testing text
	sys.stdout.write('Classifying testing text ... ')
	cmd = './uwsd -test '+ classifier +' '+ test +' ' + word
	out = subprocess.check_output(cmd, shell=True)
	fd = open(testing_results, 'w');
	fd.truncate()
	fd.write(out)
	fd.close()
	n2=dt.time()
	print 'done. Elapsed time is %.4f seconds.' % ((n2-n1))

				
				
if __name__ == "__main__":
	if len(sys.argv)  != 3:
		print 'Not enough arguments.';
		sys.exit(2);
	main(sys.argv)
