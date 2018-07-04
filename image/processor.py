import logging
import cv2
from collections import deque

green_lower = (29, 86, 6)
green_upper = (64, 255, 255)

class Processor(object):
    """
    Defines a class to apply additional processing to the image
    returned by the callback
    """

    def __init__(self):
        """
        Constructor
        """

        self.width = 320
        self.height = 240
        self.pts = deque(maxlen = 10)

    def cleanup(self):
        pass

    def image_process_entry(self, bgr_image, width, height):
        """
        Called each time an image can be processed
        """
        # Blur the image
        #MED_FILTER_APRTRE_SIZE = 5  # Must be odd number
        #bgr_blur_image = cv2.medianBlur(bgr_image, MED_FILTER_APRTRE_SIZE)

        # Convert the image from 'BGR' to HSV colour space
        #hsv_image = cv2.cvtColor(bgr_blur_image, cv2.COLOR_BGR2HSV)

        blurred = cv2.GaussianBlur(bgr_image, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, green_lower, green_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(bgr_image, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(bgr_image, center, 5, (0, 0, 255), -1)

        self.pts.appendleft(center)

        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(bgr_image, pts[i - 1], pts[i], (0, 0, 255), thickness)

        cv2.imshow('Frame', bgr_image)

        # Capture a key press. The function waits argument in ms
        # for any keyboard event
        # For some reason image does not show without this!
        cv2.waitKey(1) & 0xFF
