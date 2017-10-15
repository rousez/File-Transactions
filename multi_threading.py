from transaction import Transaction
from collections import Counter
import threading
import Queue
import time

start = time.clock()

retail_file = "retail.dat"

# specifies number of threads
thread_count = 4
# use queue for processing items in threads
queue = Queue.Queue()

log = []
history_triplet_log = []
history_pair_log = []
history_single_log = []

def get_highest_count(array_log):
    # use Counter to count all of the occurences of items in the log and get the highest count.
    highest_counter = Counter(array_log).most_common(1)
    # print counter.most_common(1)
    for combination, occurence in highest_counter:
        return combination, occurence


def get_probability_count(array_log, values):
    # counter = Counter(array_log)
    counter = array_log.count(values)
    # print counter.most_common(1)
    return counter  

class ThreadingClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
    #Assign thread working with queue
        self.queue = queue

    def run(self):

        def get_pair_log(items):
        # we only care about the co-occurences
            for item in range(len(items) - 1):
                history_pair_log.append((items[item], items[item + 1]))
            # print(items[item], items[item + 1])
            return None

        def get_single_log(items):
            for item in range(len(items)):
                history_single_log.append((items[item]))
                # print(items[item])
            return None

        def get_triplet_log(items):
            # we only care about the triple-occurences
            for item in range(len(items) - 2):
                history_triplet_log.append((items[item], items[item + 1], items[item + 2]))
            return None

        while True:
            trans = self.queue.get()
            get_pair_log(trans)
            get_triplet_log(trans)
            get_single_log(trans)   
            self.queue.task_done()

if __name__ == "__main__":
    # Create threads
    for i in range(thread_count):
        thread_instance = ThreadingClass(queue)
        thread_instance.setDaemon(True)
        thread_instance.start()

    with open(retail_file,"r") as retail_data:
        for line in retail_data:
            queue.put(line.split())
    queue.join()

    print("**** Using multi-threading ****\n")
    highest_pairs, pair_count = get_highest_count(history_pair_log)
    highest_triplets, triplet_count = get_highest_count(history_triplet_log)

    prob_val_from_pair = highest_pairs[0]
    # process the count of item a for pair probability.  use the single log to count item a.
    prob_count_from_pair = get_probability_count(history_single_log, prob_val_from_pair)
        # calculate the probability of the highest pair occurence.
    prob_of_pair = float(pair_count) / float(prob_count_from_pair)

    # get b,c items from the highest triplet occurence.
    prob_val_from_triplets = (highest_triplets[1], highest_triplets[2])
    # process the count of b,c items for triplet probability.  since we already have a log of pairs we can re-use it.
    prob_count_from_triplets = get_probability_count(history_pair_log, prob_val_from_triplets)
    # calculate the probability of the highest triplet occurence.
    prob_of_triplets = float(triplet_count) / float(prob_count_from_triplets)

    print("The highest co-occurence item pairs in the file are: %s with count %d" % (str(highest_pairs), pair_count))
    print("The probability of this occurence of pairs is:   ~%.2f" % (prob_of_pair))
    # print prob_count_from_pair
    print("\nThe highest co-occurence item triplets in the file are: %s with count %d" % (str(highest_triplets), triplet_count))
    print("The probability of this occurence of triplets is:   ~%.2f" % (prob_of_triplets))
    # print prob_count_from_triplets
    retail_data.close()
    end = time.clock()

    print("\nFinished in %s seconds." % (end - start))
    print("=======================================================================")
