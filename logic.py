from z3 import *
from copy import deepcopy

SIZE = 10
KB = Solver()

# Define constants and functions
x, y = Ints('x y')
x1, y1 = Ints('x1 y1')
W = Function('wumpus', IntSort(), IntSort(), BoolSort())
P = Function('pit', IntSort(), IntSort(), BoolSort())
S = Function('stench', IntSort(), IntSort(), BoolSort())
B = Function('breeze', IntSort(), IntSort(), BoolSort())
PG = Function('poisonous_gas', IntSort(), IntSort(), BoolSort())
WH = Function('whiff', IntSort(), IntSort(), BoolSort())
HP = Function('healing_potion', IntSort(), IntSort(), BoolSort())
GL = Function('glow', IntSort(), IntSort(), BoolSort())

# Define clauses
def Adjacent(x1, y1, x2, y2):
    return And(
      And(0 <= x1, x1 < SIZE, 0 <= y1, y1 < SIZE),  # x1, y1 in bounds
      And(0 <= x2, x2 < SIZE, 0 <= y2, y2 < SIZE),  # x2, y2 in bounds
      Or(
          And(x1 == x2, Or(y1 == y2 - 1, y1 == y2 + 1)),  # Same x, adjacent y
          And(y1 == y2, Or(x1 == x2 - 1, x1 == x2 + 1))   # Same y, adjacent x
      )
  )

ExistW = ForAll([x, y], Implies(S(x, y), Exists([x1, y1], And(Adjacent(x, y, x1, y1), W(x1, y1)))))
ExistS = ForAll([x, y, x1, y1], Implies(And(W(x, y), Adjacent(x, y, x1, y1)), S(x1, y1)))

ExistP = ForAll([x, y], Implies(B(x, y), Exists([x1, y1], And(Adjacent(x, y, x1, y1), P(x1, y1)))))
ExistB = ForAll([x, y, x1, y1], Implies(And(P(x, y), Adjacent(x, y, x1, y1)), B(x1, y1)))

ExistPG = ForAll([x, y], Implies(WH(x, y), Exists([x1, y1], And(Adjacent(x, y, x1, y1), PG(x1, y1)))))
ExistWH = ForAll([x, y, x1, y1], Implies(And(PG(x, y), Adjacent(x, y, x1, y1)), WH(x1, y1)))

ExistHP = ForAll([x, y], Implies(GL(x, y), Exists([x1, y1], And(Adjacent(x, y, x1, y1), HP(x1, y1)))))
ExistGL = ForAll([x, y, x1, y1], Implies(And(HP(x, y), Adjacent(x, y, x1, y1)), GL(x1, y1)))

def check(agentKB, key, exploredCell, sentence):
    kb = Solver()
    kb.reset()
    sign = {
        "P": P,
        "W": W,
        "P_G": PG,
        "H_P": HP,
        "S": S,
        "B": B,
        "W_H": WH,
        "G_L": GL,
    }
    obj = {
        "S": ["W", ExistW, ExistS],
        "B": ["P", ExistB, ExistP],
        "G_L": ["H_P", ExistHP, ExistGL],
        "W_H": ["P_G", ExistPG, ExistWH]
    }
    kb.add(obj[key][1])
    kb.add(obj[key][2])
    threatKey = obj[key][0]
    for cell in exploredCell:
        if cell in agentKB[threatKey]:
            kb.add(sign[threatKey](cell[0], cell[1]))
        else:
            kb.add(Not(sign[threatKey](cell[0], cell[1])))
        if cell in agentKB[key]:
            kb.add(sign[key](cell[0], cell[1]))
        else:
            kb.add(Not(sign[key](cell[0], cell[1])))
    kb.add(sentence)
    return kb.check() == sat

