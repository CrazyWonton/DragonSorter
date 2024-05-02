#camera.py

import cv2

image_corners = []
camera_index = 0

# List available cameras
def list_available_cameras():
    index = 0
    cameras = []
    for index in range(5):
        # attempt to open the camera with this index and see if it works print(index)
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            continue
        else:
            cameras.append(index)
        cap.release()
    return cameras
        
# Test list of available cameras
def test_list_available_cameras():
    cameras = list_available_cameras()
    print("Available cameras:")
    for i, cam in enumerate(cameras):
        print(f"{i}: {cam}")

# Select camera from available camera list
def select_camera(camera_list):
    """Select camera from available camera list"""
    print("Select camera from list:")
    for i, cam in enumerate(camera_list):
        print(f"{i}: {cam}")
    try:
        global camera_index
        camera_index = int(input("Enter camera index: "))
    except ValueError:
        print("Invalid input, please enter an integer")
        return select_camera(camera_list)
    if camera_index not in range(len(camera_list)):
        print("Invalid camera index, please select from available cameras")
        return select_camera(camera_list)
    return camera_list[camera_index]

# Test select_camera
def test_select_camera():
    cameras = list_available_cameras()
    select_camera(cameras)
    print(f"Selected camera: {camera_index}")

# Manual camera focus
def manual_focus():
    # Open camera with camera_index, show camera preview, and allow user to adjust focus
    cap = cv2.VideoCapture(camera_index)
    cv2.namedWindow("Adjust Focus", cv2.WINDOW_NORMAL)
    print("Adjust focus by pressing '+' or '-'. Press 'q' to exit.")
    while True:
        ret, frame = cap.read()
        cv2.imshow("Adjust Focus", frame)
        # Print a message to the user telling them to adjust focus
        k = cv2.waitKey(1) & 0xFF
        if k == ord("q"):
            break
        elif k == ord("-"):
            cap.set(10, cap.get(10)-1)
        elif k == ord("+"):
            cap.set(10, cap.get(10)+1)
    cap.release()
    cv2.destroyAllWindows()

# Test manual_focus
def test_manual_focus():
    cameras = list_available_cameras()
    select_camera(cameras)
    manual_focus()

# Take picture using selected camera and return image
def take_picture():
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    cap.release()
    return frame

# Test take_picture
def test_take_picture():
    cameras = list_available_cameras()
    select_camera(cameras)
    image = take_picture()
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Select text boundaries within frame
def select_text_boundaries(frame):
    cv2.namedWindow("preview")
    cv2.setMouseCallback("preview", lambda event, x, y, flags, param: image_corners.append((x, y)) if event == cv2.EVENT_LBUTTONDOWN and len(image_corners) < 2 else None)
    print("Please select top left and bottom right corners of text in the image to crop to. Press ESC to exit.")
    while len(image_corners) < 2:
        cv2.imshow("preview", frame)
        key = cv2.waitKey(20)
        # Print a message to the user telling them to select text boundaries
        if key == 27: # exit on ESC
            break
    cv2.destroyWindow("preview")

# Test select_text_boundaries
def test_select_text_boundaries():
    cameras = list_available_cameras()
    select_camera(cameras)
    select_text_boundaries(take_picture())
    print(f"Selected points: {image_corners}")

# Run sample calibration test to approve calibration
def calibration():
    cameras = list_available_cameras()
    select_camera(cameras)
    manual_focus()
    image = take_picture()
    select_text_boundaries(image)
    #show image cropped to selected points
    cropped_image = image[image_corners[0][1]:image_corners[1][1], image_corners[0][0]:image_corners[1][0]]
    cv2.imshow("Cropped Image", cropped_image)
    # if user approves calibration return, else rerun
    # Print a message to the user telling them to approve calibration
    print("Calibration complete. If this is correct, press 'y' to return, else rerun calibration.")
    if cv2.waitKey(0) == ord('y'):
        return
    else:
        calibration()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Take picture using selected camera and return image within selected text boundaries
def take_picture_cropped():
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    cap.release()
    cropped_frame = frame[image_corners[0][1]:image_corners[1][1], image_corners[0][0]:image_corners[1][0]]
    return cropped_frame

def test_take_picture_cropped():
    calibration()
    image = take_picture_cropped()
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#test_list_available_cameras()
#test_select_camera()
#test_manual_focus()
#test_take_picture()
#test_select_text_boundaries()
#calibration()
