
def normalize(raw):
    # str methods return NEW strings; the original is never modified (immutability).
    return raw.strip().replace(" ", "").replace("-", "").upper()


def split_parts(clean):
    state = clean[:2]
    district = clean[2:4]
    series = clean[4:-4]     # 1 char for length 9, 2 chars for length 10
    number = clean[-4:]
    return state, district, series, number


def is_valid(clean):
    if len(clean) not in (9, 10):
        return False
    state, district, series, number = split_parts(clean)
    return (state.isalpha() and district.isdigit()
            and series.isalpha() and number.isdigit())


def receipt_format(clean):
    state, district, series, number = split_parts(clean)
    return f"{state} {district} {series} {number}"


def main():
    print("=== VEHICLE REGISTRATION NUMBER VALIDATION ===")
    samples = ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]
    valid = []
    for raw in samples:
        clean = normalize(raw)
        ok = is_valid(clean)
        if ok:
            valid.append(clean)
        print(f"Input: {raw!r:<18} -> Normalized: {clean:<11} | "
              f"Status: {'VALID' if ok else 'INVALID'}")

    print("\nReceipt Formatting Output:")
    clean = valid[0]
    state, district, series, number = split_parts(clean)
    print(f"Receipt Reg Number: {receipt_format(clean)} "
          f"(State: {state}, District: {district}, Series: {series}, Unique: {number})")
    print("[SUCCESS] String immutability, slicing, and validation completed.")


if __name__ == "__main__":
    main()
