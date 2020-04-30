from pyeda.inter import *

'''These 3 conversions from 0 are equivalent, same is the case with 1'''

zeroA = expr(0)
zeroB = expr(False)
zeroC = expr("0")
print(f"zeroA == zeroB == zeroC: {zeroA == zeroB == zeroC}")


#Expression Constants
zero = expr(0)
one = expr(1)
print(type(zero))
print(type(one))

print(one.support)
print(zero.support)


a, b = map(exprvar, 'ab')
print(f"Shannon Expansion + {zero.expand([a, b], conj=True)}")
'''And(Or(a, b), Or(a, ~b), Or(~a, b), Or(~a, ~b))'''
print(f"Shannon Expansion + {one.expand([a, b])}")
'''Or(And(~a, ~b), And(~a, b), And(a, ~b), And(a, b))'''

print("From Constants, Variables, and Python Operators")
a, b, ci = map(exprvar, "a b ci".split())
s = ~a & ~b & ci | ~a & b & ~ci | a & ~b & ~ci | a & b & ci
print(f"~a & ~b & ci | ~a & b & ~ci | a & ~b & ~ci | a & b & ci : {s}")
co = a & b | a & ci | b & ci
print(f"a & b | a & ci | b & ci : {co}")

new_s = a ^ b ^ ci
print(f"using XOR, a ^ b ^ ci : {new_s}")


