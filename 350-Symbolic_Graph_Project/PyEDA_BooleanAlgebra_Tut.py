from pyeda.inter import *

#Creating Variable Instances
a, b, c, d = map(exprvar, 'abcd')
print("a, b, c, d = map(exprvar, 'abcd')")
print(type(a.name))
print(b.name)
print(c.name)
print(d.name)

#Assigning variable arrays:
## Array of size 8
X = exprvars('x', 8)
print(X)

## Multi-dimensional bit vectors:
X = exprvars('x', 4, 4)
print(X)

print(f"X[2]: {X[2]}")
print(f"X[2,2]: {X[2,2]}")
print(f"X[1:3, 2]: {X[1:3, 2]}")
print(f"X[2,1:3]: {X[2,1:3]}")
print(f"X[-1,-1]: {X[-1,-1]}")

'''
The number of variables you use is called the dimension. 
All the possible outcomes of this experiment is called the space. 
Each possible outcome is called a point.


'''
print("Use the iter_points generator to iterate through all possible points " +
 "in an N-dimensional Boolean space:")

#print (f"list(iter_points([x, y])): {list(iter_points([x, y]))}")

#Generate 3 bit variable
X = exprvars('x', 3)

print("Simulatation of coin flip game where you win when all 3 out of 3 flips are heads:")
f = truthtable(X, "00000001")
print(f"Truth Table: {f}")
print(f"Boolean Expression (truthtable2expr(f)): {truthtable2expr(f)}")


#Generate a truthtable from the output value:
print("Simulatation of coin flip game where you win with 2 out of 3 heads:")
f = truthtable(X, "00010111")
print(f"Truth Table: {f}")

print(f"Boolean Expression (truthtable2expr(f)): {truthtable2expr(f)}")


