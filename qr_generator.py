import qrcode
import pandas as pd
import os

os.makedirs("qr_codes", exist_ok=True)

df = pd.read_csv("students.csv")

for _, row in df.iterrows():
    qr_data = row["StudentID"]
    img = qrcode.make(qr_data)
    img.save(f"qr_codes/{qr_data}.png")

print("✅ Student-ID QR codes generated")
