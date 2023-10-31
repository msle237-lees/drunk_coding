import cv2
import numpy as np
from ultralytics import YOLO

class Camera_Package:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)

    def grab_image(self):
        pass

    def detect(self):
        pass

    def get_Depth_Cloud(self):
        pass

    def run(self):
        pass

if __name__ == "__main__":
    cp = Camera_Package()
    cp.run()