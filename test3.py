import pickle
import cv2
import cvzone
import face_recognition
import numpy as np
import time  # For time tracking

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load encoding file
print("Loading Encoding File....")
file = open('EncodeFileNew.p', 'rb')
encodeListKnowWithIds = pickle.load(file)
file.close()
encodeListKnow, id = encodeListKnowWithIds
print("Encode File Loaded")

# Variables for trackers, IDs, and timing
trackers = []
tracked_ids = []
person_status = {}  # Track whether a person is in or out
person_entry_time = {}  # Store entry time for each person
total_time_in_room = {}  # Store the total time in room for each person
person_exit_time = {}  # Store exit time for each person
total_time_outside = {}  # Store the total time outside the room for each person

# Zones definition (for 640x480 resolution)
LEFT_ZONE = 100
RIGHT_ZONE = 500

while True:
    success, img = cap.read()

    cv2.line(img, (LEFT_ZONE, 0), (LEFT_ZONE, img.shape[0]), (0, 0, 255), 2)
    cv2.line(img, (RIGHT_ZONE, 0), (RIGHT_ZONE, img.shape[0]), (0, 0, 255), 2)

    current_time = time.time()

    if trackers:
        # Update all trackers and check their position
        for i, (tracker, tracked_id) in enumerate(zip(trackers, tracked_ids)):
            success, track_box = tracker.update(img)
            if success:
                x, y, w, h = [int(v) for v in track_box]
                cvzone.cornerRect(img, (x, y, w, h), rt=1, colorC=(255, 0, 0))  # blue for tracked faces

                # Calculate the current time in the room for this person
                if person_status.get(tracked_id) == 'in the room':
                    current_time_in_room = total_time_in_room.get(tracked_id, 0) + (current_time - person_entry_time.get(tracked_id, current_time))
                    current_time_outside = total_time_outside.get(tracked_id, 0)  # If inside, no outside time increment
                else:
                    current_time_in_room = total_time_in_room.get(tracked_id, 0)
                    current_time_outside = total_time_outside.get(tracked_id, 0) + (current_time - person_exit_time.get(tracked_id, current_time))

                # Convert time to seconds
                time_in_text = f'Time in: {int(current_time_in_room)}s'
                time_out_text = f'Time out: {int(current_time_outside)}s'

                # Display the ID and time in the image
                cvzone.putTextRect(img, f'ID: {tracked_id}', (x, y - 25), scale=1, thickness=2, colorR=(255, 0, 0))
                cvzone.putTextRect(img, time_in_text, (x, y - 50), scale=1, thickness=1, colorR=(0, 255, 0))
                cvzone.putTextRect(img, time_out_text, (x, y - 75), scale=1, thickness=1, colorR=(0, 0, 255))

                # Check if the person is in or out of the room
                if x > RIGHT_ZONE:
                    if person_status.get(tracked_id) == 'in the room':
                        # Person has left the room from the right side
                        time_in_room = current_time - person_entry_time.get(tracked_id, current_time)
                        total_time_in_room[tracked_id] += time_in_room

                        # Start counting time outside
                        person_exit_time[tracked_id] = current_time
                        total_time_outside[tracked_id] = total_time_outside.get(tracked_id, 0)

                        print(f'Person {tracked_id} left the room. Total time spent: {total_time_in_room[tracked_id]:.2f} seconds inside.')

                        # Update status
                        person_status[tracked_id] = 'left the room'
                else:
                    if person_status.get(tracked_id) == 'left the room':
                        # Person re-entered the room
                        time_outside_room = current_time - person_exit_time.get(tracked_id, current_time)
                        total_time_outside[tracked_id] += time_outside_room

                        # Start counting time inside again
                        person_entry_time[tracked_id] = current_time

                        print(f'Person {tracked_id} re-entered the room. Total time spent: {total_time_outside[tracked_id]:.2f} seconds outside.')

                        person_status[tracked_id] = 'in the room'
            else:
                # If tracking fails, remove the tracker
                trackers.pop(i)
                tracked_ids.pop(i)

    # Face recognition for new people
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)

        matchIndex = np.argmin(faceDis)

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale up face location

        if matches[matchIndex]:
            person_id = id[matchIndex]
            if person_id not in tracked_ids:
                # New person detected, start tracking
                cvzone.cornerRect(img, (x1, y1, x2 - x1, y2 - y1), rt=1, colorC=(0, 255, 0))  # green for recognized face
                cvzone.putTextRect(img, f'ID: {person_id}', (x1, y1 - 10), scale=1, thickness=2, colorR=(255, 0, 0))

                # Initialize tracker for this person
                tracker = cv2.TrackerCSRT.create()
                track_box = (x1, y1, x2 - x1, y2 - y1)
                tracker.init(img, track_box)

                # Add to trackers list
                trackers.append(tracker)
                tracked_ids.append(person_id)

                # Start time tracking
                person_entry_time[person_id] = current_time
                total_time_in_room[person_id] = 0  # Initialize total time
                total_time_outside[person_id] = 0  # Initialize total time outside
                person_status[person_id] = 'in the room'

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)
