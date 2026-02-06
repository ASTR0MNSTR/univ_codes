import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import os

# 1. Load the pre-generated data for x
# Assuming ex20_data.txt is in the same directory
current_folder = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_folder, 'data', 'ex20_data.txt')
x_sample = np.loadtxt(data_path)

# 2. Define the theoretical distribution for x 
# Based on the data range [0, 1], we assume a Uniform distribution
uniform_dist = stats.uniform(0, 1)
x_theoretical = np.linspace(-0.2, 1.2, 1000)
px = uniform_dist.pdf(x_theoretical)

# 3. Transform the data and the PDF
# Transformation: y = exp(x)
y_sample = np.exp(x_sample)
y_theoretical = np.exp(x_theoretical)

# Applying the Jacobian: p_y(y) = p_x(ln y) / y
# We divide px by y_theoretical where the uniform distribution is defined
py = uniform_dist.pdf(np.log(y_theoretical)) / y_theoretical

# 4. Plotting
fig = plt.figure(figsize=(10, 4))
fig.subplots_adjust(wspace=0.3, bottom=0.15)

# Left Panel: Distribution of x from ex20_data.txt
ax1 = fig.add_subplot(121)
ax1.hist(x_sample, bins=20, density=True, histtype='stepfilled', fc='#CCCCCC')
ax1.plot(x_theoretical, px, '-k')
ax1.set_xlim(-0.1, 1.1)
ax1.set_xlabel('$x$')
ax1.set_ylabel('$p_x(x)$')
ax1.set_title('Distribution of $x$ (from data)')
ax1.text(0.95, 0.95, r'$p_x(x) = {\rm Uniform}(0,1)$', va='top', ha='right', transform=ax1.transAxes)

# Right Panel: Transformed Distribution y = exp(x)
ax2 = fig.add_subplot(122)
ax2.hist(y_sample, bins=20, density=True, histtype='stepfilled', fc='#CCCCCC')
ax2.plot(y_theoretical, py, '-k')
ax2.set_xlim(0.9, 2.8)
ax2.set_xlabel('$y$')
ax2.set_ylabel('$p_y(y)$')
ax2.set_title('Transformed Distribution $y = \exp(x)$')
ax2.text(0.95, 0.95, '$y=\exp(x)$\n$p_y(y)=p_x(\ln y) / y$', va='top', ha='right', transform=ax2.transAxes)

plt.show()
