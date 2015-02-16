# Change dataset1 to dataset2 to get the results for dataset2
pos = open("dataset1/positive.txt", "r")
neg = open("dataset1/negative.txt", "r")

nucleotides = ['A', 'C', 'G','T']

# consensus sequences are represented as lists of lists of nucleotides.

def choose2(list): 
    combinations = []
    for x in list:
        for y in list:
            if x < y :
                combinations.append((x,y))
    return combinations

def train(pos_list):
    num_pos_sites = len(pos_list)
    cons_sequence = []
    seq_length = len(pos_list[0]) - 1
    for i in range(seq_length):
        current_position = []
        for x in nucleotides: 
            pos_count = 0
            for site in pos_list:
                if site[i] == x:
                    pos_count += 1
                if pos_count >= num_pos_sites  * 0.9:
                    # then we have a nucleotide that is there 90% of the time
                    current_position = [x]
        if (not current_position):
            for (x,y) in choose2(nucleotides):
                pos_count = 0
                for site in pos_list:
                    if site[i] == x or site[i] == y:
                        pos_count += 1
                    if pos_count >= num_pos_sites  * 0.9:
                        # then we have two nucleotides that are there 90% of the time
                        current_position = [x,y]
        if (not current_position):
            # use [ACGT]
            current_position = nucleotides
        cons_sequence.append(current_position)
    return cons_sequence

def predict(consensus_sequence, site):
    for i in range(len(consensus_sequence)):
        if not (site[i] in consensus_sequence[i]):
            return 0
    else:
         return 1

pos_sites = pos.readlines()
true_pos = 0
false_neg = 0
for i in range(len(pos_sites)):
    consensus_sequence = train(pos_sites[:i] + pos_sites[i+1:])
    if predict(consensus_sequence, pos_sites[i]):
        true_pos +=1
    else:
        false_neg +=1
print "True positives: ", true_pos
print "False negatives: ", false_neg

neg_sites = neg.readlines()
true_neg = 0
false_pos = 0
consensus_sequence = train(pos_sites)
for i in range(len(neg_sites)):
    if predict(consensus_sequence, neg_sites[i]):
        false_pos +=1
    else:
        true_neg +=1
print "False positives: ", false_pos
print "True negatives: ", true_neg



