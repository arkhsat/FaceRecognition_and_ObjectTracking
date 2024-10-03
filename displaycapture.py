import urllib.request
import numpy as np
import cv2
import ssl
import requests
import certifi

# def display_image_from_url(image_url):
#     # Download and display the image from the URL
#     try:
#         req = urllib.request.urlopen(image_url)
#         arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#         img = cv2.imdecode(arr, -1)  # Decode image
#         cv2.imshow(f'Captured Image ({image_url})', img)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()  # Close the window after the display
#     except Exception as e:
#         print(f"Error displaying image from URL: {e}")


#THE REAL ONE ....
# def display_image_from_url(image_url):
#     try:
#         if image_url is None:
#             print("Error: Image URL is None.")
#             return
#
#         # Download the image from the URL using the trusted CA bundle
#         response = requests.get(image_url, verify=certifi.where())
#         response.raise_for_status()  # Check for HTTP errors
#
#         print(f"Response status code: {response.status_code}")
#         print(f"Content length: {len(response.content)}")
#
#         # Decode the image
#         image = np.asarray(bytearray(response.content), dtype="uint8")
#         image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#
#         if image is not None:
#             # Display the image in a window
#             cv2.imshow("Captured Image", image)
#             cv2.waitKey(3000)  #
#             cv2.destroyAllWindows()
#         else:
#             print("Error: Failed to decode the image.")
#     except requests.exceptions.RequestException as e:
#         print(f"Error downloading image: {e}")
#     except Exception as e:
#         print(f"Error displaying image from URL: {e}")


# USING MATPLOT
# import matplotlib.pyplot as plt
# import numpy as np
# import requests
# import certifi
#
# def display_image_from_url(image_url):
#     try:
#         if image_url is None:
#             print("Error: Image URL is None.")
#             return
#
#         # Download the image
#         response = requests.get(image_url, verify=certifi.where())
#         response.raise_for_status()
#
#         # Decode the image
#         image = np.asarray(bytearray(response.content), dtype="uint8")
#         image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#
#         if image is not None:
#             # Convert BGR to RGB
#             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
#             # Display using Matplotlib
#             plt.imshow(image_rgb)
#             plt.axis('off')  # Hide axis
#             plt.title("Captured Image")
#             plt.show()
#         else:
#             print("Error: Failed to decode the image.")
#     except Exception as e:
#         print(f"Error displaying image from URL: {e}")


# USING PILLOW
from PIL import Image
import requests
import io

def display_image_from_url(image_url):
    try:
        if image_url is None:
            print("Error: Image URL is None.")
            return

        # Download the image
        response = requests.get(image_url, verify=certifi.where())
        response.raise_for_status()

        # Open the image using PIL
        image = Image.open(io.BytesIO(response.content))

        # Display the image
        image.show()
    except Exception as e:
        print(f"Error displaying image from URL: {e}")




# def test_local_image():
#     image = cv2.imread('111_entered_2024-09-18_21-13-02.jpg')
#     if image is not None:c
#         cv2.imshow("Test Local Image", image)
#         cv2.waitKey(0)  # Wait indefinitely until a key is pressed
#         cv2.destroyAllWindows()
#     else:
#         print("Error: Failed to load local image.")
#
#     # success, img = image.read()
#     # cv2.imshow("Image", img)
#     # cv2.waitKey(0)
#
# test_local_image()