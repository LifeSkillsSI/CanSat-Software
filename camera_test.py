from components import ov5640
from cv2 import imwrite
import time
import sys

cam = ov5640.OV5640()

cam.prepare()

for i in range(2):
    result, image = cam.read()
    
    if result:
        imwrite("data/img"+str(i)+".jpg", image)
    else:
        print("No image detected.")
        sys.exit(1)  
    time.sleep(10)

cam.close()