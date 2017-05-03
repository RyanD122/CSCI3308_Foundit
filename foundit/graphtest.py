import numpy as np

import matplotlib.pyplot as plt

a = [1, 2]
b = [2, 5]
plt.hist(a, bins=[0, 1, 2], weights=b)

plt.show()
