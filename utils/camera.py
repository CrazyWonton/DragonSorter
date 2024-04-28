#camera.py

import cv2

selected_points = []

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
    selected_camera = select_camera(cameras)
    print(f"Selected camera: {selected_camera}")

# Manual camera focus
def manual_focus(camera_index):
    # Open camera with camera_index, show camera preview, and allow user to adjust focus
    cap = cv2.VideoCapture(camera_index)
    cv2.namedWindow("Adjust Focus", cv2.WINDOW_NORMAL)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Adjust Focus", frame)
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
    selected_camera = select_camera(cameras)
    manual_focus(selected_camera)

# Take picture using selected camera and return image
def take_picture(camera_index):
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    cap.release()
    return frame

# Test take_picture
def test_take_picture():
    cameras = list_available_cameras()
    selected_camera = select_camera(cameras)
    image = take_picture(selected_camera)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# event handler for selecting text boundaries
def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_points.append((x, y))

# Test on_mouse
def test_on_mouse():
    selected_points = []
    on_mouse(cv2.EVENT_LBUTTONDOWN, 10, 20, 0, None)
    assert selected_points == [(10, 20)]

# Todo this code does not work. It pops up the preview but does not do anything with clicks
# Select text boundaries within frame
def select_text_boundaries(frame):
    # Show frame with mouse click handler
    cv2.namedWindow("Adjust Text Boundaries", cv2.WINDOW_NORMAL)
    cv2.imshow("Adjust Text Boundaries", frame)
    cv2.setMouseCallback("Adjust Text Boundaries", on_mouse)
    selected_points = []
    # Allow user to click on a point in the image and add to selected_points
    while len(selected_points) < 2:
        k = cv2.waitKey(1) & 0xFF
        if k == ord("q"):
            break
    cv2.destroyAllWindows()
    return selected_points

# Test select_text_boundaries
def test_select_text_boundaries():
    cameras = list_available_cameras()
    selected_camera = select_camera(cameras)
    selected_points = select_text_boundaries(take_picture(selected_camera))
    print(f"Selected points: {selected_points}")

# Run sample calibration test to approve calibration



# Take picture using selected camera and return image within selected text boundaries

#test_list_available_cameras()
#test_select_camera()
#test_manual_focus()
#test_take_picture()
test_select_text_boundaries()
