import jinja2
import pdfkit
# import sys
# sys.path.append('../schedule.py/')
from schedule import is_scheduled
# import schedule
from firebase_admin import db


def pdd(person_id):
    print("ppp")
    scheduled_start_time, scheduled_end_time, current_time, time_range, current_date = is_scheduled(person_id)

    # Begin
    name = db.reference(f'Person/{person_id}/name').get()
    ID = db.reference(f'Person/{person_id}').get()
    time_range = db.reference(f'PersonEvents/{current_date}/{person_id}/time_range').get()

    # Entered The Room
    img1 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/entered/image_url').get()
    time1 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/entered/time').get()
    late = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/entered/late_time').get()

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

    template_loader = jinja2.FileSystemLoader(f'./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template("pdf.html")
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
    pdfkit.from_string(output_text, f'monitoring - {person_id} - {current_time}.pdf', configuration=config)


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
