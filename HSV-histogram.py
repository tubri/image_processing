from matplotlib import pyplot as plt
import numpy as np
import cv2

image = cv2.imread("D:/HDR/INHS_FISH_26.jpg")
cv2.imshow("Original",image)
#cv2.waitKey(0)


hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

plt.figure()#create new figure
plt.title("H-channel(Hue) Histogram")#figure title
plt.xlabel("Bins")#x axis label
plt.ylabel("# of Pixels")#Y axis label
#plt.plot(hist)# draw histgram
h = hsv[...,0]
s = hsv[...,1]
v = hsv[...,2]
hist_hsv_h = cv2.calcHist(h,[0],None,[180],[1,180])
#plt.plot(hist_hsv_h)
#np.savetxt('C:/Users/apple/Downloads/h_histogram.csv', hist_hsv_h, delimiter=',', fmt='%.4f')

#plt.xlim([0,180,0,256])#set interval of x axis
#plt.show()# show figure

plt.figure()#create new figure
plt.title("S-channel(Saturation) Histogram")#figure title
plt.xlabel("Bins")#x axis label
plt.ylabel("# of Pixels")#Y axis label
#plt.plot(hist)# draw histgram
hist_hsv_s = cv2.calcHist(s,[0],None,[256],[1,256])
#plt.plot(hist_hsv_s)
#plt.show()
#np.savetxt('C:/Users/apple/Downloads/s_histogram.csv', hist_hsv_s, delimiter=',', fmt='%.4f')


plt.figure()#create new figure
plt.title("V-channel(Value,Brightness) Histogram")#figure title
plt.xlabel("Bins")#x axis label
plt.ylabel("# of Pixels")#Y axis label
#plt.plot(hist)# draw histgram
hist_hsv_v = cv2.calcHist(v,[0],None,[256],[1,256])
plt.plot(hist_hsv_v)
#plt.show()
#np.savetxt('C:/Users/apple/Downloads/v_histogram.csv', hist_hsv_v, delimiter=',', fmt='%.4f')
