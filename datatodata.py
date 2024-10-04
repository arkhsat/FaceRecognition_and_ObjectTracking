import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    
})

ref = db.reference('Person')

data = {
    "111":
        {
            "name": "Arkhananta",
            "title": "D4561"
        },
    "122":
        {
            "name": "Elon",
            "title": "D4562"
        },
    "133":
        {
            "name": "Trump",
            "title": "D4563"
        },
}

for key, value in data.items():
    ref.child(key).set(value)
