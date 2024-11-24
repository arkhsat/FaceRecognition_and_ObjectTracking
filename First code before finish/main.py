import pickle
import cv2
import cvzone
import face_recognition
import numpy as np
import firebase_admin
# import sys
# import atexit
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta
from capture import capture_and_upload
from displaycapture import display_image_from_url
from the_time import (count_duration, start_late_timer, count_late_time, start_left_timer,
                      reset_exit_timer, count_left_time, total_time)


# Firebase setup
cred = credentials.Certificate("serviceAccountKey1.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://testing1-5b399-default-rtdb.firebaseio.com/",
    'storageBucket': "testing1-5b399.appspot.com"
})

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Variables
# Get the ID
getId = -1
# for getting name from db
capture = 0
# for detection zone
LEFT_ZONE = 100
RIGHT_ZONE = 800
# Capture img status
previous_capture_status = {}
# Trackers
trackers = []
tracked_ids = []
# Status tracking
is_tracking = False


# Load encoding file
print("Loading Encoding File....")
file = open('../EncodeFileNew.p', 'rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnow, id = encodeListKnowWithIds
print("Encode File Loaded")


# Function to check if person is scheduled
def is_scheduled(person_id):
    current_date = datetime.now().strftime("%Y - %m - %d")
    current_time = datetime.now()
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

            # print(f'time start: {scheduled_start_time}, time end: {scheduled_end_time}')

            # Handle the case where the end time is on the next day
            if scheduled_end_time < scheduled_start_time:
                scheduled_end_time += timedelta(days=1)

            if str(scheduled_id) == str(person_id):
                # for checking status base on person_id and time_range
                if scheduled_start_time <= current_time <= scheduled_end_time:
                    return scheduled_start_time, scheduled_end_time  # The person is scheduled for the current time

                # elif (current_time >= scheduled_end_time and previous_capture_status.get(person_id) in
                #       ['entered', 'left', 'return']):
                #     # print(f'currentEND = {current_time}')
                #     image_url = capture_and_upload(img, person_id, 'end')
                #     previous_capture_status[person_id] = 'end'
                #
                #     # Process after session ends
                #     # for stop tracking
                #     stop_tracking(person_id)
                #     display_image_from_url(image_url)
                #
                #     # for calculate time
                #     count_duration(scheduled_start_time, scheduled_end_time)
                #     count_late_time(person_id, scheduled_start_time)
                #     count_left_time(person_id)
                #     total_time(person_id, scheduled_start_time, scheduled_end_time)
                #
                #     previous_capture_status[person_id] = 'reset'
                #     return None

                # break

    return None


def stop_tracking(person_id):
    # Remove the tracker for the person
    for i, (tracker, tracked_id) in enumerate(zip(trackers, tracked_ids)):
        if tracked_id == person_id:
            trackers.pop(i)
            tracked_ids.pop(i)
            previous_capture_status.pop(person_id, None)
            print(f"Stopped tracking person {person_id}")


# Main loop
while True:
    success, img = cap.read()
    # Line for ROI?
    # cv2.line(img, (LEFT_ZONE, 0), (LEFT_ZONE, img.shape[0]), (0, 0, 255), 2)
    time_box = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
    # cv2.putText(img, f'{time_box}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cvzone.putTextRect(
        img, f'{time_box}', (10, 30),
        scale=1, thickness=2, colorR=(0, 0, 0),
        font=cv2.FONT_HERSHEY_SIMPLEX,
        offset=10,
    )
    cv2.line(img, (RIGHT_ZONE, 0), (RIGHT_ZONE, img.shape[0]), (255, 0, 255), 2)  # right zone is exit

    # If trackers exist, update them
    if trackers:
        for i, (tracker, tracked_id) in enumerate(zip(trackers, tracked_ids)):
            success, bbox = tracker.update(img)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                if x + w < RIGHT_ZONE:
                    if not is_tracking:
                        is_tracking = True  # Start tracking
                        print(f"Tracking started for ID: {tracked_id}")

                    cvzone.cornerRect(img, (x, y, w, h), rt=1, colorC=(255, 0, 0))  # blue for tracked faces
                    cvzone.putTextRect(img, f'ID: {tracked_id}', (x, y - 25), scale=1, thickness=2, colorR=(255, 0, 0))
                    cvzone.putTextRect(img, f'Tracking', (x, y - 50), scale=1, thickness=2, colorR=(255, 0, 0))

                    # Update capture if leaving or entering
                    # while True:
                    if (previous_capture_status.get(tracked_id) == 'left' and
                            previous_capture_status.get(tracked_id) != "return"):
                        image_url = capture_and_upload(img, tracked_id, 'return')
                        previous_capture_status[tracked_id] = 'return'
                        display_image_from_url(image_url)
                        scheduled_start_time, scheduled_end_time = is_scheduled(tracked_id)
                        count_left_time(tracked_id)
                        reset_exit_timer(tracked_id)
                        is_tracking = True

                    # elif previous_capture_status.get(tracked_id) != 'entered' and
                    # not previous_capture_status.get(tracked_id) == "return":
                    elif previous_capture_status.get(tracked_id) not in ['entered', 'return', 'left', 'end']:
                        image_url = capture_and_upload(img, tracked_id, 'entered')
                        # previous_capture_status[tracked_id] = 'entered'
                        previous_capture_status[tracked_id] = 'entered'
                        display_image_from_url(image_url)
                        # Start the timer for late
                        scheduled_start_time, scheduled_end_time = is_scheduled(tracked_id)
                        # reset_exit_timer(tracked_id)
                        count_late_time(tracked_id, scheduled_start_time)

                elif x + w > RIGHT_ZONE:
                    if is_tracking:
                        # if previous_capture_status.get(tracked_id) != 'left' and
                        # previous_capture_status.get(tracked_id) == 'return' or 'entered':
                        if previous_capture_status.get(tracked_id) != 'left' and previous_capture_status.get(
                                tracked_id) in ['return', 'entered']:
                            # calculate_total_time_outside(tracked_id)
                            image_url = capture_and_upload(img, tracked_id, 'left')
                            previous_capture_status[tracked_id] = 'left'
                            display_image_from_url(image_url)
                            # Start the timer for left the room
                            start_left_timer(tracked_id)
                            is_tracking = False

                if x + w < RIGHT_ZONE or x + w > RIGHT_ZONE:
                    scheduled_start_time, scheduled_end_time = is_scheduled(tracked_id)
                    current_time = datetime.now()
                    if (current_time >= scheduled_end_time and previous_capture_status.get(tracked_id) in
                          ['entered', 'left', 'return']):
                        # print(f'currentEND = {current_time}')
                        image_url = capture_and_upload(img, tracked_id, 'end')
                        previous_capture_status[tracked_id] = 'end'

                        # Process after session ends
                        # for stop tracking
                        stop_tracking(tracked_id)
                        display_image_from_url(image_url)

                        # for calculate time
                        count_duration(scheduled_start_time, scheduled_end_time)
                        count_late_time(tracked_id, scheduled_start_time)
                        count_left_time(tracked_id)
                        total_time(tracked_id, scheduled_start_time, scheduled_end_time)

                        previous_capture_status[tracked_id] = 'reset'

            else:
                # Remove the tracker if it fails
                trackers.pop(i)
                tracked_ids.pop(i)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    if len(faceCurFrame) == 0:
        # If no faces are detected for 10 minutes, trigger late timer
        for person_id in encodeListKnowWithIds[-1]:
            schedule_times = is_scheduled(person_id)
            if schedule_times:
                scheduled_start_time, scheduled_end_time = schedule_times
                start_late_timer(person_id, scheduled_start_time)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace, tolerance=0.5)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        matchIndex = np.argmin(faceDis)

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale up the face location

        if matches[matchIndex] and (x1 + (x2 - x1) < RIGHT_ZONE):
            getId = id[matchIndex]
            if is_scheduled(str(getId)):  # Only allow detection if the person is scheduled

                # if getId not in tracked_ids:
                # if not is_tracking and (x1 + (x2 - x1) < RIGHT_ZONE):
                if getId not in tracked_ids:
                    # New person detected, start tracking
                    cvzone.cornerRect(img, (x1, y1, x2 - x1, y2 - y1), rt=1, colorC=(0, 255, 0))  # Green recognition

                    # Initialize tracker for this person
                    tracker = cv2.TrackerCSRT.create()  # USING this method for tracking
                    tracker.init(img, (x1, y1, x2 - x1, y2 - y1))

                    # Add to trackers list
                    trackers.append(tracker)
                    tracked_ids.append(getId)

                    # if capture == 0:
                    #     capture = 1

                    # Retrieve person info from the database
                    # if capture == 1:
                    #     info = db.reference(f'Person/{getId}').get()
                    #     names = str(info['name'])
                    #     # title = str(info['title'])
                    #     cvzone.putTextRect(img, f'Name: {names}', (x1, y1 - 10),
                    #                        scale=1, thickness=2, colorR=(255, 0 , 0))
                    #     # cvzone.putTextRect(img, f'Title: {title}', (x1, y1 - 20),
                    #                           scale=1, thickness=2, colorR=(255, 0, 0))

            else:
                print(f"Person {getId} is not scheduled to be in the room at this time.")

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)
