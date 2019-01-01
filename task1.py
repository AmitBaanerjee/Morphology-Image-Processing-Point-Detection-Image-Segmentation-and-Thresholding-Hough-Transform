import cv2
import numpy as np

image = cv2.imread('noise.jpg',0)
#structuring element

element = np.asarray([[255, 255, 255], [255, 255, 255], [255, 255, 255]])
#function to perform dilation            
def dilation(image):
    l,b=image.shape
    temp = np.asarray([[0.0 for column in range(b)] for row in range(l)])
    for i in range(1,l-1):
        for j in range(1,b-1):
            val=max(image[i-1][j-1]*element[0][0],image[i-1][j]*element[0][1],image[i-1][j+1]*element[0][2],image[i][j-1]*element[1][0],image[i][j]*element[1][1],image[i][j+1]*element[1][2],image[i+1][j-1]*element[2][0],image[i+1][j]*element[2][1],image[i+1][j+1]*element[2][2])
            temp[i][j]=val
    return temp

#function to perform erosion
def erosion(image):
    l,b=image.shape
    temp2 = np.asarray([[0.0 for column in range(b)] for row in range(l)])
    for i in range(1,l-1):
        for j in range(1,b-1):
            val=min(image[i-1][j-1]*element[0][0],image[i-1][j]*element[0][1],image[i-1][j+1]*element[0][2],image[i][j-1]*element[1][0],image[i][j]*element[1][1],image[i][j+1]*element[1][2],image[i+1][j-1]*element[2][0],image[i+1][j]*element[2][1],image[i+1][j+1]*element[2][2])
            temp2[i][j]=val
    return temp2

#function to perform opening on input image
def opening(image):
    op1=erosion(image)
    op2=dilation(op1)
    #denoising by doing closing operation
    op3=dilation(op2)
    op4=erosion(op3)
    return op4

oimage=opening(image)
cv2.imwrite('res_noise1.jpg',oimage)

#function to perform closing on input image
def closing(image):
    op1=dilation(image)
    op2=erosion(op1)
    #Denoising by doing opening operation  
    op3=erosion(op2)
    op4=dilation(op3)
    return op4

cimage=closing(image)
cv2.imwrite('res_noise2.jpg',cimage)

#boundary of opened image
b1=erosion(oimage)
bound1=oimage-b1
cv2.imwrite('res_bound1.jpg',bound1)
#boundary of closed image
b2=erosion(cimage)
bound2=cimage-b2
cv2.imwrite('res_bound2.jpg',bound2)