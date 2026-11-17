CORRECT_OTP = "4829"
SECURITY_ANSWER = "blue"

# Scripted inputs so the demo is repeatable. Replace get_input with input()
# for real interactive use.
_scripted = iter(["", "1234", "5678", "9999", "4829"])


def get_input(prompt):
    value = next(_scripted)
    shown = value if value else "[blank entry ignored]"
    print(f"{prompt}{shown}", end="")
    return value


def security_question():
    print("\nStandard attempts exhausted. Triggering Security Question...")
    answer = "blue"
    print(f"Security Challenge: What is your favorite color? -> {answer}")
    return answer.strip().lower() == SECURITY_ANSWER


def verify_otp():
    attempts_used = 0
    max_attempts = 3
    extended = False

    while attempts_used < max_attempts:
        label = f"Attempt [{attempts_used + 1}/{max_attempts}] - Enter OTP: "
        raw = get_input(label)

        if raw.strip() == "":
            print()
            continue            # blank entry does NOT consume an attempt

        attempts_used += 1      # counter updated only after the blank check

        if raw.strip() == CORRECT_OTP:
            print(" -> Access Granted!")
            break               # success exits the loop

        remaining = max_attempts - attempts_used
        word = "attempt" if remaining == 1 else "attempts"
        print(f" -> Incorrect OTP. {remaining} {word} remaining.")

        if remaining == 0 and not extended:
            if security_question():
                max_attempts = 5
                extended = True
                print("Security Question Verified! Granted +2 additional attempts.")
            else:
                pass            # placeholder: audit log hook for failed challenge
    else:
        # Runs only when the loop ends without break
        print("Account locked for 30 minutes.")
        return False
    return True


def main():
    print("=== BANK KIOSK OTP VERIFICATION SYSTEM ===")
    if verify_otp():
        print("[SUCCESS] Loop state, continue/break, and dynamic extension verified.")


if __name__ == "__main__":
    main()
