import cv2

image = cv2.imread("D:/HDR/INHS_FISH_26.jpg")
#cv2.waitKey(0)

print(image.shape)
print(f"height::{image.shape[0]}")
print(f"width::{image.shape[1]}")
print(f"channel number:{image.shape[2]}")


print(f"total pixel number:{image.size}")
print(f"image datatype:{image.dtype}")
print(f"image depth:{image.depth}")