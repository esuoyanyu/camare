import io
import os

from datetime import datetime

import PIL.Image
from v4l2py.device import Device, PixelFormat, VideoCapture

from detection import detect_human, detect_face

def cam_open():
    cam = Device.from_id(0)
    if cam == None:
        return None

    cam.open()
    capture = VideoCapture(cam)
    if capture == None:
        return None

    capture.set_format(640, 480, "jpeg")

    return cam, capture

def cam_close(cam, capture):
    capture.close()
    cam.close()

def get_picture(stream):

    return next(stream)

def save_picture(frame, path, name):
    if frame.pixel_format == PixelFormat.MJPEG:
        image = PIL.Image.open(io.BytesIO(frame.data))
        if image == None:
            return None

        if not os.path.exists(path):
            os.mkdir(path)

        picture = path + "/" + name + ".jpeg"

        image.save(picture, 'jpeg')

        return picture
    else:
        print("frame {} not support".format(frame.pixel_format))

        return None

def main():
    cam, capture = cam_open()
    if cam == None:
        print("open camera fail")
        return False

    stream = iter(cam)

    frame = get_picture(stream)

    path = datetime.now().strftime("%Y-%m-%d")
    name = datetime.now().strftime("%H_%M_%S")
    picture = save_picture(frame, path, name)
    if picture == None:
        return False

    ret = detect_human(picture)
    if ret == False:
        detect_face(picture)

    return True


if __name__ == "__main__":
    main()