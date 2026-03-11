#!/usr/bin/env python3
"""bigint — Arbitrary precision integer arithmetic from scratch. Zero deps."""

class BigInt:
    def __init__(self, val=0):
        if isinstance(val, str):
            self.negative = val.startswith('-')
            self.digits = [int(c) for c in val.lstrip('-').lstrip('0') or '0']
        elif isinstance(val, int):
            self.negative = val < 0
            self.digits = [int(c) for c in str(abs(val))]
        else:
            self.digits = list(val.digits)
            self.negative = val.negative

    def __repr__(self): return ('-' if self.negative and self.digits != [0] else '') + ''.join(map(str, self.digits))
    def __eq__(self, other): return str(self) == str(BigInt(other) if isinstance(other, (int,str)) else other)

    def _cmp_abs(self, other):
        if len(self.digits) != len(other.digits):
            return 1 if len(self.digits) > len(other.digits) else -1
        for a, b in zip(self.digits, other.digits):
            if a != b: return 1 if a > b else -1
        return 0

    def _add_abs(self, other):
        a, b = self.digits[::-1], other.digits[::-1]
        result, carry = [], 0
        for i in range(max(len(a), len(b))):
            s = carry + (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
            result.append(s % 10)
            carry = s // 10
        if carry: result.append(carry)
        r = BigInt(0)
        r.digits = result[::-1]
        return r

    def _sub_abs(self, other):
        if self._cmp_abs(other) < 0:
            r = other._sub_abs(self)
            r.negative = True
            return r
        a, b = self.digits[::-1], other.digits[::-1]
        result, borrow = [], 0
        for i in range(len(a)):
            d = a[i] - borrow - (b[i] if i < len(b) else 0)
            borrow = 1 if d < 0 else 0
            result.append(d % 10)
        while len(result) > 1 and result[-1] == 0: result.pop()
        r = BigInt(0)
        r.digits = result[::-1]
        return r

    def __add__(self, other):
        other = BigInt(other) if isinstance(other, (int,str)) else other
        if self.negative == other.negative:
            r = self._add_abs(other)
            r.negative = self.negative
        elif self._cmp_abs(other) >= 0:
            r = self._sub_abs(other)
            r.negative = self.negative
        else:
            r = other._sub_abs(self)
            r.negative = other.negative
        return r

    def __mul__(self, other):
        other = BigInt(other) if isinstance(other, (int,str)) else other
        a, b = self.digits[::-1], other.digits[::-1]
        result = [0] * (len(a) + len(b))
        for i in range(len(a)):
            for j in range(len(b)):
                result[i+j] += a[i] * b[j]
                result[i+j+1] += result[i+j] // 10
                result[i+j] %= 10
        while len(result) > 1 and result[-1] == 0: result.pop()
        r = BigInt(0)
        r.digits = result[::-1]
        r.negative = self.negative != other.negative and r.digits != [0]
        return r

    def factorial(n):
        result = BigInt(1)
        for i in range(2, n+1):
            result = result * i
        return result

def main():
    a = BigInt("123456789012345678901234567890")
    b = BigInt("987654321098765432109876543210")
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a + b = {a + b}")
    print(f"a * b = {a * b}")
    print(f"50! = {BigInt.factorial(50)}")
    print(f"100! has {len(BigInt.factorial(100).digits)} digits")

if __name__ == "__main__":
    main()
