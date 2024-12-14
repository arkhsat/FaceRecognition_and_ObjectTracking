# from datetime import datetime, timedelta
import cv2
import os
from firebase_admin import storage, db
import sqlite3
from schedule import is_scheduled
from pathlib import Path


def capture_and_upload(img, getId, event):
    try:
        scheduled_start_time, scheduled_end_time, current_time, time_range, current_date = is_scheduled(getId)
        print(f"Capturing image for ID {getId}, event: {event}")
        current_time = current_time.strftime("%H:%M:%S")
        img_name = f'{getId}_{event}_{current_time}.jpg'

        # Get time range from Db and then add it to file structure
        time_range_ref = db.reference(f'schedule/{current_date}')
        time_range_data = time_range_ref.get()

        if time_range_data:
            # Create the folder if it doesn't exist for each time range
            folder_path = os.path.join('captures', current_date, getId, time_range, event)
            os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

            # Full path to save the image
            local_img_path = os.path.join(folder_path, img_name)
            # local_img_path = os.path.join(img_name)

            # Save the image locally
            cv2.imwrite(local_img_path, img)
            print(local_img_path)

            # Upload the image to sqlite
            # conn = sqlite3.connect('image_from_cap.db')
            db_path = Path(__file__).parent / "image_from_cap.db"
            conn = sqlite3.connect(db_path)
            # conn = sqlite3.connect('testing_image_from_cap.db')
            # cursor
            cursor = conn.cursor()
            # table
            # cursor.execute("""CREATE TABLE image (
            #             id INTEGER PRIMARY KEY AUTOINCREMENT,
            #             person_id TEXT NOT NULL,
            #             event INTEGER NOT NULL,
            #             date TEXT NOT NULL,
            #             time TEXT NOT NULL,
            #             img_path BLOB NOT NULL
            # )
            # """)
            # # commit
            # conn.commit()
            #
            # # close
            # conn.close()
            with open(local_img_path, 'rb') as file:
                img_data = file.read()

            cursor.execute("""
                        INSERT INTO image (person_id, event, date, time, img_path)
                        VALUES (?, ?, ?, ?, ?)
                    """, (getId, event, current_date, current_time, img_data))
            conn.commit()

            print(f"Image saved locally at {local_img_path}")
            return local_img_path

    except Exception as e:
        print(f"Error uploading image: {e}")
        return None  # Return None if there's an error
