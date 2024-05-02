#basicInterface.py

import cv2
import utils.camera as camera
import utils.img_2_txt as img_2_txt
import utils.records as records
import utils.sorter as sorter
import utils.card_db as card_db

def main():
    camera.calibration()
    # get image from camer
    image = camera.take_picture()
    # preview image
    cv2.imshow("Preview", image)
    # wait for key press to exit
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

    # read text from image
    #text = img_2_txt.read_text(image)
    
    # sort text
    #sorted_text = sorter.sort_text(text)

main()
