#!/usr/bin/env python3
"""bigint: Arbitrary-precision integer arithmetic from digit arrays."""
import sys

class BigInt:
    def __init__(self, val="0"):
        if isinstance(val, int):
            self.negative = val < 0
            self.digits = list(map(int, str(abs(val))))[::-1]  # LSB first
        else:
            s = str(val).strip()
            self.negative = s.startswith("-")
            if self.negative: s = s[1:]
            self.digits = [int(c) for c in s[::-1]]
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()
        if self.digits == [0]: self.negative = False

    def __repr__(self):
        s = "".join(str(d) for d in reversed(self.digits))
        return ("-" + s) if self.negative else s

    def _cmp_abs(self, other):
        if len(self.digits) != len(other.digits):
            return 1 if len(self.digits) > len(other.digits) else -1
        for i in range(len(self.digits)-1, -1, -1):
            if self.digits[i] != other.digits[i]:
                return 1 if self.digits[i] > other.digits[i] else -1
        return 0

    @staticmethod
    def _add_abs(a, b):
        r, carry = [], 0
        for i in range(max(len(a), len(b))):
            s = carry + (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
            r.append(s % 10); carry = s // 10
        if carry: r.append(carry)
        return r

    @staticmethod
    def _sub_abs(a, b):  # a >= b
        r, borrow = [], 0
        for i in range(len(a)):
            d = a[i] - borrow - (b[i] if i < len(b) else 0)
            if d < 0: d += 10; borrow = 1
            else: borrow = 0
            r.append(d)
        while len(r) > 1 and r[-1] == 0: r.pop()
        return r

    def __add__(self, other):
        if not isinstance(other, BigInt): other = BigInt(other)
        if self.negative == other.negative:
            result = BigInt()
            result.digits = self._add_abs(self.digits, other.digits)
            result.negative = self.negative
            if result.digits == [0]: result.negative = False
            return result
        cmp = self._cmp_abs(other)
        if cmp == 0: return BigInt(0)
        if cmp > 0:
            result = BigInt()
            result.digits = self._sub_abs(self.digits, other.digits)
            result.negative = self.negative
        else:
            result = BigInt()
            result.digits = self._sub_abs(other.digits, self.digits)
            result.negative = other.negative
        return result

    def __mul__(self, other):
        if not isinstance(other, BigInt): other = BigInt(other)
        r = [0] * (len(self.digits) + len(other.digits))
        for i in range(len(self.digits)):
            carry = 0
            for j in range(len(other.digits)):
                r[i+j] += self.digits[i] * other.digits[j] + carry
                carry = r[i+j] // 10
                r[i+j] %= 10
            r[i+len(other.digits)] += carry
        while len(r) > 1 and r[-1] == 0: r.pop()
        result = BigInt()
        result.digits = r
        result.negative = self.negative != other.negative
        if r == [0]: result.negative = False
        return result

    def __eq__(self, other):
        if not isinstance(other, BigInt): other = BigInt(other)
        return self.negative == other.negative and self.digits == other.digits

def test():
    assert str(BigInt("12345")) == "12345"
    assert str(BigInt("-42")) == "-42"
    # Add
    assert BigInt("999") + BigInt("1") == BigInt("1000")
    assert BigInt("100") + BigInt("-100") == BigInt("0")
    assert BigInt("-50") + BigInt("30") == BigInt("-20")
    # Multiply
    assert BigInt("123") * BigInt("456") == BigInt("56088")
    assert BigInt("-3") * BigInt("7") == BigInt("-21")
    assert BigInt("0") * BigInt("999") == BigInt("0")
    # Big numbers
    big = BigInt("99999999999999999999")
    assert big + BigInt("1") == BigInt("100000000000000000000")
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: bigint.py test")
