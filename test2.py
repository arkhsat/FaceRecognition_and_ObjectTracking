import pickle
import cv2
import cvzone
import face_recognition
import numpy as np
import firebase_admin
import sys
# import atexit
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta
from capture import capture_and_upload
from displaycapture import display_image_from_url

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
    'storageBucket': ""
})

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Variables
getId = -1
capture = 0  # for getting name from db
LEFT_ZONE = 100
RIGHT_ZONE = 800
previous_capture_status = {}
trackers = []
tracked_ids = []
person_exit_time = {}  # Store exit time for each person
total_time_outside = {}  # Store the total time outside the room for each person
previous_exit_time = {}
late_timers = {}
exit_timers = {}

# Load encoding file
print("Loading Encoding File....")
file = open('EncodeFileNew.p', 'rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnow, id = encodeListKnowWithIds
print("Encode File Loaded")


# Function to check if person is scheduled
def is_scheduled(person_id):
    current_date = datetime.now().strftime("%Y - %m - %d")
    current_time = datetime.now()

    # Get the schedule for the current date
    schedule_ref = db.reference(f'schedule/{current_date}')
    schedule_data = schedule_ref.get()

    if schedule_data:
        for time_range, scheduled_id in schedule_data.items():
            start_time, end_time = time_range.split(' - ')
            start_hour, start_minute = start_time.split(':')
            end_hour, end_minute = end_time.split(':')

            scheduled_start_time = datetime.strptime(f"{current_date} "
                                                     f"{start_hour}:{start_minute}", "%Y - %m - %d %H:%M")
            scheduled_end_time = datetime.strptime(f"{current_date} "
                                                   f"{end_hour}:{end_minute}", "%Y - %m - %d %H:%M")

            # Handle the case where the end time is on the next day
            if scheduled_end_time < scheduled_start_time:
                scheduled_end_time += timedelta(days=1)

            if str(scheduled_id) == str(person_id):
                if scheduled_start_time <= current_time <= scheduled_end_time:
                    return scheduled_start_time, scheduled_end_time  # The person is scheduled for the current time
                elif current_time >= scheduled_end_time and previous_capture_status.get(tracked_id) != 'end':
                    stop_tracking(person_id)
                    # matches[person_id] # face recognition stop??
                    image_url = capture_and_upload(img, tracked_id, 'end')
                    previous_capture_status[tracked_id] = 'end'
                    display_image_from_url(image_url)

                    sys.exit()

                    return None
    return None


def stop_tracking(person_id):
    # Remove the tracker for the person
    for i, (tracker, tracked_id) in enumerate(zip(trackers, tracked_ids)):
        if tracked_id == person_id:
            trackers.pop(i)
            tracked_ids.pop(i)
            print(f"Stopped tracking person {person_id}")


def left_time():
    # Calculate time outside the room
    if tracked_id in person_exit_time:
        exit_time = person_exit_time[tracked_id]
        time_outside = datetime.now() - exit_time
        total_time_outside[tracked_id] = (total_time_outside.get(tracked_id, 0)
                                          + time_outside.total_seconds())
        # print(total_time_outside)
        print(f"Person {tracked_id} has been outside the room for "
              f"{time_outside.total_seconds()} seconds")

        # Update previous time
        if tracked_id in previous_exit_time:
            previous_exit_time[tracked_id] = exit_time
        else:
            previous_exit_time[tracked_id] = exit_time

        # Calculate total time outside
        if tracked_id in previous_exit_time:
            total_time_outside[tracked_id] += (exit_time - previous_exit_time[tracked_id]).total_seconds()
            print(f"Total time outside the room for person {tracked_id}: "f"{total_time_outside[tracked_id]} seconds")


def total_time(tracked_id):
    # Calculate total time of lecture
    schedule_start_time, schedule_end_time = is_scheduled(tracked_id)
    if schedule_start_time and schedule_end_time:
        # Schedule duration TEST TO MAKE AN TIMER IN DURATION
        scheduled_duration = (schedule_end_time - schedule_start_time).total_seconds()
        if scheduled_duration < 60:
            print(f"Duration Of Class: {scheduled_duration} seconds")
        elif scheduled_duration < 3600:
            scheduled_duration /= 60
            print(f"Duration Of Class: {scheduled_duration} minutes")
            scheduled_duration = scheduled_duration * 60
        elif scheduled_duration >= 3600:
            scheduled_duration /= 3600
            print(f"Duration Of Class: {scheduled_duration} hours")
            scheduled_duration = scheduled_duration * 3600
        else:
            print("-")

        # Calculate actual entry time
        entry_time = datetime.now()
        print(f"Actual entry time: {entry_time}")

        # Calculate late time
        late_time = (entry_time - schedule_start_time).total_seconds()
        if late_time < 60:
            print(f"Late time: {late_time} seconds")
        elif late_time < 3600:
            late_time /= 60
            print(f"Late time: {late_time} minutes")
            late_time = late_time * 60
        elif late_time >= 3600:
            late_time /= 3600
            print(f"Late time: {late_time} hours")
            late_time = late_time * 3600
        else:
            print("-")

        print(late_time)

        # Testing for duration and late time
        test1 = (scheduled_duration - late_time)
        if test1 <= 60:
            print(f"Test1 {tracked_id}: {test1} seconds")
        elif test1 < 3600:
            test1 /= 60
            print(f"Test1 {tracked_id}: {test1} minutes")
        elif test1 >= 3600:
            test1 /= 3600
            print(f"Test1 {tracked_id}: {test1} hours")
        else:
            print("-")

        # Calculate total time of lecture
        total_time_lecture = scheduled_duration - late_time - total_time_outside[
            tracked_id]
        if total_time_lecture < 3600:
            total_time_lecture /= 60
            print(f"Total time lecture for person {tracked_id}: {total_time_lecture} minutes")
            # total_time_lecture = total_time_lecture * 60
        elif total_time_lecture >= 3600:
            total_time_lecture /= 3600
            print(f"Total time lecture for person {tracked_id}: {total_time_lecture} hours")
            # total_time_lecture = total_time_lecture * 3600
        else:
            print(f"Total time lecture for person {tracked_id}: {total_time_lecture} seconds")

    else:
        print(f"Error parsing schedule time range for person {tracked_id}")

def start_late_timer(person_id, scheduled_start_time):
    current_time = datetime.now()
    # If the person is late, start a timer
    if current_time > scheduled_start_time and person_id not in tracked_ids:
        if person_id not in late_timers:
            late_timers[person_id] = current_time  # Start the late timer
        else:
            elapsed_time = (current_time - late_timers[person_id]).total_seconds()
            # Check if 10 minutes have passed
            if elapsed_time >= 600:  # 600 seconds = 10 minutes
                print(f"WARNING: Person {person_id} has not entered for more than 10 minutes!")
    else:
        if person_id in late_timers:
            del late_timers[person_id]  # Reset timer if person has entered


def start_left_timer(person_id):
    current_time = datetime.now()
    if person_id not in exit_timers:
        exit_timers[person_id] = current_time
    else:
        elapsed_time = (current_time - exit_timers[person_id]).total_seconds()
        if elapsed_time > 600:
            print(f"Person {person_id} has been left the room for more than 10 minutes!")


# Function to reset exit timer (when someone re-enters the room)
def reset_exit_timer(person_id):
    if person_id in exit_timers:
        del exit_timers[person_id]

# Main loop
while True:
    success, img = cap.read()

    # Line for ROI?
    # cv2.line(img, (LEFT_ZONE, 0), (LEFT_ZONE, img.shape[0]), (0, 0, 255), 2)
    cv2.line(img, (RIGHT_ZONE, 0), (RIGHT_ZONE, img.shape[0]), (255, 0, 255), 2)  # right zone is exit

    # If trackers exist, update them
    if trackers:
        for i, (tracker, tracked_id) in enumerate(zip(trackers, tracked_ids)):
            success, bbox = tracker.update(img)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cvzone.cornerRect(img, (x, y, w, h), rt=1, colorC=(255, 0, 0))  # blue for tracked faces
                cvzone.putTextRect(img, f'ID: {tracked_id}', (x, y - 25), scale=1, thickness=2, colorR=(255, 0, 0))
                cvzone.putTextRect(img, f'Tracking', (x, y - 50), scale=1, thickness=2, colorR=(255, 0, 0))
                # cvzone.putTextRect(img, person_exit_time, (x, y - 75), scale=1, thickness=1, colorR=(0, 0, 255))

                # Update capture if leaving or entering
                if x + w > RIGHT_ZONE and previous_capture_status.get(tracked_id) != 'left':
                    image_url = capture_and_upload(img, tracked_id, 'left')
                    previous_capture_status[tracked_id] = 'left'
                    display_image_from_url(image_url)

                elif x + w < RIGHT_ZONE and previous_capture_status.get(tracked_id) != 'entered':
                    image_url = capture_and_upload(img, tracked_id, 'entered')
                    previous_capture_status[tracked_id] = 'entered'
                    display_image_from_url(image_url)

                left_time()
                total_time(tracked_id)

            else:
                # Remove the tracker if it fails
                trackers.pop(i)
                tracked_ids.pop(i)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
        matchIndex = np.argmin(faceDis)

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale up the face location

        if matches[matchIndex]:
            getId = id[matchIndex]
            # Check if the person is scheduled
            if is_scheduled(str(getId)):  # Only allow detection if the person is scheduled
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

    # Run the late timer for each scheduled person
    for person_id in encodeListKnowWithIds[1]:
        schedule_times = is_scheduled(person_id)
        if schedule_times:
            scheduled_start_time, scheduled_end_time = schedule_times
            start_late_timer(person_id, scheduled_start_time)

    # Run the exit timer for each tracked person (if they are still outside)
    for person_id in tracked_ids:
        start_left_timer(person_id)

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)
