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
    #redChannel=frame[:,:,2]
    #redChannel=cv2.blur(redChannel,(5,5))
    #thresh=cv2.adaptiveThreshold(redChannel,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,13,11,None)
    #ret,thresh=cv2.threshold(redChannel,220,255,cv2.THRESH_BINARY)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # Range for lower red
    lower_red = np.array([0,100,70])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # Range for upper range
    lower_red = np.array([170,100,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)

    #mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    #mask1 = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))


    #creating an inverted mask to segment out the cloth from the frame
    #mask2 = cv2.bitwise_not(mask1)


    #Segmenting the cloth out of the frame using bitwise and with the inverted mask
    mask2+=mask1

    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    res1 = cv2.bitwise_and(frame,frame,mask=mask2)


    cv2.namedWindow('img', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow('img', 1080, 720)
    cv2.imshow('img',mask2)

    cv2.namedWindow('mask', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow('mask', 1080, 720)
    cv2.imshow('mask',frame)
    if cv2.waitKey(1)==ord('q'):
        break
grabber.stop()

