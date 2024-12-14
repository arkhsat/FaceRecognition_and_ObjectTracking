import telebot
import threading

# FIREBASE
# from firebase_admin import credentials
from firebase_admin import db
# import firebase_admin
# import os

BOT_TOKEN = your-bot-token-here
bot = telebot.TeleBot(BOT_TOKEN)
# CHAT_ID = "6065946644"
MESSAGE = "This is Attendance Monitoring System of Binus University"


# FOR GIVEN WARNINGS
def send_warning(person_id, alert_message):
    CHAT_ID = "5091903369"  # Replace with the actual chat ID
    print(f"Sending warning: {alert_message}")
    bot.send_message(CHAT_ID, f"Person {person_id}: {alert_message}")


# FOR DISPLAY CHAT
def get_event_entered(current_date, getId, time_range, event):
    # Path reference Firebase
    ref = db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}')
    data = ref.get()

    CHAT_ID = "5091903369"

    if data:
        # key for the last
        latest_key = max(data.keys())
        value = data[latest_key]

        # get the detail of data
        name = value.get('name')
        event_name = value.get('event')
        time = value.get('time')
        late_time = value.get('late_time')
        image_url = value.get('image_url')

        # Tampilkan informasi
        # print(f"Key: {latest_key}")
        # print(f"Name: {name}")
        # print(f"Event: {event_name}")
        # print(f"Time: {time}")
        # print(f"Late Time: {late_time}")
        # print(f"Image URL: {image_url}")

        # Send massage
        message = f"{name} entered the room at {time}\n"
        bot.send_message(CHAT_ID, message)

        # For send picture/img
        caption = (
            f"\t Information \n"
            f"Name: {name}\n"
            f"Event: {event_name}\n"
            f"Time Entered: {time}\n"
            f"Late Time: {late_time}"
        )

        bot.send_photo(
            CHAT_ID,
            photo=image_url,
            caption=caption
        )

    else:
        print(f"No data found for event '{event}' on {current_date} (Time range: {time_range}).")


def get_event_left(current_date, getId, time_range, event):
    # Path reference Firebase
    ref = db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}')
    data = ref.get()

    CHAT_ID = "5091903369"

    if data:
        # key for the last
        latest_key = max(data.keys())
        value = data[latest_key]

        # get the detail of data
        name = value.get('name')
        event_name = value.get('event')
        time = value.get('time')
        image_url = value.get('image_url')

        # Send massage
        message = f"{name} left the room at {time}\n"
        bot.send_message(CHAT_ID, message)

        # For send picture/img
        caption = (
            f"\t Information \n"
            f"Name: {name}\n"
            f"Event: {event_name}\n"
            f"Time Left: {time}\n"
        )

        bot.send_photo(
            CHAT_ID,
            photo=image_url,
            caption=caption
        )

    else:
        print(f"No data found for event '{event}' on {current_date} (Time range: {time_range}).")


def get_event_return(current_date, getId, time_range, event):
    # Path reference Firebase
    ref = db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}')
    data = ref.get()

    CHAT_ID = "5091903369"

    if data:
        # key for the last
        latest_key = max(data.keys())
        value = data[latest_key]

        # get the detail of data
        name = value.get('name')
        event_name = value.get('event')
        time = value.get('time')
        left = value.get('left_time')
        image_url = value.get('image_url')

        # Send massage
        message = f"{name} return to the room at {time}\n"
        bot.send_message(CHAT_ID, message)

        # For send picture/img
        caption = (
            f"\t Information \n"
            f"Name: {name}\n"
            f"Event: {event_name}\n"
            f"Time return: {time}\n"
            f"Left: {left}"
        )

        bot.send_photo(
            CHAT_ID,
            photo=image_url,
            caption=caption
        )

    else:
        print(f"No data found for event '{event}' on {current_date} (Time range: {time_range}).")


def get_event_end(current_date, getId, time_range, event):
    # Path reference Firebase
    ref = db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}')
    data = ref.get()

    CHAT_ID = "5091903369"

    if data:
        # key for the last
        latest_key = max(data.keys())
        value = data[latest_key]

        # get the detail of data
        name = value.get('name')
        event_name = value.get('event')
        time = value.get('time')
        duration: value.get('total_duration')
        total_Time_Late: value.get('Total_Time_Late')
        total_Time_Left: value.get('Total_Time_Left')
        total_Time_Lecture: value.get('time')
        image_url = value.get('image_url')

        # For send picture/img
        caption = (
            f"\t Information \n"
            f"Name: {name}\n"
            f"Event: {event_name}\n"
            f"Time END: {time}\n"
            # f"Duration: {Duration}\n"
            # f"Total time late: {Total_Time_Late}\n"
            # f"Total time left: {Total_Time_Left}\n"
            # f"Total time in room: {Total_Time_Lecture}"
        )

        bot.send_photo(
            CHAT_ID,
            photo=image_url,
            caption=caption
        )

    else:
        print(f"No data found for event '{event}' on {current_date} (Time range: {time_range}).")



@bot.message_handler(commands=['testing'])
def send_welcome(message):
    print(message.chat.id)  # Prints the chat ID when you send /start
    bot.reply_to(message, "Chat ID received!")


@bot.message_handler(commands=['hi'])
def send_welcome(message):
    bot.reply_to(message, "supp")


def start_polling():
    bot.polling()


# Fungsi untuk menjalankan polling Telegram bot di thread terpisah
def start_bot_in_thread():
    bot_thread = threading.Thread(target=start_polling)
    bot_thread.daemon = True  # Pastikan bot thread berhenti saat program utama berhenti
    bot_thread.start()

# bot.polling()


# def log_attendance_to_telegram(face_id, recognized_data, event_type, timestamp):
#     name = recognized_data.get('name', 'Unknown')
#     attendance_status = recognized_data.get('attendance', 'Unknown')
#     occupation = recognized_data.get('occupation', 'Unknown')
#     last_time = recognized_data.get('last_attendance_time', 'N/A')
#     active_status = recognized_data.get('active', 'Inactive')
#
#     # Format the message
#     message = (
#         f"*Attendance Update:*\n"
#         f"ID: `{face_id}`\n"
#         f"Name: *{name}*\n"
#         f"Event: {event_type.title()}\n"
#         f"Occupation: {occupation}\n"
#         f"Attendance Status: {attendance_status}\n"
#         f"Last Attendance Time: {last_time}\n"
#         f"Active Status: {active_status}\n"
#         f"Timestamp: {timestamp}"
#     )
#
#     # Send the message to Telegram
#     send_message(CHAT_ID, message)
