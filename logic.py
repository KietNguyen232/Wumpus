from z3 import *
from copy import deepcopy

SIZE = 10
KB = Solver()

# Define constants and functions
x, y = Ints('x y')
x1, y1 = Ints('x1 y1')
W = Function('wumpus', IntSort(), IntSort(), BoolSort())
P = Function('pit', IntSort(), IntSort(), BoolSort())
G = Function('gold', IntSort(), IntSort(), BoolSort())
S = Function('stench', IntSort(), IntSort(), BoolSort())
B = Function('breeze', IntSort(), IntSort(), BoolSort())
PG = Function('poisonous_gas', IntSort(), IntSort(), BoolSort())
WH = Function('whiff', IntSort(), IntSort(), BoolSort())
HP = Function('healing_potion', IntSort(), IntSort(), BoolSort())
GL = Function('glow', IntSort(), IntSort(), BoolSort())
BLANK = Function('blank_cell', IntSort(), IntSort(), BoolSort())

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

ExistW = ForAll([x, y],
    S(x, y) == Exists([x1, y1], And(Adjacent(x, y, x1, y1), W(x1, y1)))
)

ExistP = ForAll([x, y],
    B(x, y) == Exists([x1, y1], And(Adjacent(x, y, x1, y1), P(x1, y1)))
)

ExistPG = ForAll([x, y],
    WH(x, y) == Exists([x1, y1], And(Adjacent(x, y, x1, y1), PG(x1, y1)))
)

ExistHP = ForAll([x, y],
    GL(x, y) == Exists([x1, y1], And(Adjacent(x, y, x1, y1), HP(x1, y1)))
)

BlankCell = ForAll([x, y], Implies(BLANK(x, y), 
                                   And(
                                       Not(P(x, y)), Not(W(x, y)), Not(PG(x, y)), Not(HP(x, y)), Not(G(x, y)),
                                       Not(B(x, y)), Not(S(x, y)), Not(WH(x, y)), Not(GL(x, y))
                                    )))

# Create Knowledge base for solving FOL
KB.add(ExistW, ExistP, ExistPG, ExistHP, BlankCell)

def check(AgentKB, exploredCell, sentence, kb=deepcopy(KB)):
    obj = {
        "-": BLANK,
        "P": P,
        "W": W,
        "P_G": PG,
        "H_P": HP,
        "S": S,
        "B": B,
        "W_H": WH,
        "G_L": GL,
        "G": G
    }
    for key in AgentKB.key():
        for cell in exploredCell:
            if cell in AgentKB[key]:
                kb.add(obj[key](cell[0], cell[1]))
            else:
                kb.add(Not(obj[key](cell[0], cell[1])))
    kb.add(sentence)
    return kb.check() == sat

# check_list = [B(1, 0), Not(B(0, 1)), S(0, 1), Not(S(1, 0)), P(1, 1)]
# check_list = [P(1, 1), W(1, 1)]
# print(check(check_list))