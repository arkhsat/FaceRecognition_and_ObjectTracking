import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta

cred = credentials.Certificate("serviceAccountKey1.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://testing1-5b399-default-rtdb.firebaseio.com/",
    'storageBucket': "testing1-5b399.appspot.com"
})

current_date = datetime.now().strftime("%Y - %m - %d")
current_time = datetime.now()

def for_display_entred():
    # Save event entered in Firebase
    db.reference(f'Display/{current_date}/{current_time}/{person_id}/{event}').push({
        'name': db.reference(f'Person/{getId}/name').get(),
        'event': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/event').get(),
        'time': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/time').get(),
        'image_url': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/image_url').get(),
        'Late': db.reference(f'time/{time}/{time_range}/{person_id}/late').get()
    })


def for_display_left():
    # Save event entered in Firebase
    db.reference(f'Display/{current_date}/{current_time}/{person_id}/{event}').push({
        'name': db.reference(f'Person/{getId}/name').get(),
        'event': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/event').get(),
        'time': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/time').get(),
        'image_url': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/image_url').get(),
    })


def for_display_return():
    # Save event entered in Firebase
    db.reference(f'Display/{current_date}/{current_time}/{person_id}/{event}').push({
        'name': db.reference(f'Person/{getId}/name').get(),
        'event': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/event').get(),
        'time': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/time').get(),
        'image_url': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/image_url').get(),
        'Return': db.reference(f'time/{time}/{time_range}/{person_id}/left').get()
    })


def for_display_end():
    # Save event entered in Firebase
    db.reference(f'Display/{current_date}/{current_time}/{person_id}/{event}').push({
        'name': db.reference(f'Person/{getId}/name').get(),
        'event': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/event/end').get(),
        'time': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/time').get(),
        'image_url': db.reference(f'PersonEvents/{time}/{getId}/{time_range}/{event}/image_url/end').get(),
        'Total_time': db.reference(f'time/{time}/{time_range}/{person_id}/Total_time').get()
    })

def display_everything():
    for_display_entred()
    for_display_left()
    for_display_return()
    for_display_end()
