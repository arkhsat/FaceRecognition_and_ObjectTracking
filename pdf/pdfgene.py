import jinja2
import pdfkit
from firebase_admin import db, storage
import os
from datetime import datetime, timedelta

# Temporary storage for collected data
event_data = {}


def pdd(getId, current_date, current_time, time_range, event):
    try:
        global event_data

        print(f"Processing event: {event} for ID: {getId}")

        # Firebase reference
        ref = db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}')
        data = ref.get()

        if not data:
            print(f"No data found for ID {getId}, event {event}.")
            return

        # Get the latest key and its value
        latest_key = max(data.keys())
        value = data[latest_key]

        # Store data for each event
        if event in ["entered", "left", "return", "end"]:
            event_data[event] = {
                "name": value.get('name', 'Unknown'),
                "event_time": value.get('time', 'Unknown'),
                "image_url": value.get('image_url', ''),
                "late_time": value.get('late_time', 'N/A'),
                "time_range_for_session": value.get('time_range_for_session', 'N/A'),
                "left_time": value.get('left_time', 'N/A'),
                "total_duration": value.get('total_duration', 'N/A'),
                "Total_Time_Late": value.get('Total_Time_Late', 'N/A'),
                "Total_Time_Left": value.get('Total_Time_Left', 'N/A'),
                "Total_Time_Lecture": value.get('Total_Time_Lecture', 'N/A'),
            }

        # If event is "end", generate the PDF
        if event == "left":
            print("Starting PDF generation...")

            # Fetch additional information from Firebase
            ID = db.reference(f'Person/{getId}/title').get()

            # Prepare context for the template
            context = {
                'name': event_data.get('entered', {}).get('name', 'Unknown'),
                'ID': ID,
                'time_range': event_data.get('entered', {}).get('time_range_for_session', 'N/A'),
                'img1': event_data.get('entered', {}).get('image_url', ''),
                'time1': event_data.get('entered', {}).get('event_time', 'Unknown'),
                'late': event_data.get('entered', {}).get('late_time', 'N/A'),
                'img2': event_data.get('left', {}).get('image_url', ''),
                'time2': event_data.get('left', {}).get('event_time', 'Unknown'),
                'img3': event_data.get('return', {}).get('image_url', ''),
                'time3': event_data.get('return', {}).get('event_time', 'Unknown'),
                'left1': event_data.get('return', {}).get('left_time', 'N/A'),
                'img4': event_data.get('end', {}).get('image_url', ''),
                'time4': event_data.get('end', {}).get('event_time', 'Unknown'),
                'dur': event_data.get('end', {}).get('total_duration', 'N/A'),
                'late2': event_data.get('end', {}).get('Total_Time_Late', 'N/A'),
                'left2': event_data.get('end', {}).get('Total_Time_Left', 'N/A'),
                'tot': event_data.get('end', {}).get('Total_Time_Lecture', 'N/A')
            }
            print(f"event_data = {event_data}")

            # Jinja2 template rendering
            template_loader = jinja2.FileSystemLoader('./')  # Adjust path if needed
            template_env = jinja2.Environment(loader=template_loader)

            try:
                template = template_env.get_template("pdf/pdf.html")  # Ensure file exists
            except jinja2.exceptions.TemplateNotFound:
                print("Template 'pdf.html' not found.")
                return

            output_text = template.render(context)

            # For output directory
            output_dir = os.path.join('pdf', 'pdffile', current_date, getId, time_range)
            os.makedirs(output_dir, exist_ok=True)

            # Generate PDF
            config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
            pdf_filename = os.path.join(output_dir, f'monitoring - {getId} - {current_date} - {current_time}.pdf')
            pdfkit.from_string(output_text, pdf_filename, configuration=config)

            print(f"Success: PDF created at {pdf_filename}")

            # Clear event data after generating the PDF
            event_data = {}

            # Save to Storage
            bucket = storage.bucket()
            blob = bucket.blob(f'PDF/{current_date}/{getId}/{time_range}')

            blob.upload_from_filename(pdf_filename)
            pdf_url = blob.generate_signed_url(expiration=datetime.utcnow() + timedelta(seconds=86400))
            return pdf_url

    except Exception as e:
        print(f"An error occurred: {e}")
