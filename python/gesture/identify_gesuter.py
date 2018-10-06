import cv2
import numpy as np
from numpy import linalg

idx = 0

example_contour = list()
font = cv2.FONT_HERSHEY_COMPLEX

gestures = np.load('gesture/gestures/composite_list.npy',encoding="latin1")
labels = np.load('gesture/gestures/composite_list_labels.npy', encoding="latin1")

class GestureRecognizer():
    # Constructor...
    def __init__(self):
        self.video = self.VideoCapture()
    
    def VideoCapture(self):
        video = cv2.VideoCapture(0)
        video.set(3, 650)
        video.set(4, 500)

        return video

    def __del__(self): 
        self.video.release()

    def get_frame(self):
        ret, img = self.video.read()
        img = cv2.flip(img, 1)
        cv2.rectangle(img,(300,300),(0,0),(0,255,0),0)
        roi= img[0:300, 0:300]
        gray =cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (35,35), 0)
        _, edges = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        _, contours, hierarchy = cv2.findContours(edges.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        y = len(contours)
        area = np.zeros(y)
        for i in range(0, y):
            area[i] =  cv2.contourArea(contours[i])
        
        index = area.argmax()
        hand = contours[index]
        x,y,w,h = cv2.boundingRect(hand)
        cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),0)
        temp = np.zeros(roi.shape, np.uint8)
        
        M = cv2.moments(hand)
        
        cv2.drawContours(temp, [hand], -1, (0, 255,0), -1)
        cv2.drawContours(img, [hand], -1, (0, 255,0), -1)
        
        key = cv2.waitKey(1)
        
        measures = list()
        for g in gestures:
            m= cv2.matchShapes(hand, g, 1, 0.0)
            measures.append(m)

        z = measures.index(min(measures))
        result = labels[z]
        cv2.putText(img,str(result), (600, 20), font, 0.7,(255,255,255),2,cv2.LINE_AA)

        ret2, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()