"""
    grayscale histogram
    rgb histogram
"""
from matplotlib import pyplot as plt
import numpy as np
import cv2

def grayHist(img_path):
    #image = cv2.imread("D:/HDR/4p2s/Phenacobius mirabilis/INHS_FISH_400.jpg")
    # image = cv2.imread("C:/work/hdr/INHS_FISH_16295.png")
    image = cv2.imread(img_path)
    if image is None:
        print("Error: [Module - RGB&GRAYSCALE Histogram] Sorry, failed to load image.")
    #cv2.imshow("Original",image)
    #cv2.waitKey(0)
    else:
        # grayscale histogram
        # opencv --> read matrix as BGR mode, not RGB! BGR-->RGB/GRAY
        grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([grayimage], [0], None, [256], [1, 255])
        # create new figure
        plt.figure()
        # figure title
        plt.title("Grayscale Histogram")
        # x axis label
        plt.xlabel("Bins")
        # Y axis label
        plt.ylabel("# of Pixels")
        # draw histgram
        plt.plot(hist)
        # set interval of x axis
        plt.xlim([1, 255])
        # show figure
        plt.show()

def rgbHist(img_path):
    image = cv2.imread(img_path)
    if image is None:
        print("Error: [Module - RGB&GRAYSCALE Histogram] Sorry, failed to load image.")
        # cv2.imshow("Original",image)
        # cv2.waitKey(0)
    else:
        chans = cv2.split(image)
        colors = ("b","g","r")
        plt.figure()
        plt.title("Flattened Color Histogram")
        plt.xlabel("Bins")
        plt.ylabel("# of Pixels")

        for (chan,color) in zip(chans, colors):
            hist = cv2.calcHist([chan], [0], None, [256], [1, 255])
            plt.plot(hist, color = color)
            plt.xlim([1, 255])
            #np.savetxt('D:/HDR/'+ color +'histogram.csv', hist, delimiter=',', fmt='%.4f')
        plt.show()

#process_gray()
