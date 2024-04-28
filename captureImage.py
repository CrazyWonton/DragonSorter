import cv2
import pytesseract

cv2.namedWindow("preview")
vc = cv2.VideoCapture()

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

# show the frame and allow user to click on the top left, top right, bottom left, and bottom right corners of the area they want to crop the image to
# save the coordinates of the corners in a list
cv2.setMouseCallback("preview", on_mouse)
image_corners = []
while len(image_corners) < 4:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")

    # calculate the coordinates of each corner relative to the image
height, width, channels = frame.shape
image_corners = [(int(x / width * frame.shape[1]), int(y / height * frame.shape[0])) for x, y in corners]

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        corners.append((x, y))

#crop the image to the area that the user clicked and show the cropped image in a new window
    cropped_im = frame[image_corners[0][1]:image_corners[1][1], image_corners[0][0]:image_corners[2][0]]
    cv2.namedWindow("cropped")
    cv2.imshow("cropped", cropped_im)
    cv2.waitKey(0)
    cv2.destroyWindow("cropped")

# explain what this does
    # capture video frames from camera #0 and display them in a window named "preview"
    # if you press ESC, exit the program
    # frame is a numpy array, so you can do whatever you want with it
    # rval is a boolean that indicates if the frame was read successfully
# while rval:
#     cv2.imshow("preview", frame)
#     #wait for user to press a key to continue or ESC to exit the program
#     key = cv2.waitKey(20)

#     if key == 27: # exit on ESC
#         break

#     # crop the image to the area that the user clicked
#     cropped_im = frame[image_corners[0][1]:image_corners[1][1], image_corners[0][0]:image_corners[2][0]]
#     #show the cropped image
#     cv2.imshow("cropped", cropped_im)

#     rval, frame = vc.read()
#     #key = cv2.waitKey(20)
    
#     # improve image quality using greyscale
#     cropped_im = cropped_im.convert('L')
#     # improve image quality for text recognition
#     cropped_im = cropped_im.point(lambda x: 0 if x<128 else 255, '1')
#     text = pytesseract.image_to_string(cropped_im)
#     # trim leading and trailing whitesapce from text
#     text = text.strip()
#     # Print the extracted text
#     #if text is not empty print the text
#     if text:
#         print(text)

#     if key == 27: # exit on ESC
#         break


# vc.release()
# cv2.destroyWindow("preview")
