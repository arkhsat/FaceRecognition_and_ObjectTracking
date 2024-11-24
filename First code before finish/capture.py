from datetime import datetime, timedelta
import cv2
import os
from firebase_admin import storage, db
# from the_time import save_time_to_db, count_duration, count_late_time, total_time, count_left_time
# from main import is_scheduled

# def capture_and_upload(img, getId, event):
#     try:
#         # File structure
#         current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # for time of the capture
#         img_name = f'{getId}_{event}_{current_time}.jpg'
#         time = datetime.now().strftime("%Y-%m-%d")  # this one is for file name
#
#         # Get time range from Db and then add it to file structure
#         current_date = datetime.now().strftime("%Y - %m - %d")
#         time_range_ref = db.reference(f'schedule/{current_date}')
#         time_range_data = time_range_ref.get()
#
#         if time_range_data:
#             for time_key, time_value in time_range_data.items():
#                 start_time, end_time = time_key.split(' - ')
#                 start_hour, start_minute = start_time.split(':')
#                 end_hour, end_minute = end_time.split(':')
#
#                 break
#
#             time_range = f"{start_hour}:{start_minute}-{end_hour}:{end_minute}"
#         else:
#             time_range = "NoSchedule"
#
#         # Create the folder if it doesn't exist
#         folder_path = os.path.join('captures', time, getId, time_range, event)  # Saves in a folder based on person ID
#         os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
#
#         # Full path to save the image
#         local_img_path = os.path.join(folder_path, img_name)
#
#         # Save the image locally
#         cv2.imwrite(local_img_path, img)
#
#         # Upload the image to Firebase Storage
#         bucket = storage.bucket()
#         blob = bucket.blob(f'Capture/{time}/{getId}/{time_range}/{event}/{img_name}')
# Store in folder for each person
#         blob.upload_from_filename(local_img_path)
#         image_url = blob.generate_signed_url(expiration=datetime.utcnow() + timedelta(seconds=3600))
#         print(f"Image URL generated: {image_url}")
#
#         # Save the event details to the Firebase database
#         db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}').push({
#             'name': db.reference(f'Person/{getId}/name').get(),
#             'event': event,
#             'time': current_time,
#             'image_url': image_url
#         })
#
#         return image_url  # Return the URL for display
#
#     except Exception as e:
#         print(f"Error uploading image: {e}")
#         return None  # Return None if there's an error


def capture_and_upload(img, getId, event):
    try:
        # File structure
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # for time of the capture
        img_name = f'{getId}_{event}_{current_time}.jpg'
        time = datetime.now().strftime("%Y-%m-%d")  # this one is for file name

        # Get time range from Db and then add it to file structure
        current_date = datetime.now().strftime("%Y - %m - %d")
        time_range_ref = db.reference(f'schedule/{current_date}')
        time_range_data = time_range_ref.get()

        if time_range_data:
            for time_key, time_value in time_range_data.items():
                start_time, end_time = time_key.split(' - ')
                start_hour, start_minute = start_time.split(':')
                end_hour, end_minute = end_time.split(':')

                time_range = f"{start_hour}:{start_minute}-{end_hour}:{end_minute}"

                # Create the folder if it doesn't exist for each time range
                folder_path = os.path.join('../captures', time, getId, time_range, event)  # Saves in a folder based on person ID
                os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

                # Full path to save the image
                local_img_path = os.path.join(folder_path, img_name)

                # Save the image locally
                cv2.imwrite(local_img_path, img)

                # Upload the image to Firebase Storage
                bucket = storage.bucket()
                blob = bucket.blob(f'Capture/{time}/{getId}/{time_range}/{event}/{img_name}')  # Store in folder for each person
                blob.upload_from_filename(local_img_path)
                image_url = blob.generate_signed_url(expiration=datetime.utcnow() + timedelta(seconds=3600))
                print(f"Image URL generated: {image_url}")

                # Save the event details to the Firebase database
                db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}').push({
                    'name': db.reference(f'Person/{getId}/name').get(),
                    'event': event,
                    'time': current_time,
                    'image_url': image_url
                })

                return image_url


        else:
            time_range = "NoSchedule"
            folder_path = os.path.join('../captures', time, getId, time_range, event)  # Create folder for "NoSchedule"
            os.makedirs(folder_path, exist_ok=True)
            local_img_path = os.path.join(folder_path, img_name)
            cv2.imwrite(local_img_path, img)

            # Handle "NoSchedule" case in Firebase
            bucket = storage.bucket()
            blob = bucket.blob(f'Capture/{time}/{getId}/{time_range}/{event}/{img_name}')
            blob.upload_from_filename(local_img_path)
            image_url = blob.generate_signed_url(expiration=datetime.utcnow() + timedelta(seconds=3600))
            print(f"Image URL generated: {image_url}")

            # Save "NoSchedule" event in Firebase
            db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}').push({
                'name': db.reference(f'Person/{getId}/name').get(),
                'event': event,
                'time': current_time,
                'image_url': image_url
            })

            return image_url  # Return the URL for display

    except Exception as e:
        print(f"Error uploading image: {e}")
        return None  # Return None if there's an error
