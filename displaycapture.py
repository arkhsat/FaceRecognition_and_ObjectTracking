import certifi
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