import sqlite3
import cv2
import numpy as np

def read_image_from_db(image_id, db_name="image_from_cap.db"):
    # Membuka koneksi ke database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Mengambil gambar dari database
    cursor.execute("SELECT img_path FROM image WHERE id=?", (image_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        print("Image not found!")
        return None

    # Mengonversi BLOB ke array NumPy
    blob_data = result[0]
    image_array = np.frombuffer(blob_data, dtype=np.uint8)

    # Decode array menjadi gambar
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

# Tampilkan gambar
image = read_image_from_db(1)
if image is not None:
    cv2.imshow("Image from SQLite", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
