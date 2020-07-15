from pypylon import pylon
import cv2
import numpy as np


# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:6,0:9].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

def save_image(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDBLCLK:
        ret, corners = cv2.findChessboardCorners(gray, (6,9),None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
            print(ret,corners)
            # Draw and display the corners
            img2 = cv2.drawChessboardCorners(img, (6,9), corners2,ret)
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        else:
            img2=img
        cv2.namedWindow('img', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('img', 1080, 720)
        cv2.imshow('img',img2)
        
    #    print(ret,corners)
    
    #print(ret,mtx,dist,rvecs,tvecs)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('Gray', cv2.WINDOW_NORMAL)
        cv2.imshow('Gray', gray)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        cv2.setMouseCallback('Gray',save_image)
    grabResult.Release()
    
# Releasing the resource    
camera.StopGrabbing()

cv2.destroyAllWindows()


