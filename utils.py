import numpy as np
import cv2


def centroid_histogram(clt):
    number_labels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=number_labels)
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist


def plot_colors(hist, centroids):

    bars = np.zeros((60, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        endX = startX + (percent * 300)
        cv2.rectangle(bar, 
                      (int(startX), 0),
                      (int(endX), 50),
                      color.astype("uint8").tolist(), 
                      -1)
        startX = endX

    return bars
