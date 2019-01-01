import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('segment.jpg', 0)
row,col= image.shape
#calculating intensity values
temp=np.asarray([[0 for j in range(col)] for i in range(row)])
list1=[]
for i in range(row):
    for j in range(col):
        val=0
        val=image[i][j]
        list1.append(image[i][j])
list2=[]
for i in range(len(list1)):
    if(list1[i] not in list2):
        list2.append(list1[i])
intensity=np.asarray(list2)
intensity=np.sort(intensity)

#calculating frequency values for all intensities
temp2=np.asarray([[0 for j in range(1)] for i in range(len(intensity))])
for i in range(row):
    for j in range(col):
        for k in range(len(intensity)):
            if(intensity[k]==image[i][j]):
                temp2[k][0]+=1

plt.plot(intensity[1:],temp2[1:])
plt.show()
final=image
#applying optimal thresholding
for i in range(row):
    for j in range(col):
        if(final[i][j]>=205):
            final[i][j]=255
        else:
            final[i][j]=0
cv2.imwrite('segment_output.jpg',final)

#creating boundary boxes for output
temp=final
cv2.rectangle(temp,(159,120),(205,170),(255,255,255),1) 
cv2.rectangle(temp,(250,73),(305,208),(255,255,255),1) 
cv2.rectangle(temp,(333,22),(368,289),(255,255,255),1) 
cv2.rectangle(temp,(385,42),(425,254),(255,255,255),1) 

cv2.imwrite('segment_box_output.jpg',temp)
