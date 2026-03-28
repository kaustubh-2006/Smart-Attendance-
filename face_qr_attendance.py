import cv2
import winsound
import csv
import time
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog

# ================== LOAD REGISTERED STUDENTS ==================
students_df = pd.read_csv("students.csv")
STUDENT_DB = {
    row["StudentID"]: (row["Name"], row["Subject"])
    for _, row in students_df.iterrows()
}

# ================== DAILY LOCK (ANTI-REUSE) ==================
today = datetime.now().strftime("%Y-%m-%d")
USED_QR_FILE = f"used_qr_{today}.txt"

USED_QR = set()
try:
    with open(USED_QR_FILE, "r") as f:
        USED_QR = set(f.read().splitlines())
except:
    pass

USED_FACE = False

# ================== SOUND ==================
def success_sound():
    winsound.MessageBeep(winsound.MB_OK)

def error_sound():
    winsound.MessageBeep(winsound.MB_ICONHAND)

# ================== FACE FALLBACK INPUT ==================
root = tk.Tk()
root.withdraw()
face_name = simpledialog.askstring("Face Mode", "Enter Student Name:")
face_subject = simpledialog.askstring("Face Mode", "Enter Subject:")

# ================== TIME ==================
date = today
current_time = datetime.now().strftime("%H:%M:%S")

# ================== CAMERA ==================
cap = cv2.VideoCapture(0)
qr = cv2.QRCodeDetector()
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

QR_VERIFY_TIME = 3
FACE_VERIFY_TIME = 2
qr_start_time = None
face_start_time = None

marked = False
method = ""
student_name = ""
subject = ""

# ================== CSV HEADER CHECK ==================
file_exists = False
try:
    with open("attendance.csv", "r"):
        file_exists = True
except:
    pass

# ================== MAIN LOOP ==================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # -------- QR VERIFICATION (STRICT) --------
    data = ""
    try:
        data, bbox, _ = qr.detectAndDecode(frame)
    except:
        data = ""

    if data:
        if data not in STUDENT_DB:
            cv2.putText(frame, "INVALID QR", (40, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            error_sound()
            qr_start_time = None

        elif data in USED_QR:
            cv2.putText(frame, "QR ALREADY USED", (40, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            error_sound()
            qr_start_time = None

        else:
            if qr_start_time is None:
                qr_start_time = time.time()

            elapsed = time.time() - qr_start_time
            cv2.putText(
                frame,
                f"Verifying QR... {max(0, int(QR_VERIFY_TIME - elapsed) + 1)}",
                (40, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
            )

            if elapsed >= QR_VERIFY_TIME:
                student_name, subject = STUDENT_DB[data]
                USED_QR.add(data)
                with open(USED_QR_FILE, "a") as f:
                    f.write(data + "\n")
                marked = True
                method = "QR"

    # -------- FACE VERIFICATION (ONE-TIME) --------
    if not marked and not USED_FACE:
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        if len(faces) > 0:
            if face_start_time is None:
                face_start_time = time.time()
            elapsed_face = time.time() - face_start_time

            cv2.putText(
                frame,
                f"Verifying Face... {max(0, int(FACE_VERIFY_TIME - elapsed_face) + 1)}",
                (40, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2
            )

            if elapsed_face >= FACE_VERIFY_TIME:
                student_name = face_name
                subject = face_subject
                USED_FACE = True
                marked = True
                method = "Face"
        else:
            face_start_time = None

    # -------- FINAL MARK --------
    if marked:
        success_sound()
        with open("attendance.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Student_Name","Subject","Date","Time","Method"])
            writer.writerow([student_name, subject, date, current_time, method])
        print("✅ VERIFIED:", student_name, method)
        break

    cv2.imshow("Smart Attendance System", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
