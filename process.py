from transaction import Transaction
from collections import Counter
import time

start = time.clock()

with open("retail.dat", "r") as f:
	history_log = []
	count = 0
	for line in f:
		trans = Transaction(count, map(int, line.split()))
		parse = trans.get_items()
		# we only care about the co-occurences
		for item in range(len(parse) - 1):
			history_log.append((parse[item], parse[item + 1]))
			
			#print(parse[item], parse[item + 1])
		count += 1
		#print(" ")
	#print sorted(history_log)
	counter = Counter(sorted(history_log))
	print counter.most_common(1)

f.close()

end = time.clock()

print("\nFinished in %s seconds." % (end - start))
