import cv2
import time
from ultralytics import YOLO
import os

# ========== SETTINGS ==========
SAVE_FRAMES = True  # Save detection results as images
SAVE_VIDEO = True   # Save entire detection output as video
DISPLAY = True      # Set to False if running on a server

video_source = 0  # Use webcam. Replace with 'video.mp4' for a file

# ========== SETUP ==========
model = YOLO("yolov8n.pt")  # You can change to yolov8s.pt or yolov8m.pt if needed

cap = cv2.VideoCapture(video_source)
assert cap.isOpened(), "Failed to open video source"

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

# Create output directories
os.makedirs("outputs/frames", exist_ok=True)
os.makedirs("outputs/videos", exist_ok=True)

# Set up video writer if saving
if SAVE_VIDEO:
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_video = cv2.VideoWriter("outputs/videos/output_yolo.mp4", fourcc, fps, (width, height))

frame_count = 0
start_time = time.time()

print("[INFO] Starting YOLOv8 detection... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(source=frame, persist=True, stream=False, verbose=False)
    result_frame = frame.copy()

    # Draw bounding boxes
    if results[0].boxes is not None:
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            cv2.rectangle(result_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(result_frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Save frame
    if SAVE_FRAMES:
        cv2.imwrite(f"outputs/frames/frame_{frame_count:05d}.jpg", result_frame)

    # Write video frame
    if SAVE_VIDEO:
        out_video.write(result_frame)

    # Show
    if DISPLAY:
        cv2.imshow("YOLOv8 Detection", result_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    frame_count += 1

# ========== CLEANUP ==========
cap.release()
if SAVE_VIDEO:
    out_video.release()
cv2.destroyAllWindows()

end_time = time.time()
print(f"[INFO] Detection completed. Processed {frame_count} frames in {end_time - start_time:.2f} seconds.")
