import cv2
import csv
import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
import winsound
import sys
import time

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

def beep():
    winsound.MessageBeep(winsound.MB_OK)

print(f"\n📘 Subject: {subject}")
print("📸 Continuous QR Attendance Started")
print("➡ Show QR | ESC to stop\n")

# ===================== SESSION MEMORY =====================
marked = set()          # prevent duplicates
last_scan_time = 0      # delay between scans
SCAN_DELAY = 2          # seconds

# ===================== FILE PREP =====================
file_exists = os.path.exists("attendance_log.csv")

# ===================== MAIN LOOP =====================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    qr_data, _, _ = qr.detectAndDecode(frame)

    current_time = time.time()

    if (
        qr_data in STUDENTS
        and qr_data not in marked
        and current_time - last_scan_time > SCAN_DELAY
    ):
        name = STUDENTS[qr_data]
        beep()
        marked.add(qr_data)
        last_scan_time = current_time

        with open("attendance_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    "StudentID","Name","Subject","Date","Time","Method"
                ])
                file_exists = True

            writer.writerow([
                qr_data,
                name,
                subject,
                today,
                datetime.now().strftime("%H:%M:%S"),
                "QR"
            ])

        print(f"✅ PRESENT: {name}")

    # Display count
    cv2.putText(
        frame,
        f"Present: {len(marked)}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("QR Attendance - Continuous Mode", frame)

    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()

print("\n🛑 Attendance Session Ended")
print("Total Present:", len(marked))
sys.exit(0)
