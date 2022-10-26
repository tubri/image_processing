#import argparse
import color_histogram, color_kmeans
import cv2
#import imageprocessing,HSV

# parser = argparse.ArgumentParser(description='manual to this script')
# parser.add_argument('--path', type=str, default = None)
# parser.add_argument('--batch-size', type=int, default=32)
# args = parser.parse_args()

import os, sys
path = sys.argv[1]
image_list = []
for dirpath, dirnames, filenames in os.walk(path):
    for file in filenames:
        fullpath = os.path.join(dirpath, file)
        print(fullpath)
        image = cv2.imread(fullpath)
        image_list.append(image)
        color_histogram.process_gray(image)
        print("color_histogram...processing...done")
        # color_kmeans.image_kmeans(image)
        print("kmeans_histogram...processing...done")

#
# for image in image_list:
#     color_histogram.process_gray()
#     color_kmeans.image_kmeans()
