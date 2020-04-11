# -*- coding: utf-8 -*-
"""CCA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N4uWYdOiUqBzi-uTQx_Xraz_2N7OkAN4
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from scipy.spatial.distance import cdist
from sklearn.metrics import pairwise_distances as pdist
from sklearn.decomposition import PCA

class CCA:
    def __init__(self, p, lmbd, alpha):
        """
        Creates the CCA object. 

        Parameters
        ----------
        p : int
            The new dimension.
        lmbd : float
            Distance limit to update points. It decreases over time : lambda(t) = lambda/(t+1).
        alpha : float
            Learning rate. It decreases over time : alpha(t) = alpha/(t+1)
        """
        self.p = p
        self.lmbd = lmbd
        self.alpha = alpha    
        
    def _stress(self, dist_y, dist_x, lmbda):
        """
        Calculates the stress function given the distances in original space (dist_y)
        and the distances in reduced space (dist_x).

        Parameters
        ----------
        dist_y : numpy.array
            Array with distances in original space.
        dist_x : numpy.array
            Array with distances in reduced space.
        lmbda : float
            Distance limit to update points.
        """
        stress = np.mean((dist_y - dist_x)**2 * (lmbda > dist_x).astype(int))
        return stress
    
    def run(self, data_y, q_max=10, show=False, tol=1e-4):
        """
        Method to reduce dimension. Every iteration run all points. The new data
        is stored in attribute 'data_x'.

        Parameters
        ----------
        data_y : numpy.array
            Array with the original data.
        q_max : int (default = 10)
            Number of iterations. Each iteration run all points in 'data_y'.
        show : boolean (default = False)
            If True, shows the stress curve along time.
        tol : float (default = 1e-4)
            Tolerance for the stopping criteria.
        
        Returns
        -------
        data_x : numpy.array
            New data representation.
        """
        self.data_y = data_y
        n = len(data_y)
        triu = np.triu_indices(n, 1)
        dist_y = pdist(data_y)
        data_x = PCA(self.p).fit_transform(data_y)
        stress = np.zeros(q_max)
        print("Progress: 0.0%", end='\r')
        for q in range(q_max):
            alpha = max(0.001, self.alpha/(1+q))
            lmbda = max(0.1, self.lmbd/(1+q))
            for i in range(n):
                dist_x = cdist(data_x[i].reshape(1,-1), data_x)    
                dy = np.delete(dist_y[i],i,0) 
                dx = np.delete(dist_x,i,1)
                delta_x = (alpha*(lmbda > dx)*(dy - dx)/dx).reshape((-1,1))*(data_x[i] - np.delete(data_x, i, 0))
                delta_x = np.insert(delta_x, i, 0, axis=0)
                data_x -= delta_x
            dist_x = pdist(data_x)
            stress[q] = self._stress(dist_y[triu], dist_x[triu], lmbda)
            if stress[q] < tol:
                print("Progress: 100.00%")
                print(f"Tol achieved in iteration {q}")
                break
            print(f"Progress: {round((q+1)*100/q_max,2)}%  ", end='\r')
        if show:
            plt.plot(np.arange(q_max), stress, marker='.', c='black')
            plt.xlabel("Iteration")
            plt.ylabel("Stress")
            plt.show()
        print()
        self.data_x = data_x
        return data_x

    def plotYX(self):
        """
        Creates the dy dx Representation with the original and the reduced data.
        """
        reduced_data = self.data_x
        original_data = self.data_y
        dy = []
        dx = []

        for i in range(reduced_data.shape[0]):
            y1 = reduced_data[i,:]
            x1 = original_data[i,:]
            for j in range(i+1, reduced_data.shape[0]):
                y2 = reduced_data[j,:]
                x2 = original_data[j,:]
                dy.append(np.linalg.norm(y2-y1))
                dx.append(np.linalg.norm(x2-x1))
        plt.scatter(dy,dx, c='black', s=1)
        lims = [
            np.min([plt.xlim(), plt.ylim()]),  # min of both axes
            np.max([plt.xlim(), plt.ylim()]),  # max of both axes
        ]
        plt.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
        plt.xlim(lims)
        plt.ylim(lims)
        plt.ylabel("Distance between points in original space")
        plt.xlabel("Distance between points in reduced space")
        plt.show()




if __name__ == '__main__':
	
	sns.set()

	# Circle
	n = 150

	theta = np.random.random(n)*7
	x = np.cos(theta)*10 + np.random.normal(0,1,n); y = np.sin(theta)*10 + np.random.normal(0,1,n)
	data = np.concatenate([x.reshape(-1,1), y.reshape(-1,1)], axis=1)

	plt.scatter(x, y, s=3, c='black')
	plt.axis('scaled')
	plt.show()

	cca = CCA(1, 25, 0.2)
	cca.run(data, q_max=10)
	cca.plotYX()

	# Sphere

	n = 500

	theta = np.random.random(n)*7
	phi = np.random.random(n)*7

	x = np.cos(theta)*np.sin(phi)*10 
	y = np.sin(theta)*np.sin(phi)*10
	z = np.cos(phi)*10 

	data = np.concatenate([x.reshape(-1,1), y.reshape(-1,1), z.reshape(-1,1)], axis=1)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(x,y,z,s=1,c='black')
	plt.show()

	cca = CCA(2, 17, 0.2)
	cca.run(data, q_max=10)
	cca.plotYX()

	plt.scatter(cca.data_x[:,0], cca.data_x[:,1], s=1, c='black')
	plt.show()

	# U-fold

	n = 500

	x = np.random.random(n)*10 - 5
	y = -0.2*x**2
	z = np.random.random(n)*10

	data = np.concatenate([x.reshape(-1,1), y.reshape(-1,1), z.reshape(-1,1)], axis=1)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(x,y,z,s=1,c='black')
	plt.show()

	cca = CCA(2, 12, 0.3)
	cca.run(data, q_max=20)
	cca.plotYX()

	plt.scatter(cca.data_x[:,0], cca.data_x[:,1], s=1, c='black')
	plt.show()

	# Two rings

	from scipy.spatial.transform import Rotation as R

	n = 250

	theta1 = np.random.random(n)*7
	theta2 = np.random.random(n)*7

	x1 = np.cos(theta1)*10 + 0.1*np.random.normal(0,1,n)
	y1 = np.sin(theta1)*10 + 0.1*np.random.normal(0,1,n)
	z1 = np.zeros(n)

	data1 = np.concatenate([x1.reshape(-1,1), y1.reshape(-1,1), z1.reshape(-1,1)], axis=1)

	x2 = np.cos(theta2)*10 + 0.1*np.random.normal(0,1,n)
	y2 = np.sin(theta2)*10  + 10 + 0.1*np.random.normal(0,1,n)
	z2 = np.zeros(n)

	data2 = np.concatenate([x2.reshape(-1,1), y2.reshape(-1,1), z2.reshape(-1,1)], axis=1)

	r1 = R.from_euler('y', 45, degrees=True)
	r2 = R.from_euler('y', -45, degrees=True)

	data1 = r1.apply(data1)
	data2 = r2.apply(data2)

	data = np.concatenate([data1, data2], axis=0)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(data1[:,0], data1[:,1], data1[:,2],s=1,c='black')
	ax.scatter(data2[:,0], data2[:,1], data2[:,2],s=1,c='black')
	plt.show()

	cca = CCA(2, 16, 0.1)
	cca.run(data, q_max=10)
	cca.plotYX()

	data_x = cca.data_x 
	data_x1 = data_x[:n,:] 
	data_x2 = data_x[n:,:]

	plt.scatter(data_x1[:,0], data_x1[:,1], s=1, c='black')
	plt.scatter(data_x2[:,0], data_x2[:,1], s=1, c='black')
	limy = plt.ylim()
	limx = plt.xlim()

	lims = [ min(limy[0], limx[0]), max(limy[1], limx[1])]

	plt.ylim(lims)
	plt.xlim(lims)
	plt.axis('scaled')
	plt.show()