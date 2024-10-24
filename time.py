from datetime import datetime
from firebase_admin import db
from capture import capture_and_upload


# Variable For left warning
exit_timers = {}
total_time_outside = {}
left_warnings = {}
last_left_warnings = {}

# Variable for late warning
late_timers = {}
late_warnings = {}
last_late_warning = {}


# for counting the duration of class
def count_duration(schedule_start_time, schedule_end_time):
    # schedule_start_time, schedule_end_time = is_scheduled(tracked_id)
    scheduled_duration = (schedule_end_time - schedule_start_time).total_seconds()
    if schedule_start_time and schedule_end_time:
        current_time = datetime.now()
        if current_time >= schedule_end_time:
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

    return scheduled_duration


# For timer time late amd giving Warning
def start_late_timer(person_id, scheduled_start_time):
    # schedule_start_time, schedule_end_time = is_scheduled(tracked_id)
    # scheduled_start_time = schedule_start_time
    current_time = datetime.now()
    late_time = 0
    # If the person is late, start a timer
    # if current_time >= scheduled_start_time and person_id not in tracked_ids:
    if person_id not in late_timers:
        late_timers[person_id] = current_time  # Start the late timer
        # late_timers[person_id] = scheduled_start_time  # Start the late timer
    else:
        late_time = (current_time - late_timers[person_id]).total_seconds()
        # late_time = (scheduled_start_time - late_timers[person_id]).total_seconds()
        # print(f"late time1 : {late_time}")
        # Check if 10 minutes have passed
        # if late_time >= 5:  # 600 seconds = 10 minutes
        #     print(f"WARNING: Person {person_id} has not entered for more than 10 minutes!")
        if late_time >= 5 and person_id not in late_warnings:  # 600 seconds = 10 minutes
            print(f"WARNING: Person {person_id} has not entered for more than 10 minutes!")
            late_warnings[person_id] = True
            last_late_warning[person_id] = current_time
        elif late_time >= 5 and person_id in late_warnings:
            time_since_last_warning = (current_time - last_late_warning[person_id]).total_seconds()
            if time_since_last_warning >= 300:
                print(f"WARNING: Person {person_id} is still not entered for more than 10 minutes!")
                last_late_warning[person_id] = current_time

    return late_time


# for counting the total time late
def count_late_time(person_id, scheduled_start_time):
    late_time = start_late_timer(person_id, scheduled_start_time)
    # total_late_time = late_warnings[person_id, 0]

    # Calculate actual entry time
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

    return late_time


# Function for timer left the room and warning
# def start_left_timer(person_id):
#     current_time = datetime.now()
#     print(f"Current time: {current_time}")
#     left_time = 0
#     if person_id not in exit_timers:
#         exit_timers[person_id] = current_time
#         print(f"Timer started for person {person_id} at {current_time}")
#         print(exit_timers)
#     else:
#         left_time = (current_time - exit_timers[person_id]).total_seconds()
#         print(f"Person {person_id} has been left for {left_time} seconds.")
#         if left_time >= 5 and person_id not in left_warnings:  # 600 seconds = 10 minutes
#             print(f"WARNING: Person {person_id} has left for more than 10 minutes!")
#             left_warnings[person_id] = True
#             last_left_warnings[person_id] = current_time
#         elif left_time >= 5 and person_id in left_warnings:
#             time_since_last_warning = (current_time - last_left_warnings[person_id]).total_seconds()
#             if time_since_last_warning >= 300:
#                 print(f"WARNING: Person {person_id} is still not entered for more than 10 minutes!")
#                 last_left_warnings[person_id] = current_time
#
#     print(left_time)
#
#     return left_time



    # if person_id not in exit_timers:
    #     exit_timers[person_id] = current_time
    # else:
    #     elapsed_time = (current_time - exit_timers[person_id]).total_seconds()
    #
    #     if person_id not in total_time_outside:
    #         total_time_outside[person_id] = 0
    #     total_time_outside[person_id] += elapsed_time
    #     print(total_time_outside)

        # if elapsed_time > 6 and person_id not in left_waring:
        #     print(f"Person {person_id} has been left the room for more than 10 minutes!")
        #     left_waring[person_id] = True
        # elif elapsed_time > 6 and person_id in left_waring:
        #     time_since_left_warning = (current_time - left_waring[person_id]).total_seconds()
        #     if time_since_left_warning > 300:
        #         print(f"Person {person_id} is still left the room for more than 10 minutes!")
        #         left_waring[person_id] = elapsed_time

        # if elapsed_time > 6:
        #     if person_id not in left_waring:
        #         # First warning after 10 minutes
        #         print(f"Person {person_id} has been left the room for more than 10 minutes!")
        #         left_waring[person_id] = current_time  # Store the time of the warning
        #     else:
        #         # Check if 5 more minutes (300 seconds) have passed since the last warning
        #         time_since_last_warning = (current_time - left_waring[person_id]).total_seconds()
        #         if time_since_last_warning > 300:
        #             print(f"Person {person_id} is still left the room for more than {int(elapsed_time // 60)} minutes!")
        #             left_waring[person_id] = current_time  # Update the warning time
        #
        # return elapsed_time

        # print(f"Person {person_id} has been outside the room for "
        #       f"{elapsed_time} seconds")


def start_left_timer(person_id):
    current_time = datetime.now()
    print(f"Current time: {current_time}")  # Print waktu saat ini
    left_time = 0

    if person_id not in exit_timers:
        exit_timers[person_id] = current_time
        print(f"Timer started for person {person_id} at {current_time}")  # Timer dimulai
    else:
        left_time = (current_time - exit_timers[person_id]).total_seconds()
        print(f"Person {person_id} has been left for {left_time} seconds.")  # Tampilkan waktu yang telah berlalu

        # Ubah 5 detik menjadi 600 detik untuk peringatan lebih dari 10 menit
        if left_time >= 600 and person_id not in left_warnings:
            print(f"WARNING: Person {person_id} has left for more than 10 minutes!")
            left_warnings[person_id] = True
            last_left_warnings[person_id] = current_time
        elif left_time >= 600 and person_id in left_warnings:
            time_since_last_warning = (current_time - last_left_warnings[person_id]).total_seconds()
            print(
                f"Time since last warning for person {person_id}: {time_since_last_warning} seconds.")  # Print waktu sejak peringatan terakhir

            if time_since_last_warning >= 300:
                print(f"WARNING: Person {person_id} is still not entered for more than 10 minutes!")
                last_left_warnings[person_id] = current_time

    print(f"Left time: {left_time} seconds.")  # Print waktu left_time yang dihitung

    return left_time


# Function to reset exit timer (when someone re-enters the room)
def reset_exit_timer(person_id):
    if person_id in exit_timers:
        del exit_timers[person_id]


def count_left_time(person_id):
    left_time = start_left_timer(person_id)

    # Showing the total time outside
    # if person_id in total_time_outside:
    #     total_time_left = total_time_outside[person_id]
        # total_time = total_time.total_seconds()
    if left_time < 60:
        print(f"Total time outside for person {person_id}: {left_time} seconds")
    elif left_time < 3600:
        left_time /= 60
        print(f"Total time outside for person {person_id}: {left_time} minutes")
        left_time = left_time * 60
    elif left_time >= 3600:
        left_time /= 3600
        print(f"Total time outside for person {person_id}: {left_time} hours")
        left_time = left_time * 3600
    else:
        print("-")
    print(f"Total time outside for person {person_id} in second: {left_time} seconds")

    return left_time


    # else:
    #     return None
        # print(f"No exit time recorded for person {person_id}")


# For count the total time
def total_time(tracked_id, schedule_start_time, schedule_end_time):
    # Duration of class
    scheduled_duration = count_duration(schedule_start_time, schedule_end_time)
    # Late time
    late_time = count_late_time(tracked_id, schedule_start_time)
    # Total time outside
    outside = count_left_time(tracked_id)
    # if total_time_outside is None:
    #     total_time_outside = 0

    # else:
    #     # total_time_outside = count_left_time(tracked_id)
    #     print(total_time_outside)

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
    # total_time_outside[tracked_id] = total_time_outside.get(tracked_id, 0)

    total = scheduled_duration - late_time - outside

    if total < 3600:
        total /= 60
        print(f"Total time lecture for person {tracked_id}: {total} minutes")
    elif total >= 3600:
        total /= 3600
        print(f"Total time lecture for person {tracked_id}: {total} hours")
    else:
        print(f"Total time lecture for person {tracked_id}: {total} seconds")

    save_time_to_db(tracked_id, scheduled_duration, late_time, total, outside)


def save_time_to_db(person_id, scheduled_duration, late_time, total, outside):
    try:
        # time, time_range = capture_and_upload(img, person_id, event)
        # Save the event details to the Firebase database
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.reference(f'time/{current_time}/{person_id}').set({
            # 'name': db.reference(f'Person/{person_id}/name').get(),
            'Duration': scheduled_duration,
            'Late': late_time,
            'left': outside,
            'Total_time': total
        })
        print(f"Saved total time for person {person_id} to database.")
    except Exception as e:
        print(f"Error saving total time to database: {e}")
