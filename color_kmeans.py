"""
    color palette
"""

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import utils
import cv2
import numpy as np


def colorPalette(img_path):
    # array_ = np.zeros((10000,10000),dtype='float32')
    # image = cv2.imread("D:/HDR/4p2s/Phenacobius mirabilis/INHS_FISH_400.jpg")
    image = cv2.imread(img_path)
    if image is None:
        print("Error: [Module - Color Palette] Sorry, failed to load image.")
    else:
        # show image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.figure()
        plt.axis("off")
        plt.imshow(image)
        # image-> list of pixels
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        # cluster
        clt = KMeans(n_clusters=8)
        clt.fit(image)

        # build a histogram of clusters and then create a figure
        # representing the number of pixels labeled to each color
        hist = utils.centroid_histogram(clt)
        bar = utils.plot_colors(hist, clt.cluster_centers_)

        # np.savetxt('C:/Users/apple/Downloads/color_paltte.csv', bar, delimiter=',', fmt='%f')
        # np.savetxt("C:/Users/apple/Downloads/color_paltte.csv", bar.reshape((3,-1)), fmt="%f", header=str(bar.shape))
        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()

