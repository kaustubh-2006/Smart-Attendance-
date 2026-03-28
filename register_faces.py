import cv2, os
import pandas as pd

os.makedirs("faces", exist_ok=True)

df = pd.read_csv("students.csv")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

for _, row in df.iterrows():
    sid = row["StudentID"]
    folder = f"faces/{sid}"
    os.makedirs(folder, exist_ok=True)

    print(f"📸 Capture face for {sid} (press SPACE)")
    count = 0

    while count < 5:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x,y,w,h) in faces:
            face = gray[y:y+h, x:x+w]
            cv2.imwrite(f"{folder}/{count}.jpg", face)
            count += 1

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) == 32:
            pass

    print(f"✅ Face registered for {sid}")

cap.release()
cv2.destroyAllWindows()
