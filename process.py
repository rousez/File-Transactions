from transaction import Transaction
from collections import Counter
import time

retail_file = "retail.dat"
history_triplet_log = []
history_pair_log = []

def get_highest_count(array_log):
	# use Counter to count all of the occurences of items in the log.
	highest_counter = Counter(array_log).most_common(1)
	# print counter.most_common(1)
	for combination, occurence in highest_counter:
		return combination, occurence


def get_pair_log(items):
	# we only care about the co-occurences
	for item in range(len(items) - 1):
		history_pair_log.append((items[item], items[item + 1]))
		# print(items[item], items[item + 1])
	return None


def get_triplet_log(items):
	# we only care about the triple-occurences
	for item in range(len(items) - 2):
		history_triplet_log.append((items[item], items[item + 1], items[item + 2]))
	return None

def main():
	with open(retail_file, "r") as retail_data:
		start = time.clock()
		count = 0
		for line in retail_data:
			trans = Transaction(count, map(int, line.split()))
			parsed_items = trans.get_items()
			get_pair_log(parsed_items)
			get_triplet_log(parsed_items)
			count += 1
	print("File: %s contains %d lines.\n" % (retail_file, count))
	pairs, pair_count = get_highest_count(history_pair_log)
	triplets, triplet_count = get_highest_count(history_triplet_log)
	print("The highest co-occurence item pairs in the file are: %s  with count %d" % (str(pairs), pair_count))
	print("The highest co-occurence item triplets in the file are: %s  with count %d" % (str(triplets), triplet_count))
	retail_data.close()
	end = time.clock()
	print("\nFinished in %s seconds." % (end - start))

if __name__ == "__main__":
	main()
	