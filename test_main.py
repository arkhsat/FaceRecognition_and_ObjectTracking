import pickle
import cv2
import cvzone
import face_recognition
import numpy as np
from datetime import datetime
from timess import (count_duration, start_late_timer, count_late_time, start_left_timer, count_left_time,
                    count_left_time_total, total_time, stop_late_timer, delete_left_timer)
                    # (update_to_db_for_left, update_to_db_for_late, update_to_db_for_return, update_to_db_for_end)

# FOR FIREBASE
from schedule import is_scheduled  # for import schedule from firebase
from capture_test import capture_and_upload  # this for capture and upload to firebase
from personeventdb import (update_to_db_for_left, update_to_db_for_return, update_to_db_for_late, update_to_db_for_end)


# FOR SQLITE
# from capture_test_sql import capture_and_upload  # this for capture and upload to sqlite
# from fortestdb.capture_test_sql import capture_and_upload  # from capture db sqlite
# from fortestdb.personevent import (update_to_db_for_left, update_to_db_for_return, update_to_db_for_late,
#                                    update_to_db_for_end)  # for save personEvent in sqlite

# FOR PDF
# from pdflangsung import pdd  # for PDF, the file is in the root
from pdf.pdfgene import pdd  # pdf_entry, pdf_left, pdf_return, pdf_end  # from pdf folder


# FOR CSV
# from csvencode import csv_code  # for CSV, the file is in the root
from CSV.csvencode import csv_code  # the file is in the folder


# FOR TELEBOT
from telegrambot.telegrambot import get_event_entered, get_event_left, get_event_return, get_event_end


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
file = open('EncodeFileNew.p', 'rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnow, id = encodeListKnowWithIds
print("Encode File Loaded")


def stop_tracking(person_id):
    # Remove the tracker for the person
    for i, (tracker, tracked_id) in enumerate(zip(trackers, tracked_ids)):
        if tracked_id == person_id:
            trackers.pop(i)
            tracked_ids.pop(i)
            previous_capture_status.pop(person_id, None)
            print(f"Stopped tracking person {person_id}")


while True:
    success, img = cap.read()
    time_box = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
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
                scheduled_start_time, scheduled_end_time, current_time, time_range, current_date = is_scheduled(
                    tracked_id)

                if current_time >= scheduled_end_time:
                    print("Just Checking if this code work")
                    # Capture and update to 'end'
                    if previous_capture_status.get(tracked_id) in ['entered', 'left', 'return']:
                        print("Just Checking if this code work")
                        current_times_str = current_time.strftime("%H:%M:%S")
                        image_url = capture_and_upload(img, tracked_id, 'end')
                        previous_capture_status[tracked_id] = 'end'
                        stop_tracking(tracked_id)

                        # Display the capture image or take further actions
                        dur = count_duration(tracked_id, scheduled_start_time, scheduled_end_time)
                        lates = count_late_time(tracked_id, scheduled_start_time)
                        lefts = count_left_time_total(tracked_id)
                        total = total_time(tracked_id)
                        left_times = count_left_time(tracked_id)
                        update_to_db_for_end(tracked_id, current_date, time_range, 'end', lates, dur, lefts, total,
                                             current_times_str, image_url)  # FOR FIREBASE
                        # update_to_db_for_end(tracked_id, current_date, time_range, 'end', lates, dur, lefts, total,
                        #                      current_times_str)  # THIS ONE FOR SQLITE
                        get_event_end(current_date, getId, time_range, 'end')
                        csv_code(tracked_id, time_range, current_times_str, lates, lefts, total)
                        pdd(getId, current_date, current_time, time_range, 'end')

                if x + w < RIGHT_ZONE:
                    # scheduled_start_time, scheduled_end_time, current_time, time_range, current_date = is_scheduled(
                    #     tracked_id)
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
                        # print(f"current_time11: {current_time} (type: {type(current_time)})")
                        current_time = current_time.strftime("%H:%M:%S")
                        image_url = (capture_and_upload(img, tracked_id, 'return'))
                        previous_capture_status[tracked_id] = 'return'
                        left = count_left_time(tracked_id)
                        count_left_time_total(tracked_id)
                        delete_left_timer(tracked_id)
                        is_tracking = True

                        update_to_db_for_return(tracked_id, current_date, time_range, 'return', left, current_time, image_url)  # FOR FIREBASE
                        get_event_return(current_date, getId, time_range, 'return')
                        # update_to_db_for_return(tracked_id, current_date, time_range, 'return', left, current_time, image_url)  # FOR SQLITE
                        pdd(getId, current_date, current_time, time_range, 'return')
                        # pdd(tracked_id, 'return', time_range, current_date, current_time)
                        # display_image_from_url(image_url) # for display the image

                    elif previous_capture_status.get(tracked_id) not in ['entered', 'return', 'left', 'end']:
                        image_url = (capture_and_upload(img, tracked_id, 'entered'))
                        current_time = current_time.strftime("%H:%M:%S")

                        # current_time = datetime.strftime(current_time, "%H:%M:%S")
                        previous_capture_status[tracked_id] = 'entered'
                        # display_image_from_url(image_url)

                        stop_late_timer(tracked_id)
                        lates = count_late_time(tracked_id, scheduled_start_time)

                        update_to_db_for_late(tracked_id, current_date, time_range, 'entered', lates, current_time, image_url)  # FOR FIREBASE
                        # update_to_db_for_late(tracked_id, current_date, time_range, 'entered', lates, current_time)  # FOR SQLITE
                        get_event_entered(current_date, getId, time_range, 'entered')
                        # pfd(tracked_id, 'entered', current_time, lates)
                        pdd(tracked_id, current_date, current_time, time_range, 'entered')

                elif x + w > RIGHT_ZONE:
                    if is_tracking:
                        if previous_capture_status.get(tracked_id) != 'left' and previous_capture_status.get(
                                tracked_id) in ['return', 'entered']:

                            # calculate_total_time_outside(tracked_id)
                            image_url = capture_and_upload(img, tracked_id, 'left')
                            previous_capture_status[tracked_id] = 'left'
                            current_time = current_time.strftime("%H:%M:%S")

                            update_to_db_for_left(tracked_id, current_date, time_range, 'left', current_time, image_url)  # FOR FIREBASE
                            # update_to_db_for_left(tracked_id, current_date, time_range, 'left', current_time)  # FOR SQLITE
                            get_event_left(current_date, getId, time_range, 'left')
                            pdd(tracked_id, current_date, current_time, time_range, 'left')
                            is_tracking = False

                # elif x + w < RIGHT_ZONE or x + w > RIGHT_ZONE:
                #     print("test if this work i guess")
                #     current_times = datetime.now()
                #
                #     if (current_times >= scheduled_end_time and
                #             previous_capture_status.get(tracked_id) in ['entered', 'left', 'return']):
                #         # Capture and update to 'end'
                #         print("Just Checking if this code work")
                #         current_times_str = current_times.strftime("%H:%M:%S")
                #         image_url = capture_and_upload(img, tracked_id, 'end')
                #         previous_capture_status[tracked_id] = 'end'
                #         stop_tracking(tracked_id)
                #
                #         # Display the capture image or take further actions
                #         dur = count_duration(tracked_id, scheduled_start_time, scheduled_end_time)
                #         lates = count_late_time(tracked_id, scheduled_start_time)
                #         lefts = count_left_time_total(tracked_id)
                #         total = total_time(tracked_id)
                #         left_times = count_left_time(tracked_id)
                #         update_to_db_for_end(tracked_id, current_date, time_range, 'end', lates, dur, lefts, total,
                #                              current_times_str, image_url)  # FOR FIREBASE
                #         # update_to_db_for_end(tracked_id, current_date, time_range, 'end', lates, dur, lefts, total,
                #         #                      current_times_str)  # THIS ONE FOR SQLITE
                #         # pdd(tracked_id, current_date, current_time)
                #         csv_code(tracked_id, time_range, current_times_str, lates, lefts, total)

            else:
                # Remove the tracker if it fails
                trackers.pop(i)
                tracked_ids.pop(i)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    if len(faceCurFrame) == 0 or len(faceCurFrame) != 0:
        # If no faces are detected for 10 minutes, trigger late timer
        for person_id in encodeListKnowWithIds[-1]:
            schedule_times = is_scheduled(person_id)
            if schedule_times:
                scheduled_start_time, scheduled_end_time, current_time, time_range, current_date = schedule_times
                if previous_capture_status.get(person_id) not in ['entered', 'left', 'return', 'end']:
                    start_late_timer(person_id)

                elif previous_capture_status.get(person_id) == 'left':
                    start_left_timer(person_id)

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
                    cvzone.cornerRect(img, (x1, y1, x2 - x1, y2 - y1), rt=1,
                                      colorC=(0, 255, 0))  # Green recognition

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

    # start_telegram_bot()

# cap.release()
# cv2.destroyAllWindows()
