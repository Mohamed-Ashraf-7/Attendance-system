import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("Final Project/ServcieAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-f03aa-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendancerealtime-f03aa.appspot.com"
})

bucket=storage.bucket()


# To opeen the camera we take object of cv2 and give camera inc=dex in pracets
cap=cv2.VideoCapture(0)
cap.set(3,640) # size
cap.set(4,480) # quality

imgBackground=cv2.imread('Final Project/Resources/background.png')
#Importing the mode images into a list 
folderModePath='Final Project/Resources/Modes'
modePathList=os.listdir(folderModePath)
imgModeList=[]
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imgModeList))

#load the encoding file 
print("Loading Encode File ...")
file=open('EncodeFile.p','rb')
encodeListKnownWithIds=pickle.load(file)
file.close()
encodeListKnown,studentIds=encodeListKnownWithIds
#print(studentIds)
print("Encode File Loaded ...")

modeType=0
counter=0
id=-1
imgStudent=[]

bbox_color=(255, 255, 255)

while True:
    success,img=cap.read()

    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame=face_recognition.face_encodings(imgs,faceCurFrame)


    imgBackground[162:162 + 480, 55:55 + 640]=img
    imgBackground[44:44 + 633, 808:808 + 414]=imgModeList[modeType]

    for encodeFace,faceloc in zip(encodeCurFrame,faceCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace) #true on wich index
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace) #how much look alike
        #print("matches",matches)
        #print("faceDis",faceDis)

        matchIndex=np.argmin(faceDis)
        #print("Match Index",matchIndex)

        if matches[matchIndex]:
            print("Known face Deteceted")
            print(studentIds[matchIndex])
            y1,x2,y2,x1=faceloc
            y1,x2,y2,x1 =y1*4,x2*4,y2*4,x1*4
            bbox=55+x1,162+y1,x2-x1,y2-y1
            imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0,colorC=(255,255,255))
            #cv2.rectangle(imgBackground, (55 + x1, 162 + y1), (55 + x2, 162 + y2), bbox_color, 2)

            id=studentIds[matchIndex]
            if counter==0:
                counter=1
                modeType=1
    if counter != 0:
        if counter ==1:
            #Getting the data
            studentInfo=db.reference(f'Students/{id}').get()
            print(studentInfo)
            #Getting image from storage

            blob=bucket.get_blob(f'Images/{id}.png')
            array = np.frombuffer(blob.download_as_string(),np.uint8)
            imgStudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

        cv2.putText(imgBackground,str(studentInfo['total attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        #cv2.putText(imgBackground,str(studentInfo['name']),(808,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
        cv2.putText(imgBackground,str(studentInfo['Major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
        cv2.putText(imgBackground,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
        cv2.putText(imgBackground,str(studentInfo['Standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
        cv2.putText(imgBackground,str(studentInfo['year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
        cv2.putText(imgBackground,str(studentInfo['Starting year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
        
        (w,h),_=cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
        offset= (414-w)//2
        cv2.putText(imgBackground,str(studentInfo['name']),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
        
        imgBackground[175:175+216,909:909+216]=imgStudent

        counter


    #cv2.imshow("Webcam",img) #open webcam
    cv2.imshow("Face attendance",imgBackground) #graphics
    cv2.waitKey(1)