import random
import time

max = (1 << 1025) - 1

random.seed(time.time())

print("max", max)
print("random", random.randint(3, max))

