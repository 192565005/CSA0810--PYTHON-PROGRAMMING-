
import os

def process_mess_bills(filename):
    total = 0
    valid_lines_count = 0
    rejected_records = []
    
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return
        
    with open(filename, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line_stripped = line.strip()
            if not line_stripped:  
                continue
            parts = line_stripped.split(",")
            if len(parts) != 3:
                rejected_records.append((line_num, line_stripped, "Incorrect field count"))
                continue
            try:
                amount = float(parts[2])
                total += amount
                valid_line = f"{parts[1].strip()} | {amount:.2f}\n"
                print(valid_line, end="")
                valid_lines_count += 1
            except ValueError as e:
                rejected_records.append((line_num, line_stripped, f"ValueError: {e}"))

    print(f"\nTotal Valid Mess Bill: {total:.2f}")
    if rejected_records:
        rejected_log_path = "rejected.log"
        with open(rejected_log_path, "w", encoding="utf-8") as rej_file:
            for lno, content, reason in rejected_records:
                rej_file.write(f"Line {lno}: {content} [{reason}]\n")
        print(f"Rejected records logged to '{rejected_log_path}' ({len(rejected_records)} errors).")

if __name__ == "__main__":
    process_mess_bills("mess_oct.txt")
