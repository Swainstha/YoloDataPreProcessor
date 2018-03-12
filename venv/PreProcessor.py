import cv2
import numpy as np
import os
import sys
import glob
import math


drawing=False # true if mouse is pressed
mode=True # if True, draw rectangle. Press 'm' to toggle to curve
breakloop = False
lineWidth = 2

class data:
    i=0
    draw = True
    img = 0
    drawImage = False
    name = ""

# mouse callback function
def points_draw(event,former_x,former_y,flags,param):
    global current_former_x,current_former_y,drawing, mode, center_x, center_y, width, length, name

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        if data.draw == True:
            current_former_x,current_former_y=former_x,former_y
            data.draw = False
            data.i = data.i + 1
            print("first")
        else:
            if data.i == 1:
                center_x = (current_former_x + former_x) / 2
                center_y = (current_former_y + former_y) / 2
                angle = math.atan((current_former_y - former_y)/(current_former_x - former_x))
                diagonal = np.sqrt(np.square(current_former_x - former_x) + np.square(current_former_y - former_y))
                width = diagonal * math.cos(angle)
                length = diagonal * math.sin(angle)

                if data.drawImage == False:
                    data.drawImage = True
                    cv2.line(data.img, (current_former_x, current_former_y), (int(former_x - width), former_y),
                             (0, 0, 255), lineWidth)
                    cv2.line(data.img, (current_former_x, current_former_y), (former_x, int(former_y - length)),
                             (0, 0, 255), lineWidth)
                    cv2.line(data.img, (former_x, former_y), (int(former_x - width), former_y), (0, 0, 255), lineWidth)
                    cv2.line(data.img, (former_x, former_y), (former_x, int(former_y - length)), (0, 0, 255), lineWidth)
                    cv2.imshow('Interface', data.img)
                else:
                    cv2.line(data.temp, (current_former_x, current_former_y), (int(former_x - width), former_y),
                             (0, 0, 255), lineWidth)
                    cv2.line(data.temp, (current_former_x, current_former_y), (former_x, int(former_y - length)),
                             (0, 0, 255), lineWidth)
                    cv2.line(data.temp, (former_x, former_y), (int(former_x - width), former_y), (0, 0, 255), lineWidth)
                    cv2.line(data.temp, (former_x, former_y), (former_x, int(former_y - length)), (0, 0, 255), lineWidth)
                    cv2.imshow('Interface', data.temp)
                current_former_x = former_x
                current_former_y = former_y
                print("second")
                data.name = "1-" + str(int(center_x)) + "-" + str(int(center_y)) + "-" + str(int(length)) + "-" + str(
                    int(width))
                print(data.name)
                data.i = data.i + 1


    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if mode==True:
                cv2.line(data.img,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),lineWidth)
                current_former_x = former_x
                current_former_y = former_y
                #print former_x,former_y
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode==True:
            cv2.line(data.img,(current_former_x,current_former_y),(former_x,former_y),(0,0,255),lineWidth)
            current_former_x = former_x
            current_former_y = former_y
    return former_x,former_y

cv2.namedWindow("Interface", cv2.WINDOW_NORMAL)
cv2.resizeWindow('Interface', 1000, 1000)
cv2.setMouseCallback('Interface', points_draw)

for infile in glob.glob( os.path.join("1-1000/", '*.*') ):
    ext = os.path.splitext(infile)[1][1:]  # get the filename extenstion
    if ext == "png" or ext == "jpg" or ext == "bmp" or ext == "tiff" or ext == "pbm":

        data.img = cv2.imread(infile,1)
        data.temp = cv2.imread(infile,1)
        data.save = cv2.imread(infile,1)
        data.draw = True
        # data.drawImage = True

        if data.img is None:
            continue
        cv2.imshow('Interface', data.img)
        while(1):

            k = (cv2.waitKey(0) & 0xFF)
            if k == 27:
                breakloop = True
                break
            elif k == 32:
                if data.i == 2:
                    cv2.imwrite("Positive_Processed/" + data.name + ".jpg", data.save)
                    os.remove(infile)
                data.i = 0

                break
            elif k == 102:
                data.i = 0
                cv2.imshow('Interface', data.temp)
                data.drawImage = True
                data.draw = True
                print("changed")


        if breakloop == True:
            break

cv2.destroyAllWindows()