import cv2
import numpy as np
import time
import random

def detect_lanes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=200)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return frame

def check_obstacle():
    # Simulate ultrasonic sensor data for testing
    distance = random.randint(10, 100)  # Example range in cm
    if distance < 20:
        return True, distance
    return False, distance

def main():
    cap = cv2.VideoCapture("C:\\Users\\MYPC\\Downloads\\80400-572395752_small.mp4")  # Path to input video

    if not cap.isOpened():
        print("Error: Couldn't open video.")
        return

    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()

        if not ret:
            break

        # Lane detection
        frame = detect_lanes(frame)

        # Object detection
        obstacle, distance = check_obstacle()
        if obstacle:
            cv2.putText(frame, f"Obstacle Detected: {distance} cm", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            cv2.putText(frame, f"Clear Path: {distance} cm", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Calculate frame processing time
        end_time = time.time()
        fps = 1 / (end_time - start_time)

        # Display FPS in terminal
        print(f"Frame processed in {end_time - start_time:.4f} seconds | FPS: {fps:.2f}")

        # Display output frame
        cv2.imshow('Lane Detection & Obstacle Avoidance', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
