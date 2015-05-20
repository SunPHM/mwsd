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

def main(argv):
	fd = argv[1]
	for w in words:
		#transform(w, fd)	
		crosssplit(w, fd)
if __name__ == "__main__":
	#if len(sys.argv)  != 3:
        #        print 'Not enough arguments.';
        #        sys.exit(2);
        main(sys.argv)
















