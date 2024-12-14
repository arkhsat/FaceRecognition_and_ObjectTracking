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
    "2024 - 11 - 19":
        {
            "10:00 - 10:37": "111",
            "10:38 - 10:46": "111",
            "10:50 - 10:55": "111",
            "11:20 - 11:24": "111",
            "11:40 - 11:44": "111",
            "11:50 - 11:52": "111",
            "13:30 - 13:52": "111",
            "23:40 - 23:44": "111",
        },
    "2024 - 11 - 22":
        {
            "22:00 - 22:25": "111",
        },
    "2024 - 11 - 25":
        {
            # "00:00 - 23:59": "111",
            "23:00 - 23:07": "111",
            "23:00 - 23:19": "111"
        },
    "2024 - 12 - 02":
        {
            "09:10 - 10:10": "111",
            "11:00 - 15:00": "111",
            "17:00 - 23:00": "111",

        },
    "2024 - 12 - 03":
        {
            "09:10 - 23:10": "111",
        },
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
    "2024 - 12 - 14":
        {
            "00:00 - 23:43": "111",
        },
}

for key, value in data.items():
    ref.child(key).set(value)
