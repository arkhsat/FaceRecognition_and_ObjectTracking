import telebot
import threading
import json

# FIREBASE
from firebase_admin import db

BOT_TOKEN = "7543908439:AAFn3aK-CQLjhMVsIXgrj599i5nS4-OA35M"
bot = telebot.TeleBot(BOT_TOKEN)
# CHAT_ID = "5091903369"
MESSAGE = "This is Attendance Monitoring System of Binus University"


# Get ID from firebase
def get_chat_id(person_id):
    ref = db.reference(f"Person/{person_id}")
    person_data = ref.get()
    if person_data and "CHAT_ID" in person_data:
        return person_data["CHAT_ID"]
    return None


# FOR GIVEN WARNINGS
def send_warning(person_id, alert_message):
    CHAT_ID_PERSON = get_chat_id(person_id)  # Replace with the actual chat ID
    CHAT_ID_ADMIN = "5091903369"
    CHAT_ID = [CHAT_ID_PERSON, CHAT_ID_ADMIN]
    if not CHAT_ID:
        print(f"Error: CHAT_ID not found for person_id {person_id}. Unable to send warning.")
        return

    try:
        for chat_id in CHAT_ID:
            if chat_id:
                print(f"Sending warning to CHAT_ID {chat_id}: {alert_message}")
                bot.send_message(chat_id, f"Person {person_id}: {alert_message}")
    except Exception as e:
        print(f"Failed to send message: {e}")
    # print(f"Sending warning: {alert_message}")
    # bot.send_message(CHAT_ID, f"Person {person_id}: {alert_message}")


# FOR DISPLAY CHAT
def get_event_entered(current_date, getId, time_range, event):
    # Path reference Firebase
    ref = db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}')
    data = ref.get()

    # CHAT_ID = "5091903369"
    CHAT_ID = get_chat_id(getId)

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

    # CHAT_ID = "5091903369"
    CHAT_ID = get_chat_id(getId)

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

    # CHAT_ID = "5091903369"
    CHAT_ID = get_chat_id(getId)

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

    # CHAT_ID = "5091903369"
    CHAT_ID = get_chat_id(getId)

    if data:
        # key for the last
        latest_key = max(data.keys())
        value = data[latest_key]

        # get the detail of data
        name = value.get('name')
        event_name = value.get('event')
        time = value.get('time')
        duration = value.get('Duration')
        total_time_late = value.get('Total_Time_Late')
        total_time_left = value.get('Total_Time_Left')
        total_time_room = value.get('Total_Time_Lecture')
        image_url = value.get('image_url')

        # For send picture/img
        caption = (
            f"\t Information \n"
            f"Name: {name}\n"
            f"Event: {event_name}\n"
            f"Time END: {time}\n"
            f"Duration: {duration}\n"
            f"Total time late: {total_time_late}\n"
            f"Total time left: {total_time_left}\n"
            f"Total time in room: {total_time_room}"
        )

        bot.send_photo(
            CHAT_ID,
            photo=image_url,
            caption=caption
        )

    else:
        print(f"No data found for event '{event}' on {current_date} (Time range: {time_range}).")


def send_pdf(current_date, getId, time_range, event):
    CHAT_ID_PERSON = get_chat_id(getId)  # Replace with the actual chat ID
    CHAT_ID_ADMIN = "5091903369"
    CHAT_ID = [CHAT_ID_PERSON, CHAT_ID_ADMIN]

    ref = db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}/PDF')

    if not CHAT_ID:
        print(f"Error: CHAT_ID not found for person_id {getId}. Unable to send warning.")
        return

    try:
        for chat_id in CHAT_ID:
            if chat_id:
                print(f"Sending warning to CHAT_ID {chat_id}")
                bot.send_document(chat_id, ref)
    except Exception as e:
        print(f"Failed to send message: {e}")


@bot.message_handler(commands=['testing'])
def send_welcome(message):
    print(message.chat.id)  # Prints the chat ID when you send /start
    bot.reply_to(message, "Chat ID received!")


@bot.message_handler(commands=['hi'])
def send_welcome(message):
    bot.reply_to(message, "supp")


# FOR SAVE ID IN FIREBASE
@bot.message_handler(func=lambda message: True)
def log_user(message):
    user_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    last_name = message.chat.last_name

    # Save user data in Firebase
    # ref = db.reference('UsersBOT')
    # ref.set({
    #     'CHAT_ID': user_id,
    #     'username': username,
    #     'first_name': first_name,
    #     'last_name': last_name,
    # })

    db.reference(f'UsersBOT/{user_id}').set({
        'CHAT_ID': user_id,
        'username': username,
        'first_name': first_name,
        'last_name': last_name
    })

    # Cari entri di Person berdasarkan nama (first_name)
    person_ref = db.reference('Person')
    persons = person_ref.get()

    # Menentukan kunci (ID) entri Person
    person_id = None
    for key, value in (persons or {}).items():
        if value.get('name') == first_name:  # Cocokkan dengan first_name
            person_id = key
            break

    if person_id:
        # Tambahkan atau perbarui CHAT_ID untuk entri di Person
        person_ref.child(person_id).update({
            'CHAT_ID': user_id
        })
        bot.reply_to(message, f"Your CHAT_ID has been added to the Person database!")
    else:
        bot.reply_to(message, f"No matching person found with the name {first_name} in the database!")

    # bot.reply_to(message, "You have been logged!")


# def get_id(getId):
#     ref = db.reference(f'Person/{getId}')
#
#     return ref
#
#
# @bot.message_handler(func=lambda message: True)
# def log_user(message):
#     user_id = message.chat.id
#
#     db.reference(f'Person/{getId}').update({
#         'CHAT_ID': user_id,
#     })
#
#     bot.reply_to(message, "You have been logged!")
#
#     # @bot.message_handler(func=lambda msg: True)
#     # def get_person_id(msg):
#     #     getId = msg.text  # Ambil teks yang dimasukkan pengguna sebagai getId
#     #     if not db.reference(f'Person/{getId}').get():
#     #         bot.reply_to(msg, "Person ID not found in the database.")
#     #         return
#     #
#     #     # Simpan chat_id ke database
#     #     db.reference(f'Person/{getId}').update({
#     #         'chat_id': user_id,
#     #     })
#     #     bot.reply_to(msg, f"You have been logged with Person ID: {getId}")


# Store Users in a Local File (Optional)
@bot.message_handler(func=lambda message: True)
def log_user_to_file(message):
    user_data = {
        'user_id': message.chat.id,
        'username': message.chat.username,
        'first_name': message.chat.first_name,
        'last_name': message.chat.last_name
    }

    # Save user data to a file
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

    users[user_data['user_id']] = user_data

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    bot.reply_to(message, "You have been logged to json!")


def start_polling():
    bot.polling()


# Fungsi untuk menjalankan polling Telegram bot di thread terpisah
def start_bot_in_thread():
    bot_thread = threading.Thread(target=start_polling)
    bot_thread.daemon = True  # Pastikan bot thread berhenti saat program utama berhenti
    bot_thread.start()
