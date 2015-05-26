import sklearn
from sklearn import svm
import sys

def getft(filename):
	# get features and targets
	targets = []
	features = []
	files = []
	f = open(filename,"r+")
	for line in f:
		targets.append(int(line[0]))
		files.append(line.split("\t")[0][:-4])
		ls = line.split("\t")[1].split()
		feature = []
		for value in ls:
			feature.append(int(value))
		features.append(feature)
	return features, targets, files

def store_results(files, ans, probs, truth, filename):
	f = open(filename,"w")
	for i in range(len(files)):
		f.write(files[i] + " ")
		f.write(str(ans[i]) + " ")
		f.write(str(probs[i][0]) + " ")
		f.write(str(probs[i][1]) + " ")
		f.write(str(truth[i]) + "\n")
	f.close()

def dis2conf(ds):
	cs = []
	for i in range(len(ds)):
		x = ds[i]
		p = x + 2	

folder = "/home/yp/projects/mwsd/data/ed/"
if len(sys.argv) >= 2:
	folder += sys.argv[1]
else:
	folder += "bass"

train = folder + "/img_training.txt"
valid = folder + "/img_valid.txt"
test = folder + "/img_testing.txt"
testing_results = folder + "/img_test_results.txt"
valid_results = folder + "/img_valid_results.txt"

#get the class labels from training set
samples, targets, train_files = getft(train)
testing_features, testing_truth, testing_files = getft(test)
#valid_features, valid_truth, valid_files = getft(valid)
			
print "samples length " + str(len(samples))
print "feature size " + str(len(samples[0]))
print "target length " + str(len(targets))
print "testing_features length " + str(len(testing_features))
print "testing_truth length " + str(len(testing_truth))
#print "valid_features length " + str(len(valid_features))
#print "valid_truth length " + str(len(valid_truth))

# training
#clf = svm.SVC(probability=True)
#clf = svm.LinearSVC()
clf = svm.SVC()
clf.fit(samples,targets)

# validation
#vans = clf.predict(valid_features)
#print "validation ans length " + str(len(vans))
#vprobs = clf.predict_proba(valid_features)
#print "validation probs length " + str(len(vprobs))
#store_results(valid_files, vans, vprobs, valid_truth, valid_results)

# testing
tans = clf.predict(testing_features)
print "testing ans length " + str(len(tans))
tprobs = clf.decision_function(testing_features)
print "testing probs length " + str(len(tprobs))
#store_results(testing_files, tans, tprobs, testing_truth, testing_results)

for i in range(len(testing_truth)):
	print testing_files[i], testing_truth[i], tans[i], tprobs[i]

print "Image: SVM training, validation and testing is done"
	

