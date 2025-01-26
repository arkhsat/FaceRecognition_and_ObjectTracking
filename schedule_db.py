import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey1.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://testing1-5b399-default-rtdb.firebaseio.com/"
})

ref = db.reference('schedule')

data = {
    "2024 - 12 - 04":
        {
            "13:10 - 14:48": "111",
            "14:50 - 23:48": "111",
        },
    "2024 - 12 - 10":
        {
            "00:30 - 17:00": "111",
            "21:02 - 21:57": "111"
        },
    "2024 - 12 - 11":
        {
            # "00:30 - 23:00": "111",
            "18:30 - 20:19": "111",
            "23:00 - 23:59": "111"
        },
    "2024 - 12 - 20":
        {
            "09:51 - 23:34": "111",
        },
    "2025 - 01 - 10":
        {
            "16:00 - 20:39": "111"
        },
    "2025 - 01 - 13":
        {
            "16:50 - 20:39": "111"
        },
    "2025 - 01 - 14":
        {
            "16:56 - 18:47": "111",
        },
    "2025 - 01 - 17":
        {
            # "10:27 - 12:29": "111",
            "18:30 - 20:00": "111",
        },
    "2025 - 01 - 23":
        {
            "18:48 - 20:05": "111",
        },
    "2025 - 01 - 25":
        {
            "00:00 - 23:00": "111",
        },
    "2025 - 01 - 26":
        {
            # "15:00 - 22:52": "111",
            "16:00 - 16:31": "111",
            "16:50 - 16:56": "111",
        },
}

for key, value in data.items():
    ref.child(key).set(value)
