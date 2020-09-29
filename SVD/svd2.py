import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact,interactive,interact_manual
from skimage import data
from skimage.color import rgb2gray
from skimage import img_as_ubyte,img_as_float
from numpy.linalg import svd


def compress_svd(image, k):
    """
    Perform svd decomposition and truncated (using k singular values/vectors) reconstruction
    returns
    --------
      reconstructed matrix reconst_matrix, array of singular values s
    """
    U, s, V = svd(image, full_matrices=False)
    reconst_matrix = np.dot(U[:, :k], np.dot(np.diag(s[:k]), V[:k, :]))

    return reconst_matrix, s



