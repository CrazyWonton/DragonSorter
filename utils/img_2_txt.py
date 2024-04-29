#img_2_txt.py

import cv2
import pytesseract

# Process image for text recognition
def process_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    enhancer = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    image = enhancer.apply(image)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return image

# Test process_image
def test_process_image():
    image = cv2.imread("../resources/text_recognition.jpg")
    processed_image = process_image(image)
    cv2.imshow("Processed Image", processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Read text from image
def read_text(image):
    text = pytesseract.image_to_string(image)
    return text

# Test read_text
def test_read_text():
    image = cv2.imread("../resources/text_recognition.jpg")
    text = read_text(image)
    print(text)

#test_process_image()
#test_read_text()
