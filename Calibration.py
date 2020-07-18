from pypylon import pylon
import cv2
import numpy as np
from camera import camera_grabber


grabber=camera_grabber()

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
            # Draw and display the corners
            img2 = cv2.drawChessboardCorners(i, (6,9), corners2,ret)
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
            print(mtx)
            print(dist)
            #print(rvecs)
            #print(tvecs)

        else:
            img2=i
        # if image's number reach to 10 save to file
        if len(objpoints)%2==0:
            np.savez('matrix',mtx1=np.array(mtx),dist1=np.array(dist),tvecs1=np.array(tvecs), rvecs1 = np.array(rvecs))  
        cv2.namedWindow('img', cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('img', 1080, 720)
        cv2.imshow('img',img2)
        
    #    print(ret,corners)
    
    #print(ret,mtx,dist,rvecs,tvecs)
def calibration():
    for i in grabber.grab():
            gray=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
            cv2.namedWindow('Gray', cv2.WINDOW_NORMAL)
            cv2.imshow('Gray', gray)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break
            cv2.setMouseCallback('Gray',save_image)
        
    grabber.stop()

def undistorted(img, file="matrxi.npz"):
    data_arrays = np.load(file)
    mtx = data_arrays['mtx1']
    dist = data_arrays['dist1']
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    
    return dst

