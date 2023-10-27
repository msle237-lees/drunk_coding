import cv2

class CP:
    """
    ## CP Class
    Responsible for capturing video frames from a camera using OpenCV.
    """

    def __init__(self):
        """
        ### __init__ method
        Initializes the CP class by setting camera properties.
        """
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.cam_send_width = int(1280 / 4)  # convert to int to avoid float
        self.cam_send_height = int(720 / 4)  # convert to int to avoid float

    def get_frame(self):
        """
        ### get_frame method
        Captures a frame from the camera and resizes it.

        **Returns:**
        - Resized frame or None if capture failed.
        """
        ret, frame = self.cam.read()
        if ret:
            frame = self.resize_image(frame, width=self.cam_send_width, height=self.cam_send_height)
            return frame
        else:
            return None

    def run(self):
        """
        ### run method
        Runs the camera capturing loop and displays the frames.
        """
        while True:
            frame = self.get_frame()
            if frame is not None:
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    def __del__(self):
        """
        ### __del__ method
        Releases the camera when the object is deleted.
        """
        self.cam.release()

    @staticmethod
    def resize_image(image, width=None, height=None, inter=cv2.INTER_AREA):
        """
        ### resize_image static method
        Resizes an image to given dimensions.

        **Arguments:**
        - `image`: Image to resize.
        - `width (optional)`: Desired width.
        - `height (optional)`: Desired height.
        - `inter`: Interpolation method.

        **Returns:**
        - Resized image.
        """
        dim = None
        (h, w) = image.shape[:2]
        
        if width is None and height is None:
            return image
        
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)

if __name__ == "__main__":
    cp = CP()
    cp.run()
