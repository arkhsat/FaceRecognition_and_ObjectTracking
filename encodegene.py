import os
import cv2
import face_recognition
import pickle
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    
})


#importing images
folderpath = 'Images'
pathList = os.listdir(folderpath)
imgList =[]
id = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderpath, path)))
    id.append(os.path.splitext(path)[0])

    fileName = os.path.join(folderpath, path)
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(id)


#create encoding
def findencodigs (imageslist):
    encodelist = []

    for img in imageslist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #from BGR TO RGB
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
        #print(encode)

    return encodelist


print("Encoding Start")
encodeListKnow = findencodigs(imgList)
print(encodeListKnow)
encodeListKnowWithIds =[encodeListKnow, id]
print("Encoding Complete")

file = open("EncodeFileNew.p", 'wb')
pickle.dump(encodeListKnowWithIds, file)
file.close()
print("File Save")
