
import sys
import time
from functools import lru_cache

naive_calls = 0


def climb_naive(n):
    global naive_calls
    naive_calls += 1
    if n <= 2:                 # base cases: climb(1)=1, climb(2)=2
        return n
    return climb_naive(n - 1) + climb_naive(n - 2)


@lru_cache(maxsize=None)
def climb_memoized(n):
    if n <= 2:
        return n
    return climb_memoized(n - 1) + climb_memoized(n - 2)


def climb_iterative(n):
    if n <= 2:
        return n
    prev, curr = 1, 2
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr


def main():
    print("=== RECURSION AND MEMOISATION BENCHMARK ===")
    print("Hand check:", [climb_iterative(i) for i in range(1, 7)])  # 1 2 3 5 8 13
    for n in (10, 20, 25, 30):
        global naive_calls
        naive_calls = 0
        ways = climb_naive(n)
        climb_memoized.cache_clear()
        climb_memoized(n)
        misses = climb_memoized.cache_info().misses
        print(f"n = {n:<2} | Ways = {ways:<8} | Naive Calls: {naive_calls:<9} "
              f"| Memoized Calls: {misses}")

    print("\nEvaluating n = 1000:")
    climb_memoized.cache_clear()
    try:
        climb_memoized(1000)
        print("Memoized Recursion: completed (raise recursion limit would be needed elsewhere)")
    except RecursionError:
        print(f"Memoized Recursion: RecursionError (sys.getrecursionlimit() "
              f"exceeded at {sys.getrecursionlimit()})")
    start = time.perf_counter()
    result = climb_iterative(1000)
    elapsed = time.perf_counter() - start
    print(f"Iterative Loop    : Result calculated in {elapsed:.4f}s "
          f"({len(str(result))} digits, O(1) space)")
    print("[SUCCESS] Tree call redundancy and recursion limits evaluated.")


if __name__ == "__main__":
    main()
