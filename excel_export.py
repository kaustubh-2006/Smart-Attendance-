import pandas as pd
import os

csv_file = "attendance.csv"
excel_file = "attendance.xlsx"
temp_file = "attendance_temp.xlsx"

# Read CSV
df = pd.read_csv(csv_file)

# Write to temp file first
df.to_excel(temp_file, index=False)

# Replace old Excel safely
if os.path.exists(excel_file):
    os.remove(excel_file)

os.rename(temp_file, excel_file)

print("✅ attendance.xlsx updated successfully")
