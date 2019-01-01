# Q2.a
import cv2
import numpy as np

image=cv2.imread('turbine-blade.jpg',0)

#laplacian kernel
kernel=[[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]

row,col=image.shape

temp = np.asarray([[0 for j in range(col)] for i in range(row)])
val=[]

#Convoluting image with kernel
for i in range(1,row-1):
    for j in range(1,col-1):
        r = (kernel[0][0] * image[i-1][j-1]) + (kernel[0][1] * image[i-1][j]) + (kernel[0][2] * image[i-1][j+1])\
        + (kernel[1][0] * image[i][j-1]) + (kernel[1][1] * image[i][j]) + (kernel[1][2] * image[i][j+1]) + \
        (kernel[2][0] * image[i+1][j-1]) + (kernel[2][1] * image[i+1][j]) + (kernel[2][2] * image[i+1][j+1])
        temp[i][j]=abs(r)
        val.append(r)
maxval=max(val)
threshold=0.9*maxval
final=temp-threshold
cv2.imwrite('point_output.jpg',final)

#Finding Coordinates of porosity 
ci=0
cj=0
maxval2=0
for i in range(len(final)-1):
    for j in range(len(final[0])-1):
        if(final[i][j]>maxval2):
            maxval2=image[i][j]
            ci=i
            cj=j
print("Coordinates of point are (%s , %s) ",ci,cj)

