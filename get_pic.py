import random
import tempfile
import numpy as np
import cv2


def get_pic(filename):
    cap = cv2.VideoCapture(filename)
    ret, frame = cap.read(image=cap.get(cv2.CAP_PROP_POS_MSEC) // 2)
    t = tempfile.TemporaryFile()
    name = t.name
    cv2.imwrite(name, frame)
    cap.release()
    cv2.destroyAllWindows()
    return name
