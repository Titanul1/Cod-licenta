import numpy as np
import random
import matplotlib.pyplot as plt

numbers = random.uniform(0, 1)

formatted_number = "{:.2f}".format(numbers)
print(formatted_number)

# Plot a histogram of the generated ages
#plt.hist(numbers, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
#plt.xlabel('Age')
#plt.ylabel('Probability Density')
#plt.title('Histogram of Random Ages (Asymmetric Distribution Favoring Large Numbers)')
#plt.grid(True)
#plt.show()