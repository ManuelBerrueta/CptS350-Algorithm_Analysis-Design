#!/usr/bin/python3
from pyeda.inter import *

#! Constructing Binary Decision Diagrams (BDD)
#?  There is 2 ways:
#*      1. Convert an Expression
#*      2. Use operators on existing BDDs

#! Convert an Expression
#? Since the Boolean expression is PyEDA’s central data type, you can use the
#?  expr2bdd function to convert arbitrary expressions to BDDs:
f = expr("a & b | a & c | b & c")
print(f"expr('a & b | a & c | b & c'): {expr('a & b | a & c | b & c')}" )

#* Converting the expression to BDD
f = expr2bdd(f)

#! Using Operators
#? BDDs have their own variable and you can use the function bddvar to construct
a, b, c = map(bddvar, 'abc')
print(type(a))
print(isinstance(a, BinaryDecisionDiagram))

f = a & b | a & c | b & c
print(f)

#! Satisfiability
a, b = map(bddvar, 'ab')
f = ~a & ~b | ~a & b | a & ~b | a & b
print(f)
print(f.is_one())

g = (~a | ~b) & (~a | b) & (a | ~b) & (a | b)
print(g)
print(g.is_zero())

'''If you need one or more satisfying input points, use the satisfy_one and
 satisfy_all functions. The algorithm that implements SAT is very simple and
  elegant; it just finds a path from the function’s root node to one.'''

a, b, c = map(bddvar, 'abc')
f = a ^ b ^ c
print(f.satisfy_one())
print(list(f.satisfy_all()))

#! Formal Equivalence
'''Because BDDs are a canonical form, functional equivalence is trivial.'''
a, b, c = map(bddvar, 'abc')
f1 = a ^ b ^ c
f2 = a & ~b & ~c | ~a & b & ~c | ~a & ~b & c | a & b & c
print(f"f1.equivalent(f2): {f1.equivalent(f2)}\nf1 is f2: {f1 is f2}")

g2 = f2.compose({X[0]: Y[0], X[1]: Y[2], X[2]: Y[4],
                         X[3]: Y[1], X[4]: Y[3], X[5]: Y[5]})

%dotobj g2

