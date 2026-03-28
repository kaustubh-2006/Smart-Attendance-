import cv2
import csv
import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
import winsound
import sys

# ===================== TEACHER ENTERS SUBJECT =====================
root = tk.Tk()
root.withdraw()

subject = simpledialog.askstring(
    "Subject",
    "Enter Subject Name (e.g. AI Lab, DBMS):"
)

if not subject:
    print("❌ Subject not entered")
    sys.exit(1)

# ===================== LOAD STUDENTS =====================
df = pd.read_csv("students.csv")
STUDENTS = {
    row["StudentID"]: row["Name"]
    for _, row in df.iterrows()
}

# ===================== CAMERA & QR =====================
cap = cv2.VideoCapture(0)
qr = cv2.QRCodeDetector()

today = datetime.now().strftime("%Y-%m-%d")
time_now = datetime.now().strftime("%H:%M:%S")

def beep():
    winsound.MessageBeep(winsound.MB_OK)

print(f"📘 Subject: {subject}")
print("📸 Show student QR")

verified_sid = None

# ===================== MAIN LOOP =====================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    qr_data, _, _ = qr.detectAndDecode(frame)

    if qr_data in STUDENTS:
        verified_sid = qr_data
        beep()
        break

    cv2.imshow("QR Attendance", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

if not verified_sid:
    print("❌ QR not verified")
    sys.exit(1)

# ===================== SAVE ATTENDANCE =====================
name = STUDENTS[verified_sid]

file_exists = os.path.exists("attendance_log.csv")
with open("attendance_log.csv", "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([
            "StudentID","Name","Subject","Date","Time","Method"
        ])

    writer.writerow([
        verified_sid,
        name,
        subject,
        today,
        time_now,
        "QR"
    ])

print("✅ PRESENT MARKED")
print("Student:", name)
print("Subject:", subject)

sys.exit(0)
