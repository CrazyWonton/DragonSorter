import cv2
import pytesseract
import tkinter.filedialog
from PIL import Image
import csv
import urllib.request
import json
import re

global cap
image_corners = []
csv_file = "/home/crazywonton/Downloads/search-export_2024-04-13.csv"

def list_available_cameras():
    """prints a list of available cameras and returns the user's selection"""
    index = 0
    cameras = []
    for index in range(5):
        # attempt to open the camera with this index and see if it works print(index)
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            continue
        else:
            #print(index)
            cameras.append(index)
        cap.release()
    
    print("Available cameras:")
    for i, cam in enumerate(cameras):
        print(f"{i}: {cam}")
    selection = input("Select a camera: ")
    try:
        selection = int(selection)
        return cameras[selection]
    except ValueError:
        print("Invalid input.")
    return list_available_cameras()

def calibrateCamera():
    # show camera video until user presses enter

    while True:          
        ret, img = cap.read()
        if ret == False:
            print("Error reading video stream.")
            input_char = input()
            if input_char == '\x1b': # exit on ESC
                break
        else:
            cv2.imshow("preview", img)
        input_char = input()
        if input_char == '\x1b': # exit on ESC
            break
        
        
    # capture image from webcam
    _, img = cap.read()

    # show the frame and allow user to click on the top left and bottom right corners of the area they want to crop the image to
    # save the coordinates of the corners in a list
    cv2.namedWindow("preview")
    cv2.setMouseCallback("preview", lambda event, x, y, flags, param: image_corners.append((x, y)) if event == cv2.EVENT_LBUTTONDOWN and len(image_corners) < 2 else None)

    while len(image_corners) < 2:
        cv2.imshow("preview", img)
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

    cv2.destroyWindow("preview")

def select_csv_file():
    """Pop up a file selection dialog and set csv_file to the selected filename"""
    global csv_file
    temp_csv_file = tkinter.filedialog.askopenfilename(filetypes = (("CSV files", "*.csv"), ("all files", "*.*")))
    if temp_csv_file:
        csv_file = temp_csv_file

def get_nth_column_name( n):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        if n < len(headers):
            return headers[n]
        else:
            return None  # or handle the case when n is out of range

def lookup_average_price(name):
    c_header = get_nth_column_name(2)
    g_header = get_nth_column_name(6)
    
    if c_header is None or g_header is None:
        return 0
    
    prices = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[c_header] == name:
                prices.append(float(row[g_header]))
    if prices:
        return sum(prices) / len(prices)
    else:
        return 0  # or handle the case when there are no matches

def take_and_crop_picture():
    """Takes a picture on the same webcam and crops it to the corners which were just set"""
    cv2.waitKey(2000)
    cap.read()
    _, img = cap.read()
    cropped_im = img[image_corners[0][1]:image_corners[1][1], image_corners[0][0]:image_corners[1][0]]
    return cropped_im

def image_to_text():
    try:
        cropped_im = take_and_crop_picture()
        if cropped_im is None:
            raise TypeError("Cropped image is None")
        # improve cropped image quality using greyscale
        cropped_im = cv2.cvtColor(cropped_im, cv2.COLOR_BGR2GRAY)
        if cropped_im is None:
            raise TypeError("Cropped grayscale image is None")
        # boost the contrast of the image
        enhancer = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cropped_im = enhancer.apply(cropped_im)
        # improve image quality for text recognition
        # apply a threshold to the image to make text more visible
        _, cropped_im = cv2.threshold(cropped_im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if cropped_im is None:
            raise TypeError("Cropped OTSU threshold image is None")
        # Perform OCR using PyTesseract
        text = pytesseract.image_to_string(cropped_im)
        if text is None:
            raise TypeError("OCR text is None")
        # trim leading and trailing whitesapce from text
        text = text.strip()
        
        # remove all non-alphanumeric characters from text
        
        text = re.sub(r'\W+', '_', text)
        
        # Print the extracted text and average price
        print(text + " : $" + str(lookup_average_price2(text)))
    except Exception as e:
        print("Error in image_to_text:")
        print(e)


def lookup_average_price2(name):
    url = "https://api.scryfall.com/cards/named?fuzzy=" + urllib.parse.quote(name)
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        prices = []
        for price in data["prices"]:
            prices.append(float(price["usd"]))
        if prices:
            return sum(prices) / len(prices)
        else:
            return 0
    except Exception as e:
        print("Error with URL: " + url)
        print(e)
        return 0


#test
#select_csv_file()
# cap = cv2.VideoCapture(list_available_cameras())
# cap = cv2.VideoCapture()
# cap.set(38, 1)
# calibrateCamera()
# while True:
#     image_to_text()
#     input_char = input()
#     if input_char == '\x1b': # exit on ESC
#         break

