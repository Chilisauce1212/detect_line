import cv2


cv2.namedWindow("edge_detection")
cv2.createTrackbar("minThreshold", "edge_detection", 50, 1000, lambda x:x)
cv2.createTrackbar("maxThreshold", "edge_detection", 50, 1000, lambda x:x)


gray = cv2.imread("line.jpg", cv2.IMREAD_GRAYSCALE)
while True:
    minThreshold = cv2.getTrackbarPos("minThreshold", "edge_detection")
    maxThreshold = cv2.getTrackbarPos("maxThreshold", "edge_detection")
    edge = cv2.Canny(gray, minThreshold, maxThreshold)
    cv2.imshow("edge_detection", edge)
    cv2.waitKey(10)