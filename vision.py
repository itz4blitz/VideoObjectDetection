import cv2 as cv
import numpy as np

class Vision:
    # constants
    TRACKBAR_WINDOW = "Trackbars"

    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

        #consutrctor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):

        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        self.method = method


    def find(self, haystack_img, threshold=0.6):

        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)


        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)


        return rectangles


    def get_click_points(self, rectangles):

        points = []

        for (x, y, w, h) in rectangles:
                
            center_x = x + int(w/2)
            center_y = y + int(h/2)

            points.append((center_x, center_y))
        return points

    def draw_rectangles(self, haystack_img, rectangles):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            #determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img

    def draw_crosshairs(self, haystack_img, points):
        # colors are BGR instead of RGB
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            #draw the center point
            cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img

    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        def nothing(position):
            pass


        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)