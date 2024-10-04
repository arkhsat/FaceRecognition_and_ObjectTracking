import urllib.request
import numpy as np
import cv2
import ssl
import requests
import certifi
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
