import cv2
import numpy as np

# Store history of chosen paths for visualization
path_history = []

def find_clear_path(frame):
    """
    Analyzes the frame to detect free space and determine best movement direction.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold to detect obstacles
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Optional smoothing
    thresh = cv2.GaussianBlur(thresh, (5, 5), 0)

    height, width = thresh.shape

    num_slices = 5
    slice_width = width // num_slices

    free_spaces = []

    for i in range(num_slices):
        x_start = i * slice_width
        slice_roi = thresh[:, x_start:x_start+slice_width]

        free_space = cv2.countNonZero(slice_roi)
        free_spaces.append(free_space)

        # Draw slice area at the top
        cv2.rectangle(frame, (x_start, 0), (x_start+slice_width, 20), (0, 255, 255), -1)
        cv2.putText(frame, str(free_space), (x_start+5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

    # Choose the slice with maximum free space
    best_index = np.argmax(free_spaces)
    x_best = best_index * slice_width

    # Highlight best slice
    cv2.rectangle(frame, (x_best, 0), (x_best+slice_width, height), (0,255,0), 2)

    # Decide command
    if best_index < num_slices//2:
        command = "Move Left"
    elif best_index > num_slices//2:
        command = "Move Right"
    else:
        command = "Move Forward"

    # Add to path history
    path_history.append((best_index, command))

    # Draw path history
    for idx, (slice_idx, cmd) in enumerate(path_history[-30:]):
        x_hist = slice_idx * slice_width + slice_width//2
        y_hist = height - idx*5
        cv2.circle(frame, (x_hist, y_hist), 2, (255,0,255), -1)

    cv2.putText(frame, f"Direction: {command}", (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    return frame, command

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access camera.")
        return

    print("Press 'q' to quit.")
    print("Press 's' to save a snapshot of the current path planning frame.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, direction = find_clear_path(frame)

        # Show the frame
        cv2.imshow("Drone Path Planning", processed_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save snapshot
            cv2.imwrite("path_planning_snapshot.jpg", processed_frame)
            print("Snapshot saved as 'path_planning_snapshot.jpg'.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
