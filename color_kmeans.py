# import the necessary packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import utils
import cv2
import numpy as np
def image_kmeans():
    #array_ = np.zeros((10000,10000),dtype='float32')
    #image = cv2.imread("D:/HDR/4p2s/Phenacobius mirabilis/INHS_FISH_400.jpg")
    image = cv2.imread("D:/HDR/4p2s/Phenacobius mirabilis/cut-off-border/cut_off_INHS_FISH_400.png")
    # BGR-->RGB cv to matplotlib show
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # show our image
    plt.figure()
    plt.axis("off")
    #plt.imshow(image)

    # reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # cluster the pixel intensities
    clt = KMeans(n_clusters=8)
    clt.fit(image)

    # build a histogram of clusters and then create a figure
    # representing the number of pixels labeled to each color
    hist = utils.centroid_histogram(clt)
    bar = utils.plot_colors(hist, clt.cluster_centers_)

    #np.savetxt('C:/Users/apple/Downloads/color_paltte.csv', bar, delimiter=',', fmt='%f')
    #np.savetxt("C:/Users/apple/Downloads/color_paltte.csv", bar.reshape((3,-1)), fmt="%f", header=str(bar.shape))
    # show our color bart
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.show()

image_kmeans()