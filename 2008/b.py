import operator

# Change dataset1 to dataset2 to get the results for dataset2
pos = open("dataset1/positive.txt", "r")
neg = open("dataset1/negative.txt", "r")

pos_sites = pos.readlines()
num_sites = len(pos_sites)
neg_sites = neg.readlines()
seq_length = len(pos_sites[0]) -1 
nucleotides = ['A', 'C', 'G','T']
M = dict()
for x in nucleotides:
    for i in range(seq_length):
        M[(i,x)] = 0
for site in pos_sites:
    for i in range(seq_length):
        M[(i,site[i])] += float(1) / num_sites

# predict whether or not a site will be predicted from the PWM 'matrix' given the threshold 'threshold'
def predict(matrix, site, threshold):
    score =reduce (operator.mul, [matrix[(i,site[i])] for i in range(seq_length)]) 
    if score <= threshold:
        return 0
    else:
        return 1

class_errors = []

def threshold(index):
    return float(index) / 1000

for i in range(1000):
    curr_threshold = threshold(i)
    true_pos = 0
    false_neg = 0
    true_neg = 0
    false_pos = 0
    for site in pos_sites:
        if predict(M, site, curr_threshold):
            true_pos +=1
        else:
            false_neg +=1
    for site in neg_sites:
        if predict(M, site, curr_threshold):
            false_pos +=1
        else:
            true_neg +=1
    class_errors.append(false_neg + false_pos)

#print class_errors

# choose the threshold to minimize classification errors 
opt_threshold =  threshold(class_errors.index(min(class_errors)))
print "Optimal threshold: ", opt_threshold

true_pos = 0
false_neg = 0
true_neg = 0
false_pos = 0
for site in pos_sites:
    if predict(M, site, opt_threshold):
        print site
        true_pos +=1
    else:
        false_neg +=1
for site in neg_sites:
    if predict(M, site, opt_threshold):
        false_pos +=1
    else:
        true_neg +=1
print "True positives: ", true_pos
print "False negatives: ", false_neg
print "False positives: ", false_pos
print "True negatives: ", true_neg

print "Sensitivity: ", float(true_pos) / float(true_pos + false_neg)
print "Specificity: ", float(true_neg) / float(true_neg + false_pos)
