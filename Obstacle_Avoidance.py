import cv2
import numpy as np

def find_clear_path(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold to create obstacle mask
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Optional: Blur to smooth noise
    thresh = cv2.GaussianBlur(thresh, (5, 5), 0)

    height, width = thresh.shape

    # Parameters
    num_slices = 5
    slice_width = width // num_slices

    # Store free space heights
    free_spaces = []

    for i in range(num_slices):
        x_start = i * slice_width
        slice_roi = thresh[:, x_start:x_start+slice_width]

        # Count non-obstacle pixels (white area)
        free_space = cv2.countNonZero(slice_roi)
        free_spaces.append(free_space)

        # Visual debug
        cv2.rectangle(frame, (x_start, 0), (x_start+slice_width, 20), (255,0,0), -1)
        cv2.putText(frame, str(free_space), (x_start+5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    # Determine best slice (max free space)
    best_index = np.argmax(free_spaces)

    # Visual highlight
    x_best = best_index * slice_width
    cv2.rectangle(frame, (x_best, 0), (x_best+slice_width, height), (0,255,0), 2)

    # Decide command
    if best_index < num_slices//2:
        command = "Move Left"
    elif best_index > num_slices//2:
        command = "Move Right"
    else:
        command = "Move Forward"

    cv2.putText(frame, f"Direction: {command}", (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    return frame, command

# def main():
#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         print("Error: Cannot access camera.")
#         return

#     print("Press 'q' to quit.")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         processed_frame, direction = find_clear_path(frame)

#         # Here you integrate drone movement commands:
#         # send_movement_command(direction)

#         cv2.imshow("Drone Path Planning", processed_frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access camera.")
        return

    print("Press 'q' to quit.")
    print("Press 's' to save a snapshot of the current frame.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, direction = find_clear_path(frame)

        # Show window
        cv2.imshow("Drone Path Planning", processed_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save the frame
            cv2.imwrite("drone_obstacle_avoidance_snapshot.jpg", processed_frame)
            print("Snapshot saved as 'drone_obstacle_avoidance_snapshot.jpg'.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
