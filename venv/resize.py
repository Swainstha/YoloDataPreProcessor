import os
import sys
import glob
import cv2

W = 1000.
i=0
cv2.namedWindow('Interface',cv2.WINDOW_NORMAL)

for infile in glob.glob( os.path.join("/home/nic/python/yoloDataPreProcessor/Positive_test", '*.*') ):
    ext = os.path.splitext(infile)[1][1:]  # get the filename extenstion
    if ext == "png" or ext == "jpg" or ext == "bmp" or ext == "tiff" or ext == "pbm":

        img = cv2.imread(infile, 1)
        if img is None:
            continue

        height, width, depth = img.shape
        imgScale = W / width
        newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
        newimg = cv2.resize(img, (int(newX), int(newY)),interpolation = cv2.INTER_CUBIC)
        cv2.imshow("Interface", newimg)
        # cv2.imwrite("resize_photos/" + str(i) + ".jpg",newimg)
        cv2.imwrite("/home/nic/python/yoloDataPreProcessor/Resize_test/" + str(i) + ".jpg",newimg)
        i = i+1


cv2.destroyAllWindows()