import sys
from tkinter import *
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import imageMagic   

def csv_button_clicked():
    imageMagic.select_csv_file()
    file_label["text"] = imageMagic.csv_file

def cameras_button_clicked():
    imageMagic.list_available_cameras()

window = tk.Tk()
window.title("ImageMagic")

# create a gui with 3 columns
column_left = tk.Frame(window, width=50)
column_center = tk.Frame(window, width=600)
column_right = tk.Frame(window, width=100)

column_left.pack(side=tk.LEFT, padx=5, pady=5)
column_center.pack(side=tk.LEFT, padx=5, pady=5, expand=True)
column_right.pack(side=tk.RIGHT, padx=5, pady=5)

# left column: list of buttons
buttons_frame = tk.Frame(column_left)
buttons_frame.pack(side=tk.TOP, padx=5, pady=5)

# right column: list of stats
stats_frame = tk.Frame(column_right)
stats_frame.pack(side=tk.TOP, padx=5, pady=5)

# center column: image
image_label = tk.Label(column_center)
image_label.pack(side=tk.TOP, padx=5, pady=5, expand=True)

# populate buttons with sample data
button = tk.Button(buttons_frame, text="Select CSV file", command=csv_button_clicked)
button.pack(side=tk.TOP, padx=5, pady=2)

file_label = tk.Label(buttons_frame, text="")
file_label.pack(side=tk.TOP, padx=5, pady=2)
file_label["text"] = imageMagic.csv_file

button = tk.Button(buttons_frame, text="List available cameras", command=cameras_button_clicked)
button.pack(side=tk.TOP, padx=5, pady=2)

for i in range(3):
    button = tk.Button(buttons_frame, text=f"Button {i+3}")
    button.pack(side=tk.TOP, padx=5, pady=2)

# populate stats with sample data
for i in range(5):
    label = tk.Label(stats_frame, text=f"Stat {i+1}")
    label.pack(side=tk.TOP, padx=5, pady=2)

# display image
try:
    image = Image.open("/home/crazywonton/Pictures/test1.png")
    width, height = image.size
    aspect_ratio = height / width
    window_width = column_center.winfo_width()
    image_width = min(max(window_width, 300), 600)
    image_height = int(image_width * aspect_ratio)
    resize_image = image.resize((image_width, image_height))
    img = ImageTk.PhotoImage(resize_image)
    image_label = Label(image = img)
    image_label.image = img
    image_label.bind('<Configure>', lambda e: resize_image.thumbnail((e.width, int(e.width * aspect_ratio)), Image.ANTIALIAS))
    image_label.pack(fill=BOTH, expand=True)
except Exception as e:
    print(f"Error on line {sys.exc_info()[-1].tb_lineno}: {e}")

window.mainloop()

