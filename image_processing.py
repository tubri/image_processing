import sys
import color_histogram, color_kmeans, hsv_histogram


def generateplots(img_path):
    color_histogram.grayHist(img_path)
    color_histogram.rgbHist(img_path)
    color_kmeans.colorPalette(img_path)
    hsv_histogram.hsvHist(img_path)


if __name__ == "__main__":
    image_path = sys.argv[1]
    with open(image_path) as file:
        generateplots(image_path)
