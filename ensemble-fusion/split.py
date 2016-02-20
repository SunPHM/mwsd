# split the data 10-fold for validation
import os
import sys
import shutil

words = ["bass", "crane", "squash"]
N = 10

def transform(word, fd):	
	print "transform processing", word
	raw = fd + "/raw/" + word
	proc = fd + "/processed/" + word
	if not os.path.exists(proc):
		os.mkdir(proc)
	at = raw + "/" + word + "_annotations.txt"
	img = raw + "/images"
	info = raw + "/info"
	nimg = proc + "/images"
	if not os.path.exists(nimg):
		os.mkdir(nimg)
	ntxt = proc + "/" + word + ".info"
	nf = open(ntxt, "w")

	f = open(at)
	for line in f:
		#print line
		es = line.split("\t:\t")
		no = es[0].zfill(4)
		lab = int(es[1])
		imgf = img + "/image_" + no + ".jpg"
		#print imgf
		#print lab
		if (lab == 1 or lab == 2) and os.path.exists(imgf):  
			#print "found one"
			newf = nimg + "/" + str(lab) + "_" + no + ".jpg"
			shutil.copy2(imgf, newf)
			info_file = open(info + "/info_" + no + ".txt", "r")
			x = 0
			for line in info_file:	
				if x == 3: 
					nf.write(str(lab) + "_" + no + "\t" + line + "\n")
				x += 1
			info_file.close()
	nf.close()						 	
	#print len(f.readlines())
	print "image filtering and copy are done. textual titles are merged"

def crosssplit(word, fd):
	# folder initialization
	print "crosssplit processing", word
	cv = fd + "/cv"
	if os.path.exists(cv) == False:
		os.mkdir(cv)
	proc = fd + "/processed/" + word
	out = cv + "/" + word
	if os.path.exists(out) == False:
		os.mkdir(out)
	for i in range(N):
		x = out + "/" + str(i)
		if os.path.exists(x) == False:
                	os.mkdir(x)
		if os.path.exists(x + "/images") == False:
			os.mkdir(x + "/images")
	# split the data into N fold
	info = open(proc + "/" + word + ".info")
	files = []
	sens = []
	for line in info:
		files.append(line.split("\t")[0])
		sens.append(line.split("\t")[1])	
	m = len(files)
	for i in range(N):
		folder = cv + "/" + word + "/" + str(i)
		txt = open(folder + "/info.txt", "w")
		for x in range(i * (m / N), min(m, (i + 1) * (m / N))):
			txt.write(files[x] + "\t" + sens[x])
			ori_image = proc + "/images/" + files[x] + ".jpg"
			tar_image = folder + "/images/" + files[x] + ".jpg"
			shutil.copy2(ori_image, tar_image)
		txt.close()
			
	print "crosssplit processing", word, "ends"	

def checkcreate(folder):
	if os.path.exists(folder) == False:
		os.mkdir(folder)

def evensplit(word, fd):
	# folder initialization
	print "evensplit processing", word
	ed = fd + "/ed"
	checkcreate(ed)
	proc = fd + "/processed/" + word
	out = ed + "/" + word
	train = out + "/train"
	valid = out + "/valid"
	test = out + "/test"
	checkcreate(out)
	checkcreate(train)
	checkcreate(valid)
	checkcreate(test)
	checkcreate(train + "/images")
	checkcreate(valid + "/images")
	checkcreate(test + "/images")
	
	# split the data into 3 parts, training, validation and testing
	info = open(proc + "/" + word + ".info", "r")
	files_1 = []
	files_2 = []
	sens_1 = []
	sens_2 = []
	for line in info:
		lab = int(line[0])
		filename = line.split("\t")[0]
		sen = line.split("\t")[1]
		if lab == 1:
			files_1.append(filename)
			sens_1.append(sen)
		else:
			files_2.append(filename)
			sens_2.append(sen)	
	
	# write to train/ folder
	train_out = open(train + "/info.txt", "w")
	
	for i in range(int(0.8 * len(files_1))):
		train_out.write(files_1[i] + "\t" + sens_1[i])
		ori_image = proc + "/images/" + files_1[i] + ".jpg"
		tar_image = train + "/images/" + files_1[i] + ".jpg"
		shutil.copy2(ori_image, tar_image)
	
	for i in range(int(0.8 * len(files_2))):
		train_out.write(files_2[i] + "\t" + sens_2[i])
		ori_image = proc + "/images/" + files_2[i] + ".jpg"
		tar_image = train + "/images/" + files_2[i] + ".jpg"
		shutil.copy2(ori_image, tar_image)

	train_out.close()	
	
	# write to valid/ folder
	valid_out = open(valid + "/info.txt", "w")

	for i in range(int(0.8 * len(files_1)), int(0.9 * len(files_1))):
		valid_out.write(files_1[i] + "\t" + sens_1[i])
		ori_image = proc + "/images/" + files_1[i] + ".jpg"
		tar_image = valid + "/images/" + files_1[i] + ".jpg"
		shutil.copy2(ori_image, tar_image)
	
	for i in range(int(0.8 * len(files_2)), int(0.9 * len(files_2))):
		valid_out.write(files_2[i] + "\t" + sens_2[i])
		ori_image = proc + "/images/" + files_2[i] + ".jpg"
		tar_image = valid + "/images/" + files_2[i] + ".jpg"
		shutil.copy2(ori_image, tar_image)
	
	valid_out.close()
	
	# write to test/ folder
	test_out = open(test + "/info.txt", "w")
	
	for i in range(int(0.9 * len(files_1)), len(files_1)):
		test_out.write(files_1[i] + "\t" + sens_1[i])
		ori_image = proc + "/images/" + files_1[i] + ".jpg"
		tar_image = test + "/images/" + files_1[i] + ".jpg"
		shutil.copy2(ori_image, tar_image)
	
	for i in range(int(0.9 * len(files_2)), len(files_2)):
		test_out.write(files_2[i] + "\t" + sens_2[i])
		ori_image = proc + "/images/" + files_2[i] + ".jpg"
		tar_image = test + "/images/" + files_2[i] + ".jpg"
		shutil.copy2(ori_image, tar_image)
	
	test_out.close()

	print "evenplit processing", word, "ends"

def clean(word, fd):
	# folder initialization
        print "clean processing", word
        ed = fd + "/ed"
        out = ed + "/" + word
        train = out + "/train"
        valid = out + "/valid"
        test = out + "/test"
	x = [train, valid, test]
	for s in x:
		txt = open(s + "/info.txt", "r")
		txt_out = open(s + "/info_new.txt", "w")
		images = s + "/images"
		for line in txt:
			filename = line.split("\t")[0]
			if os.path.exists(images + "/" + filename + ".jpg"):
				txt_out.write(line)
	print "data clean is down"	



def main(argv):
	fd = argv[1]
	for w in words:
		#transform(w, fd)	
		#evensplit(w, fd)
		clean(w, fd)
if __name__ == "__main__":
	#if len(sys.argv)  != 3:
        #        print 'Not enough arguments.';
        #        sys.exit(2);
       	#main(sys.argv)
	evensplit('apple', '../apple/')















