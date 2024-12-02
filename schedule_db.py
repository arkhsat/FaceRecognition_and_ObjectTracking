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
    "2024 - 09 - 18":
        {
            "21:00 - 23:59": "111",
            "13:00 - 14:00": "122",
            "15:00 - 17:00": "133",

        },
    "2024 - 09 - 19":
        {
            "10:00 - 23:50": "111",
            "14:00 - 15:00": "122",
            "16:00 - 17:00": "133",
        },
    "2024 - 09 - 20":
        {
            "15:00 - 23:50": "111",
            "00:00 - 01:00": "122",
            "00:00 - 02:00": "133",
        },
    "2024 - 09 - 21":
        {
            "10:00 - 23:59": "111",
            "00:00 - 01:00": "122",
            "00:00 - 02:00": "133",
        },
    "2024 - 09 - 23":
        {
            "23:30 - 23:59": "111",
            "00:00 - 01:00": "122",
            "00:00 - 02:00": "133",
        },
    "2024 - 09 - 24":
        {
            "14:00 - 23:30": "111",
            "00:00 - 01:00": "122",
            "00:00 - 02:00": "133",
        },
    "2024 - 09 - 25":
        {
            "14:00 - 23:30": "111",
            "00:00 - 01:00": "122",
            "00:00 - 02:00": "133",
        },
    "2024 - 09 - 26":
        {
            "10:00 - 23:30": "111",
            "00:00 - 01:00": "122",
            "00:00 - 02:00": "133",
        },
    "2024 - 09 - 27":
        {
            "21:00 - 21:30": "111",
        },
    "2024 - 09 - 28":
        {
            "13:30 - 22:30": "111",
        },
    "2024 - 09 - 29":
        {
            "21:30 - 23:59": "111",
        },
    "2024 - 09 - 30":
        {
            "09:30 - 23:59": "111",
        },
    "2024 - 10 - 01":
        {
            "09:30 - 23:59": "111",
        },
    "2024 - 10 - 02":
        {
            "09:30 - 23:59": "111",
        },
    "2024 - 10 - 03":
        {
            "17:00 - 22:00": "111",
        },
    "2024 - 10 - 04":
        {
            # "09:00 - 09:34": "111",
            "10:30 - 17:00": "111",
        },
    "2024 - 10 - 06":
        {
            "17:00 - 18:00": "111",
            "23:00 - 23:59": "111"
        },
    "2024 - 10 - 07":
        {
            # "11:40 - 11:49": "111",
            # "12:00 - 12:30": "111",
            # "12:31 - 13:00": "111",
            # "14:00 - 14:50": "111",
            "22:00 - 22:44": "111",


            # "12:00 - 12:30": "122",
            # "12:35 - 13:00": "122"
        },
    "2024 - 10 - 08":
        {
            "16:00 - 16:30": "111",
            "20:00 - 21:30": "111",
        },
    "2024 - 10 - 09":
        {
            "12:00 - 13:30": "111",
            "15:31 - 16:00": "111",

        },
    "2024 - 10 - 10":
        {
            "16:00 - 16:21": "111",
            "21:52 - 23:00": "111",

        },
    "2024 - 10 - 11":
        {
            "09:00 - 11:00": "111",
            "12:30 - 15:00": "111",

        },
    "2024 - 10 - 12":
        {
            "00:00 - 01:00": "111",

        },
    "2024 - 10 - 14":
        {
            # "10:00 - 10:10": "111",
            "21:00 - 23:59": "111"

        },
    "2024 - 10 - 15":
        {
            # "10:00 - 10:10": "111",
            "16:00 - 23:50": "111"

        },
    "2024 - 10 - 16":
        {
            # "20:28 - 20:30": "111",
            "20:31 - 23:59": "111",

        },
    "2024 - 10 - 17":
        {
            "00:00 - 23:59": "111",
            "13:00 - 23:59": "144",

        },
    "2024 - 10 - 18":
        {
            # "10:00 - 10:24": "111",
            # "15:00 - 15:04": "111",
            "15:39 - 23:42": "111"

        },
    "2024 - 10 - 24":
        {
            "14:00 - 17:00": "111"

        },
    "2024 - 10 - 25":
        {
            "23:00 - 23:17": "111"

        },
    "2024 - 10 - 26":
        {
            "01:00 - 01:08": "111"

        },
    "2024 - 10 - 28":
        {
            "16:40 - 16:59": "111"

        },
    "2024 - 11 - 06":
        {
            "00:00 - 23:00": "111"
        },
    "2024 - 11 - 07":
        {
            "00:00 - 23:00": "111",
            "00:00 - 22:00": "122"
            # "13:10 - 13:20": "111"
        },
    "2024 - 11 - 08":
        {
            "00:00 - 23:00": "111",
            "14:00 - 23:00": "144",
            "00:00 - 22:00": "122"
        },
    "2024 - 11 - 11":
        {
            "00:00 - 23:50": "111",
            # "14:00 - 23:00": "144",
            # "00:00 - 22:00": "122"
        },
    "2024 - 11 - 12":
        {
            "00:00 - 23:50": "111",
            # "14:00 - 23:00": "144",
            # "00:00 - 22:00": "122"
        },
    "2024 - 11 - 13":
        {
            "23:40 - 23:57": "111",
            # "14:00 - 23:00": "144",
            # "00:00 - 22:00": "122"
        },
    "2024 - 11 - 14":
        {
            "13:13 - 13:20": "111",
            "15:50 - 16:30": "111",
        },
    "2024 - 11 - 15":
        {
            # "09:45 - 09:48": "111",
            "09:50 - 23:59": "111",
        },
    "2024 - 11 - 16":
        {
            # "09:45 - 09:48": "111",
            "00:00 - 23:59": "111",
        },
    "2024 - 11 - 18":
        {
            # "09:45 - 09:48": "111",
            # "00:00 - 23:59": "111",
            "00:00 - 01:59": "111",
            "10:00 - 13:00": "111",
        },
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

        },


}

for key, value in data.items():
    ref.child(key).set(value)
