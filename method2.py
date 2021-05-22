# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 18:28:32 2020

@author: Nallely
"""
import numpy as np
import cv2

#Download the required files/sample videos here : https://users.soe.ucsc.edu/~pang/30/s20/prog4/data/
cascade1 = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cascade2 = cv2.CascadeClassifier('haarcascade_upperbody.xml')
cascade3 = cv2.CascadeClassifier('haarcascade_lowerbody.xml')

cap = cv2.VideoCapture("sample1.avi")
#cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1280,720))

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    body1 = cascade1.detectMultiScale(gray, 1.3, 5)
    body2 = cascade2.detectMultiScale(gray, 1.3, 5)
    body3 = cascade3.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in body1:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    for (x, y, w, h) in body2:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)


    for (x, y, w, h) in body3:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    out.write(img)
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
