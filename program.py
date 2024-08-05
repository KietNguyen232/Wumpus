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
                for i in range(self.size):
                    for j in range(self.size):
                        if "A" in self.map[i][j]:
                            self.map[i][j].append("-")
                            self.agentLocation = (i, j)
                        if "W" in self.map[i][j]:
                            self.assignValue("S", i, j)
                        if "P" in self.map[i][j]:
                            self.assignValue("B", i, j)
                        if "P_G" in self.map[i][j]:
                            self.assignValue("W_H", i, j)
                        if "H_P" in self.map[i][j]:
                            self.assignValue("G", i, j)
                for i in range(self.size):
                    for j in range(self.size):
                        if len(self.map[i][j]) > 1 and "-" in self.map[i][j]:
                            self.map[i][j].pop(self.map[i][j].index("-"))
        except:
            raise Exception("Invalid input file or file format!")
    
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
    
    def AgentShoot(self, cell):
        row, col = cell
        deleteCell = []
        if "W" in self.map[row][col]:
            self.map[row][col].pop(self.map[row][col].index("W"))
            if "W" in self.map[row][col]:
                return "SCREAM", deleteCell
            if row + 1 < self.size:
                self.map[row + 1][col].pop(self.map[row + 1][col].index("S"))
                if len(self.map[row + 1][col]) == 0:
                    self.map[row + 1][col].append("-")
                deleteCell.append((row + 1, col))
            if col + 1 < self.size:
                self.map[row + 1][col].pop(self.map[row][col + 1].index("S"))
                if len(self.map[row][col + 1]) == 0:
                    self.map[row][col + 1].append("-")
                deleteCell.append((row, col + 1))
            if row - 1 >= 0:
                self.map[row + 1][col].pop(self.map[row - 1][col].index("S"))
                if len(self.map[row - 1][col]) == 0:
                    self.map[row - 1][col].append("-")
                deleteCell.append((row - 1, col))
            if col - 1 >= 0:
                self.map[row + 1][col].pop(self.map[row][col - 1].index("S"))
                if len(self.map[row][col - 1]) == 0:
                    self.map[row][col - 1].append("-")
                deleteCell.append((row, col - 1))
            return "SCREAM", deleteCell
        return "", deleteCell
      
# print(Program().StartingStateRepresentation())