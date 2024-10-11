import cv2

# Thử tất cả các ID từ 0 đến 10 (hoặc nhiều hơn nếu cần)
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Device {i} is available.")
        cap.release()
    else:
        print(f"Device {i} is not available.")