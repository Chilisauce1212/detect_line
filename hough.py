import cv2
import numpy as np
import slope


def filter(lines, threshold):
    slopes = [slope.Slope(line) for line in lines]
    while len(lines) > 0:
        mean = np.mean(slopes)
        diff = [abs(s - mean) for s in slopes]
        idx = np.argmax(diff)
        if diff[idx] > threshold:
            slopes.pop(idx)
            lines.pop(idx)
        else:
            break
    return lines


def least_square(lines):
    x_cord = np.ravel([[line[0][0], line[0][2]] for line in lines])
    y_cord = np.ravel([[line[0][1], line[0][3]] for line in lines])
    poly = np.polyfit(x_cord, y_cord, deg=1)
    point_min = (np.min(x_cord), np.polyval(poly, np.min(x_cord)))
    point_max = (np.max(x_cord), np.polyval(poly, np.max(x_cord)))
    print("max point={}".format(point_max))
    return np.array([point_min, point_max], dtype=np.int32)


ROI = cv2.imread("ROI.jpg",cv2.IMREAD_ANYCOLOR)
raw = cv2.imread("line.jpg",cv2.IMREAD_ANYCOLOR)
draw = cv2.imread("line.jpg",cv2.IMREAD_ANYCOLOR)
lines = cv2.HoughLinesP(ROI, 1, np.pi / 180, 30, 40)

# cv2.imshow("draw", draw)
# cv2.waitKey(0)

for line in lines:
    start_pts = np.array([line[0][0], line[0][1]])
    end_pts = np.array([line[0][2], line[0][3]])
    cv2.line(draw, start_pts, end_pts, (255, 0, 0), 2)
    cv2.imshow("draw", draw)
    cv2.waitKey(1)
    cv2.imwrite("draw.jpg", draw)


left_lines = [line for line in lines if slope.Slope(line) < 0]
right_lines = [line for line in lines if slope.Slope(line) > 0]
print("before left_lines={}".format(len(left_lines)))
print("before right_lines={}".format(len(right_lines)))

left_lines = filter(left_lines, 0.1)
right_lines = filter(right_lines, 0.1)
# for line in left_lines:
#     start_pts = np.array([line[0][0], line[0][1]])
#     end_pts = np.array([line[0][2], line[0][3]])
#     cv2.line(draw, start_pts, end_pts, (255, 0, 0), 2)
#     cv2.imshow("draw2", draw)
#     cv2.waitKey(5)
print("after left_lines={}".format(left_lines[0]))
print("after right_lines={}".format(len(right_lines)))

left_line = least_square(left_lines)
right_line = least_square(right_lines)

cv2.line(raw, tuple(left_line[0]), tuple(left_line[1]), (255, 0, 0), 3)
cv2.line(raw, tuple(right_line[0]), tuple(right_line[1]), (255, 0, 0), 3)

cv2.imshow("final", raw)
cv2.waitKey(0)
