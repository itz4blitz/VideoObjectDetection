import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision

WindowCapture.list_window_names()

wincap = WindowCapture()

vision_crystal = Vision('crystal.png')

loop_time= time()
while(True):

    screenshot = wincap.get_screenshot()

    rectangles = vision_crystal.find(screenshot, 0.6)

    output_image = vision_crystal.draw_rectangles(screenshot, rectangles)

    cv.imshow('Matches', output_image)
    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')

