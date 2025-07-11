import cv2
import numpy as np

# === Load Image ===
image = cv2.imread("input.jpg")  # Replace with your image
clone = image.copy()

# === Step 1: Select 4 Points with Mouse ===
points = []

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print(f"Point {len(points)}: ({x}, {y})")

cv2.namedWindow("Select 4 Points")
cv2.setMouseCallback("Select 4 Points", mouse_click)

while True:
    temp = clone.copy()
    for i, pt in enumerate(points):
        cv2.circle(temp, pt, 5, (0, 255, 0), -1)
        cv2.putText(temp, f"{i+1}", (pt[0] + 10, pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.imshow("Select 4 Points", temp)
    key = cv2.waitKey(1)
    if key == 27 or len(points) == 4:  # ESC or 4 points
        break

cv2.destroyAllWindows()

if len(points) != 4:
    print("You need to select 4 points.")
    exit()

# === Step 2: Compute Homography ===
pts_src = np.array(points, dtype="float32")

# Desired output size (you can adjust this)
width, height = 500, 700

pts_dst = np.array([
    [0, 0],
    [width - 1, 0],
    [width - 1, height - 1],
    [0, height - 1]
], dtype="float32")

# Compute homography matrix
H, status = cv2.findHomography(pts_src, pts_dst)

# === Step 3: Apply Perspective Warp ===
warped = cv2.warpPerspective(image, H, (width, height))

# === Step 4: Show and Save Result ===
cv2.imshow("Original", image)
cv2.imshow("Warped Top View", warped)
cv2.imwrite("warped_output.jpg", warped)
cv2.waitKey(0)
cv2.destroyAllWindows()
