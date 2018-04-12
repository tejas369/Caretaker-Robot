
############################################
## Import OpenCV
import numpy
import cv2

##define function
def draw_grid(filename,m,n):
    
    
    for i in range(0,n):
        #define coordinate for vertical line
        x1 = i*w/(n-1)
        #draw vertical line
        cv2.line(filename,(x1,0),(x1,480),(0,0,255),1)

    for j in range(0,m):
        #define coordinate for horizontal line
        y1 = j*h/(m-1)
        #draw horizontal line
        cv2.line(filename,(0,y1),(540,y1),(0,0,255),1)
        #storing modified image in "img" matrix
    img = filename
    #return image with grids    
    return(img)

#reading the image
filename = cv2.imread('output_image_test.jpg')

h,w,c = filename.shape
#enter number of lines
m = 23
n = 26
res = draw_grid(filename,m,n)
cv2.imshow('image',res)
cv2.imwrite("output_image_test2.jpg", res)

## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()


