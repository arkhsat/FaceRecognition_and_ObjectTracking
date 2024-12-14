import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta
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
        # active_schedule = []

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
                    return scheduled_start_time, scheduled_end_time, current_time, time_range, current_date

                    # active_schedule.append((scheduled_start_time, scheduled_end_time, time_range))

                # elif current_time >= scheduled_end_time:
                #     #     print("time is up ")
                #     return scheduled_start_time, scheduled_end_time, current_time, time_range, current_date
        #         else:
        #             return None
        #
        # if len(active_schedule) > 1:
        #     for i, (start1, end1, _) in enumerate(active_schedule):
        #         for j, (start2, end2, _) in enumerate(active_schedule):
        #             if i != j:  # Avoid self-comparison
        #                 if not (end1 <= start2 or start1 >= end2):  # Overlap condition
        #                     print(f"Conflict detected between {start1}-{end1} and {start2}-{end2}")
        #                     return None
        #
        # if active_schedule:
        #     scheduled_start_time, scheduled_end_time, time_range = active_schedule[0]
        #     return scheduled_start_time, scheduled_end_time, current_time, time_range, current_date

        #     if str(scheduled_id) == str(person_id):
        #         # return scheduled_start_time, scheduled_end_time, current_time, time_range, current_date
        #         # for checking status base on person_id and time_range
        #         if scheduled_start_time <= current_time <= scheduled_end_time:
        #             print(f"Schedule active for ID {person_id}")
        #             return scheduled_start_time, scheduled_end_time, current_time, time_range, current_date
        #         elif current_time >= scheduled_end_time:
        #             # print(f"Schedule ended for ID {person_id}")
        #             return scheduled_start_time, scheduled_end_time, current_time, time_range, current_date
        #         # return scheduled_start_time, scheduled_end_time, current_time, time_range, current_date
    # return None

    else:
        print("No Schedule")

    return None

# def is_scheduled(person_id):
#     """
#     Periksa apakah saat ini person_id memiliki jadwal aktif.
#     """
#     current_date = datetime.now().strftime("%Y-%m-%d")
#     current_time = datetime.now()
#
#     schedules_today = current_date
#
#     relevant_schedule = None
#     for schedule_id, schedule in schedules_today.items():
#         scheduled_start_time = datetime.strptime(schedule['start'], "%H:%M:%S")
#         scheduled_end_time = datetime.strptime(schedule['end'], "%H:%M:%S")
#
#         if scheduled_start_time <= current_time <= scheduled_end_time:
#             # Jadwal aktif
#             return scheduled_start_time, scheduled_end_time, current_time, schedule[
#                 'time_range'], current_date, schedule_id
#
#         if current_time >= scheduled_end_time and not relevant_schedule:
#             # Jadwal yang baru saja selesai
#             relevant_schedule = (scheduled_start_time, scheduled_end_time, schedule['time_range'], schedule_id)
#
#     # Kembalikan jadwal yang selesai jika tidak ada jadwal aktif
#     if relevant_schedule:
#         return relevant_schedule[0], relevant_schedule[1], current_time, relevant_schedule[2], current_date, \
#         relevant_schedule[3]
#
#     return None  # Tidak ada jadwal yang cocok

