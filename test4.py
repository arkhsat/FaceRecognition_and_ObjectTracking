import pickle
import cv2
import cvzone
import os
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
    'storageBucket': ""
})


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


# load encoding file
print("Loading Encoding File....")
file = open('EncodeFileNew.p', 'rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnow, id = encodeListKnowWithIds
# print(id)
# print(encodeListKnow)
print("Encode File Loaded")

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # from BGR TO RGB

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        print("matches", matches)
        print("faceDis", faceDis)
        # print(sum(faceDis))

        matchIndex = np.argmin(faceDis)
        # print("Match Index", matchIndex)

            # print("Knowing the Face")
            # print(id[matchindex])
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # scale up the face location

        if matches[matchIndex]:
            cvzone.cornerRect(img, (x1, y1, x2 - x1, y2 - y1), rt=1,
                              colorC=(0, 255, 0))  # green color for matched faces
            #cvzone.putTextRect(img, f'ID: {id}', (x1, y1 - 10), scale=1, thickness=2, colorR=(255, 0, 0))

        # else:
            # cvzone.cornerRect(img, (x1, y1, x2 - x1, y2 - y1), rt=0,
                              # colorC=(0, 0, 255))

    cv2.imshow("Webcame", img)
    cv2.waitKey(1)
