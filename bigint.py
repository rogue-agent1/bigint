#!/usr/bin/env python3
"""bigint - Big integer operations (demo without Python's built-in)."""
import sys

class BigInt:
    def __init__(self, val="0"):
        if isinstance(val, list): self.digits=val; self.neg=False; return
        s=str(val).strip(); self.neg=s.startswith("-"); s=s.lstrip("-+")
        self.digits=[int(c) for c in s]  # most significant first
    def __repr__(self): 
        s="".join(map(str,self.digits)).lstrip("0") or "0"
        return ("-" if self.neg and s!="0" else "")+s
    def _cmp(a,b):
        if len(a.digits)!=len(b.digits): return 1 if len(a.digits)>len(b.digits) else -1
        for x,y in zip(a.digits,b.digits):
            if x!=y: return 1 if x>y else -1
        return 0
    def __eq__(s,o): return str(s)==str(BigInt(o) if not isinstance(o,BigInt) else o)
    def _add_abs(a,b):
        r=[]; carry=0; ad=a.digits[::-1]; bd=b.digits[::-1]
        for i in range(max(len(ad),len(bd))):
            s=(ad[i] if i<len(ad) else 0)+(bd[i] if i<len(bd) else 0)+carry
            r.append(s%10); carry=s//10
        if carry: r.append(carry)
        return BigInt(r[::-1])
    def _sub_abs(a,b):
        if a._cmp(b)<0: r=b._sub_abs(a); r.neg=True; return r
        r=[]; borrow=0; ad=a.digits[::-1]; bd=b.digits[::-1]
        for i in range(len(ad)):
            d=ad[i]-(bd[i] if i<len(bd) else 0)-borrow
            if d<0: d+=10; borrow=1
            else: borrow=0
            r.append(d)
        while len(r)>1 and r[-1]==0: r.pop()
        return BigInt(r[::-1])
    def __add__(a,b):
        b=b if isinstance(b,BigInt) else BigInt(b)
        if a.neg==b.neg: r=a._add_abs(b); r.neg=a.neg; return r
        return a._sub_abs(b) if not a.neg else b._sub_abs(a)
    def __mul__(a,b):
        b=b if isinstance(b,BigInt) else BigInt(b)
        r=[0]*(len(a.digits)+len(b.digits)); ad=a.digits[::-1]; bd=b.digits[::-1]
        for i,x in enumerate(ad):
            for j,y in enumerate(bd): r[i+j]+=x*y
        for i in range(len(r)-1): r[i+1]+=r[i]//10; r[i]%=10
        while len(r)>1 and r[-1]==0: r.pop()
        res=BigInt(r[::-1]); res.neg=a.neg!=b.neg; return res
    def factorial(n):
        r=BigInt("1")
        for i in range(2,n+1): r=r*BigInt(str(i))
        return r
    def power(base,exp):
        r=BigInt("1"); b=base
        while exp>0:
            if exp%2: r=r*b
            b=b*b; exp//=2
        return r

if __name__=="__main__":
    if len(sys.argv)<2: print("Usage: bigint.py <add|mul|fact|pow> args..."); sys.exit(1)
    cmd=sys.argv[1]
    if cmd=="add": print(BigInt(sys.argv[2])+BigInt(sys.argv[3]))
    elif cmd=="mul": print(BigInt(sys.argv[2])*BigInt(sys.argv[3]))
    elif cmd=="fact": print(BigInt.factorial(int(sys.argv[2])))
    elif cmd=="pow": print(BigInt.power(BigInt(sys.argv[2]),int(sys.argv[3])))
