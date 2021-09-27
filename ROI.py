import cv2
import numpy as np

raw = cv2.imread("line.jpg", cv2.IMREAD_ANYCOLOR)
grey = cv2.imread("grey.jpg", cv2.IMREAD_ANYCOLOR)


zero3 = np.zeros_like(raw)
mask3 = cv2.fillPoly(zero3, np.array([[[0,558],[0,508],[500,360],[700,360],[1080,400],[1080,558]]]), color=(255,255,255))
masked = cv2.addWeighted(mask3, 0.5, raw, 0.5, 0)


zero2 = np.zeros_like(grey)
mask2 = cv2.fillPoly(zero2, np.array([[[0,558],[0,508],[500,360],[700,360],[1080,400],[1080,558]]]), 255)
ROI = cv2.bitwise_and(grey, mask2)
ROI = cv2.Canny(ROI, 192, 433, )
cv2.imshow("ROI", ROI)
cv2.imwrite("ROI.jpg", ROI)
cv2.waitKey(0)