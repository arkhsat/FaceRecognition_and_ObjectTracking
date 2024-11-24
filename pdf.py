# import jinja2
# import pdfkit
# # import sys
# # sys.path.append('../schedule.py/')
# from schedule import is_scheduled
# # import schedule
# from firebase_admin import db
#
#
# def pdd(person_id, event):
#     print("ppp")
#     scheduled_start_time, scheduled_end_time, current_time, time_range, current_date = is_scheduled(person_id)
#     # Begin
#     name = db.reference(f'Person/{person_id}/name').get()
#     ID = db.reference(f'Person/{person_id}/title').get()
#     time_rangesss = db.reference(f'PersonEvents/{current_date}/{person_id}/time_range').get()
#     print(time_rangesss)
#
#     print(f"current_date: {current_date}")
#     print(f"person_id: {person_id}")
#     print(f"time_range: {time_range}")
#     print(f"event: {event}")
#
#     # Entered The Room
#     img1 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/{event}/image_url').get()
#     time1 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/{event}/time').get()
#     late = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/{event}/late_time').get()
#
#     # Left The Room
#     img2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/left/image_url').get()
#     time2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/left/time').get()
#
#     # Return The Room
#     img3 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/return/image_url').get()
#     time3 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/return/time').get()
#     left1 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/return/left').get()
#
#     # End of Time
#     img4 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/image_url').get()
#     time4 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/time').get()
#     dur = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Duration').get()
#     late2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Total_Time_Late').get()
#     left2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Total_Time_Left').get()
#     tot = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Total_Time_Lecture').get()
#
#     context = {'name': name, 'ID': ID, 'time_range': time_range, 'img1': img1, 'img2': img2, 'img3': img3, 'img4': img4,
#                'time1': time1, 'time2': time2, 'time3': time3, 'time4': time4, 'late': late, 'late2': late2, 'left1':
#                    left1, 'left2': left2, 'dur': dur, 'tot': tot}
#
#     # context = {'name': name, 'ID': ID, 'time_range': time_range, 'img1': img1, 'img2': img2, 'img3': img3,
#     #            'time1': time1, 'time2': time2, 'time3': time3, 'late': late, 'left1': left1}
#
#     # context = {'name': name, 'ID': ID, 'time_range': time_range}
#
#     template_loader = jinja2.FileSystemLoader(f'./')
#     template_env = jinja2.Environment(loader=template_loader)
#
#     template = template_env.get_template("pdf.html")
#     output_text = template.render(context)
#
#     config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
#     pdfkit.from_string(output_text, f'monitoring - {person_id} - {current_date} - {current_time}.pdf', configuration=config)
#
#
# # name = "rendo"
# # ID = "1234"
# # time_range = "10"
# # img1 = "11"
# # time1= "11"
# # late= "11"
# # img2= "11"
# # time3= "11"
# # time4= "11"
# # left1= "11"
# # img4= "11"
# # time5= "11"
# # dur= "11"
# # late2= "11"
# # left2= "11"
# # tot= "11"
# #
# # context = {'name': name, 'ID': ID, 'time_range': time_range, 'img1': img1, 'img2':
# # img2, 'img4': img4, 'time1': time1, 'time3': time1, 'time4': time4, 'time5': time5,
# # 'late': late, 'late2': late2, 'left1': left1, 'left2': left2, 'dur': dur, 'tot': tot}
# #
# # template_loader = jinja2.FileSystemLoader('./')
# # template_env = jinja2.Environment(loader=template_loader)
# #
# # template = template_env.get_template("pdf.html")
# # output_text = template.render(context)
# #
# # config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
# # pdfkit.from_string(output_text, 'pdf_generated.pdf', configuration = config)


import jinja2
import pdfkit
from firebase_admin import db
from timess import update_to_db_for_late
from schedule import is_scheduled


def pdd(person_id, event, current_date, time_range, current_time, lates, image_url):
    print("Processing data for person:", person_id)

    # scheduled_start_time, scheduled_end_time, current_time, time_range, current_date = is_scheduled(person_id)
    event, time_range, lates, image_url, current_time = update_to_db_for_late(person_id, current_date, time_range, event, lates, current_time, image_url)

    name = db.reference(f'Person/{person_id}/name').get() or "Unknown"
    ID = db.reference(f'Person/{person_id}/title').get() or "Unknown"
    time_range = db.reference(f'Person/{person_id}/title').get() or "Unknown"

    # def entry(person_id):
    img1 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/{event}/image_url').get()
    time1 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/{event}/time').get()
    late = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/{event}/late_time').get()

    #
    # img2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/left/image_url').get()
    # time2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/left/time').get()
    #
    # img3 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/return/image_url').get()
    # time3 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/return/time').get()
    # left1 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/return/left').get()
    #
    # img4 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/image_url').get()
    # time4 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/time').get()
    # dur = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Duration').get()
    # late2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Total_Time_Late').get()
    # left2 = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Total_Time_Left').get()
    # tot = db.reference(f'PersonEvents/{current_date}/{person_id}/{time_range}/end/Total_Time_Lecture').get()

    # context = {
    #     'name': name, 'ID': ID, 'time_range': time_range, 'img1': img1, 'img2': img2, 'img3': img3, 'img4': img4,
    #     'time1': time1, 'time2': time2, 'time3': time3, 'time4': time4, 'late': late, 'late2': late2, 'left1': left1,
    #     'left2': left2, 'dur': dur, 'tot': tot
    # }

    context = {'name': name, 'ID': ID, 'time_range': time_range, 'img1': img1, 'time1': time1, 'late': late}

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("pdf.html")
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
    pdf_filename = f'monitoring - {person_id} - {current_date} - {current_time}.pdf'
    pdfkit.from_string(output_text, pdf_filename, configuration=config)

    print(f"PDF generated: {pdf_filename}")


