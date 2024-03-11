import glob
import os
import cv2
import matplotlib.pyplot as plt

img_dir = "./Training/images/"
mask_dir = "./Training/mask_images/"


# img_dir = os.listdir("./Training/images")
# mask_dir = os.listdir("./Training/mask_images")

img = plt.imread("mask_sample.png")
# img = plt.imread(mask_dir + os.listdir(mask_dir)[900])
# mask = plt.imread(mask_dir[0])  # cv2.IMREAD_COLOR

# plt.subplot(2, 1, 1)
# plt.imshow(img)
plt.figure(figsize=(10, 10))
# plt.subplot(2, 2, 1)
plt.imshow(img)

plt.show()
