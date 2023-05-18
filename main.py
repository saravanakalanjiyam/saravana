import cv2
import numpy as np
import cvzone
import pickle


width, height = (100), (150)

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos','rb') as f:
    posList = pickle.load(f)

def checkParkingspace(imgPro):
    spaceCounter = 0
    for pos in posList:


        x,y = pos
        #cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
        cv2.imshow('Video', img)

        imgCrop = imgPro[y:y+height, x:x+width]
        cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-10),scale=1,thickness=2,offset=0,colorR=(0,0,255))

        if count < 420:
            color = (0,255,0)
            thickness=5
            spaceCounter +=1
        else:
            color = (0,0,255)
            thickness =2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(img,f'FREE{str(spaceCounter)}/{len(posList)}',(1000,20),scale=1,thickness=1,offset=10,colorR=(200,0,0))

while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                          cv2.THRESH_BINARY_INV,25,16)

    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.zeros((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)


    if not success:
        cap.release()
        cap = cv2.VideoCapture('carPark.mp4')
        success, img = cap.read()

    checkParkingspace(imgDilate)
    # for pos in posList:
    #     x,y = pos
    #     cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)

    cv2.imshow('Image',img)
    cv2.imshow('ImageBlur',imgBlur)
    cv2.imshow('Imagethreshold',imgThreshold)
    cv2.imshow('ImageMedian',imgMedian)
    cv2.imshow('ImageDilate',imgDilate)


    if cv2.waitKey(1) == 27:  # esc key to exit
        break

cv2.destroyAllWindows()

