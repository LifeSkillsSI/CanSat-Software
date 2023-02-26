from cv2 import VideoCapture, CAP_V4L2
import os

class OV5640:
    def __init__(self):
        # TODO: currently using the 640x480 resolution, test if other settings work
        os.system('sudo media-ctl --device /dev/media1 --set-v4l2 \'"ov5640 2-003c":0[fmt:YUYV8_2X8/640x480]\'')
        self.cam = VideoCapture(1, CAP_V4L2)

    def __del__(self):
        self.close()

    def __exit__(self, type, value, tb):
        self.close()

    def __enter__(self):
        return self

    def close(self):
        self.cam.release()
    
    def is_opened(self):
        return self.cam.isOpened()
    
    def read(self):
        return self.cam.read()
    
    def prepare(self):
        # Takes 10 images to prepare the camera (fixing the brightness)
        for i in range(10):
            self.read()
