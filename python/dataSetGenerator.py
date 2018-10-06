
# coding: utf-8
import cv2
import os
import sqlite3
import numpy as np
import os

face_cascade = cv2.CascadeClassifier('casscade/haarcascade_frontalface_default.xml')

def get_file_directory_count():
    return len([dI for dI in os.listdir('training-images') if os.path.isdir(os.path.join('training-images',dI))]) + 1

def gen_randon_num():
    return np.random.randint(0, 10000)

def insertNewUser(cust_id, name, balance):
    p_id = cust_id
    p_name = name
    p_balance = balance
    
    conn = sqlite3.connect('hl.db')
    
    try:
        if conn:
            command = "SELECT * FROM Customer WHERE cust_id = ?"
            cursor = conn.execute(command, str(p_id))
            
            isRecordExist = 0
            for row in cursor:
                isRecordExist = 1
            
            if isRecordExist is True:
                command = "UPDATE Customer SET cust_name" + str(p_name) + " WHERE cust_id= " + str(p_id)
            else:
                command = "INSERT INTO Customer(cust_id, cust_name, cust_bal) Values(?,?,?)"
            
            conn.execute(command,(p_id, p_name, p_balance))
            conn.commit()
            conn.close()
    except sqlite3.ProgrammingError as ex:
        print("Error: " + str(ex))

def detect_face(face_id):
    cap = cv2.VideoCapture(0)
    count = 0
    
    while True:
        ret, img = cap.read()
        gray = 0
        
        if ret is True:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            continue
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            
            count+=1
            if not os.path.exists('training-images/' + face_id):
                os.mkdir('training-images/' + face_id)
            cv2.imwrite("training-images/" + str(face_id) + "/" + str(count) + ".jpg", roi_gray)
        
        if count > 20:
            cap.release()
            cv2.destroyAllWindows()
            break
        
        cv2.imshow('facial', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

insertNewUser(get_file_directory_count(), 'Edwin', gen_randon_num())
detect_face('Edwin')
