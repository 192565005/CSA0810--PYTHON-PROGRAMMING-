import os
from pathlib import Path

def process_monthly_attendance(data_dir):
    attendance_records = {}
    error_logs = []
    
    dir_path = Path(data_dir)
    if not dir_path.exists():
        print(f"Directory {data_dir} does not exist.")
        return

    file_list = sorted(dir_path.glob("*.txt"))
    total_files = len(file_list)
    
    if total_files == 0:
        print("No daily attendance files found.")
        return

    for file_path in file_list:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    error_logs.append((file_path.name, line_no, "Malformed fields"))
                    continue
                regno, date_str, status = parts[0].strip(), parts[1].strip(), parts[2].strip().upper()
                if status not in ("P", "A"):
                    error_logs.append((file_path.name, line_no, f"Invalid status '{status}'"))
                    continue
                
                if regno not in attendance_records:
                    attendance_records[regno] = {"P": 0, "A": 0, "total": 0}
                
                if status == "P":
                    attendance_records[regno]["P"] += 1
                else:
                    attendance_records[regno]["A"] += 1
                attendance_records[regno]["total"] += 1

    print(f"Processed {total_files} daily attendance files successfully.")
    print("--- Student Monthly Attendance Summary ---")
    below_75 = []
    for regno, stats in attendance_records.items():
        total_days = stats["total"]
        pct = (stats["P"] / total_days) * 100 if total_days > 0 else 0
        print(f"RegNo: {regno} | Present: {stats['P']} | Absent: {stats['A']} | Attendance: {pct:.2f}%")
        if pct < 75.0:
            below_75.append((regno, pct))

    print(f"Students below 75% attendance: {len(below_75)}")
    if error_logs:
        print(f"Total damaged/error lines logged: {len(error_logs)}")

if __name__ == "__main__":
    # Create sample daily biometric file for testing
    os.makedirs("Task02/data", exist_ok=True)
    sample_file = Path("Task02/data/day1.txt")
    sample_file.write_text("192524478,2026-11-01,P\n192524479,2026-11-01,A\n192524480,2026-11-01,INVALID\n")
    process_monthly_attendance("Task02/data")
