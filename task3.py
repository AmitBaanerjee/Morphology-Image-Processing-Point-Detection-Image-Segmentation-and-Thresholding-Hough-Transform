#Reference :- https://gist.github.com/rishabhsixfeet/45cb32dd5c1485e273ab81468e531f09

import cv2 as cv
import numpy as np
import math
image = cv.imread('hough.jpg',0)
coloredimg1= cv.imread('hough.jpg')
coloredimg2= cv.imread('hough.jpg')
circleimg=cv.imread('hough.jpg')

#performing sobel filter on input image
sobel_x = [[-1, 0, 1], [-2,0,2], [-1,0,1]]
sobel_y = [[-1, -2, -1], [0,0,0], [1,2,1]]
def sobel(image):    
    sobelx = np.asarray([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobely = np.asarray([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    l,b=image.shape

    sobelxImage = np.asarray([[0.0 for column in range(b)] for row in range(l)])
    sobelyImage = np.asarray([[0.0 for column in range(b)] for row in range(l)])
    sobelGrad = np.asarray([[0.0 for column in range(b)] for row in range(l)])
    for i in range(1, l-1):
        for j in range(1, b-1):  
            gradientx = (sobelx[0][0] * image[i-1][j-1]) + (sobelx[0][1] * image[i-1][j]) + (sobelx[0][2] * image[i-1][j+1])\
            + (sobelx[1][0] * image[i][j-1]) + (sobelx[1][1] * image[i][j]) + (sobelx[1][2] * image[i][j+1]) + \
            (sobelx[2][0] * image[i+1][j+1]) + (sobelx[2][1] * image[i+1][j]) + (sobelx[2][2] * image[i+1][j+1])    
        
            sobelxImage[i][j] = gradientx
            
            gradienty = (sobely[0][0] * image[i-1][j-1]) + (sobely[0][1] * image[i-1][j]) + \
                 (sobely[0][2] * image[i-1][j+1]) + (sobely[1][0] * image[i][j-1]) + \
                 (sobely[1][1] * image[i][j]) + (sobely[1][2] * image[i][j+1]) + \
                 (sobely[2][0] * image[i+1][j-1]) + (sobely[2][1] * image[i+1][j]) + \
                 (sobely[2][2] * image[i+1][j+1])   
        
            sobelyImage[i][j] = gradienty
            mag_gradient = math.sqrt((gradientx * gradientx) + (gradienty * gradienty))
            sobelGrad[i][j] = mag_gradient   
    for i in range(len(sobelxImage)):
        for j in range(len(sobelxImage[0])):
            if((sobelxImage[i][j])>100):
                sobelxImage[i][j]=255
            else:
                sobelxImage[i][j]=0
    for i in range(len(sobelyImage)):
        for j in range(len(sobelyImage[0])):
            if((sobelyImage[i][j])>110):
                sobelyImage[i][j]=255
            else:
                sobelyImage[i][j]=0
    return sobelxImage,sobelyImage

sobelop,sobelc=sobel(image)

#Calculate hough accumulator for line
def houghacc(image):
    l,b = image.shape
    diag = int(np.ceil(np.sqrt((l**2) + (b**2))))
    deg = np.deg2rad(np.arange(-90.0, 90.0))
    rho=np.arange(-diag,diag+1,1)
    cosdeg = np.cos(deg)
    sindeg = np.sin(deg)
    a = np.zeros((2 * diag, len(deg)), dtype=np.uint64)
    y_idx, x_idx = np.nonzero(image)
    for i in range(len(x_idx)):
        x = x_idx[i]
        y = y_idx[i]
        for t_idx in range(len(deg)):
            r = int(round(x * cosdeg[t_idx] + y * sindeg[t_idx]) + diag)
            a[r, t_idx] += 1     
    return a, deg, rho

#Calculate peak values of rho
def peaks(h, peakno):
    indices =  np.argpartition(h.flatten(), -2)[-peakno:]
    return np.vstack(np.unravel_index(indices, h.shape)).T

#Drawing lines on output image
def draw(img, points, rhos, thetas,type):
    if(type==1):
        vals=[]
        for i in range(len(points)):
            for j in range(1,2):
                if(points[i][j]>=88):
                    if(points[i][j]<89):
                        vals.append([points[i][0],points[i][j]])
        vals=np.asarray(vals)
        vals=vals[:15,:]
        
    if(type==2):
        val2=[]
        for i in range(len(points)):
            for j in range(1,2):
                if(53<points[i][j]<55):
                    if(points[i][0]>=700):
                        val2.append([points[i][0],points[i][j]])
        print(val2)
        vals=np.asarray(val2)
        vals=vals[:20,:]               
    for i in range(len(vals)):
        r = rhos[vals[i][0]]
        deg = thetas[vals[i][1]]
        a = np.cos(deg)
        b = np.sin(deg)
        x0 = a*r
        y0 = b*r
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        if(type==1):
            cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        else:
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)


a, deg, rhos = houghacc(sobelop)
peak = peaks(a,475)
draw(coloredimg1, peak,rhos, deg,1)
cv.imwrite("red_line.jpg",coloredimg1)

draw(coloredimg2, peak,rhos, deg,2)
cv.imwrite("blue_lines.jpg",coloredimg2)

'##################Hough Circle#########################'
#Function to perform hough transform for circle detection
def houghcircle(image,opimage):
    r = 20
    theta=np.linspace(0.0,360.0,360)
    deg=np.deg2rad(theta)
    l,b = image.shape
    diag = int(np.ceil(np.sqrt((l**2) + (b**2))))
    cost = np.cos(deg)
    sint = np.sin(deg)
    ac = np.zeros((diag, diag), dtype=np.uint64)
    y_idx, x_idx = np.nonzero(image)
    #Generating accumulator for circles
    for i in range(len(x_idx)):
        x = x_idx[i]
        y = y_idx[i]
        for val in range(len(deg)):
            a = int(round(x - r * cost[val]) )
            b = int(round(y - r * sint[val]) )
            ac[a, b] += 1
    pc=peaks(ac,130)
    #Drawing circles on output image
    for a in range(len(pc)):
        cv.circle(opimage,(pc[a][0],pc[a][1]),r,(0,255,255),1)
    return opimage
houghcircle(sobelc,circleimg)
cv.imwrite("coin.jpg",circleimg)
