import qrcode
import pandas as pd
import os

# Load students
df = pd.read_csv("students.csv")

# Create folder for QR codes
os.makedirs("qr_codes", exist_ok=True)

for _, row in df.iterrows():
    student_id = row["StudentID"]
    name = row["Name"]
    subject = row["Subject"]

    # QR DATA (ONLY STUDENT ID – SAFE & UNIQUE)
    qr_data = student_id

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    filename = f"qr_codes/{student_id}_{name}.png"
    img.save(filename)

    print(f"✅ QR generated for {student_id} - {name}")

print("\n🎉 All student QR codes generated successfully!")
