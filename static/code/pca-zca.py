# (c) Clemens Brunner, licensed under the BSD 3-Clause license

import numpy as np
import matplotlib.pyplot as plt

# generate toy data
np.random.seed(1)
mu = [0, 0]
sigma = [[5, 4], [4, 5]]  # must be positive semi-definite
n = 1000
x = np.random.multivariate_normal(mu, sigma, size=n).T

# store 20 most extreme values for visualization
set1 = np.argsort(np.linalg.norm(x, axis=0))[-20:]
set2 = list(set(range(n)) - set(set1))

# plot original data
fig, ax = plt.subplots()
ax.scatter(x[0, set1], x[1, set1], s=20, c="red", alpha=0.2)
ax.scatter(x[0, set2], x[1, set2], s=20, alpha=0.2)
ax.set_aspect("equal")
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_title("Original")

np.corrcoef(x)[0, 1]

sigma = np.cov(x)
evals, evecs = np.linalg.eigh(sigma)

# PCA
z = np.diag(evals**(-1/2)) @ evecs.T @ x

fig, ax = plt.subplots()
ax.scatter(z[0, set1], z[1, set1], s=20, c="red", alpha=0.2)
ax.scatter(z[0, set2], z[1, set2], s=20, alpha=0.2)
ax.set_aspect("equal")
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_xlabel("$z_1$")
ax.set_ylabel("$z_2$")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_title("PCA")

np.corrcoef(z)[0, 1]

# ZCA
z = evecs @ np.diag(evals**(-1/2)) @ evecs.T @ x

fig, ax = plt.subplots()
ax.scatter(z[0, set1], z[1, set1], s=20, c="red", alpha=0.2)
ax.scatter(z[0, set2], z[1, set2], s=20, alpha=0.2)
ax.set_aspect("equal")
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_xlabel("$z_1$")
ax.set_ylabel("$z_2$")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_title("ZCA")
