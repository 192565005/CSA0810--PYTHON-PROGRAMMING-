"""Main execution script for attendance package."""
from reader import read_attendance_file
from stats import compute_statistics
from report import generate_report
import tempfile
import os

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write("192524478,2026-11-01,P\n192524479,2026-11-01,A\n")
        tmp_name = tmp.name

    recs = read_attendance_file(tmp_name)
    stats = compute_statistics(recs)
    rep = generate_report(stats)
    
    print("--- Package Attendance Report ---")
    for line in rep:
        print(line)
        
    os.remove(tmp_name)
