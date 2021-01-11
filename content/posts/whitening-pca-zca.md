---
title: Whitening with PCA and ZCA
date: 2018-12-17T00:00:00+00:00
summary: Whitening (or sphering) is an important preprocessing step prior to performing independent component analysis (ICA) on EEG/MEG data. In this post, I explain the intuition behind whitening and illustrate the difference between two popular whitening methods &ndash; PCA (principal component analysis) and ZCA (zero-phase component analysis).
tags:
  - Python
  - EEG
  - ICA
aliases:
  - 2018-12-17-whitening-pca-zca
---

## Introduction
[Whitening](https://en.wikipedia.org/wiki/Whitening_transformation) (also known as sphering) is a linear transformation used for decorrelating signals. Applied to EEG, this means that the original channel time series (which tend to be highly correlated) are transformed into uncorrelated signals with identical variances. The term whitening is derived from [white noise](https://en.wikipedia.org/wiki/White_noise) (which in turn draws its name from white light), which consists of serially uncorrelated samples. Whitening thus transforms a random vector into a [white noise vector](https://en.wikipedia.org/wiki/White_noise#White_noise_vector) with uncorrelated components.

Theoretically, there are infinitely many possibilities to perform a whitening transformation. We will explore two popular whitening methods in more detail, namely [principal component analysis (PCA)](https://en.wikipedia.org/wiki/Principal_component_analysis) and zero-phase component analysis (ZCA), which was introduced by [Bell and Sejnowski (1997)](https://doi.org/10.1016/S0042-6989(97)00121-1). These methods are commonly used in EEG/MEG analysis as a preprocessing step prior to independent component analysis (ICA) (see [this previous post]({{< ref removing-eog-ica >}}) on how to remove ocular artifacts with ICA). If you want to delve into the matter more deeply, [Kessy et al. (2018)](https://doi.org/10.1080/00031305.2016.1277159) discuss even more possible whitening methods.

Mathematically, whitening transforms a random vector $\mathbf{x}$ (the original EEG channel time series) into a random vector $\mathbf{z}$ using a whitening matrix $\mathbf{W}$:

$$\mathbf{z} = \mathbf{W} \mathbf{x}$$

Importantly, the original covariance matrix $\text{cov}(\mathbf{x}) = \mathbf{\Sigma}$ becomes $\text{cov}(\mathbf{z}) = \mathbf{I}$ after the transformation &ndash; the identity matrix. This means that all components of $\mathbf{z}$ have unit variance and all correlations have been removed.

## Toy data
To illustrate the differences between PCA and ZCA whitening, let's create some toy data. Specifically, we generate 1000 samples of two correlated time series $x_1$ and $x_2$.

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1)
mu = [0, 0]
sigma = [[5, 4], [4, 5]]  # must be positive semi-definite
n = 1000
x = np.random.multivariate_normal(mu, sigma, size=n).T
```

The two time series are stored in the NumPy array `x` of shape `(2, 1000)`.

For visualization purposes that will become clear in a moment, we determine the 20 most extreme values and denote their indices as `set1` (the indices of the remaining data points are stored in `set2`):

```python
set1 = np.argsort(np.linalg.norm(x, axis=0))[-20:]
set2 = list(set(range(n)) - set(set1))
```

Let's now plot all values of $x_1$ versus their corresponding values of $x_2$.

```python
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
```

![](/images/scatter_x.png)

Clearly, these two time series appear to be highly correlated. The ellipsoidal shape of the scatter plot indicates that as the values of $x_1$ increase, the values of $x_2$ also tend to increase. Indeed, the Pearson correlation between $x_1$ and $x_2$ is 0.80 and can be computed with:

```python
np.corrcoef(x)[0, 1]
```

The red dots indicate the most extreme values, and we will observe how these points are transformed by the subsequent whitening procedures.

## Eigendecomposition
Both PCA and ZCA are based on eigenvectors and eigenvalues of the (empirical) covariance matrix. In particular, the covariance matrix can be decomposed into its eigenvectors $\mathbf{U}$ and eigenvalues $\mathbf{\Lambda}$ as:

$$\mathbf{\Sigma} = \mathbf{U} \mathbf{\Lambda} \mathbf{U}^T$$

Let's compute these quantities for our toy data:

```python
sigma = np.cov(x)
evals, evecs = np.linalg.eigh(sigma)
```

Note that we now use the empirical covariance matrix derived from the data instead of the true covariance matrix, which is generally unknown. Furthermore, note that since a covariance matrix is always symmetric, we can use the optimized `np.linalg.eigh` function instead of the more generic `np.linalg.eig` version (this also makes sure that we will always get real eigenvalues instead of complex ones). Alternatively, we could also use `np.linalg.svd` directly on the data `x` (instead of the covariance matrix) to compute the eigenvectors and eigenvalues, which can be numerically more stable in some situations.

## Whitening with PCA
The whitening matrix $\mathbf{W}^{\mathrm{PCA}}$ for PCA can be written as:

$$\mathbf{W}^{\mathrm{PCA}} = \mathbf{\Lambda}^{-\frac{1}{2}} \mathbf{U}^T$$

This means that the data can be transformed as follows:

$$\mathbf{z} = \mathbf{W}^{\mathrm{PCA}} \mathbf{x} = \mathbf{\Lambda}^{-\frac{1}{2}} \mathbf{U}^T \mathbf{x}$$

Therefore, we can whiten our toy data accordingly:

```python
z = np.diag(evals**(-1/2)) @ evecs.T @ x
```

Let's see how our transformed toy data looks like in a scatter plot:

```python
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
```

![](/images/scatter_pca.png)

Clearly, the transformation removed the correlation between the two time series, because the scatter plot now looks like a sphere (a circle in two dimensions) &ndash; hence the name sphering. Indeed, the correlation coefficient (`np.corrcoef(z)[0, 1]`) yields a value practically equal to zero. Importantly, PCA has rotated all data points as illustrated by the new positions of the red dots; these do not lie on a diagonal with roughly 45 degrees anymore, but are now aligned with the vertical axis.

## Whitening with ZCA
The whitening matrix $\mathbf{W}^{\mathrm{ZCA}}$ for ZCA can be written as:

$$\mathbf{W}^{\mathrm{ZCA}} = \mathbf{U} \mathbf{\Lambda}^{-\frac{1}{2}} \mathbf{U}^T$$

In fact, this transformation looks almost like PCA whitening, but with an additional rotation by $\mathbf{U}$. Again, the original data can be transformed as follows:

$$\mathbf{z} = \mathbf{W}^{\mathrm{ZCA}} \mathbf{x} = \mathbf{U} \mathbf{\Lambda}^{-\frac{1}{2}} \mathbf{U}^T \mathbf{x}$$

We whiten our data accordingly and take a look at the resulting scatter plot:

```python
z = evecs @ np.diag(evals**(-1/2)) @ evecs.T @ x
```

```python
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
```

![](/images/scatter_zca.png)

Again, ZCA has decorrelated the data because the scatter plot looks spherical (and the value of `np.corrcoef(z)[0, 1]` is practically zero). In contrast to PCA, ZCA has preserved the orientation of the original data points. This can be observed from the positions of the red dots, which are aligned along the same direction as the original data. This property has given this whitening transformation its name "zero-phase", because it minimally distorts the original phase (i.e. orientation) of the data.

## Conclusions
Both PCA and ZCA whiten the original data, but they perform different rotations. It can be shown that PCA is optimal if the goal is compression of the original data (because principal components are sorted according to their explained variance), whereas ZCA is optimal if the goal is to keep the transformed random vector as similar as possible to the original one (thus ZCA cannot be used to compress the data). [Kessy et al. (2018)](https://doi.org/10.1080/00031305.2016.1277159) provide mathematical proofs of these propositions.

It is worth mentioning that [standardizing](https://en.wikipedia.org/wiki/Standard_score) the data prior to whitening might sometimes be useful, especially if the individual signals are on different scales. Usually, standardization is not necessary if all signals are EEG signals, but if a combination of EEG and MEG signals simultaneously enter the analysis, all data should be rescaled to avoid biasing the whitening transformation to signals with higher variance.

ICA algorithms are typically kick-started from whitened data. A recent article by [Montoya-Martínez et al. (2017)](https://hal.archives-ouvertes.fr/hal-01451432) suggests that some ICA variants can be sensitive to the choice of the initial whitening procedure. Specifically, it can make a difference whether PCA or ZCA is used prior to performing [Extended Infomax](https://doi.org/10.1162/089976699300016719) as implemented in [EEGLAB](https://sccn.ucsd.edu/eeglab/index.php). The reason seems to be the slow convergence of this particular ICA algorithm. [PICARD](https://github.com/pierreablin/picard) ([Ablin et al., 2018](https://doi.org/10.1109/TSP.2018.2844203)) improves upon this implementation and provides much faster convergence for both Extended Infomax and [FastICA](https://doi.org/10.1109%2F72.761722) variants. Therefore, it should be rather insensitive to the choice of the particular whitening procedure.

Finally, regarding the common practice of reducing dimensionality with PCA prior to ICA, a recent article by [Artoni et al. (2018)](https://doi.org/10.1016/j.neuroimage.2018.03.016) argues that pruning principal components might adversely affect the quality of the resulting independent components. This means that if PCA is used to whiten the data, all components should be retained (i.e. the data should not be compressed).

## Acknowledgments
I'd like to thank [Pierre Ablin](https://pierreablin.com/) for his very helpful comments on an earlier version of this post.