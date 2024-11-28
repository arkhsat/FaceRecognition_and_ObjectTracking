import pandas as pd
import os
from datetime import datetime


def csv_code(person_id, time_range, current_time, late_time, total_time_left, total_time_lecture):
    current_date = datetime.now().strftime("%Y-%m-%d")

    data = [
        {
            "Date": current_date,
            "ID": person_id,
            "Time_Range": time_range,
            "Time_first_in": current_time,
            "Late_Time": late_time,
            # "Time_left": time_left,
            "Left_Time": total_time_left,
            # "Time_return": time_return,
            "Total_Time": total_time_lecture,
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
