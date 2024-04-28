import pytesseract
import csv
from PIL import Image

# Go here to get excel sheet https://sellyourcards.starcitygames.com/mtg
csv_file = '/home/crazywonton/Downloads/search-export_2024-03-23.csv'


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


# Open the image file
# image = Image.open('/home/crazywonton/Pictures/test2.jpg')

# Perform OCR using PyTesseract
#text = pytesseract.image_to_string(image)

# Print the extracted text
#print(text)

# Test 2, cropping an image and grabbing text
image = Image.open('/home/crazywonton/Pictures/test1.jpg')
width, height = image.size
crop_rectangle = (0+55, 0+45, width-120, 90)
cropped_im = image.crop(crop_rectangle)

# improve image quality using greyscale
cropped_im = cropped_im.convert('L')
# improve image quality for text recognition
cropped_im = cropped_im.point(lambda x: 0 if x<128 else 255, '1')
#cropped_im.show()

# Perform OCR using PyTesseract
text = pytesseract.image_to_string(cropped_im)
# trim leading and trailing whitesapce from text
text = text.strip()

# Print the extracted text
print(text)

print(lookup_average_price(text))