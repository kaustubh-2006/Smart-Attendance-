import cv2
import time

qr_start_time = None
QR_VERIFY_TIME = 3  # seconds

from datetime import datetime

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    ret, frame = cap.read()
    data, bbox, _ = detector.detectAndDecode(frame)

    if data:
        time = datetime.now().strftime('%H:%M:%S')
        with open("attendance.csv", "a") as f:
            f.write(f"{data},{time}\n")
        print("Attendance Marked:", data)
        break

    cv2.imshow("QR Attendance", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
