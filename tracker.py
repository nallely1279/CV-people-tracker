# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 09:56:30 2020

@author: Nallely
"""


#import numpy as np
import cv2

cap = cv2.VideoCapture("video2.webm")

frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

ret, frame1 = cap.read()
ret, frame2 = cap.read()

cascade1 = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cascade2 = cv2.CascadeClassifier('haarcascade_upperbody.xml')
cascade3 = cv2.CascadeClassifier('haarcascade_lowerbody.xml')

all_dots=[]

def bodypair(body1, body2):
    #checks if two different body cascades are detecting the same person by 
    #setting an acceptable margin of error and returning True if they are detecting
    #the same person or false if they arent
            x1=body1[0]
            x2=body2[0]
            
            if (abs(x1-x2)<=75):
                return True
            else:
                return False

def draw_dots(list0):
    #draws all dots
    for i in range(len(list0)):
        for ii in range(len(list0[i])):
            
            dot_coordinate=list0[i][ii][0]
            color=list0[i][ii][1]
            cv2.circle(frame1, dot_coordinate, 3, color, -1)
        
def draw_bodies(list_bodies1,list_bodies2,list_bodies3, contour_bodies, current_dots, xc,yc,wc,hc):
    
    red=(0, 0, 255)
    green=(0, 128, 0)
    #current_dots=[]
    for i in range(len(list_bodies1)):
        #drawing all full bodies
        x1=list_bodies1[i][0]
        y1=list_bodies1[i][1]
        w1=list_bodies1[i][2]
        h1=list_bodies1[i][3]
        
        
        dot_coordinate=(int(xc+(w1/2)),int(yc+(h1/2)))
        current_dots+=[[dot_coordinate,green]]
        
        #if more than one body is detected in the same contour then it is assumed
        #they arent social distancing and all boex in the contour are drawn red
        
        if contour_bodies==1:
            cv2.rectangle(reconstructedImg, (x1, y1), (x1 + w1, y1 + h1), green, 2)
            current_dots+=[[dot_coordinate,green]]
            
        elif contour_bodies>1:
            cv2.rectangle(reconstructedImg, (x1, y1), (x1 + w1, y1 + h1), red, 2)
            current_dots+=[[dot_coordinate,red]]
            
            
    for i in range(len(list_bodies2)):
        #drawing all upper bodies
        x2=list_bodies2[i][0]+xc
        y2=list_bodies2[i][1]+yc
        w2=list_bodies2[i][2]+wc
        h2=list_bodies2[i][3]+hc
        yh=2*(y2 + h2)
        
        dot_coordinate=(int(xc+(w2/2)),int(yc+(yh/2)))
               
        if contour_bodies==1:
            cv2.rectangle(reconstructedImg, (x2, y2), (x2 + w2, y2 + yh), green, 2)
            current_dots+=[[dot_coordinate,green]]
            
        elif contour_bodies>1:
            cv2.rectangle(reconstructedImg, (x2, y2), (x2 + w2, yh), red, 2)
            current_dots+=[[dot_coordinate,red]]
            
            
    for i in range(len(list_bodies3)):
         #drawing all lower bodies
        x3=list_bodies3[i][0]+xc
        y3=list_bodies3[i][1]+yc
        w3=list_bodies3[i][2]+wc
        h3=list_bodies3[i][3]+hc
        y=y3-(0.5*h3)
        
        
        dot_coordinate=(int(xc+(w3/2)),int(y+(h3/2)))
        
        
        if contour_bodies==1:
            
            cv2.rectangle(reconstructedImg, (x3, y3), (x3 + w3, y3 + h3), green, 2)
            current_dots+=[[dot_coordinate,green]]
            
        elif contour_bodies>1:
            
            cv2.rectangle(reconstructedImg, (x3, y3), (x3 + w3, y3 + h3), red, 2)
            current_dots+=[[dot_coordinate,red]]

while cap.isOpened():
    
   
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    total_bodies=0
    current_dots=[]
    for contour in contours:
        
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 900:
            continue

        reconstructedImg=frame1[y:y+h+75, x:x+w+75]
        reconstuctedImg = cv2.cvtColor(reconstructedImg, cv2.COLOR_BGR2GRAY)
        
        
        body1 = cascade1.detectMultiScale(reconstructedImg, 1.3, 2)
        body2 = cascade2.detectMultiScale(reconstructedImg, 1.3, 2)
        body3 = cascade3.detectMultiScale(reconstructedImg, 1.3, 2)
                                  
        
        #checking of there is a person detected in the contour if not it is
        #assumed the contour is not a person                
        if (len(body1)!=0) or (len(body2)!=0) or (len(body3)!=0):
            #finding overlapping bodies and counting people in countour
            list_body1=[]
            list_body2=[]
            list_body3=[]
            
            #fist checks for full bodies then upper than lower
            #if they are detecting the same person it is not added to the total
            for i in range(len(body1)):
                list_body1+=[body1[i]]
                body_1=(body1[i][0],body1[i][1],body1[i][2],body1[i][3])
               
                for ii in range(len(body2)):
                    body_2=(body2[ii][0],body2[ii][1],body2[ii][2],body2[ii][3])
                    if bodypair(body_1,body_2)==False:
                        list_body2+=[body2[ii]]
                        
                    for iii in range(len(body3)):
                        body_3=(body3[iii][0],body3[iii][1],body3[iii][2],body3[iii][3])
                        if bodypair(body_1,body_3)==False:
                            list_body3+=[body3[iii]]
                      
                        
                
            #adding to bodycounts
            contour_bodies=len(list_body1+list_body2+list_body3)
            total_bodies+=contour_bodies
            
           
            
            draw_bodies(list_body1,list_body2,list_body3, contour_bodies, current_dots,x,y,w,h)
            #dot trail
            if len(current_dots)>0:
                all_dots.append(current_dots)
            if len(all_dots)>=25:
                all_dots.pop(0)
            contour_bodies=0
        
        cv2.putText(frame1, "People Count: {}".format(total_bodies), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)
                
                
        draw_dots(all_dots)
                
            

    image = cv2.resize(frame1, (640,480))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()