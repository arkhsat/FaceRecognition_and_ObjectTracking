from datetime import datetime, timedelta
import cv2
import os
from firebase_admin import storage, db
from schedule import is_scheduled


def capture_and_upload(img, getId, event):
    try:
        scheduled_start_time, scheduled_end_time, current_time, time_range, current_date = is_scheduled(getId)
        print(f"Capturing image for ID {getId}, event: {event}")
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

            # Save the image locally
            cv2.imwrite(local_img_path, img)

            # Upload the image to Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob(f'Capture/{current_date}/{getId}/{time_range}/{event}/{img_name}')

            blob.upload_from_filename(local_img_path)
            image_url = blob.generate_signed_url(expiration=datetime.utcnow() + timedelta(seconds=3600))
            print(f"Image URL generated: {image_url}")
            return image_url

        else:
            time_range = "NoSchedule"
            folder_path = os.path.join('captures', current_date, getId, time_range, event)
            os.makedirs(folder_path, exist_ok=True)
            local_img_path = os.path.join(folder_path, img_name)
            cv2.imwrite(local_img_path, img)

            # Handle "NoSchedule" case in Firebase
            bucket = storage.bucket()
            blob = bucket.blob(f'Capture/{current_date}/{getId}/{time_range}/{event}/{img_name}')
            blob.upload_from_filename(local_img_path)
            image_url = blob.generate_signed_url(expiration=datetime.utcnow() + timedelta(seconds=3600))
            print(f"Image URL generated: {image_url}")

            return image_url

    except Exception as e:
        print(f"Error uploading image: {e}")
        return None  # Return None if there's an error
