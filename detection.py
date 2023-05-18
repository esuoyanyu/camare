import os

import sys
import cv2

from datetime import datetime

class log():
    def __init__(self, path, name):
        if not os.path.exists(path):
            os.mkdir(path)

        log = path + "/" + name
        self.fd = open(log, 'a')
        if self.fd == None:
            print("open {} file fail".format(log))

    def write(self, data):
        self.fd.write(data)

loger = log("log", "detect.log")

def detect_human(picture):
    img = cv2.imread(picture)
    if img.any() == False:
        print("open file fail")
        return False

    hog = cv2.HOGDescriptor()
    if hog == None:
        return False

    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    found, _ = hog.detectMultiScale(img)

    if len(found) > 0:
        file = os.path.basename(picture)
        date = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
        loger.write("date: {} {} detect human, number: {}\n".format(date, file, len(found)))
    else:
        return False

    return True

def detect_face(picture):
    img = cv2.imread(picture)
    if img.any() == False:
        print("open file fail")
        return False

    cascade = cv2.CascadeClassifier(r'opencv/data/haarcascades/haarcascade_frontalface_default.xml')
    faces = cascade.detectMultiScale(img, scaleFactor = 1.1, minNeighbors = 5, minSize = (30, 30),
                             flags = cv2.CASCADE_SCALE_IMAGE)
    if len(faces) > 0:
        file = os.path.basename(picture)
        date = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
        loger.write("date: {} {} detect face, number: {}\n".format(date, file, len(faces)))
    else:
        return False

    return True


if __name__ == "__main__":
    if len(sys.argv) == 2:
        detect_human(sys.argv[1])
    else:
        print("argv is illegal")
