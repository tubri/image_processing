import cv2

def contours_demo(image):
    dst = cv2.GaussianBlur(image, (1, 1), 0)
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape


    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 11, 2)
    th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                cv2.THRESH_BINARY, 11, 2)
    # cv.imshow("thresh image", thresh)

    edges = cv2.Canny(th3, 15, 150)  # Edge detection
    #edges = cv2.dilate(edges, None)  # default(3x3)
    #edges = cv2.erode(edges, None)
    Image = cv2.bitwise_not(dst)
    cv2.namedWindow("res1", cv2.WINDOW_NORMAL)  #
    cv2.resizeWindow("res1", 640, 480)
    cv2.imshow("res1", edges)


    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  #
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    max_contour = contours[0]

    epsilon = 0.001 * cv2.arcLength(max_contour, True)
    approx = cv2.approxPolyDP(max_contour, epsilon, True)

    draw_img = src.copy()  # drawContours create new copy
    res = cv2.drawContours(draw_img, contours, -1, (0, 0, 255), 2)
    cv2.namedWindow("res", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("res", 640, 480)
    cv2.imshow("res", res)

def access_pixels(image):
    dst = cv2.GaussianBlur(image, (1, 1), 0)
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            for c in range(image.shape[2]):
                pv=image[row,col,c]
                if pv == 0:
                    image[row,col,c]=255-pv
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    draw_img = image.copy()
    resdd = cv2.drawContours(draw_img, contours, -1, (0, 0, 255), 2)
    cv2.namedWindow("pixels_demo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("pixels_demo", 640, 480)
    cv2.imshow('pixels_demo', resdd)


image = cv2.imread("D:/HDR/INHS_FISH_26.jpg")
#access_pixels(imagge)



def CannyThreshold(lowThreshold):
    detected_edges = cv2.GaussianBlur(gray, (3, 3), 0)
    detected_edges = cv2.Canny(detected_edges, lowThreshold, lowThreshold * ratio, apertureSize=kernel_size)
    dst = cv2.bitwise_and(img, img, mask=detected_edges)  # just add some colours to edges from original image.
    cv2.imshow('canny demo', dst)



lowThreshold = 0
max_lowThreshold = 100
ratio = 4
kernel_size = 3

img = cv2.imread("D:/HDR/INHS_FISH_26.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



cv2.namedWindow('canny demo',cv2.WINDOW_NORMAL)


cv2.createTrackbar('Min threshold', 'canny demo', lowThreshold, max_lowThreshold, CannyThreshold)


CannyThreshold(0)  # initialization
cv2.resizeWindow("canny demo", 640, 480)
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()


if __name__ == '__main__':
    src = cv2.imread("D:/HDR/INHS_FISH_26.jpg")
    #cv2.namedWindow("input image", cv2.WINDOW_NORMAL)  #
    #cv2.resizeWindow("input image", 640, 480)
    #cv2.imshow("input image", src)


    contours_demo(src)

    cv2.waitKey(0)  #
    cv2.destroyAllWindows()