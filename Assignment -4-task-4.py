import os
from pathlib import Path

def save_returns_correct(books, log_filename="returns.log"):
    # Corrected using append mode 'a', newline character, and 'with' statement
    with open(log_filename, "a", encoding="utf-8") as log:
        for b in books:
            log.write(f"{b}\n")

def process_day(day_file, log_filename="Task04/returns.log"):
    try:
        with open(day_file, "r", encoding="utf-8") as f:
            books = [line.strip() for line in f if line.strip()]
        save_returns_correct(books, log_filename)
        print(f"Successfully processed and logged returns from '{day_file}'.")
    except FileNotFoundError:
        print(f"Error: Day return file '{day_file}' missing.")

if __name__ == "__main__":
    os.makedirs("Task04", exist_ok=True)
    day1 = "day1_returns.txt"
    with open(day1, "w", encoding="utf-8") as f:
        f.write("Python Cookbook\nFluent Python\n")
    
    process_day(day1)
    
    if os.path.exists("Task04/returns.log"):
        print("--- Current Log Contents ---")
        print(Path("Task04/returns.log").read_text(encoding="utf-8"))
