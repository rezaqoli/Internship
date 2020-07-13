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
x=int(1080*1.3)
y=int(720*1.3)

def save_image(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDBLCLK:
        cv2.imwrite('binarized_image.png',opening2)
        height,width= opening2.shape[:2]
        print('height:' + str(height)+'\t'+'width:'+str(width)+'\n' )
        #cv2.imwrite('binarized_image.png',cv2.bitwise_and(gray,gray,mask=cv2.bitwise_not(opening2)))

        sure_bg = cv2.dilate(opening2,kernel,iterations=3)
        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening2,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)


        # Marker labelling
        ret, markers = cv2.connectedComponents(opening2)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers+1

        # Now, mark the region of unknown with zero
        markers[unknown==255] = 0
        markers = cv2.watershed(img,markers)
        img[markers == -1] = [255,0,0]
        cv2.imwrite('picture.png',img)
        print(ret)
        

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        #cv2.namedWindow('title', cv2.WINDOW_NORMAL| cv2.WINDOW_GUI_NORMAL)
        #cv2.resizeWindow('title', 1080, 720)
        #cv2.imshow('title', img)

        #GrayScale Image
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        median = cv2.medianBlur(gray,5)
        cv2.namedWindow('gray',cv2.WINDOW_NORMAL| cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('gray', 1080, 720)
        cv2.imshow('gray',gray)

        #THRESHOLD
        th2 = cv2.adaptiveThreshold(median,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY_INV,201,4)
        #th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #    cv2.THRESH_BINARY_INV,201,5)
        cv2.namedWindow('MEAN', cv2.WINDOW_NORMAL| cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('MEAN', 1080, 720)
        cv2.imshow('MEAN', th2)    
        #cv2.namedWindow('GAUS', cv2.WINDOW_NORMAL| cv2.WINDOW_GUI_NORMAL)
        #cv2.resizeWindow('GAUS', 1080, 720)
        #cv2.imshow('GAUS', th3)

        #MORPHOLOGY
        kernel=np.ones((4,4),np.uint8)
        #opening = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel)
        opening2 = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)
        cv2.namedWindow('MEAN_MOTPH', cv2.WINDOW_NORMAL| cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('MEAN_MOTPH', x, y)
        cv2.imshow('MEAN_MOTPH', opening2)    
        #cv2.namedWindow('GAUS_MORPH', cv2.WINDOW_NORMAL| cv2.WINDOW_GUI_NORMAL)
        #cv2.resizeWindow('GAUS_MORPH', 1080, 720)
        #cv2.imshow('GAUS_MORPH', opening)

   
        #MOUSE EVENT
        cv2.setMouseCallback('MEAN_MOTPH',save_image)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break
    grabResult.Release()
    
# Releasing the resource    
camera.StopGrabbing()

cv2.destroyAllWindows()