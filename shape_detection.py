import cv2
import numpy as np

def detect_shapes(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur for better contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Approximate the contour
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(approx)

        # Ignore small contours (noise)
        if area < 100:
            continue

        # Determine shape based on the number of vertices
        shape = "Undefined"
        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            aspect_ratio = float(w) / h
            shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
        elif len(approx) > 4:
            shape = "Circle"

        # Annotate the shape on the frame
        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)
        text = f"{shape}, Area: {int(area)}, Height: {h}px"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return frame

def main():
    # Initialize webcam (0 for the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access the camera.")
        return

    print("Press 'q' to exit the webcam feed.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Detect shapes in the current frame
        processed_frame = detect_shapes(frame)

        # Display the processed frame
        cv2.imshow("Real-Time Shape Detection", processed_frame)

        # Press 'q' to quit the webcam feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
