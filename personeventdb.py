from firebase_admin import db


def update_to_db_for_left(getId, current_date, time_range, event, current_time, image_url):
    db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}').push({
        'name': db.reference(f'Person/{getId}/name').get(),
        'event': event,
        'time_range': time_range,
        'time': current_time,
        'image_url': image_url,
    })


def update_to_db_for_return(getId, current_date, time_range, event, left_times, current_time, image_url):
    db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}').push({
        'name': db.reference(f'Person/{getId}/name').get(),
        'event': event,
        'time': current_time,
        'left_time': left_times if event == "return" else None,
        'image_url': image_url
    })


def update_to_db_for_late(getId, current_date, time_range, event, lates, current_time, image_url):

    db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}').push({
        'name': db.reference(f'Person/{getId}/name').get(),
        'event': event,
        'time': current_time,
        'time_range_for_session': time_range,
        'late_time': lates if event == "entered" else None,
        'image_url': image_url
    })


def update_to_db_for_end(getId, current_date, time_range, event, late_time, total_duration, total_time_left,
                         total_time_lecture, current_time, image_url):
    db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}').push({
        'name': db.reference(f'Person/{getId}/name').get(),
        'event': event,
        'time': current_time,
        'Duration': total_duration,
        'Total_Time_Late': late_time,
        'Total_Time_Left': total_time_left,
        'Total_Time_Lecture': total_time_lecture,
        'image_url': image_url,
    })


def update_pdf(getId, current_date, time_range, event, pdf_url):
    db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}').update({
        'PDF': pdf_url
    })
