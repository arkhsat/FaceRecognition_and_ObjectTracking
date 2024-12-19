import jinja2
import pdfkit
from firebase_admin import db
from pathlib import Path


def pdd(getId, current_date, current_time, time_range, event):
    print("ppp")

    ref = db.reference(f'PersonEvents/{current_date}/{getId}/{time_range}/{event}')
    data = ref.get()

    if data:
        # key for the last
        latest_key = max(data.keys())
        value = data[latest_key]

        # get the detail of data
        name = value.get('name')
        time = value.get('time')
        image_url = value.get('image_url')
        late = value.get('late_time')
        ranges = value.get('time_range_for_session')

        # Begin
        name = {name}
        ID = db.reference(f'Person/{getId}').get()
        time_range = {ranges}

        # Entered The Room
        img1 = {image_url}
        time1 = {time}
        late = {late}

        # # Left The Room
        # img2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/left/image_url').get()
        # time2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/left/time').get()
        #
        # # Return The Room
        # img3 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/return/image_url').get()
        # time3 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/return/time').get()
        # left1 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/return/left').get()

        # End of Time
        # img4 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/image_url').get()
        # time4 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/time').get()
        # dur = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Duration').get()
        # late2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Total_Time_Late').get()
        # left2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Total_Time_Left').get()
        # tot = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Total_Time_Lecture').get()

        # context = {'name': name, 'ID': ID, 'time_range': time_range, 'img1': img1, 'img2': img2, 'img3': img3, 'img4': img4,
        #            'time1': time1, 'time2': time2, 'time3': time3, 'time4': time4, 'late': late, 'late2': late2, 'left1':
        #                left1, 'left2': left2, 'dur': dur, 'tot': tot}

        # context = {'name': name, 'ID': ID, 'time_range': time_range, 'img1': img1, 'img2': img2, 'img3': img3,
        #            'time1': time1, 'time2': time2, 'time3': time3, 'late': late, 'left1': left1}

        context = {'name': name, 'ID': ID, 'time_range': time_range, 'img1': img1,
                   'time1': time1, 'late': late}

        # context = {'img1': img1}

        template_loader = jinja2.FileSystemLoader(f'./')
        template_env = jinja2.Environment(loader=template_loader)

        template = template_env.get_template("pdf.html")
        output_text = template.render(context)

        config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
        pdfkit.from_string(output_text, f'monitoring - {getId} - {current_time}.pdf', configuration=config)


# name = "rendo"
# ID = "1234"
# time_range = "10"
# img1 = "11"
# time1= "11"
# late= "11"
# img2= "11"
# time3= "11"
# time4= "11"
# left1= "11"
# img4= "11"
# time5= "11"
# dur= "11"
# late2= "11"
# left2= "11"
# tot= "11"
#
# context = {'name': name, 'ID': ID, 'time_range': time_range, 'img1': img1, 'img2':
# img2, 'img4': img4, 'time1': time1, 'time3': time1, 'time4': time4, 'time5': time5,
# 'late': late, 'late2': late2, 'left1': left1, 'left2': left2, 'dur': dur, 'tot': tot}
#
# template_loader = jinja2.FileSystemLoader('./')
# template_env = jinja2.Environment(loader=template_loader)
#
# template = template_env.get_template("pdf.html")
# output_text = template.render(context)
#
# config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
# pdfkit.from_string(output_text, 'pdf_generated.pdf', configuration = config)
