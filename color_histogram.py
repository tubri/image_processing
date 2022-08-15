from matplotlib import pyplot as plt
import numpy as np
import cv2

def process_gray():
    #image = cv2.imread("D:/HDR/4p2s/Phenacobius mirabilis/INHS_FISH_400.jpg")
    image = cv2.imread("D:/HDR/4p2s/Phenacobius mirabilis/cut-off-border/cut_off_INHS_FISH_400.png")
    #cv2.imshow("Original",image)
    #cv2.waitKey(0)

    grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([grayimage],[0],None,[256],[1,255])

    plt.figure()#create new figure
    plt.title("Grayscale Histogram")#figure title
    plt.xlabel("Bins")#x axis label
    plt.ylabel("# of Pixels")#Y axis label
    plt.plot(hist)# draw histgram
    plt.xlim([1,255])#set interval of x axis
    plt.show()# show figure



    chans = cv2.split(image)
    colors = ("b","g","r")
    plt.figure()
    plt.title("Flattened Color Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")

    for (chan,color) in zip(chans,colors):
        hist = cv2.calcHist([chan],[0],None,[256],[1,255])
        plt.plot(hist,color = color)
        plt.xlim([1,255])
        #np.savetxt('D:/HDR/'+ color +'histogram.csv', hist, delimiter=',', fmt='%.4f')
    plt.show()

process_gray()
