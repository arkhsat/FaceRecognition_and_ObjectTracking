import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey1.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://testing1-5b399-default-rtdb.firebaseio.com/"
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
    "144":
        {
            "name": "Hardwin",
            "title": "D4564"
        },
    "155":
        {
            "name": "Indra",
            "title": "D4565"
        },
    "166":
        {
            "name": "Benny",
            "title": "D4566"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
