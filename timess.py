from datetime import datetime, timedelta

from telegrambot.telegrambot import send_warning, start_bot_in_thread, get_chat_id

# Variable For left warning
exit_timers = {}
left_warnings = {}
last_left_warnings = {}
total_left_times = {}


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
    print(f" {schedule_start_time} - {schedule_end_time}")
    scheduled_duration = (schedule_end_time - schedule_start_time).total_seconds()
    scheduledb = formating(scheduled_duration)
    duration[person_id] = scheduled_duration
    if schedule_start_time and schedule_end_time:
        print(f"Duration Of Class: {format_duration(scheduled_duration)}")
    print(f"Duration in second: {scheduled_duration}")
    return scheduledb


# For timer time late amd giving Warning
def start_late_timer(person_id):
    time_takes[person_id] = datetime.now()
    current_time = datetime.now()
    late_time = 0
    get_chat_id(person_id)

    # If the person is late, start a timer
    if person_id not in late_timers or late_timers[person_id] is None:
        late_timers[person_id] = current_time  # Start the late timer
        timer_active[person_id] = True

    else:
        late_time = (current_time - late_timers[person_id]).total_seconds()
        if late_time >= 5 and person_id not in late_warnings:  # 600 seconds = 10 minutes
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
    test = formating(late[person_id])

    # Calculate actual entry time base on timer
    print(f"Late Time for1 {person_id}: {format_duration(late[person_id])}")

    # For Checking if the count of the timer is already same in DB
    time_take = time_takes.get(person_id)
    time_take_tot = (time_take - schedule_end_times).total_seconds()
    if time_take_tot > late[person_id]:
        late[person_id] = time_take_tot
        test = formating(time_take_tot)

    print(f"Late Time for2 {person_id}: {format_duration(late[person_id])}")

    return test


def start_left_timer(person_id):
    current_time = datetime.now()
    left_time = 0

    if person_id not in exit_timers:
        exit_timers[person_id] = current_time

    else:
        left_time = (current_time - exit_timers[person_id]).total_seconds()

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
    if person_id in exit_timers:

        del exit_timers[person_id]
        # del left_time
        if person_id in left_warnings:
            del left_warnings[person_id]
        if person_id in last_left_warnings:
            del last_left_warnings[person_id]
        print(f"Timer and warnings deleted for person {person_id}")


def count_left_time(person_id):
    left_time = start_left_timer(person_id)
    leftdb = formating(left_time)

    # Showing the total time outside
    print(f"Person {person_id} left room for {format_duration(left_time)}")

    return leftdb


def count_left_time_total(person_id):
    left_time = start_left_timer(person_id)

    if person_id not in total_left_times:
        total_left_times[person_id] = left_time
        lefttotdb = formating(total_left_times[person_id])
        print(f"total1: {total_left_times[person_id]}")
    else:
        total_left_times[person_id] += left_time
        lefttotdb = formating(total_left_times[person_id])

        print(f"total: {total_left_times[person_id]}")
        print(f"total2: {lefttotdb}")

    return lefttotdb


# For count the total time
def total_time(tracked_id):
    # Duration of class
    scheduled_duration = duration.get(tracked_id, 0)
    print(f"Duration ril: {scheduled_duration}")
    # Late time
    late_time = late.get(tracked_id, 0) 
    print(f"Late Time ril: {late_time}")
    # Total time outside
    outside = total_left_times.get(tracked_id, 0)
    print(f"Time in outside ril= {outside}")
    # Total time
    total = scheduled_duration - late_time - outside
    totaldb = formating(total)
    # Display result
    print(f"Total {tracked_id} in the room {format_duration(total)}")

    return totaldb


def format_duration(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} hours"


def formating(seconds):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


start_bot_in_thread()
