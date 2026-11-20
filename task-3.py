import os
import tempfile

class InvalidRecord(Exception):
    """Raised when a line of the attendance file is not in the expected format."""
    pass

def parse_line(line):
    """192311001,2026-10-08,P -> ('192311001', '2026-10-08', 'P')"""
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    regno, date, status = parts[0].strip(), parts[1].strip(), parts[2].strip().upper()
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")
    return regno, date, status

def summarise(path):
    present, absent = 0, 0
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    regno, date, status = parse_line(line)
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
                except InvalidRecord as e:
                    errors.append((line_no, str(e)))
    except FileNotFoundError as e:
        print(f"Error: File not found -> {e}")
        raise
    except PermissionError as e:
        print(f"Error: Permission denied -> {e}")
        raise
    return present, absent, errors

if __name__ == "__main__":
    data = (
        "192311001,2026-10-08,P\n"
        "192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n"
        "192311004,2026-10-08,L\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(data)
        tmp_name = tmp.name

    try:
        res = summarise(tmp_name)
        print("Summarise result:", res)
    finally:
        os.remove(tmp_name)
