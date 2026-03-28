import pandas as pd
import os

if not os.path.exists("attendance_log.csv"):
    print("❌ No attendance data found")
    exit(1)

df = pd.read_csv("attendance_log.csv")

writer = pd.ExcelWriter("attendance.xlsx", engine="openpyxl")

for subject in df["Subject"].unique():
    sub_df = df[df["Subject"] == subject]

    pivot = sub_df.pivot_table(
        index="Name",
        columns="Date",
        values="Method",
        aggfunc="first"
    )

    pivot.fillna("Absent", inplace=True)
    pivot.to_excel(writer, sheet_name=subject)

writer.close()

print("✅ Excel updated successfully")
