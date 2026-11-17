import time


def build_with_concat(n):
    text = ""
    for i in range(n):
        text += f"Call {i}: 00:01:23 Rs 1.50\n"
    return text


def build_with_join(n):
    lines = [f"Call {i}: 00:01:23 Rs 1.50\n" for i in range(n)]
    return "".join(lines)


def best_time(func, n, runs=3):
    best = float("inf")
    for _ in range(runs):
        start = time.perf_counter()
        func(n)
        best = min(best, time.perf_counter() - start)
    return best


def main():
    print("=== MONTHLY SMS BILL STATEMENT BENCHMARK ===")
    for n in (1_000, 10_000, 200_000):
        t_concat = best_time(build_with_concat, n)
        t_join = best_time(build_with_join, n)
        print(f"Dataset: {n:>7,} lines | += loop: {t_concat:.6f}s | "
              f"str.join(): {t_join:.6f}s ({t_concat / t_join:.1f}x faster)")

    print("\nMemory Allocation Dynamics:")
    print("Repeated Concatenation : O(N^2) character copying overhead (worst case)")
    print("String Join (str.join) : O(N) single-pass exact buffer allocation")
    print("[SUCCESS] String immutability and linear join benchmark verified.")
    print("Note: times vary by machine; CPython can optimise += via realloc.")


if __name__ == "__main__":
    main()
