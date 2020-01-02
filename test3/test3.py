
import cv2
import numpy as np,sys

A = cv2.imread('E:/QQ/test3/images1/left1.jpg')
B = cv2.imread('E:/QQ/test3/images1/right1.jpg')
# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in range(6):
    G = cv2.pyrDown(G)
    gpA.append(G)
G = B.copy()
gpB = [G]
for i in range(6):
    G = cv2.pyrDown(G)
    gpB.append(G)
lpA = [gpA[5]]
for i in range(6,0,-1):
    GE = cv2.pyrUp(gpA[i])
    GE=cv2.resize(GE,gpA[i - 1].shape[-2::-1])
    L = cv2.subtract(gpA[i-1],GE)
    lpA.append(L)
# generate Laplacian Pyramid for B
lpB = [gpB[5]]
for i in range(6,0,-1):
    GE = cv2.pyrUp(gpB[i])
    GE = cv2.resize(GE, gpB[i - 1].shape[-2::-1])
    L = cv2.subtract(gpB[i-1],GE)
    lpB.append(L)
# Now add left and right halves of images in each level
LS = []
lpAc=[]
for i in range(len(lpA)):
    b=cv2.resize(lpA[i],lpB[i].shape[-2::-1])
    lpAc.append(b)
for i in zip(lpAc,lpB):
    la,lb=i
    rows,cols,dpt = la.shape
    ls = np.hstack((la[:,0:cols//2], lb[:,cols//2:]))
    LS.append(ls)
ls_ = LS[0]
for i in range(1,6):
    ls_ = cv2.pyrUp(ls_)
    ls_= cv2.resize(ls_, LS[i].shape[-2::-1])
    ls_ = cv2.add(ls_, LS[i])
# image with direct connecting each half
B= cv2.resize(B, A.shape[-2::-1])
real = np.hstack((A[:,:cols//2],B[:,cols//2:]))
cv2.imwrite('E:/QQ/test3/images1/Pyramid_blending6.jpg',ls_)
cv2.imwrite('E:/QQ/test3/images1/Direct_blending6.jpg',real)


