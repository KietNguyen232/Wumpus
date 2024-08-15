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
        self.agentLocation = (self.start[0] + 1, self.start[1])
        self.agentDirection = DIRECTION[0]
        self.agentHP = 100
        self.gold = 0
        self.potion = 0
        self.score = 10
        self.action = []
        self.explored = []
        self.PerceptPit = []
        self.PerceptGas = []
        self.PerceptPotion = []
        self.PerceptWumpus = []
        self.unexplorePit = []
        self.unexploreGas = []
        self.unexplorePotion = []
        self.unexploreWumpus = []

        self.maxExplored = self.size * self.size
        self.countExplored = [self.start]
        self.predictMap = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.predictPath = self.DFS(self.start, self.agentDirection)

        self.countMove = 0
        
        #for fucking bullshit technique
##        self.fuckingMap = [[0 for _ in range(self.size)] for _ in range(self.size)]
##        self.fuckingAnotherMap = copy.deepcopy(self.fuckingMap)
##        self.fuckingAnotherTempMap = copy.deepcopy(self.fuckingAnotherMap)
##        self.fuckingTempScore = self.size * self.size * 100
##        self.fuckingCountMove = 0
##        self.fuckingExploreCount = self.size * self.size
##        self.fuckingRemainPath = []
##        self.fuckingRemainCountMove = 0
##        self.fuckingKnightTour(self.size - 1, 0, self.agentDirection, 0)
##        self.fuckingPredictPath = [(-1, -1) for _ in range(self.size * self.size)]
##        for i in range(self.size):
##            for j in range(self.size):
##                self.fuckingPredictPath[self.fuckingAnotherTempMap[i][j] - 1] = (i, j)
##        self.fuckingTempScore = self.size * self.size * 100
##        self.fuckingExploreCount = self.size * self.size
##        self.fuckingCountMove = 0
##        self.CurCount = self.fuckingCountMove
    
    def updatePercept(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.agentPercept[i][j] is not None:
                    self.agentPercept[i][j] = self.WumpusWorld.map[i][j]
    
    def turnRight(self):
        i = DIRECTION.index(self.agentDirection)
        self.agentDirection = DIRECTION[(i + 1) % 4]
        self.score -= 10

    def turnLeft(self):
        i = DIRECTION.index(self.agentDirection)
        self.agentDirection = DIRECTION[(i + 3) % 4]
        self.score -= 10
        
    def move(self):
        temp = self.predictPath[self.countMove]
        newDirection = (temp[0] - self.agentLocation[0], temp[1] - self.agentLocation[1])
        if newDirection != self.agentDirection:
            if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                print(self.agentLocation, 'turn right')
                self.turnRight()
            elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                print(self.agentLocation, 'turn left')
                self.turnLeft()
            elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                print(self.agentLocation, 'turn right')
                self.turnRight()
                print(self.agentLocation, 'turn right')
                self.turnRight()
        if temp[0] >= 0 and temp[0] < self.size and temp[1] >= 0 and temp[1] < self.size:
            print(self.agentLocation, 'move foward')
            self.agentLocation = temp
            self.explored.append(temp)
            if temp not in self.countExplored:
                self.countExplored.append(temp)
            self.agentPercept[temp[0]][temp[1]] = self.WumpusWorld.map[temp[0]][temp[1]]
            for item in self.WumpusWorld.map[temp[0]][temp[1]]:
                if temp not in self.KB[item]:
                    self.KB[item].append(temp)
            self.score -= 10
            return True
        return False
    
    def shoot(self):
        temp = (self.agentLocation[0] + self.agentDirection[0], self.agentLocation[1] + self.agentDirection[1])
        if temp[0] >= 0 and temp[0] < self.size and temp[1] >= 0 and temp[1] < self.size:
            self.score -= 100
            print(self.agentLocation, 'shoot')
            result, cell = self.WumpusWorld.AgentShoot(temp)
            if result == "SCREAM":
                print("SCREAM")
                self.updatePercept()
                for item in cell:   
                    if item in self.KB["S"]:
                        self.KB["S"].pop(self.KB["S"].index(item))
                    if self.agentPercept[item[0]][item[1]] == ['-']:
                        self.KB["-"].append(item)
                if len(self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]) == 1 and \
                    "-" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
                    self.KB["-"].append(self.agentLocation)
                return True
            return False
    
    def grab(self):
        if "G" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
            self.gold += 1
            self.WumpusWorld.agentGrabGold(self.agentLocation)
            self.updatePercept()
            self.KB["G"].pop(self.KB["G"].index(self.agentLocation))
            if len(self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]) == 1 and \
                "-" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
                self.KB["-"].append(self.agentLocation)
            self.score += 5000
                
        elif "H_P" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
            self.potion += 1
            status, cell = self.WumpusWorld.agentGrabHP(self.agentLocation)
            if status:
                self.updatePercept()
                for item in cell:
                    if item in self.KB["G_L"]:
                        self.KB["G_L"].pop(self.KB["G_L"].index(item))
                    if self.agentPercept[item[0]][item[1]] == ['-']:
                        self.KB["-"].append(item)
                if len( self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]) == 1 and \
                    "-" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
                    self.KB["-"].append(self.agentLocation)
            self.score -= 10
    
    def useHealingPotion(self):
        if self.potion > 0 and self.agentHP < 100:
            self.agentHP = min(100, self.agentHP + 25)
            self.potion -= 1
            self.score -= 10

    def canMoveCount(self):
        self.maxExplored = 1
        visited = {}
        visited[(self.size - 1, 0)] = (self.size - 1, 0)
        queue = [(self.size - 1, 0)]
        while queue:
            curR, curC = queue.pop(0)
            for i in range(4):
                neighborX, neighborY = (curR + DIRECTION[i][0], curC + DIRECTION[i][1])
                if neighborX < 0 or neighborX >= self.size or neighborY < 0 or neighborY >= self.size:
                    continue
                if self.predictMap[neighborX][neighborY] != -1 and (neighborX, neighborY) not in visited:
                    visited[(neighborX, neighborY)] = (curR, curC)
                    self.maxExplored += 1
                    queue.append((neighborX, neighborY))
    
    def trace(self, visited, start, end):
        path = [end]
        while path[-1] != start:
            path.append(visited[path[-1]])
        path.reverse()
        return path

    def DFS(self, start, direction):
        goal = (self.size - 1, 0)
        path = [start]
        pathExplored = copy.deepcopy(self.countExplored)
        explored = len(pathExplored)
        score = 0
        stack = [(start, explored, path, pathExplored, score, direction)]
        exploredTemp = 1
        scoreTemp = self.size * self.size * 30 * 2
        pathTemp = []
        while stack:
            (curR, curC), curE, curP, curL, curS, curD = stack.pop()
            #print((curR, curC), curE, curP, curS, curD)
            if exploredTemp >= self.maxExplored:
                if curE <= exploredTemp and curS >= scoreTemp:
                    continue
            for i in range(4):
                neighborX, neighborY = (curR + DIRECTION[i][0], curC + DIRECTION[i][1])
                if neighborX < 0 or neighborX >= self.size or neighborY < 0 or neighborY >= self.size:
                    continue
                if self.predictMap[neighborX][neighborY] < 0:
                    continue
                if (neighborX, neighborY) in curL:
                    #delete from here
                    flag = False
                    for j in range(4):
                        if j != i:
                            nX2, nY2 = (curR + DIRECTION[j][0], curC + DIRECTION[j][1])
                            if nX2 < 0 or nX2 >= self.size or nY2 < 0 or nY2 >= self.size:
                                continue
                            if self.predictMap[nX2][nY2] < 0:
                                continue
                            if (nX2, nY2) not in curL:
                                flag = True
                                break
                    if flag:
                        continue
                    #delete to here
                    NcurE = curE
                    NcurL = copy.deepcopy(curL)
                elif (neighborX, neighborY) not in curL:
                    NcurE = curE + 1
                    NcurL = copy.deepcopy(curL)
                    NcurL.append((neighborX, neighborY))
                if DIRECTION[i] == curD:
                    NcurS = curS + 10
                elif DIRECTION[i][0] * curD[0] + DIRECTION[i][1] * curD[1] == 0:
                    NcurS = curS + 20
                elif DIRECTION[i][0] + curD[0] + DIRECTION[i][1] + curD[1] == 0:
                    NcurS = curS + 30
                NcurP = copy.deepcopy(curP)
                NcurP.append((neighborX, neighborY))
                NcurD = DIRECTION[i]
                if curS <= self.size * self.size * 30:
                    if (neighborX, neighborY) == (self.size - 1, 0) and (NcurE > exploredTemp or (NcurE == exploredTemp and NcurS < scoreTemp)):
                        pathTemp = NcurP
                        exploredTemp = NcurE
                        scoreTemp = NcurS
                    if NcurE <= self.maxExplored:
                        stack.append(((neighborX, neighborY), NcurE, NcurP, NcurL, NcurS, NcurD))
        return pathTemp

    def agentLogic(self):
        self.move()
        self.countMove += 1
        self.predictMap[self.agentLocation[0]][self.agentLocation[1]] = self.countMove

        checkflag = False
        for idx in range(len(self.unexplorePit)):
            if self.agentLocation in self.unexplorePit[idx]:
                r, c = self.PerceptPit[idx][0], self.PerceptPit[idx][1]
                if not check(self.KB, "B", self.explored, P(r, c)):
                    print('check', (r, c), 'does not have pit')
                    self.unexplorePit.pop(idx)
                    self.PerceptPit.pop(idx)
                    self.predictMap[r][c] = 0
                    checkflag = True
        if checkflag:
            self.canMoveCount()
            self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
            self.countMove = 1

##        if 'P' in self.map[self.agentLocation[0]][self.agentLocation[1]] or 'W' in self.map[self.agentLocation[0]][self.agentLocation[1]] or ('P_G' in self.map[self.agentLocation[0]][self.agentLocation[1]] and self.agentHP <= 25):
        if 'P' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
            print(self.agentLocation, 'died')
            self.score -= 10000
            return False
        
        if 'G' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
            print(self.agentLocation, 'grap gold')
            self.grab()
        if 'H_P' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
            print(self.agentLocation, 'grap potion')
            self.grab()
        
##        if 'P_G' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
##            print(self.agentLocation, 'get poisoning')
##            self.agentHP -= 25
##        if self.agentHP <= 25 and self.potion > 0:
##            print(self.agentLocation, 'use healing potion')
##            self.useHealingPotion()

        if 'B' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
            for i in range(4):
                r, c = self.agentLocation[0] + DIRECTION[i][0], self.agentLocation[1] + DIRECTION[i][1]
                if r >= 0 and r < self.size and c >= 0 and c < self.size:
                    if check(self.KB, "B", self.explored, P(r, c)):
                        if (r, c) not in self.PerceptPit:
                            print('check', (r, c), 'can has pit')
                            unexplore = []
                            for u in range(2):
                                for v in range(2):
                                    if (u, v) not in self.countExplored:
                                        unexplore.append((u, v))
                            self.PerceptPit.append((r, c))
                            self.unexplorePit.append(unexplore)
                            self.predictMap[r][c] = -1
                    else:
                        if (r, c) in self.PerceptPit:
                            self.unexplorePit.pop(self.PerceptPit.index((r, c)))
                            self.PerceptPit.pop(self.PerceptPit.index((r, c)))
                            self.predictMap[r][c] = 0
            self.canMoveCount()
            self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
            self.countMove = 1

        if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
            r, c = self.predictPath[self.countMove]
            shootflag = True
            for _ in range(3):
                if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]] and not check(self.KB, 'S', self.explored, Not(W(r, c))):
                    print('check', (r, c), 'has wumpus')
                    newDirection = (r - self.agentLocation[0], c - self.agentLocation[1])
                    if newDirection != self.agentDirection:
                        if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                            print(self.agentLocation, 'turn right')
                            self.turnRight()
                        elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                            print(self.agentLocation, 'turn left')
                            self.turnLeft()
                        elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                            print(self.agentLocation, 'turn right')
                            self.turnRight()
                            print(self.agentLocation, 'turn right')
                            self.turnRight()
                    shootflag = self.shoot()
                    if shootflag == False:
                        break
                else:
                    break
            if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]] and shootflag and check(self.KB, 'S', self.explored, W(r, c)):
                if not check(self.KB, 'S', self.explored, Not(W(r, c))):
                    print('check', (r, c), 'still has wumpus')
                    self.PerceptWumpus.append((r, c))
                    self.unexploreWumpus.append([])
                    self.predictMap[r][c] = -1
                    while self.predictMap[r][c] != -1:
                        self.canMoveCount()
                        self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
                        self.countMove = 1
                        r, c = self.predictPath[self.countMove]
                        shootflag = True
                        for _ in range(3):
                            if check(self.KB, 'S', self.explored, W(r, c)):
                                print('check', (r, c), 'can has wumpus')
                                newDirection = (r - self.agentLocation[0], c - self.agentLocation[1])
                                if newDirection != self.agentDirection:
                                    if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                                        print(self.agentLocation, 'turn right')
                                        self.turnRight()
                                    elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                                        print(self.agentLocation, 'turn left')
                                        self.turnLeft()
                                    elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                                        print(self.agentLocation, 'turn right')
                                        self.turnRight()
                                        print(self.agentLocation, 'turn right')
                                        self.turnRight()
                                shootflag = self.shoot()
                                if shootflag == False:
                                    break
                            else:
                                break
                        if shootflag and check(self.KB, 'S', self.explored, W(r, c)):
                            if not check(self.KB, 'S', self.explored, Not(W(r, c))):
                                print('check', (r, c), 'still has wumpus')
                                self.PerceptWumpus.append((r, c))
                                self.unexploreWumpus.append([])
                                self.predictMap[r][c] = -1
                            else:
                                print('check', (r, c), 'can has wumpus')
                                unexplore = []
                                for u in range(2):
                                    for v in range(2):
                                        if (u, v) not in self.countExplored:
                                            unexplore.append((u, v))
                            self.PerdictWumpus.append((r, c))
                            self.unexploreWumpus.append(unexplore)
                            self.predictMap[r][c] = -1
                else:
                    for i in range(4):
                        ri, ci = self.agentLocation[0] + DIRECTION[i][0], self.agentLocation[1] + DIRECTION[i][1]
                        if ri < 0 or ri >= self.size or ci < 0 or ci >= self.size:
                            continue
                        shootflag = True
                        if (ri, ci) != (r, c):
                            if not check(self.KB, 'S', self.explored, Not(W(ri, ci))):
                                for _ in range(3):
                                    if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]] and not check(self.KB, 'S', self.explored, Not(W(ri, ci))):
                                        print('check', (ri, ci), 'has wumpus')
                                        newDirection = (ri - self.agentLocation[0], ci - self.agentLocation[1])
                                        if newDirection != self.agentDirection:
                                            if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                                                print(self.agentLocation, 'turn right')
                                                self.turnRight()
                                            elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                                                print(self.agentLocation, 'turn left')
                                                self.turnLeft()
                                            elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                                                print(self.agentLocation, 'turn right')
                                                self.turnRight()
                                                print(self.agentLocation, 'turn right')
                                                self.turnRight()
                                        shootflag = self.shoot()
                                        if shootflag == False:
                                            break
                                    else:
                                        break
                                if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]] and shootflag and not check(self.KB, 'S', self.explored, Not(W(ri, ci))):
                                    print('check', (ri, ci), 'still has wumpus')
                                    self.PerceptWumpus.append((ri, ci))
                                    self.unexploreWumpus.append([])
                    if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]] and check(self.KB, 'S', self.explored, W(r, c)):
                        shootflag = True
                        for _ in range(3):
                            if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]] and check(self.KB, 'S', self.explored, W(r, c)):
                                print('check', (r, c), 'can has wumpus')
                                newDirection = (r - self.agentLocation[0], c - self.agentLocation[1])
                                if newDirection != self.agentDirection:
                                    if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                                        print(self.agentLocation, 'turn right')
                                        self.turnRight()
                                    elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                                        print(self.agentLocation, 'turn left')
                                        self.turnLeft()
                                    elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                                        print(self.agentLocation, 'turn right')
                                        self.turnRight()
                                        print(self.agentLocation, 'turn right')
                                        self.turnRight()
                                shootflag = self.shoot()
                                if shootflag == False:
                                    break
                            else:
                                break
                        if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]] and shootflag and check(self.KB, 'S', self.explored, W(r, c)):
                            print('check', (r, c), 'can have wumpus')
                            unexplore = []
                            for u in range(2):
                                for v in range(2):
                                    if (u, v) not in self.countExplored:
                                        unexplore.append((u, v))
                            self.PerdictWumpus.append((r, c))
                            self.unexploreWumpus.append(unexplore)
                            self.predictMap[r][c] = -1
                            while self.predictMap[r][c] != -1:
                                self.canMoveCount()
                                self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
                                self.countMove = 1
                                r, c = self.predictPath[self.countMove]
                                shootflag = True
                                for _ in range(3):
                                    if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]] and check(self.KB, 'S', self.explored, W(r, c)):
                                        print('check', (r, c), 'can has wumpus')
                                        newDirection = (r - self.agentLocation[0], c - self.agentLocation[1])
                                        if newDirection != self.agentDirection:
                                            if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                                                print(self.agentLocation, 'turn right')
                                                self.turnRight()
                                            elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                                                print(self.agentLocation, 'turn left')
                                                self.turnLeft()
                                            elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                                                print(self.agentLocation, 'turn right')
                                                self.turnRight()
                                                print(self.agentLocation, 'turn right')
                                                self.turnRight()
                                        shootflag = self.shoot()
                                        if shootflag == False:
                                            break
                                    else:
                                        break
                                if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]] and shootflag and check(self.KB, 'S', self.explored, W(r, c)):
                                    if not check(self.KB, 'S', self.explored, Not(W(r, c))):
                                        print('check', (r, c), 'still has wumpus')
                                        self.PerceptWumpus.append((r, c))
                                        self.unexploreWumpus.append([])
                                        self.predictMap[r][c] = -1
                                    else:
                                        print('check', (r, c), 'can has wumpus')
                                        unexplore = []
                                        for u in range(2):
                                            for v in range(2):
                                                if (u, v) not in self.countExplored:
                                                    unexplore.append((u, v))
                                    self.PerdictWumpus.append((r, c))
                                    self.unexploreWumpus.append(unexplore)
                                    self.predictMap[r][c] = -1
                    self.canMoveCount()
                    self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
                    self.countMove = 1
            
        if self.countMove >= len(self.predictPath):
            return False
        return True

##    def fuckingKnightTour(self, fuckingRow, fuckingCol, fuckingDirection, fuckingScore):
##        if self.fuckingCountMove > self.size * self.size:
##            return
##        self.fuckingCountMove += 1
##        
##        self.fuckingAnotherMap[fuckingRow][fuckingCol] = self.fuckingCountMove
##        for i in range(4):
##            if self.size * self.size - self.fuckingCountMove <= self.fuckingExploreCount:
##                fuckingBFSPath, fuckingPrice = self.fuckingBFS(self.fuckingAnotherMap, (fuckingRow, fuckingCol), (self.size - 1, 0), fuckingDirection)
##                fuckingDistance = len(fuckingBFSPath)
##                if self.size * self.size - self.fuckingCountMove < self.fuckingExploreCount or (self.size * self.size - self.fuckingCountMove == self.fuckingExploreCount and fuckingScore + fuckingPrice < self.fuckingTempScore):
##                    self.fuckingTempScore = fuckingScore + fuckingPrice
##                    self.fuckingRemainPath = copy.deepcopy(fuckingBFSPath)
##                    self.fuckingAnotherTempMap = copy.deepcopy(self.fuckingAnotherMap)
##                    self.fuckingExploreCount = self.size * self.size - self.fuckingCountMove
##                    if self.fuckingCountMove >= self.size * self.size:
##                        self.fuckingCountMove -= 1
##                        self.fuckingAnotherMap[fuckingRow][fuckingCol] = 0
##                        return
##            fuckingNextRow = fuckingRow + DIRECTION[i][0]
##            fuckingNextCol = fuckingCol + DIRECTION[i][1]
##            if fuckingDirection == (DIRECTION[i][0], DIRECTION[i][1]):
##                fuckingNextScore = fuckingScore + 10
##            elif DIRECTION[i][0] * fuckingDirection[0] + DIRECTION[i][1] * fuckingDirection[1] == 0:
##                fuckingNextScore = fuckingScore + 20
##            elif DIRECTION[i][1] + fuckingDirection[0] + DIRECTION[i][1] + fuckingDirection[1] == 0:
##                fuckingNextScore = fuckingScore + 30
##            fuckingNextDirection = (DIRECTION[i][0], DIRECTION[i][1])
##            if fuckingNextRow >= 0 and fuckingNextRow < self.size and fuckingNextCol >= 0 and fuckingNextCol < self.size and self.fuckingAnotherMap[fuckingNextRow][fuckingNextCol] >= 0:
##                self.fuckingKnightTour(fuckingNextRow, fuckingNextCol, fuckingNextDirection, fuckingNextScore)
##        self.fuckingCountMove -= 1
##        self.fuckingAnotherMap[fuckingRow][fuckingCol] = 0
##
##    def agentLogic(self):
##        if self.fuckingCountMove >= len(self.fuckingPredictPath) and self.fuckingRemainCountMove >= len(self.fuckingRemainPath):
##            return False
##        self.move()
##        self.fuckingCountMove += 1
##        if self.fuckingCountMove >= len(self.fuckingPredictPath):
##            self.fuckingRemainCountMove += 1
##        self.fuckingMap[self.agentLocation[0]][self.agentLocation[1]] = self.fuckingCountMove
##
##        if 'G' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
##            print(self.agentLocation, 'grap gold')
##            self.grab()
##        if 'H_P' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
##            print(self.agentLocation, 'grap potion')
##            self.grab()
##            
##        if 'B' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
##            PitLoc = [0, 0, 0]
##            r, c = self.agentLocation[0] + self.agentDirection[0], self.agentLocation[1] + self.agentDirection[1]
##            if check(self.KB, "B", self.explored, P(r, c)):
##                PitLoc[0] = 1
##                if (r, c) not in self.PerceptPit:
##                    self.PerceptPit.append((r, c))
##                    self.fuckingMap[r][c] = -1
##            for turn in range(2):
##                r, c = self.agentLocation[0] + DIRECTION[(DIRECTION.index(self.agentDirection) + turn * 2 + 1) % 4][0], self.agentLocation[1] + DIRECTION[(DIRECTION.index(self.agentDirection) + turn * 2 + 1) % 4][1]
##                if r >= 0 and r < self.size and c >= 0 and c < self.size:
##                    if check(self.KB, "B", self.explored, P(r, c)):
##                        if turn == 0:
##                            PitLoc[1] = 1
##                        else:
##                            PitLoc[2] = 1
##                        if (r, c) not in self.PerceptPit:
##                            self.PerceptPit.append((r, c))
##                            self.fuckingMap[r][c] = -1
##            if not (PitLoc[0] == 0 or PitLoc == [1, 1, 1]):
##                self.fuckingAnotherMap = copy.deepcopy(self.fuckingMap)
##                self.fuckingAnotherTempMap = copy.deepcopy(self.fuckingAnotherMap)
##                self.fuckingTempScore = self.size * self.size * 100
##                self.fuckingExploreCount = self.size * self.size - self.fuckingCountMove
##                self.fuckingRemainPath = []
##                self.CurCount = self.fuckingCountMove
##                self.fuckingKnightTour(self.agentLocation[0], self.agentLocation[1], self.agentDirection, -self.score)
##                for i in range(self.size):
##                    for j in range(self.size):
##                        self.fuckingPredictPath[self.fuckingAnotherTempMap[i][j] - 1] = (i, j)
##                self.fuckingCountMove = self.CurCount
##                
##            
##        return True

##            
##        if 'G_L' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
##            r, c = self.agentLocation[0] + self.agentDirection[0], self.agentLocation[1] + self.agentDirection[1]
##            if check(self.KB, "G_L", self.explored, HP(r, c)):
##                continue
##            for turn in range(2):
##                i = DIRECTION.index(self.agentDirection)
##                r, c = DIRECTION[(i + turn * 2 + 1) % 4]
##                if check(self.KB, "G_L", self.explored, HP(r, c)):
##                    if turn == 0:
##                        self.turnRight()
##                    else:
##                        self.turnLeft()
##                    break
##            self.fuckingAnotherMap = copy.deepcopy(self.fuckingMap)
##            self.fuckingAnotherTempMap = copy.deepcopy(self.fuckingAnotherMap)
##            self.fuckingTempScore = self.size * self.size * 2
##            fuckingTempCountMove = self.fuckingCountMove
##            self.fuckingKnightTour(self.size - 1, 0, self.agentDirection, 0)
##            for i in range(self.size):
##                for j in range(self.size):
##                    self.fuckingPredictPath[self.fuckingAnotherTempMap[i][j]] = (i, j)
##            self.fuckingTempScore = self.size * self.size * 2
##            self.fuckingCountMove = fuckingTempCountMove
##        if 'S' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
##
##        if 'W_H' in self.map[self.agentLocation[0]][self.agentLocation[1]]:
    
        
        #Wumpus = check(self.KB, "S", self.explored, W(r, c))
        #Pit = check(self.KB, "B", self.explored, P(r, c))
        #Gas = check(self.KB, "W_H", self.explored, PG(r, c))            
            
            
A = Agent()

##print(A.DFS(A.fuckingMap, A.start, A.agentDirection))
##a = input()
flag = True
while flag:
    flag = A.agentLogic()
print(A.agentLocation, 'climb up')
print('score', A.score)
#print(A.KB)
print(A.agentPercept)
a = input()
