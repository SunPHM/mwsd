# to generate outputs with the same format as image classification
import os
import sys

def main(word, folder):
	test_truth = folder + "/test/info.txt"
	test_res = folder + "/" + word + ".txt.test"
	test_out = folder + "/txt_test_results.txt"
	valid_truth = folder + "/valid/info.txt"
	valid_res = folder + "/" + word + ".txt.valid"
	valid_out = folder + "/txt_valid_results.txt"
	output(test_truth, test_res, test_out)
	output(valid_truth, valid_res, valid_out)

def output(truth, res, out):		
	print truth, res, out		
	target = []
	files = []
	t = open(truth, "r+")
	for line in t:
		#print line
		target.append(int(line[0]))
		files.append(line.split("\t")[0])
	print len(target)
	prob = []
	labels = []
	l = open(res, "r+")
	for line in l:
		lab = int(line.split()[0])
		pro = float(line.split()[1])
		if lab == 0 or lab == -1:
			labels.append(0)
		else:
			labels.append(lab)
		if lab == 0 or lab == - 1:
			p = []
			p.append(0.0)
			p.append(0.0)
			prob.append(p)
		elif lab == 1:
			p = []
			p.append(pro)
			p.append(1.0 - pro)
			prob.append(p)
		else:
			p = []
			p.append(1.0 - pro)
			p.append(pro)
			prob.append(p)
	print len(labels)
	print len(prob)
	# write the results
	o = open(out, "w")
	for i in range(len(target)):
		o.write(files[i] + " ")
		o.write(str(labels[i]) + " ")
		o.write(str(prob[i][0]) + " ")
		o.write(str(prob[i][1]) + " ")
		o.write(str(target[i]) + "\n")
	o.close()	



main(sys.argv[1], sys.argv[2])
	
