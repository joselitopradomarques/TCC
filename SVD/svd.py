import matplotlib.pyplot as plt
import numpy as np
import time
from PIL import Image
from numpy.linalg import svd
import imageio

"""
#path = ("ch1_01.png")
try:
    image = Image.open(path)
except IOError:
    print("Import Error: IMAGE NOT FOUND!")
    pass
"""
def read_img(path):
    image = imageio.imread(path)
    return image

def svd_01(image):
    U, s, V = svd(image, full_matrices=False)
    return U, s, V

def svd_02(U, s, V, k):
    reconst_matrix = np.dot(U[:, :k], np.dot(np.diag(s[:k]), V[:k, :]))
    return reconst_matrix

def save_img(filename, matrix):
    imageio.imwrite(filename, matrix.astype('uint8'))
    pass

def all(path,k):
    image = read_img(path)
    U, s, V = svd_01(image)
    matrix = svd_02(U, s, V, k)
    save_img("m.png",matrix)

