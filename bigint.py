#!/usr/bin/env python3
"""Big Integer - Arbitrary precision integer arithmetic from scratch."""
import sys

class BigInt:
    def __init__(self, val="0"):
        if isinstance(val, int): val = str(val)
        self.neg = val.startswith("-"); val = val.lstrip("-")
        self.digits = [int(c) for c in val.lstrip("0") or "0"]
    def __repr__(self): return ("-" if self.neg and self.digits != [0] else "") + "".join(map(str, self.digits))
    def _cmp(self, o):
        if len(self.digits) != len(o.digits): return 1 if len(self.digits) > len(o.digits) else -1
        for a, b in zip(self.digits, o.digits):
            if a != b: return 1 if a > b else -1
        return 0
    def __add__(self, o):
        if self.neg != o.neg:
            if self.neg: return o._sub_abs(BigInt("".join(map(str, self.digits))))
            else: return self._sub_abs(BigInt("".join(map(str, o.digits))))
        a, b = self.digits[::-1], o.digits[::-1]
        n = max(len(a), len(b)); result = []; carry = 0
        for i in range(n):
            s = carry + (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
            result.append(s % 10); carry = s // 10
        if carry: result.append(carry)
        r = BigInt("".join(map(str, reversed(result)))); r.neg = self.neg; return r
    def _sub_abs(self, o):
        cmp = self._cmp(o)
        if cmp == 0: return BigInt("0")
        if cmp < 0: r = o._sub_abs(BigInt("".join(map(str, self.digits)))); r.neg = True; return r
        a, b = self.digits[::-1], o.digits[::-1]; result = []; borrow = 0
        for i in range(len(a)):
            d = a[i] - borrow - (b[i] if i < len(b) else 0)
            if d < 0: d += 10; borrow = 1
            else: borrow = 0
            result.append(d)
        return BigInt("".join(map(str, reversed(result))))
    def __mul__(self, o):
        a, b = self.digits[::-1], o.digits[::-1]
        result = [0] * (len(a) + len(b))
        for i in range(len(a)):
            for j in range(len(b)):
                result[i+j] += a[i] * b[j]
                result[i+j+1] += result[i+j] // 10
                result[i+j] %= 10
        r = BigInt("".join(map(str, reversed(result)))); r.neg = self.neg != o.neg; return r
    def factorial(n):
        result = BigInt("1")
        for i in range(2, n+1): result = result * BigInt(str(i))
        return result

def main():
    a = BigInt("123456789012345678901234567890")
    b = BigInt("987654321098765432109876543210")
    print("=== Big Integer ===\n")
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a + b = {a + b}")
    print(f"a * b = {a * b}")
    print(f"\n100! = {BigInt.factorial(100)}")

if __name__ == "__main__":
    main()
