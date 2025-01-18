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


