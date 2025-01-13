# import jinja2
# import pdfkit
# from firebase_admin import db
# import sys
# sys.path.append('../schedule.py/')
#
#
# def entry(image_url, current_time, lates):
#     img1 = image_url
#     time1 = current_time
#     late = lates
#
#     contect_entry = {'img1': img1, 'time1': time1, 'late': lates}
#
#     print(f" img1: {img1}, time1: {time1}, late: {late}")
#     return contect_entry
#
#
# def left(current_time, image_url):
#     img2 = image_url
#     time2 = current_time
#
#     context_left ={'img2': img2, 'time2': time2}
#
#     print(f" Img2: {img2}, time2: {time2}")
#     return context_left
#
#
# def back(image_url, current_time, left_times):
#     img3 = image_url
#     time3 = current_time
#     left1 = left_times
#
#     context_back = {'img3': img3, 'time3': time3, 'left1': left1}
#
#     print(f"img3: {img3}, time3: {time3}, left1: {left1}")
#     return context_back
#
#
# def end(image_url, current_time, total_duration, late_time, total_time_left, total_time_lecture):
#     img4 = image_url
#     time4 = current_time
#     dur = total_duration
#     late2 = late_time
#     left2 = total_time_left
#     tot = total_time_lecture
#
#     context_end = {'img4': img4, 'time': time4, 'dur': dur, 'late2': late2, 'left2': left2, 'tot': tot}
#
#     print(f"img4: {img4}, time4: {time4}, dur: {dur}, late2: {late2}, left2: {left2}, tot: {tot}")
#     return context_end
#
#
# # def pdd(person_id, current_date, current_time, image_url, lates, left_times, total_duration, late_time, total_time_left,
# #         total_time_lecture):
# def pdd(person_id, current_date, current_time):
#     print("Processing data for person:", person_id)
#
#     # For name
#     name = db.reference(f'Person/{person_id}/name').get() or "Unknown"
#
#     # For ID
#     ID = db.reference(f'Person/{person_id}/title').get() or "Unknown"
#
#     # For time ranges
#     time_range_ref = db.reference(f'PersonEvents/{current_date}/{person_id}')
#     time_range_data = time_range_ref.get()
#
#     if time_range_data:
#         for time_range in time_range_data.keys():
#             # print(time_range)
#             time_rangesss = time_range
#             print(time_rangesss)
#     else:
#         print("NO")
#
#     context_entry = entry(image_url, current_time, lates))
#     context_left = left(current_time, image_url)
#     context_back = back(image_url, current_time, left_times)
#     context_end = end(image_url, current_time, total_duration, late_time, total_time_left, total_time_lecture)
#
#
#     # img1, time1, late = entry(image_url, current_time, lates)
#     # img2, time2 = left(current_time, image_url)
#     # img3, time3, left1 = back(image_url, current_time, left_times)
#     # img4, time4, dur, late2, left2, tot = end(image_url, current_time, total_duration, late_time, total_time_left,
#     #                                           total_time_lecture)
#
#     context = {
#         context_entry,
#         context_left,
#         context_back,
#         context_end
#     }
#
#     # context = {'name': name, 'ID': ID, 'time_rangesss': time_rangesss, 'img1': img1, 'time1': time1, 'late': late}
#
#     template_loader = jinja2.FileSystemLoader('./')
#     template_env = jinja2.Environment(loader=template_loader)
#     template = template_env.get_template("pdf.html")
#     output_text = template.render(context)
#
#     config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
#     pdf_filename = f'monitoring - {person_id} - {current_date} - {current_time}.pdf'
#     pdfkit.from_string(output_text, pdf_filename, configuration=config)
#
#     print(f"PDF generated: {pdf_filename}")


# import jinja2
# import pdfkit
# from firebase_admin import db
# import sys
#
# sys.path.append('../schedule.py/')
#
# def get_event_data(person_id, current_date, time_range, event):
#     """Ambil data event untuk time_range tertentu."""
#     event_path = f'PersonEvents/{current_date}/{person_id}/{time_range}/{event}'
#     event_data = db.reference(event_path).get()
#
#     if event_data:
#         return {
#             'image_url': event_data.get('image_url', 'No Image URL'),
#             'time': event_data.get('time', 'No Time'),
#             'late': event_data.get('late', 'No Late Time'),
#             'duration': event_data.get('Duration', 'No Duration'),
#             'total_time_late': event_data.get('Total_Time_Late', 'No Total Late Time'),
#             'total_time_left': event_data.get('Total_Time_Left', 'No Total Left Time'),
#             'total_time_lecture': event_data.get('Total_Time_Lecture', 'No Total Lecture Time'),
#         }
#     else:
#         return {}
#
# def pdd(person_id, current_date, current_time):
#     """Fungsi utama untuk memproses data dan membuat PDF."""
#     print(f"Processing data for person: {person_id}")
#
#     # Ambil data utama (nama dan ID)
#     name = db.reference(f'Person/{person_id}/name').get() or "Unknown"
#     ID = db.reference(f'Person/{person_id}/title').get() or "Unknown"
#
#     # Ambil time ranges
#     time_range_ref = db.reference(f'PersonEvents/{current_date}/{person_id}')
#     time_range_data = time_range_ref.get()
#
#     # Jika tidak ada time range, hentikan proses
#     if not time_range_data:
#         print("No time ranges found.")
#         return
#
#     # Siapkan struktur data untuk context
#     events_data = []
#     for time_range in time_range_data.keys():
#         print(f"Processing time range: {time_range}")
#
#         # Ambil data untuk setiap event dalam time range ini
#         entry_data = get_event_data(person_id, current_date, time_range, "Entry")
#         left_data = get_event_data(person_id, current_date, time_range, "Left")
#         back_data = get_event_data(person_id, current_date, time_range, "Return")
#         end_data = get_event_data(person_id, current_date, time_range, "End")
#
#         # Tambahkan data time range ke daftar events_data
#         events_data.append({
#             'time_range': time_range,
#             'entry': entry_data,
#             'left': left_data,
#             'back': back_data,
#             'end': end_data
#         })
#
#     # Context untuk template Jinja2
#     context = {
#         'name': name,
#         'ID': ID,
#         'current_date': current_date,
#         'current_time': current_time,
#         'events': events_data
#     }
#
#     # Muat template dan render dengan context
#     template_loader = jinja2.FileSystemLoader('./')
#     template_env = jinja2.Environment(loader=template_loader)
#     template = template_env.get_template("pdf.html")
#     output_text = template.render(context)
#
#     # Konfigurasi dan buat PDF
#     config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
#     pdf_filename = f'monitoring - {person_id} - {current_date} - {current_time}.pdf'
#     pdfkit.from_string(output_text, pdf_filename, configuration=config)
#
#     print(f"PDF generated: {pdf_filename}")


import jinja2
import pdfkit
from firebase_admin import db
import sys
sys.path.append('../schedule.py/')


def entry(image_url, current_time, lates):
    return {'img1': image_url, 'time1': current_time, 'late': lates}


def left(current_time, image_url):
    return {'img2': image_url, 'time2': current_time}


def back(image_url, current_time, left_times):
    return {'img3': image_url, 'time3': current_time, 'left1': left_times}


def end(image_url, current_time, total_duration, late_time, total_time_left, total_time_lecture):
    return {
        'img4': image_url,
        'time4': current_time,
        'dur': total_duration,
        'late2': late_time,
        'left2': total_time_left,
        'tot': total_time_lecture
    }


def pdd(person_id, current_date, current_time, **kwargs):
    """
    Generate a PDF based on provided person data and their activities.

    Args:
        person_id: ID of the person.
        current_date: Current date.
        current_time: Current time.
        **kwargs: Additional keyword arguments for entry, left, back, and end functions.
    """
    print("Processing data for person:", person_id)

    # Fetch person details from Firebase
    name = db.reference(f'Person/{person_id}/name').get() or "Unknown"
    title = db.reference(f'Person/{person_id}/title').get() or "Unknown"

    # Fetch time ranges from Firebase
    time_range_ref = db.reference(f'PersonEvents/{current_date}/{person_id}')
    time_range_data = time_range_ref.get()
    time_ranges = list(time_range_data.keys()) if time_range_data else []

    print("Time ranges:", time_ranges if time_ranges else "No events found")

    # Prepare context by calling each function with relevant kwargs
    context = {
        **entry(kwargs['image_url'], current_time, kwargs.get('lates', 0)),
        **left(current_time, kwargs['image_url']),
        **back(kwargs['image_url'], current_time, kwargs.get('left_times', 0)),
        **end(
            kwargs['image_url'],
            current_time,
            kwargs.get('total_duration', 0),
            kwargs.get('late_time', 0),
            kwargs.get('total_time_left', 0),
            kwargs.get('total_time_lecture', 0)
        ),
        'name': name,
        'title': title,
        'time_ranges': time_ranges
    }

    # Generate PDF
    template_loader = jinja2.FileSystemLoader('../')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("pdf.html")
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
    pdf_filename = f'monitoring - {person_id} - {current_date} - {current_time}.pdf'
    pdfkit.from_string(output_text, pdf_filename, configuration=config)

    print(f"PDF generated: {pdf_filename}")


