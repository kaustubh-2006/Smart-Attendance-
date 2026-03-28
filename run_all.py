import subprocess
import sys

print("🚀 SMART ATTENDANCE SYSTEM (CONTINUOUS QR MODE)\n")

print("📸 Starting Continuous QR Attendance...")
ret = subprocess.call([sys.executable, "verify_qr_continuous.py"])

if ret != 0:
    print("❌ Attendance session failed")
    sys.exit(1)

print("📊 Updating Excel...")
subprocess.call([sys.executable, "excel_manager.py"])

print("🎉 ATTENDANCE SESSION COMPLETED")
