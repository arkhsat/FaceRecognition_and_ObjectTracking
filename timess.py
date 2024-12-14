from datetime import datetime  # timedelta
# from firebase_admin import storage, db
# from schedule import is_scheduled
# from firebase_admin import credentials
# import firebase_admin
# from pdf import pdd
from pdflangsung import entry, left, back, end

from telegrambot.telegrambot import send_warning, start_bot_in_thread

# start_bot_in_thread()

# Variable For left warning
exit_timers = {}
left_warnings = {}
last_left_warnings = {}
total_left_times = {}
# paused_timers = {}
# pause_start_time = {}

# Variable for late warning
late_timers = {}
late_warnings = {}
last_late_warning = {}
total_time_late = {}
timer_active = {}
time_takes = {}
late = {}

# count_duration
duration = {}


# for counting the duration of class
def count_duration(person_id, schedule_start_time, schedule_end_time):
    # schedule_start_time, schedule_end_time = is_scheduled(tracked_id)
    print(f" {schedule_start_time} - {schedule_end_time}")
    scheduled_duration = (schedule_end_time - schedule_start_time).total_seconds()
    duration[person_id] = scheduled_duration
    if schedule_start_time and schedule_end_time:
        print(f"Duration Of Class: {format_duration(scheduled_duration)}")
    print(f"Duration in second: {scheduled_duration}")
    return duration


# For timer time late amd giving Warning
def start_late_timer(person_id):
    time_takes[person_id] = datetime.now()
    current_time = datetime.now()
    late_time = 0

    # If the person is late, start a timer
    if person_id not in late_timers or late_timers[person_id] is None:
        late_timers[person_id] = current_time  # Start the late timer
        timer_active[person_id] = True
        # late_timers[person_id] = scheduled_start_time  # Start 8the late timer
    else:
        late_time = (current_time - late_timers[person_id]).total_seconds()
        if late_time >= 60 and person_id not in late_warnings:  # 600 seconds = 10 minutes
            print(f"WARNING: Person {person_id} has not entered for more than 10 minutes!")
            send_warning(person_id, f"Person {person_id} has not entered for 10 minutes!")
            late_warnings[person_id] = True
            last_late_warning[person_id] = current_time
        elif late_time >= 60 and person_id in late_warnings:
            time_since_last_warning = (current_time - last_late_warning[person_id]).total_seconds()

            if time_since_last_warning >= 300:
                print(f"WARNING: Person {person_id} is still not entered for another 10 minutes!")
                send_warning(person_id, f"Person {person_id} has not entered for another 10 minutes!")
                last_late_warning[person_id] = current_time

    print(f"Timer for late time: {late_time}")
    return late_time


def stop_late_timer(person_id):
    late_time = start_late_timer(person_id)
    if person_id in late_timers and late_timers[person_id] is not None:
        # Stop the timer and store the elapsed time
        # current_time = datetime.now()
        # late_time = (current_time - late_timers[person_id]).total_seconds()

        # Store the time before resetting
        total_time_late[person_id] = late_time
        print(total_time_late[person_id])

        # Reset the late timer
        late_timers[person_id] = None
        timer_active[person_id] = False

        print(f"Person {person_id} entered the room after {total_time_late} seconds.")
    else:
        print(f"Person {person_id} was not late.")

    return total_time_late


# for counting the total time late
def count_late_time(person_id, schedule_end_time):
    # Get the end time from DB
    schedule_end_times = schedule_end_time

    # Get the late_time from total_time_late dict
    late[person_id] = total_time_late.get(person_id)

    # Calculate actual entry time base on timer
    print(f"Late Time for1 {person_id}: {format_duration(late[person_id])}")

    # For Checking if the count of the timer is already same in DB
    time_take = time_takes.get(person_id)
    time_take_tot = (time_take - schedule_end_times).total_seconds()
    if time_take_tot > late[person_id]:
        late[person_id] = time_take_tot
        # time_take_tot = late_time

    print(f"Late Time for2 {person_id}: {format_duration(late[person_id])}")

    return late[person_id]


def start_left_timer(person_id):
    current_time = datetime.now()
    left_time = 0

    if person_id not in exit_timers:
        exit_timers[person_id] = current_time
        # print(f"Timer initialized for person {person_id} at {exit_timers}")
    else:
        left_time = (current_time - exit_timers[person_id]).total_seconds()
        # print(f"Left time for person {current_time}: {exit_timers} seconds")
        # print(f"Person {person_id} has been left for {left_time} seconds.")

        if left_time >= 60 and person_id not in left_warnings:
            print(f"WARNING: Person {person_id} has left for more than 10 minutes!")
            send_warning(person_id, f"Person {person_id} has left the room for 10 minutes!")
            left_warnings[person_id] = True
            last_left_warnings[person_id] = current_time

        elif left_time >= 60 and person_id in left_warnings:
            time_since_last_warning = (current_time - last_left_warnings[person_id]).total_seconds()

            if time_since_last_warning >= 300:
                print(f"WARNING: Person {person_id} is still not entered for more than 10 minutes!")
                send_warning(person_id, f"Person {person_id} not return to the room for another 10 minutes!")
                last_left_warnings[person_id] = current_time

    print(f"Timer for Left time = {left_time}")
    return left_time


def delete_left_timer(person_id):
    # left_time = start_left_timer(person_id)
    if person_id in exit_timers:
        # Menghapus semua data terkait person_id
        del exit_timers[person_id]
        # del left_time
        if person_id in left_warnings:
            del left_warnings[person_id]
        if person_id in last_left_warnings:
            del last_left_warnings[person_id]
        print(f"Timer and warnings deleted for person {person_id}")


def count_left_time(person_id):
    left_time = start_left_timer(person_id)

    # Showing the total time outside
    print(f"Person {person_id} left room for {format_duration(left_time)}")

    # print(f"Total time outside for person {person_id} in second: {left_time} seconds")
    return left_time


def count_left_time_total(person_id):
    # total_left_time = total_left_times.get(person_id, 0)
    left_time = start_left_timer(person_id)

    if person_id not in total_left_times:
        total_left_times[person_id] = left_time
        print(f"total1: {total_left_times[person_id]}")
    else:
        total_left_times[person_id] += left_time

        print(f"total: {total_left_times[person_id]}")

    return total_left_times[person_id]


# For count the total time
def total_time(tracked_id):
    # Duration of class
    scheduled_duration = duration.get(tracked_id, 0)
    print(f"Duration ril: {scheduled_duration}")
    # Late time
    late_time = late.get(tracked_id, 0)  # count_late_time(tracked_id, schedule_start_time)
    print(f"Late Time ril: {late_time}")
    # Total time outside
    outside = total_left_times.get(tracked_id, 0)
    print(f"Time in outside ril= {outside}")
    # Total time
    total = scheduled_duration - late_time - outside
    # Display result
    print(f"Total {tracked_id} in the room {format_duration(total)}")

    # save_time_to_db(tracked_id, scheduled_duration, late_time, total, outside)

    return total


def format_duration(seconds):

    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} hours"


start_bot_in_thread()


# def save_time_to_db(person_id, scheduled_duration, late_time, total, outside):
#     try:
#         # time, time_range = capture_and_upload(img, person_id, event)
#         # Save the event details to the Firebase database
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         db.reference(f'time/{current_time}/{person_id}').set({
#             # 'name': db.reference(f'Person/{person_id}/name').get(),
#             'Duration': scheduled_duration,
#             'Late': late_time,
#             'left': outside,
#             'Total_time': total
#         })
#         print(f"Saved total time for person {person_id} to database.")
#     except Exception as e:
#         print(f"Error saving total time to database: {e}")


# def update_to_db(getId, time, time_range, event, late_time, left_times, total_duration,
#                  total_time_left, total_time_lecture):
#     db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}').set({
#         # 'name': db.reference(f'Person/{getId}/name').get(),
#         # 'event': event,
#         # 'time': current_time,
#         'late_time': late_time if event == "entered" else None,
#         'left_time': left_times if event == "return" else None,
#         'Duration': total_duration if event == "end" else None,
#         'Total_Time_Late': late_time if event == "end" else None,
#         'Total_Time_Left': total_time_left if event == "end" else None,
#         'total_time_lecture': total_time_lecture if event == "end" else None,
#         # 'image_url': image_url
#     })


# def update_to_db_for_left(getId, current_date, time_range, event, current_time, image_url):
#     db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}').push({
#         'name': db.reference(f'Person/{getId}/name').get(),
#         'event': event,
#         'time_range': time_range,
#         'time': current_time,
#         'image_url': image_url
#     })
#     left(current_time, image_url)
#
#
# def update_to_db_for_return(getId, current_date, time_range, event, left_times, current_time, image_url):
#     db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}').push({
#         'name': db.reference(f'Person/{getId}/name').get(),
#         'event': event,
#         'time': current_time,
#         'left_time': left_times if event == "return" else None,
#         'image_url': image_url
#     })
#     # return current_time
#     back(getId, current_date, left_times)
#
#
# def update_to_db_for_late(getId, current_date, time_range, event, lates, current_time, image_url):
#
#     db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}').push({
#         'name': db.reference(f'Person/{getId}/name').get(),
#         'event': event,
#         'time': current_time,
#         'time_range_for_session': time_range,
#         'late_time': lates if event == "entered" else None,
#         'image_url': image_url
#     })
#
#     # return current_time
#     entry(image_url, current_time, lates)
#
#
# def update_to_db_for_end(getId, current_date, time_range, event, late_time, total_duration, total_time_left,
#                          total_time_lecture, current_time, image_url):
#     db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}').push({
#         'name': db.reference(f'Person/{getId}/name').get(),
#         'event': event,
#         'time': current_time,
#         'Duration': total_duration,
#         'Total_Time_Late': late_time,
#         'Total_Time_Left': total_time_left,
#         'Total_Time_Lecture': total_time_lecture,
#         'image_url': image_url
#     })
#     # return total_duration, late_time, total_time_left, total_time_lecture
#     end(image_url, current_time, total_duration, late_time, total_time_left, total_time_lecture)

