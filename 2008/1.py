import re
import operator

pos = open("promoterPositive.fa", "r")
neg = open("promoterNegative.fa", "r")

nucleotides = ['A', 'C', 'G','T']
def choose2(list): 
    combinations = []
    for x in list:
        for y in list:
            if x < y :
                combinations.append((x,y))
    return combinations


alphabet = nucleotides + choose2(nucleotides) + [tuple(nucleotides)]

# generate all possible sequences
sigmastar = [ [a,b,c,d,e,f] for a in alphabet for b in alphabet for c in alphabet for d in alphabet for e in alphabet for f in alphabet]

d = dict()

pos_lines = pos.readlines()
neg_lines = neg.readlines()

# calculate probabilities of A,C,G,T occurring

promoter_length = len(pos_lines[0]) - 1

num_A = sum([s.count('A') for s in pos_lines])
num_C = sum([s.count('C') for s in pos_lines])
num_G = sum([s.count('G') for s in pos_lines])
num_T = sum([s.count('T') for s in pos_lines])
total = num_A + num_C + num_G + num_T
pos_probs = {'A' : float(num_A) / total,
         'C' : float(num_C) / total,
         'G' : float(num_G) / total,
         'T' : float(num_T) / total}

num_A = sum([s.count('A') for s in neg_lines])
num_C = sum([s.count('C') for s in neg_lines])
num_G = sum([s.count('G') for s in neg_lines])
num_T = sum([s.count('T') for s in neg_lines])
total = num_A + num_C + num_G + num_T
neg_probs = {'A' : float(num_A) / total,
         'C' : float(num_C) / total,
         'G' : float(num_G) / total,
         'T' : float(num_T) / total}

print pos_probs
print neg_probs

for word in sigmastar:
    pos_matches = 0
    neg_matches = 0
    re_string = "".join(map(lambda x: "[" + "".join(x) + "]", word))
    my_re = re.compile(re_string)
    expected_num_pos = reduce(operator.mul, [sum([pos_probs[x] for x in w]) for w in word]) * promoter_length * len(pos_lines)
    expected_num_neg = reduce(operator.mul, [sum([neg_probs[x] for x in w]) for w in word]) * promoter_length * len(neg_lines)
    for str in pos_lines:
        if my_re.search(str): pos_matches += 1
    for str in neg_lines:
        if my_re.search(str): neg_matches += 1
    if (pos_matches > expected_num_pos and neg_matches < expected_num_neg):
        print pos_matches, neg_matches, expected_num_pos, expected_num_neg,  re_string
