from pypylon import pylon
import cv2

class camera_grabber():
    def __init__(self):
        
        # conecting to the first available camera
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Grabing Continusely (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        self.converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    def grab(self):

        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Access the image data
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                yield img
            grabResult.Release()
    def stop(self):
        # Releasing the resource    
        self.camera.StopGrabbing()
        cv2.destroyAllWindows()

grabber=camera_grabber()
for i in grabber.grab():
    cv2.namedWindow('img', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow('img', 1080, 720)
    cv2.imshow('img',i[:,:,2])
    if cv2.waitKey(1)==ord('q'):
        break
grabber.stop()

