import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("Final Project/ServcieAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-f03aa-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendancerealtime-f03aa.appspot.com"
})

# Encoding Images 1 by 1 then inserting in a list 1 by 1

#Importing the student images into a list 
folderPath='Final Project/Images'
PathList=os.listdir(folderPath)
print(PathList)
imgList=[]
studentIds=[]
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])
    #print(path)
    #print(os.path.splitext(path)[0])
    #fileName=os.path.join(folderPath,path)
    fileName=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)
print(studentIds)


def findEncodings(imagesList):
    encodeList=[]
    for img in imagesList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding Started ...")
encodingListKnown=findEncodings(imgList)
encodingListKnownWithIds=[encodingListKnown,studentIds]
#print(encodingListKnown) 
print("Encoding Complete")

file=open("EncodeFile.p",'wb')
pickle.dump(encodingListKnownWithIds,file)
file.close()
print("File Saved")