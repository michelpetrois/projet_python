import numpy as np
import matplotlib.pyplot as plotter

def graph1(entete, data):
    # transform nump array
    label = np.array2string(entete, prefix='-', suffix='_', separator='", "')
    print(label)


a = np.array([1, 1, 2, 3, 4, 1, 2, 5, 6, 7, 2, 3, 1, 2, 4, 8, 9, 0, 4, 1, 2, 6, 2, 6, 2, 1, 9])
entete, cumul = np.unique(a, return_counts=True)
print(entete)
print(entete.ndim)
print(entete.shape)
print(cumul)
print(cumul.ndim)
print(cumul.shape)
taille = np.shape(entete)
deux_dim = np.vstack((entete, cumul))
print(a)
print(entete)
print(cumul)
print(deux_dim)
print(deux_dim.ndim)
print(deux_dim.shape)

graph1(entete, cumul)
