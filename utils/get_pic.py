import random
import tempfile
import numpy as np
import cv2


def get_pic(filename):
    cap = cv2.VideoCapture(filename)
    ret, frame = cap.read()
    cv2.imwrite(filename[:-4] + '.png', frame)
    cap.release()
    cv2.destroyAllWindows()