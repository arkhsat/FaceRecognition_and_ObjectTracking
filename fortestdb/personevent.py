import sqlite3
from pathlib import Path

# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()
db_path = Path(__file__).parent / "database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

db_image_path = Path(__file__).parent / "image_from_cap.db"
conn_image = sqlite3.connect(db_image_path)
cursor_image = conn_image.cursor()

# cursor.execute("""CREATE TABLE PersonEvent (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         person_id INTEGER,
#                         date TEXT,
#                         time_range TEXT,
#                         event TEXT,
#                         time TEXT,
#                         image BLOB,  -- Kolom untuk menyimpan gambar dalam format BLOB
#                         left_time TEXT,
#                         duration INTEGER,
#                         total_time_late INTEGER,
#                         total_time_left INTEGER,
#                         total_time_lecture INTEGER,
#                         FOREIGN KEY(person_id) REFERENCES Person(id)
#             )
#             """)

# cursor.execute("""CREATE TABLE PersonEventEnd (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         person_id INTEGER,
#                         date TEXT,
#                         time_range TEXT,
#                         event TEXT,
#                         time TEXT,
#                         left_time TEXT,
#                         duration INTEGER,
#                         total_time_late INTEGER,
#                         total_time_left INTEGER,
#                         total_time_lecture INTEGER,
#                         image BLOB,  -- Kolom untuk menyimpan gambar dalam format BLOB
#                         FOREIGN KEY(person_id) REFERENCES Person(id)
#             )
#             """)


def get_image_blob(person_id, event, current_date):
    cursor_image.execute("""
        SELECT img_path FROM image
        WHERE person_id = ? AND event = ? AND date = ?
    """, (person_id, event, current_date))
    result = cursor_image.fetchone()
    return result[0] if result else None

# with open(local_img_path, 'rb') as file:
#     img_data = file.read()


# conn.commit()

# def get_person_name(cursor, person_id):
#     cursor.execute("SELECT name FROM Person WHERE id = ?", (person_id,))
#     result = cursor.fetchone()
#     return result[0] if result else None


def update_to_db_for_left(person_id, current_date, time_range, event, current_time):
    # name = get_person_name(cursor, person_id)
    image_url = get_image_blob(person_id, event, current_date)
    cursor.execute('''
        INSERT INTO PersonEventLeft (person_id, date, time_range, event, time, image)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (person_id, current_date, time_range, event, current_time, image_url))
    conn.commit()


def update_to_db_for_return(person_id, current_date, time_range, event, left_times, current_time):
    image_url = get_image_blob(person_id, event, current_date)
    cursor.execute('''
        INSERT INTO PersonEventReturn (person_id, date, time_range, event, time, left_time, image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (person_id, current_date, time_range, event, current_time, left_times, image_url))
    conn.commit()


def update_to_db_for_late(person_id, current_date, time_range, event, lates, current_time):
    # name = get_person_name(cursor, person_id)
    image_url = get_image_blob(person_id, event, current_date)
    cursor.execute('''
        INSERT INTO PersonEventLate (person_id, date, time_range, event, time, total_time_late, image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (person_id, current_date, time_range, event, current_time, lates, image_url))
    conn.commit()


def update_to_db_for_end(person_id, current_date, time_range, event, late_time, total_duration, total_time_left, total_time_lecture, current_time):
    # name = get_person_name(cursor, person_id)
    image_url = get_image_blob(person_id, event, current_date)
    cursor.execute('''
        INSERT INTO PersonEventEnd (person_id, date, time_range, event, time, duration, total_time_late, total_time_left, total_time_lecture, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (person_id, current_date, time_range, event, current_time, total_duration, late_time, total_time_left, total_time_lecture, image_url))
    conn.commit()


# Cek tabel dalam database
cursor_image.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor_image.fetchall()
print("Tabel yang ada di database:", tables)
