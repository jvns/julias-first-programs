import operator
# change x and the dataset to obtain different results
x = 100
pos = open("dataset2/positive.txt", "r")
neg = open("dataset2/negative.txt", "r")

pos_sites = pos.readlines()
num_sites = len(pos_sites)
neg_sites = neg.readlines()
seq_length = len(pos_sites[0]) -1 
nucleotides = ['A', 'C', 'G','T']
M = dict()
for n in nucleotides:
    for i in range(seq_length):
        M[(i,n)] = float(x) / (num_sites + 4*x)
for site in pos_sites:
    for i in range(seq_length):
        M[(i,site[i])] += 1.0 / (num_sites + 4*x)

def predict(matrix, site, threshold):
    score =reduce (operator.mul, [(matrix[(i,site[i])]) for i in range(seq_length)]) 
#    print score , threshold
    if score < threshold:
        return 0
    else:
        return 1

class_errors = []
def threshold(index):
    return float(index) / 10000000

for i in range(20000):
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
    print float(true_pos) / float(false_neg + true_pos) ,float(true_neg) / float(false_pos + true_neg) 
