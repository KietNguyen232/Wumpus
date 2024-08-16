class Program:
    def __init__(self, inputFile="map1.txt"):
        try:
            with open(inputFile, "r") as f:
                self.size = int(f.readline())
                self.map = [[] for _ in range(self.size)] 
                self.agentLocation = [] 
                for i in range(self.size):
                    temp = f.readline().split(".")
                    while temp[-1][-1] == '\n' or  temp[-1][-1] == ' ':
                        temp[-1] = temp[-1][:-1]
                    for j in range(self.size):
                        self.map[i].append(temp[j].split(" "))
                self.updateMap()
        except:
            raise Exception("Invalid input file or file format!")
    
    def updateMap(self):
        for i in range(self.size):
            for j in range(self.size):
                if "A" in self.map[i][j]:
                    self.map[i][j].pop(self.map[i][j].index("A"))
                    self.map[i][j].append("-")
                    self.agentLocation = (i, j)
                if "W" in self.map[i][j]:
                    self.assignValue("S", i, j)
                if "P" in self.map[i][j]:
                    self.assignValue("B", i, j)
                if "P_G" in self.map[i][j]:
                    self.assignValue("W_H", i, j)
                if "H_P" in self.map[i][j]:
                    self.assignValue("G_L", i, j)
        for i in range(self.size):
            for j in range(self.size):
                if len(self.map[i][j]) > 1 and "-" in self.map[i][j]:
                    self.map[i][j].pop(self.map[i][j].index("-"))
    
    def assignValue(self, value, row, col):
        if row + 1 < self.size and value not in self.map[row + 1][col]:
                self.map[row + 1][col].append(value)
        if row - 1 >= 0 and value not in self.map[row - 1][col]:
                self.map[row - 1][col].append(value)
        if col + 1 < self.size and value not in self.map[row][col + 1]:
                self.map[row][col + 1].append(value)
        if col - 1 >= 0 and value not in self.map[row][col - 1]:
                self.map[row][col - 1].append(value)
        
    def StartingStateRepresentation(self):
        return self.map, self.agentLocation, self.size

    def getObject(self, cell):
        return self.map[cell[0]][cell[1]]
    
    def AgentShoot(self, cell):
        row, col = cell
        deleteCell = []
        temp = []
        if "W" in self.map[row][col]:
            self.map[row][col].pop(self.map[row][col].index("W"))
            if len(self.map[row][col]) == 0:
                self.map[row][col].append("-")
            if row + 1 < self.size:
                self.map[row + 1][col].pop(self.map[row + 1][col].index("S"))
                if len(self.map[row + 1][col]) == 0:
                    self.map[row + 1][col].append("-")
                temp.append((row + 1, col))
            if col + 1 < self.size:
                self.map[row][col + 1].pop(self.map[row][col + 1].index("S"))
                if len(self.map[row][col + 1]) == 0:
                    self.map[row][col + 1].append("-")
                temp.append((row, col + 1))
            if row - 1 >= 0:
                self.map[row - 1][col].pop(self.map[row - 1][col].index("S"))
                if len(self.map[row - 1][col]) == 0:
                    self.map[row - 1][col].append("-")
                temp.append((row - 1, col))
            if col - 1 >= 0:
                self.map[row][col - 1].pop(self.map[row][col - 1].index("S"))
                if len(self.map[row][col - 1]) == 0:
                    self.map[row][col - 1].append("-")
                temp.append((row, col - 1))
            self.updateMap()
            for cell in temp:
                if "S" not in self.map[cell[0]][cell[1]]: 
                    deleteCell.append(cell)
            return "SCREAM", deleteCell
        return "", deleteCell
      
    def agentGrabGold(self, cell):
        row, col = cell
        deleteCell = []
        if "G" in self.map[row][col]:
            self.map[row][col].pop(self.map[row][col].index("G"))
            if len(self.map[row][col]) == 0:
                self.map[row][col].append("-")
    
    def agentGrabHP(self, cell):
        row, col = cell
        deleteCell = []
        temp = []
        if "H_P" in self.map[row][col]:
            self.map[row][col].pop(self.map[row][col].index("H_P"))
            if len(self.map[row][col]) == 0:
                self.map[row][col].append("-")
            if row + 1 < self.size:
                self.map[row + 1][col].pop(self.map[row + 1][col].index("G_L"))
                if len(self.map[row + 1][col]) == 0:
                    self.map[row + 1][col].append("-")
                temp.append((row + 1, col))
            if col + 1 < self.size:
                self.map[row][col + 1].pop(self.map[row][col + 1].index("G_L"))
                if len(self.map[row][col + 1]) == 0:
                    self.map[row][col + 1].append("-")
                temp.append((row, col + 1))
            if row - 1 >= 0:
                self.map[row - 1][col].pop(self.map[row - 1][col].index("G_L"))
                if len(self.map[row - 1][col]) == 0:
                    self.map[row - 1][col].append("-")
                temp.append((row - 1, col))
            if col - 1 >= 0:
                self.map[row][col - 1].pop(self.map[row][col - 1].index("G_L"))
                if len(self.map[row][col - 1]) == 0:
                    self.map[row][col - 1].append("-")
                temp.append((row, col - 1))
            self.updateMap()
            for cell in temp:
                if "G_L" not in self.map[cell[0]][cell[1]]: 
                    deleteCell.append(cell)
            return True, deleteCell
        return False, deleteCell
    
    
#print(Program().StartingStateRepresentation())
