import cv2
from datetime import datetime

face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        time = datetime.now().strftime('%H:%M:%S')
        with open("attendance.csv", "a") as f:
            f.write(f"Face_Detected,{time}\n")

        print("Face detected → Attendance Marked")
        cap.release()
        cv2.destroyAllWindows()
        exit()

    cv2.imshow("Face Attendance", frame)
    if cv2.waitKey(1) == 27:
        break
