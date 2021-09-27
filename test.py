import cv2
grey = cv2.imread("line.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("grey", grey)
cv2.imwrite("grey.jpg",grey)
cv2.waitKey(0)
edge_img = cv2.Canny(grey, 50, 100)
cv2.imshow("edge", edge_img)
cv2.imwrite("edge.jpg",edge_img)
cv2.waitKey(0)