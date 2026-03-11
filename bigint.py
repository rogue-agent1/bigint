#!/usr/bin/env python3
"""Arbitrary precision integer arithmetic (educational - Python has this built-in)."""
import sys
def factorial(n):
    r=1
    for i in range(2,n+1): r*=i
    return r
def fibonacci(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a
if len(sys.argv)<2: sys.exit("Usage: bigint <factorial|fib|pow|expr> <n> [m]")
cmd=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 100
if cmd=='factorial': r=factorial(n); print(f"{n}! = {r}\n({len(str(r))} digits)")
elif cmd=='fib': r=fibonacci(n); print(f"F({n}) = {r}\n({len(str(r))} digits)")
elif cmd=='pow': m=int(sys.argv[3]) if len(sys.argv)>3 else 2; r=m**n; print(f"{m}^{n} = {r}\n({len(str(r))} digits)")
