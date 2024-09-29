import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("Final Project/ServcieAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-f03aa-default-rtdb.firebaseio.com/"
})

ref=db.reference('Students')
data={
    "20221":{
        #"id":20221,
        "name":"Elon Musk",
        "Major":"Computer science",
        "Starting year":2008,
        "total attendance":19,
        "Standing":"G",
        "year":4,
        "last_attendance_time":"2005-7-4 00:54:34"
    },
    "20224":{
        #"id":20224,
        "name":"Mohamed Ashraf",
        "Major":"AI engineer",
        "Starting year":2022,
        "total attendance":20,
        "Standing":"G",
        "year":3,
        "last_attendance_time":"2024-7-4 00:54:34"
    },
    "20225":{
        #"id":20225,
        "name":"Emly Blunt",
        "Major":"Acting",
        "Starting year":2002,
        "total attendance":24,
        "Standing":"VG",
        "year":2,
        "last_attendance_time":"2016-7-4 00:54:34"
    },
    "20227":{
        #"id":20227,
        "name":"Cristiano ronaldo",
        "Major":"Football",
        "Starting year":2008,        
        "total attendance":7,
        "Standing":"Awesome",
        "year":4,
        "last_attendance_time":"2007-7-7 00:54:34"
    }


}
for key,value in data.items():
    ref.child(key).set(value)