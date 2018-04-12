import numpy as np
import cv2

#read a test image 1
img = cv2.imread('output_image_test.jpg')

#set an appropriate range of threshold so that red portion will be displayed
hsv_low = [0,0,150]
hsv_high = [100,100,255]



#define a function
def red_threshold(img, hsv_low, hsv_high):
#take lower values in "lower"
    lower = np.array(hsv_low)

#take upper values in "upper"    
    upper = np.array(hsv_high)

#code to take pixels which lie in range
#red pixels which lie in range 150 to 255 are converted to '255' and displayed.Rest are converted to '0'
    mask = cv2.inRange(img, lower, upper)

#to display red part in red color do bitwise and image with red part is stored in matrix res    
    res = cv2.bitwise_and(img, img, mask= mask)
    
#image is returned    
    return(res)

#function is called which do the processing written in above function
res = red_threshold(img, hsv_low, hsv_high)


#normal image is displayed
cv2.imshow('img',img)

#image with red part is displayed
cv2.imshow('res',res)

cv2.waitKey(0)
cv2.destroyAllWindows()

    
