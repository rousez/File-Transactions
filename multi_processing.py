from multiprocessing import Pool
import time
from collections import Counter

start = time.clock()
retail_file = "retail.dat"

def get_highest_count(array_log):
    # use Counter to count all of the occurences of items in the log and get the highest count.
    highest_counter = Counter(array_log).most_common(1)
    # print counter.most_common(1)
    for combination, occurence in highest_counter:
        return combination, occurence

def get_probability_count(array_log, values):
    counter = array_log.count(values)
    return counter

def get_single_log(items):
    single_log = []
    for trans in items:
        for item in range(len(trans)):
            single_log.append((trans[item]))
    return single_log

def get_pair_log(items):
    pair_log = []
    # we only care about the co-occurences
    for trans in items:
        for item in range(len(trans) - 1):
            pair_log.append((trans[item], trans[item + 1]))
    return pair_log

def get_triplet_log(items):
    # we only care about the triple-occurences
    triplet_log = []
    for trans in items:
        for item in range(len(trans) - 2):
            triplet_log.append((trans[item], trans[item + 1], trans[item + 2]))
    return triplet_log

def get_log(items):
    return map(int, items.split())

if __name__ == "__main__":
    # use pool to split up the work in chunks amongst processors
    pool = Pool(4)
    with open('retail.dat', 'r') as source_file:
        log = pool.map(get_log, source_file, 1000)
    source_file.close()   
    pairs = get_pair_log(log)
    singles = get_single_log(log)
    triplets = get_triplet_log(log)

    highest_pairs, pair_count = get_highest_count(pairs)
    highest_triplets, triplet_count = get_highest_count(triplets)

    # get item a of the highest pair occurence.
    prob_val_from_pair = highest_pairs[0]
    # process the count of item a for pair probability.  use the single log to count item a.
    prob_count_from_pair = get_probability_count(singles, prob_val_from_pair)
    # calculate the probability of the highest pair occurence.
    prob_of_pair = float(pair_count) / float(prob_count_from_pair)
    # get b,c items from the highest triplet occurence.
    prob_val_from_triplets = (highest_triplets[1], highest_triplets[2])
    # process the count of b,c items for triplet probability.  since we already have a log of pairs we can re-use it.
    prob_count_from_triplets = get_probability_count(pairs, prob_val_from_triplets)
    # calculate the probability of the highest triplet occurence.
    prob_of_triplets = float(triplet_count) / float(prob_count_from_triplets)
    print("**** Using multi-processing ****\n")
    print("The highest co-occurence item pairs in the file are: %s with count %d" % (str(highest_pairs), pair_count))
    print("The probability of this occurence of pairs is:   ~%.2f" % (prob_of_pair))
    print("\nThe highest co-occurence item triplets in the file are: %s with count %d" % (str(highest_triplets), triplet_count))
    print("The probability of this occurence of triplets is:   ~%.2f" % (prob_of_triplets))

    end = time.clock()

    print("\nFinished in %s seconds." % (end - start))
    print("=======================================================================")