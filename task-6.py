"""Task 6: Design Challenge: College Fest Registration Desk."""

import os
import tempfile

class RegistrationManager:
    """Manages college fest registrations with atomic file transactions and validation."""
    def __init__(self, db_path="Task06/registrations.csv"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        if not os.path.exists(db_path):
            with open(db_path, "w", encoding="utf-8") as f:
                f.write("regno,name,event,fee_paid\n")

    def register_participant(self, regno, name, event, fee_paid):
        # Validate inputs
        if not regno or not name or not event:
            raise ValueError("All fields (regno, name, event, fee_paid) are mandatory.")
        try:
            fee = float(fee_paid)
        except ValueError:
            raise ValueError("Fee paid must be a valid numeric amount.")

        # Atomic write using temporary file replacement
        temp_file = self.db_path + ".tmp"
        try:
            with open(self.db_path, "r", encoding="utf-8") as src, open(temp_file, "w", encoding="utf-8") as dst:
                for line in src:
                    dst.write(line)
                dst.write(f"{regno},{name},{event},{fee:.2f}\n")
            os.replace(temp_file, self.db_path)
            print(f"Successfully registered student {regno} ({name}) for event '{event}'.")
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                raise RuntimeError(f"Registration transaction failed: {e}") from e

    def generate_summary(self):
        total_revenue = 0.0
        count = 0
        with open(self.db_path, "r", encoding="utf-8") as f:
            header = f.readline()
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    total_revenue += float(parts[3])
                    count += 1
        print(f"--- College Fest Registration Summary ---")
        print(f"Total Registrations: {count}")
        print(f"Total Fee Revenue: Rs {total_revenue:.2f}")

if __name__ == "__main__":
    mgr = RegistrationManager("Task06/test_regs.csv")
    mgr.register_participant("192524478", "J. Sam Agal", "AI Hackathon", 500)
    mgr.register_participant("192524479", "Ravi Kumar", "RoboWars", 750)
    mgr.generate_summary()
