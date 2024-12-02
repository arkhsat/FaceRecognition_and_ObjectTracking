import pandas as pd
import os
from datetime import datetime, timedelta


def csv_code(person_id, time_range, current_time, late_time, total_time_left, total_time_lecture):
    current_date = datetime.now().strftime("%Y-%m-%d")

    late_time_timedelta = timedelta(seconds=late_time)
    formatted_late_time = str(late_time_timedelta).split('.')[0]

    total_time_left_timedelta = timedelta(seconds=total_time_left)
    formatted_total_time_left = str(total_time_left_timedelta).split('.')[0]

    total_time_timedelta = timedelta(seconds=total_time_lecture)
    formatted_total_time = str(total_time_timedelta).split('.')[0]

    data = [
        {
            "Date": current_date,
            "ID": person_id,
            "Time_Range": time_range,
            "Time_first_in": current_time,
            "Late_Time": formatted_late_time,
            # "Time_left": time_left,
            "Left_Time": formatted_total_time_left,
            # "Time_return": time_return,
            "Total_Time": formatted_total_time,
        }
    ]

    file_name = "Monitoring_log.csv"

    # Periksa apakah file sudah ada
    if os.path.exists(file_name):
        # Append data ke file yang sudah ada
        df = pd.DataFrame(data)
        df.to_csv(file_name, mode="a", header=False, index=False)
        print(f"Data berhasil ditambahkan ke file {file_name}.")
    else:
        # Buat file baru dan tulis data
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False)
        print(f"File {file_name} berhasil dibuat dan data disimpan.")
