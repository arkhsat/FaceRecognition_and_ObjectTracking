from datetime import datetime, timedelta
import cv2
import os
from firebase_admin import storage, db


# def capture_and_upload(img, getId, event):
#     try:
#         current_time = datetime.now()  # for time of the capture
#         current_time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
#         img_name = f'{getId}_{event}_{current_time}.jpg'
#         time = datetime.now().strftime("%Y-%m-%d")  # this one is for file name
#
#         schedule_ref = db.reference('schedule')
#         schedule_data = schedule_ref.get()
#
#         image_url = None
#
#         # Check if the current time falls within any of the time ranges
#         for date, time_ranges in schedule_dataitems():
#             if date == time:
#                 for time_range, event_id in time_ranges.items():
#                     start_time, end_time = time_range.split(' - ')
#                     start_time = datetime.strptime(f'{time} {start_time}', '%Y-%m-%d %H:%M')
#                     end_time = datetime.strptime(f'{time} {end_time}', '%Y-%m-%d %H:%M')
#                     if start_time <= current_time <= end_time:
#                         # Create the folder if it doesn't exist
#                         folder_path = os.path.join('captures', time, getId, event)
#                         os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
#
#                         # Full path to save the image
#                         local_img_path = os.path.join(folder_path, img_name)
#
#                         # Save the image locally
#                         try:
#                             cv2.imwrite(local_img_path, img)
#                             print(f"Gambar berhasil disimpan di {local_img_path}")
#                         except Exception as e:
#                             print(f"Gagal menyimpan gambar: {e}")
#
#                         # Upload the image to Firebase Storage
#                         try:
#                             bucket = storage.bucket()
#                             blob = bucket.blob(f'Capture/{time}/{getId}/{event}/{img_name}')
#                             blob.upload_from_filename(local_img_path)
#                             # image_url = blob.generate_signed_url(expiration=3600)
#                             image_url = blob.generate_signed_url(expiration=datetime.utcnow() + timedelta(seconds=3600))
#                             print(f"Image URL generated: {image_url}")
#                         except Exception as e:
#                             print(f"Gagal mengunggah gambar: {e}")
#
#                         # Save the event details to the Firebase database
#                         db.reference(f'PersonEvents/{time}/{getId}/{event}').push({
#                             'name': db.reference(f'Person/{getId}/name').get(),
#                             'event': event,
#                             'time': current_time,
#                             'image_url': image_url
#                         })
#
#                         return image_url  # Return the URL for display
#
#     except Exception as e:
#         print(f"Error uploading image: {e}")
#         return None  # Return None if there's an error

def capture_and_upload(img, getId, event):
    try:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # for time of the capture
        img_name = f'{getId}_{event}_{current_time}.jpg'
        time = datetime.now().strftime("%Y-%m-%d")  # this one is for file name


        # Create the folder if it doesn't exist
        folder_path = os.path.join('captures', time, getId, event)  # Saves in a folder based on person ID
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

        # Full path to save the image
        local_img_path = os.path.join(folder_path, img_name)

        # Save the image locally
        cv2.imwrite(local_img_path, img)

        # Upload the image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'Capture/{time}/{getId}/{event}/{img_name}')  # Store in folder for each person
        blob.upload_from_filename(local_img_path)
        # image_url = blob.generate_signed_url(expiration=3600)
        image_url = blob.generate_signed_url(expiration=datetime.utcnow() + timedelta(seconds=3600))
        print(f"Image URL generated: {image_url}")

        # Save the event details to the Firebase database
        db.reference(f'PersonEvents/{time}/{getId}/{event}').push({
            'name': db.reference(f'Person/{getId}/name').get(),
            'event': event,
            'time': current_time,
            'image_url': image_url
        })

        return image_url  # Return the URL for display

    except Exception as e:
        print(f"Error uploading image: {e}")
        return None  # Return None if there's an error
