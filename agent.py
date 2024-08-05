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
            self.KB[item] = self.start
        self.agentLocation = self.start
        self.agentDirection = DIRECTION[0]
    
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
    
    # This one is not finished yet.
    def shoot(self):
        temp = (self.agentLocation[0] + self.agentDirection[0], self.agentLocation[1] + self.agentDirection[1])
        if temp[0] >= 0 and temp[0] < self.size and temp[1] > 0 and temp[1] < self.size:
            result, cell = self.WumpusWorld.AgentShoot(temp)
            if result == "SCREAM":
                if len(cell) > 0:
                    for item in cell:
                        if item in self.KB["S"]:
                            self.KB["S"].pop(self.KB["S"].index(item))
    
    def grab(self):
        pass

A = Agent()
A.move()
A.shoot()
print(A.KB)