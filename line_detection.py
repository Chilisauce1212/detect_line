import cv2
import numpy as np


def Slope(line):
    if (line[0][0] == line[0][2]):
        return 0
    else:
        return (line[0][3] - line[0][1]) / (line[0][2] - line[0][0])


def filter(lines, threshold):
    slopes = [Slope(line) for line in lines]
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


def edge(path):
    grey = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    edge = cv2.Canny(grey, 192, 433)
    cv2.imwrite("edge.jpg", edge)
    return edge


def ROI(edge_img):
    zero = np.zeros_like(edge_img)
    mask = cv2.fillPoly(zero, np.array([[[0, 558], [0, 508], [500, 360], [600, 360], [1080, 558]]]), 255)
    ROI = cv2.bitwise_and(edge_img, mask)
    cv2.imwrite("ROI.jpg", ROI)
    return ROI


def hough(ROI_img):
    lines = cv2.HoughLinesP(ROI_img, 1, np.pi / 180, 30, 40)
    left_lines = [line for line in lines if Slope(line) < 0]
    right_lines = [line for line in lines if Slope(line) > 0]
    left_lines = filter(left_lines, 0.1)
    right_lines = filter(right_lines, 0.1)
    left_line = least_square(left_lines)
    right_line = least_square(right_lines)
    return left_line, right_line


def draw(path):
    raw = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
    edge_img = edge(path)
    ROI_img = ROI(edge_img)
    left_line, right_line = hough(ROI_img)
    cv2.line(raw, tuple(left_line[0]), tuple(left_line[1]), (255, 0, 0), 3)
    cv2.line(raw, tuple(right_line[0]), tuple(right_line[1]), (255, 0, 0), 3)
    cv2.imwrite("draw.jpg", raw)


if __name__ == "__main__":
    draw("line.jpg")
