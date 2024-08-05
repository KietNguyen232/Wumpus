from program import Program
from logic import *

DIRECTION = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Agent:
    def __init__(self, inputFile="map1.txt"):
        self.WumpusWorld = Program(inputFile)
        self.map, self.start, self.size = self.WumpusWorld.StartingStateRepresentation()
        self.agentPercept = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.agentPercept[self.start[0]][self.start[1]] = self.map[self.start[0]][self.start[1]]
        self.KB = {
            "-": [],
            "P": [],
            "W": [],
            "P_G": [],
            "H_P": [],
            "S": [],
            "B": [],
            "W_H": [],
            "G_L": [],
            "G": [],
        }
        self.inventory = []
        for item in self.map[self.start[0]][self.start[1]]:
            self.KB[item].append(self.start)
        self.agentLocation = self.start
        self.agentDirection = DIRECTION[0]
        self.agentHP = 100
    
    def updatePercept(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.agentPercept[i][j] is not None:
                    self.agentPercept[i][j] = self.WumpusWorld.map[i][j]
    
    def turnRight(self):
        i = DIRECTION.index(self.agentDirection)
        self.agentDirection = DIRECTION[(i + 1) % 4]

    def turnLeft(self):
        i = DIRECTION.index(self.agentDirection)
        self.agentDirection = DIRECTION[(i + 3) % 4]
        
    def move(self):
        temp = (self.agentLocation[0] + self.agentDirection[0], self.agentLocation[1] + self.agentDirection[1])
        if temp[0] >= 0 and temp[0] < self.size and temp[1] >= 0 and temp[1] < self.size:
            self.agentLocation = temp
            self.agentPercept[temp[0]][temp[1]] = self.WumpusWorld.map[temp[0]][temp[1]]
            for item in self.WumpusWorld.map[temp[0]][temp[1]]:
                self.KB[item].append(temp)
            return True
        return False
    
    def shoot(self):
        temp = (self.agentLocation[0] + self.agentDirection[0], self.agentLocation[1] + self.agentDirection[1])
        if temp[0] >= 0 and temp[0] < self.size and temp[1] >= 0 and temp[1] < self.size:
            result, cell = self.WumpusWorld.AgentShoot(temp)
            if result == "SCREAM":
                self.updatePercept()
                for item in cell:
                    if item in self.KB["S"]:
                        self.KB["S"].pop(self.KB["S"].index(item))
                if len(self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]) == 1 and \
                    "-" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
                    self.KB["-"].append(self.agentLocation)
    
    def grab(self):
        if "G" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
            self.inventory.append("G")
            self.WumpusWorld.agentGrabGold(self.agentLocation)
            self.updatePercept()
            self.KB["G"].pop(self.KB["G"].index(self.agentLocation))
            if len(self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]) == 1 and \
                "-" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
                self.KB["-"].append(self.agentLocation)
                
        if "H_P" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
            self.inventory.append("H_P")
            cell = self.WumpusWorld.agentGrabHP(self.agentLocation)
            if len(cell) > 0:
                self.updatePercept()
                for item in cell:
                    if item in self.KB["G_L"]:
                        self.KB["G_L"].pop(self.KB["G_L"].index(item))
                if len(self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]) == 1 and \
                    "-" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
                    self.KB["-"].append(self.agentLocation)
    
    def useHealingPotion(self):
        if "H_P" in self.inventory:
            self.agentHP = min(100, self.agentHP + 25)
            self.inventory.pop(self.inventory.index("H_P"))

    def agentLogic(self):
        pass
# A = Agent()
# A.move()
# A.shoot()
# A.move()
# A.turnRight()
# A.move()
# print(A.KB)
# print(A.agentPercept)
# print(A.WumpusWorld.map)
# print(A.inventory)
# A.grab()
# print(A.KB)
# print(A.agentPercept)
# print(A.WumpusWorld.map)
# print(A.inventory)
# A.useHealingPotion()
# print(A.inventory)
# print(A.agentHP)