#!/usr/bin/env python3
"""Big integer arithmetic using Python's native arbitrary precision."""

def factorial(n: int) -> int:
    if n < 0: raise ValueError("Negative factorial")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fibonacci(n: int) -> int:
    if n < 0: raise ValueError("Negative fibonacci")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def power_mod(base: int, exp: int, mod: int) -> int:
    return pow(base, exp, mod)

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b) if a and b else 0

def is_prime(n: int) -> bool:
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: bigint.py <factorial|fibonacci|prime> <n>"); sys.exit(1)
    cmd, n = sys.argv[1], int(sys.argv[2])
    if cmd == "factorial": print(factorial(n))
    elif cmd == "fibonacci": print(fibonacci(n))
    elif cmd == "prime": print(is_prime(n))

def test():
    assert factorial(0) == 1
    assert factorial(10) == 3628800
    assert factorial(20) == 2432902008176640000
    assert fibonacci(0) == 0
    assert fibonacci(10) == 55
    assert fibonacci(50) == 12586269025
    assert gcd(12, 8) == 4
    assert lcm(4, 6) == 12
    assert is_prime(2) and is_prime(97) and not is_prime(100)
    assert power_mod(2, 10, 1000) == 24
    print("  bigint: ALL TESTS PASSED")
