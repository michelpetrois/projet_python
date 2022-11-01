import matplotlib.pyplot as plt
import numpy as np


# make data
#x = 4 + np.random.normal(0, 1.5, 200)
x = np.array( [1, 4, 8, 6, 3, 5, 2, 0])
y = np.array( [10, 4, 8, 6, 3, 5, 2, 8])


print(x)
print(y)

# plot:
fig, ax = plt.subplots()

ax.bar(x,y)

ax.set(xticks=x,
       yticks=y)

plt.show()
