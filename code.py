import cv2
import numpy as np

prev_left_fit_average = None
prev_right_fit_average = None


def canny(image):
    blue = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(blue, (5, 5), 0)
    return cv2.Canny(blur, 50, 150)


def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    return cv2.bitwise_and(image, mask)

def make_coordinates(image, line_parameters):
    if line_parameters is None or len(line_parameters) != 2:
        return None

    slope, intercept = line_parameters
    if slope == 0:
        return None

    y1 = image.shape[0]
    y2 = int(y1 * 0.6)

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    global prev_left_fit_average, prev_right_fit_average

    left_fit = []
    right_fit = []

    if lines is None:
        return None

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)

        if x1 == x2:
            continue

        slope, intercept = np.polyfit((x1, x2), (y1, y2), 1)

        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_avg = np.average(left_fit, axis=0) if len(left_fit) > 0 else prev_left_fit_average
    right_avg = np.average(right_fit, axis=0) if len(right_fit) > 0 else prev_right_fit_average

    prev_left_fit_average = left_avg
    prev_right_fit_average = right_avg

    left_line = make_coordinates(image, left_avg)
    right_line = make_coordinates(image, right_avg)

    lines_out = []
    if left_line is not None:
        lines_out.append(left_line)
    if right_line is not None:
        lines_out.append(right_line)

    if len(lines_out) == 0:
        return None

    return np.array(lines_out)

def display_lines(image, lines):
    line_image = np.zeros_like(image)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 10)  # RED

    return line_image

def display_filled_lanes(image, lines):
    lane_image = np.zeros_like(image)

    if lines is not None and len(lines) == 2:
        left, right = lines

        pts = np.array([
            [left[0], left[1]],
            [left[2], left[3]],
            [right[2], right[3]],
            [right[0], right[1]]
        ])

        cv2.fillPoly(lane_image, [pts], (0, 255, 0))  # GREEN

    return lane_image


cap = cv2.VideoCapture("road background short video..mp4")  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)

    lines = cv2.HoughLinesP(
        cropped_image,
        2,
        np.pi / 180,
        100,
        np.array([]),
        minLineLength=40,
        maxLineGap=5
    )

    averaged_lines = average_slope_intercept(frame, lines)

    line_image = display_lines(frame, averaged_lines)
    fill_image = display_filled_lanes(frame, averaged_lines)

  
    combo = cv2.addWeighted(frame, 0.7, line_image, 1, 1)
    combo = cv2.addWeighted(combo, 1, fill_image, 0.5, 0)


    combo = cv2.convertScaleAbs(combo, alpha=1.2, beta=20)

    cv2.imshow("Lane Detection", combo)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
