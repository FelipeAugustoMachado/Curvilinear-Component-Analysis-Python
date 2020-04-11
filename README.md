# Curvilinear-Component-Analysis-Python
Curvilinear Component Analysis implementation for Python.

This code was implemented using the following article https://ieeexplore.ieee.org/document/554199 and the book "Nonlinear Dimensionality Reduction" by Michel Verleysen, John A. R. Lee.

# The Algorithm
Curvilinear Component Analysis (CCA) is a Non-linear Dimensionality Reduction technic, basead on the distance betweens the points: it tries to create a new space, with a small dimension, which the distance betweens points are equal in the original space (if this distance is smaller than Lambda, one of the parameters of the algorithm).

# Results
The author from the article tests the algorithm in 3 artificials examples, with 500 points each: sphere, U-fold and two circles. All these tests tries to reduce a 3 dimensional data to a 2 dimensional data. The results from my implementation are show in the following subsections.

## Sphere
The original space: 

![Sphere original](/images/sphere.jpg)

The dy dx representation after CCA training:

![dydx Sphere](/images/dydx_sphere.jpg)

The reduced space:
![Sphere reduced](/images/cca_sphere.jpg)

## U-fold
The original space: 

![U-fold original](/images/ufold.jpg)

The dy dx representation after CCA training:

![dydx U-fold](/images/dydx_ufold.jpg)

The reduced space:
![U-fold reduced](/images/cca_ufold.png)

## Two Circle
The original space: 

![Two Circle original](/images/twocircle.jpg)

The dy dx representation after CCA training:

![dydx Two Circle](/images/dydx_twocircle.png)

The reduced space:
![Two Circle reduced](/images/cca_twocircle.jpg)
