import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta
import time

import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # Lokasi file schedule.py
cred_path = os.path.join(base_dir, "serviceAccountKey1.json")

# cred = credentials.Certificate("serviceAccountKey1.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://testing1-5b399-default-rtdb.firebaseio.com/",
    'storageBucket': "testing1-5b399.appspot.com"

})


def is_scheduled(person_id):
    current_date = datetime.now().strftime("%Y - %m - %d")
    # print(f"Accessing Firebase path: schedule/{current_date}")
    current_time = datetime.now()
    # current_time = datetime.now().strftime("%H:%M:%S")
    # print(f"current_time: {current_time} (type: {type(current_time)})")

    # print(current_time)

    # Get the schedule for the current date
    schedule_ref = db.reference(f'schedule/{current_date}')
    schedule_data = schedule_ref.get()
    # print(schedule_data)

    if schedule_data:
        for time_range, scheduled_id in schedule_data.items():
            start_time, end_time = time_range.split(' - ')
            start_hour, start_minute = start_time.split(':')
            end_hour, end_minute = end_time.split(':')

            scheduled_start_time = datetime.strptime(f"{current_date} "
                                                     f"{start_hour}:{start_minute}", "%Y - %m - %d %H:%M")
            scheduled_end_time = datetime.strptime(f"{current_date} "
                                                   f"{end_hour}:{end_minute}", "%Y - %m - %d %H:%M")

            # print(f" schedule stat time: {scheduled_start_time}")
            # print(f" schedule end time : {scheduled_end_time}")

            # Handle the case where the end time is on the next day
            if scheduled_end_time < scheduled_start_time:
                scheduled_end_time += timedelta(days=1)

            if str(scheduled_id) == str(person_id):
                if scheduled_start_time <= current_time <= scheduled_end_time:
                    return scheduled_start_time, scheduled_end_time, current_time, time_range, current_date,
                # elif current_time > scheduled_end_time:
                #     time.sleep(10)
                #     return scheduled_start_time, scheduled_end_time, current_time, time_range, current_date
                # elif current_time > scheduled_end_time:
                #     scheduled_start_time = None
                #     scheduled_end_time = None
                #     return scheduled_start_time, scheduled_end_time
    return None
