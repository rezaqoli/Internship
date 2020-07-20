from pypylon import pylon
import cv2
import numpy as np

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
for frame in grabber.grab():
    redChannel=frame[:,:,2]
    
    redChannel=cv2.blur(redChannel,(3,3))
    thresh=cv2.adaptiveThreshold(redChannel,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,13,11,None)
    #ret,thresh=cv2.threshold(redChannel,220,255,cv2.THRESH_BINARY)

    #sobelx64f = cv2.Sobel(redChannel,cv2.CV_64F,1,0,ksize=3)
    #abs_sobel64f = np.absolute(sobelx64f)
    #sobel_8u = np.uint8(abs_sobel64f)
    #sobely = cv2.Sobel(redChannel,cv2.CV_64F,0,1,ksize=5)
    #laplacian = cv2.Laplacian(redChannel,cv2.CV_64F)

    #edges = cv2.Canny(redChannel,80,255)
    #cv2.namedWindow('CANY', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
    #cv2.resizeWindow('CANY', 1080, 720)
    #cv2.imshow('CANY',edges)


    cv2.namedWindow('img', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow('img', 1080, 720)
    cv2.imshow('img',redChannel)

    cv2.namedWindow('mask', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow('mask', 1080, 720)
    cv2.imshow('mask',thresh)
    if cv2.waitKey(1)==ord('q'):
        break
grabber.stop()

