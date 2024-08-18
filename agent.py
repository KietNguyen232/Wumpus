from program import Program
from logic import *

DIRECTION = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Agent:
    def __init__(self, inputFile="map2.txt"):
        self.WumpusWorld = Program(inputFile)
        _, self.start, self.size = self.WumpusWorld.StartingStateRepresentation()
        self.agentPercept = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.agentPercept[self.start[0]][self.start[1]] = self.WumpusWorld.getObject(self.start)
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
        for item in self.WumpusWorld.getObject(self.start):
            self.KB[item].append(self.start)
        self.agentLocation = (self.start[0] + 1, self.start[1])
        self.agentDirection = DIRECTION[0]
        self.agentHP = 100
        self.gold = 0
        self.potion = 0
        self.score = 10
        self.action = []
        self.perceptStatus = False
        self.explored = [self.start]
        self.PerceptPit = []
        self.PerceptGas = []
        self.PerceptPotion = []
        self.PerceptWumpus = []
        self.unexplorePit = []
        self.unexploreGas = []
        self.unexplorePotion = []
        self.unexploreWumpus = []
        self.potemp = []
        
        self.maxExplored = self.size * self.size
        self.predictMap = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.predictPath = self.DFS(self.start, self.agentDirection)

        self.countMove = 0        
    
    def updatePercept(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.agentPercept[i][j] is not None:
                    self.agentPercept[i][j] = self.WumpusWorld.getObject((i, j))
                    
    def addAction(self, action):
        self.action.append((self.agentPercept, self.agentLocation, self.agentDirection, self.score, self.agentHP, self.gold, self.potion, action))
        
    def turnRight(self):
        self.addAction('turn right')
        i = DIRECTION.index(self.agentDirection)
        self.agentDirection = DIRECTION[(i + 1) % 4]
        self.score -= 10

    def turnLeft(self):
        self.addAction('turn left')
        i = DIRECTION.index(self.agentDirection)
        self.agentDirection = DIRECTION[(i + 3) % 4]
        self.score -= 10
        
    def move(self):
        temp = self.predictPath[self.countMove]
        newDirection = (temp[0] - self.agentLocation[0], temp[1] - self.agentLocation[1])
        if newDirection != self.agentDirection:
            if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                self.turnRight()
            elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                self.turnLeft()
            elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                self.turnRight()
                self.turnRight()
        if temp[0] >= 0 and temp[0] < self.size and temp[1] >= 0 and temp[1] < self.size:
            self.addAction('move foward')
            self.agentLocation = temp
            if temp not in self.explored:
                self.explored.append(temp)
                self.agentPercept[temp[0]][temp[1]] = self.WumpusWorld.getObject(temp)
                for item in self.WumpusWorld.getObject(temp):
                    self.KB[item].append(temp)
            self.score -= 10
            return True
        return False
    
    def shoot(self):
        temp = (self.agentLocation[0] + self.agentDirection[0], self.agentLocation[1] + self.agentDirection[1])
        if temp[0] >= 0 and temp[0] < self.size and temp[1] >= 0 and temp[1] < self.size:
            self.score -= 100
            self.addAction('shoot')
            result, cell = self.WumpusWorld.AgentShoot(temp)
            if result == "SCREAM":
                self.addAction('SCREAM')
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
            self.addAction('grap gold')
            self.gold += 1
            self.WumpusWorld.agentGrabGold(self.agentLocation)
            self.updatePercept()
            self.KB["G"].pop(self.KB["G"].index(self.agentLocation))
            if len(self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]) == 1 and \
                "-" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
                self.KB["-"].append(self.agentLocation)
            self.score += 5000
                
        elif "H_P" in self.agentPercept[self.agentLocation[0]][self.agentLocation[1]]:
            self.addAction('grap potion')
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
            self.addAction('use healing potion')
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
                if self.predictMap[neighborX][neighborY] >= 0 and (neighborX, neighborY) not in visited:
                    visited[(neighborX, neighborY)] = (curR, curC)
                    self.maxExplored += 1
                    queue.append((neighborX, neighborY))
    
    def trace(self, visited, start, end):
        path = [end]
        while path[-1] != start:
            path.append(visited[path[-1]][0])
        path.reverse()
        return path

    def BFS(self, start, end, direction, agentHP, agentPotion):
        if start == end:
            return [start], 0, agentHP, agentPotion
        
        visited = {} 
        visited[start] = (start, 0)
        queue = [(start, 0, direction, agentHP, agentPotion)]
        
        scoreTemp = self.size * self.size * 30 * 2
        pathTemp = [start]
        hpTemp = 0
        poTemp = 0
        while queue:
            (curR, curC), curS, curD, curH, curO = queue.pop(0)
            for i in range(4):
                neighborX, neighborY = (curR + DIRECTION[i][0], curC + DIRECTION[i][1])
                if neighborX < 0 or neighborX >= self.size or neighborY < 0 or neighborY >= self.size:
                    continue
                if DIRECTION[i] == curD:
                    NcurS = curS + 10
                elif DIRECTION[i][0] * curD[0] + DIRECTION[i][1] * curD[1] == 0:
                    NcurS = curS + 20
                elif DIRECTION[i][0] + curD[0] + DIRECTION[i][1] + curD[1] == 0:
                    NcurS = curS + 30
                if (neighborX, neighborY) in self.PerceptGas:
                    if curO > 0 and curH <= 50:
                        NcurO = curO - 1
                        NcurH = curH
                        NcurS -= 10
                    else:
                        NcurH = curH - 25
                        NcurO = curO
                else:
                    NcurH = curH
                    NcurO = curO
                if NcurH <= 0:
                    continue
                NcurD = DIRECTION[i]
                if self.predictMap[neighborX][neighborY] >= 0 and ((neighborX, neighborY) not in visited or (neighborX, neighborY) in visited and NcurS < visited[(neighborX, neighborY)][1]):
                    visited[(neighborX, neighborY)] = ((curR, curC), NcurS)
                    if (neighborX, neighborY) == end:
                        if NcurS < scoreTemp:
                            pathTemp = self.trace(visited, start, end)
                            scoreTemp = NcurS
                            hpTemp = NcurH
                            poTemp = NcurO
                    queue.append(((neighborX, neighborY), NcurS, NcurD, NcurH, NcurO))
        return pathTemp, scoreTemp, hpTemp, poTemp

    def DFS(self, start, direction):
        goal = (self.size - 1, 0)
        unexplored = []
        for i in range(self.size):
            for j in range(self.size):
                if self.predictMap[i][j] == 0:
                    unexplored.append((i, j))
        path = [start]
        pathExplored = copy.deepcopy(self.explored)
        explored = len(pathExplored)
        score = 0
        level = 0
        agentHP = self.agentHP
        agentPotion = self.potion
        stack = [(start, explored, path, pathExplored, unexplored, score, direction, agentHP, agentPotion, level)]
        exploredTemp = 1
        scoreTemp = self.size * self.size * 30 * 2
        pathTemp = []
        while stack:
            #print(len(stack))
            (curR, curC), curE, curP, curL, curU, curS, curD, curH, curO, curT = stack.pop(0)
##            print((curR, curC), curE, curP, curL, curS, curD, curH, curO)
            breakflag = False
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
                    NcurU = copy.deepcopy(curU)
                    if len(NcurU) != 0:
                        tScore = self.size * self.size * 30 * 2
                        tPath = []
                        tHP = curH
                        tPotion = curO
                        for Nunexplore in NcurU:
                            NPath, NScore, NHP, NPotion = self.BFS((curR, curC), Nunexplore, curD, curH, curO)
                            if NHP <= 0:
                                continue
                            if NScore < tScore:
                                tPath = NPath
                                tScore = NScore
                                tHP = NHP
                                tPotion = NPotion
                        if tPath != []:
                            neighborX, neighborY = tPath[-1]
                            NcurL = copy.deepcopy(curL)
                            NcurL.append(tPath[-1])
                            NcurE = curE + 1
                            NcurD = (tPath[-1][0] - tPath[-2][0], tPath[-1][1] - tPath[-2][1])
                            NcurP = copy.deepcopy(curP)
                            NcurP.pop()
                            NcurP += tPath
                            NcurS = curS + tScore
                            NcurU.pop(NcurU.index(tPath[-1]))
                            NcurT = len(NcurP) - 1
                            stack.append(((neighborX, neighborY), NcurE, NcurP, NcurL, NcurU, NcurS, NcurD, tHP, tPotion, NcurT))
                            breakflag = True
                            break
                    NcurE = curE
                    NcurL = copy.deepcopy(curL)
                elif (neighborX, neighborY) not in curL:
                    NcurE = curE + 1
                    NcurL = copy.deepcopy(curL)
                    NcurL.append((neighborX, neighborY))
                    NcurU = copy.deepcopy(curU)
                    NcurU.pop(NcurU.index((neighborX, neighborY)))
                    breakflag = True
                if DIRECTION[i] == curD:
                    NcurS = curS + 10
                elif DIRECTION[i][0] * curD[0] + DIRECTION[i][1] * curD[1] == 0:
                    NcurS = curS + 20
                elif DIRECTION[i][0] + curD[0] + DIRECTION[i][1] + curD[1] == 0:
                    NcurS = curS + 30
                if (neighborX, neighborY) in self.PerceptGas:
                    if curO > 0 and curH <= 50:
                        NcurO = curO - 1
                        NcurH = curH
                        NcurS -= 10
                    else:
                        NcurH = curH - 25
                        NcurO = curO
                else:
                    NcurH = curH
                    NcurO = curO
                if NcurH <= 0:
                    continue
                NcurT = curT + 1
                NcurP = copy.deepcopy(curP)
                NcurP.append((neighborX, neighborY))
                NcurD = DIRECTION[i]
                if NcurE >= self.maxExplored:
                    remainPath, remainScore, remainHP, remainPotion = self.BFS((neighborX, neighborY), (self.size - 1, 0), NcurD, NcurH, NcurO)
                    NcurP.pop()
                    NcurP += remainPath
                    NcurS += remainScore
                    neighborX, neighborY = NcurP[-1]
                    NcurH = remainHP
                    NcurO = remainPotion
                if NcurH <= 0:
                    continue
                if NcurS <= self.maxExplored * 30:
                    if (neighborX, neighborY) == (self.size - 1, 0) and (NcurE > exploredTemp or (NcurE == exploredTemp and NcurS < scoreTemp)):
                        pathTemp = NcurP
                        exploredTemp = NcurE
                        scoreTemp = NcurS
##                        if NcurE == self.maxExplored:
##                            return pathTemp
                    if NcurE < self.maxExplored:
                        stack.append(((neighborX, neighborY), NcurE, NcurP, NcurL, NcurU, NcurS, NcurD, NcurH, NcurO, NcurT))
                    if breakflag:
                        delt = []
                        for st in range(len(stack)):
                            if stack[st][9] <= curT and stack[st][5] > curS:
                                delt.append(st)
                        delt.reverse()
                        for i in delt:
                            stack.pop(i)
##                        break
        return pathTemp

    def agentLogic(self):
        self.action = []
        self.move()
        self.countMove += 1
        self.predictMap[self.agentLocation[0]][self.agentLocation[1]] = self.countMove

        checkflag = False
        rev = []
        for idx in range(len(self.unexplorePit)):
            if self.agentLocation in self.unexplorePit[idx]:
                r, c = self.PerceptPit[idx][0], self.PerceptPit[idx][1]
                if not check(self.KB, "B", self.explored, P(r, c)):
                    if self.perceptStatus:
                        self.addAction(f'check {(r, c)} do not have pit')
                    rev.append(idx)
                    self.predictMap[r][c] += 1
                    checkflag = True
                else:
                    self.unexplorePit[idx].pop(self.unexplorePit[idx].index(self.agentLocation))
        rev.reverse()
        for idx in range(len(rev)):
            self.unexplorePit.pop(rev[idx])
            self.PerceptPit.pop(rev[idx])
        if checkflag:
            self.canMoveCount()
            self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
            self.countMove = 1

        checkflag = False
        rev = []
        for idx in range(len(self.unexploreWumpus)):
            if self.agentLocation in self.unexploreWumpus[idx]:
                r, c = self.PerceptWumpus[idx][0], self.PerceptWumpus[idx][1]
                if not check(self.KB, "S", self.explored, W(r, c)):
                    if self.perceptStatus:
                        self.addAction(f'check {(r, c)} do not have wumpus')
                    rev.append(idx)
                    self.predictMap[r][c] += 1
                    checkflag = True
                else:
                    self.unexploreWumpus[idx].pop(self.unexploreWumpus[idx].index(self.agentLocation))
        rev.reverse()
        for idx in range(len(rev)):
            self.unexploreWumpus.pop(rev[idx])
            self.PerceptWumpus.pop(rev[idx])
        if checkflag:
            self.canMoveCount()
            self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
            self.countMove = 1

        checkflag = False
        rev = []
        for idx in range(len(self.unexploreGas)):
            if self.agentLocation in self.unexploreGas[idx]:
                r, c = self.PerceptGas[idx][0], self.PerceptGas[idx][1]
                if (r, c) in self.KB['P_G']:
                    if self.perceptStatus:
                        self.addAction(f'check {(r, c)} have poison gas')
                    self.unexploreGas[idx] = []
                else:
                    if not check(self.KB, "W_H", self.explored, PG(r, c)):
                        if self.perceptStatus:
                            self.addAction(f'check {(r, c)} do not have poison gas')
                        rev.append(idx)
                        checkflag = True
                    else:
                        self.unexploreGas[idx].pop(self.unexploreGas[idx].index(self.agentLocation))
        rev.reverse()
        for idx in range(len(rev)):
            self.unexploreGas.pop(rev[idx])
            self.PerceptGas.pop(rev[idx])
        if checkflag:
            self.canMoveCount()
            self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
            self.countMove = 1
        
        if len(self.potemp) > 0:
            for _ in range(len(self.potemp)):
                rev = self.potemp.pop()
                self.predictMap[rev[0]][rev[1]] += 1
            self.canMoveCount()
            self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
            self.countMove = 1

        if 'P' in self.WumpusWorld.getObject(self.agentLocation) or 'W' in self.WumpusWorld.getObject(self.agentLocation) or ('P_G' in self.WumpusWorld.getObject(self.agentLocation) and self.agentHP <= 25):
            self.addAction('died')
            self.score -= 10000
            return False
        
        if 'G' in self.WumpusWorld.getObject(self.agentLocation):
            self.grab()
        if 'H_P' in self.WumpusWorld.getObject(self.agentLocation):
            self.grab()
        
        if 'P_G' in self.WumpusWorld.getObject(self.agentLocation):
            self.addAction('get poisoning')
            self.agentHP -= 25
        if self.agentHP <= 25 and self.potion > 0:
            self.useHealingPotion()

        if 'B' in self.WumpusWorld.getObject(self.agentLocation):
            changeflag = False
            for i in range(4):
                r, c = self.agentLocation[0] + DIRECTION[i][0], self.agentLocation[1] + DIRECTION[i][1]
                if r >= 0 and r < self.size and c >= 0 and c < self.size:
                    if (r, c) in self.explored:
                        continue
                    if not check(self.KB, 'B', self.explored, Not(P(r, c))):
                        if (r, c) not in self.PerceptPit:
                            if self.perceptStatus:
                                self.addAction(f'check {(r, c)} have pit')
                            changeflag = True
                            self.PerceptPit.append((r, c))
                            self.unexplorePit.append([])
                            self.predictMap[r][c] = min(self.predictMap[r][c] - 1, -1)
                    elif check(self.KB, "B", self.explored, P(r, c)):
                        if (r, c) not in self.PerceptPit:
                            if self.perceptStatus:
                                self.addAction(f'check {(r, c)} may have pit')
                            changeflag = True
                            unexplore = []
                            for u in range(-2, 3):
                                for v in range(-2, 3):
                                    if r + u < 0 or r + u >= self.size or c + v < 0 or c + v >= self.size:
                                        continue
                                    if (r + u, c + v) not in self.explored:
                                        unexplore.append((r + u, c + v))
                            self.PerceptPit.append((r, c))
                            self.unexplorePit.append(unexplore)
                            self.predictMap[r][c] = min(self.predictMap[r][c] - 1, -1)
            if changeflag:
                    self.canMoveCount()
                    self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
                    self.countMove = 1

        if 'G_L' in self.WumpusWorld.getObject(self.agentLocation):
            r0, c0 = self.predictPath[self.countMove]
            r1, c1 = self.agentLocation[0] + self.agentDirection[0], self.agentLocation[1] + self.agentDirection[1]
            if r1 < 0 or r1 >= self.size or c1 < 0 or c1 > self.size:
                r1, c1 = r0, c0
            r2, c2 = self.agentLocation[0] + DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4][0], self.agentLocation[1] + DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4][1]
            if r2 < 0 or r2 >= self.size or c2 < 0 or c2 > self.size:
                r2, c2 = r0, c0
            r3, c3 = self.agentLocation[0] + DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4][0], self.agentLocation[1] + DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4][1]
            if r3 < 0 or r3 >= self.size or c3 < 0 or c3 > self.size:
                r3, c3 = r0, c0
            r, c = [r0, r1, r2, r3], [c0, c1, c2, c3]
            PoGu = [[0, 0, 0, 0], [0, 0, 0, 0]]
            for i in range(4):
                if not check(self.KB, 'G_L', self.explored, Not(HP(r[i], c[i]))):
                    PoGu[0][i] = 1
                if check(self.KB, 'G_L', self.explored, HP(r[i], c[i])):
                    PoGu[1][i] = 1
            changeflag = False
            if PoGu[0][0] == 0 and (PoGu[0][1] == 1 or PoGu[0][2] == 1 or PoGu[0][3] == 1):
                changeflag = True
                if PoGu[0][1] == 0:
                    self.predictMap[r1][c1] = min(self.predictMap[r1][c1] - 1, -1)
                    self.potemp.append((r1, c1))
                else:
                    if self.perceptStatus:
                        self.addAction(f'check {(r[1], c[1])} have potion')
                if PoGu[0][2] == 0:
                    self.predictMap[r2][c2] = min(self.predictMap[r2][c2] - 1, -1)
                    self.potemp.append((r2, c2))
                else:
                    if self.perceptStatus:
                        self.addAction(f'check {(r[2], c[2])} have potion')
                if PoGu[0][3] == 0:
                    self.predictMap[r3][c3] = min(self.predictMap[r3][c3] - 1, -1)
                    self.potemp.append((r3, c3))
                else:
                    if self.perceptStatus:
                        self.addAction(f'check {(r[3], c[3])} have potion')
            elif PoGu[0][0] == 0 and PoGu[0][1] == 0 and PoGu[0][2] == 0 and PoGu[0][3] == 0:
                if PoGu[1][0] == 0 and (PoGu[1][1] == 1 or PoGu[1][2] == 1 or PoGu[1][3] == 1):
                    changeflag = True
                    if PoGu[1][1] == 0:
                        self.predictMap[r1][c1] = min(self.predictMap[r1][c1] - 1, -1)
                        self.potemp.append((r1, c1))
                    else:
                        if self.perceptStatus:
                            self.addAction(f'check {(r[1], c[1])} may have potion')
                    if PoGu[1][2] == 0:
                        self.predictMap[r2][c2] = min(self.predictMap[r2][c2] - 1, -1)
                        self.potemp.append((r2, c2))
                    else:
                        if self.perceptStatus:
                            self.addAction(f'check {(r[2], c[2])} may have potion')
                    if PoGu[1][3] == 0:
                        self.predictMap[r3][c3] = min(self.predictMap[r3][c3] - 1, -1)
                        self.potemp.append((r3, c3))
                    else:
                        if self.perceptStatus:
                            self.addAction(f'check {(r[3], c[3])} may have potion')
            else:
                if self.perceptStatus:
                    self.addAction(f'check {(r[0], c[0])} may have potion')
            if changeflag:
                self.canMoveCount()
                self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
                self.countMove = 1

        if 'W_H' in self.WumpusWorld.getObject(self.agentLocation):
            changeflag = False
            for i in range(4):
                r, c = self.agentLocation[0] + DIRECTION[i][0], self.agentLocation[1] + DIRECTION[i][1]
                if r >= 0 and r < self.size and c >= 0 and c < self.size:
                    if (r, c) in self.explored:
                        continue
                    if not check(self.KB, 'W_H', self.explored, Not(PG(r, c))):
                        if (r, c) not in self.PerceptGas:
                            if self.perceptStatus:
                                self.addAction(f'check {(r, c)} have poison gas')
                            changeflag = True
                            self.PerceptGas.append((r, c))
                            self.unexploreGas.append([])
                    elif check(self.KB, "W_H", self.explored, PG(r, c)):
                        if (r, c) not in self.PerceptGas:
                            if self.perceptStatus:
                                self.addAction(f'check {(r, c)} may have poison gas')
                            changeflag = True
                            unexplore = []
                            for u in range(-2, 3):
                                for v in range(-2, 3):
                                    if r + u < 0 or r + u >= self.size or c + v < 0 or c + v >= self.size:
                                        continue
                                    if (r + u, c + v) not in self.explored:
                                        unexplore.append((r + u, c + v))
                            self.PerceptGas.append((r, c))
                            self.unexploreGas.append(unexplore)
            if changeflag:
                    self.canMoveCount()
                    self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
                    self.countMove = 1
        
        if 'S' in self.WumpusWorld.getObject(self.agentLocation):
            r, c = self.predictPath[self.countMove]
            shootflag = True
            for _ in range(3):
                if 'S' in self.WumpusWorld.getObject(self.agentLocation) and not check(self.KB, 'S', self.explored, Not(W(r, c))):
                    if self.perceptStatus:
                        self.addAction(f'check {(r, c)} have wumpus')
                    newDirection = (r - self.agentLocation[0], c - self.agentLocation[1])
                    if newDirection != self.agentDirection:
                        if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                            self.turnRight()
                        elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                            self.turnLeft()
                        elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                            self.turnRight()
                            self.turnRight()
                    shootflag = self.shoot()
                    if shootflag == False:
                        break
                else:
                    break
            if 'S' in self.WumpusWorld.getObject(self.agentLocation) and shootflag and check(self.KB, 'S', self.explored, W(r, c)):
                if not check(self.KB, 'S', self.explored, Not(W(r, c))):
                    if self.perceptStatus:
                        self.addAction(f'check {(r, c)} still have wumpus')
                    self.PerceptWumpus.append((r, c))
                    self.unexploreWumpus.append([])
                    self.predictMap[r][c] = min(self.predictMap[r][c] - 1, -1)
                    while self.predictMap[r][c] != -1:
                        self.canMoveCount()
                        self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
                        self.countMove = 1
                        r, c = self.predictPath[self.countMove]
                        if (r, c) in self.explored:
                            break
                        shootflag = True
                        for _ in range(3):
                            if check(self.KB, 'S', self.explored, W(r, c)):
                                if self.perceptStatus:
                                    self.addAction(f'check {(r, c)} may have wumpus')
                                newDirection = (r - self.agentLocation[0], c - self.agentLocation[1])
                                if newDirection != self.agentDirection:
                                    if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                                        self.turnRight()
                                    elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                                        self.turnLeft()
                                    elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                                        self.turnRight()
                                        self.turnRight()
                                shootflag = self.shoot()
                                if shootflag == False:
                                    break
                            else:
                                break
                        if shootflag and check(self.KB, 'S', self.explored, W(r, c)):
                            if not check(self.KB, 'S', self.explored, Not(W(r, c))):
                                if self.perceptStatus:
                                    self.addAction(f'check {(r, c)} still have wumpus')
                                self.PerceptWumpus.append((r, c))
                                self.unexploreWumpus.append([])
                                self.predictMap[r][c] = min(self.predictMap[r][c] - 1, -1)
                            else:
                                if self.perceptStatus:
                                    self.addAction(f'check {(r, c)} may have wumpus')
                                unexplore = []
                                for u in range(-2, 3):
                                    for v in range(-2, 3):
                                        if r + u < 0 or r + u >= self.size or c + v < 0 or c + v >= self.size:
                                            continue
                                        if (r + u, c + v) not in self.explored:
                                            unexplore.append((r + u, c + v))
                            self.PerdictWumpus.append((r, c))
                            self.unexploreWumpus.append(unexplore)
                            self.predictMap[r][c] = min(self.predictMap[r][c] - 1, -1)
                else:
                    for i in range(4):
                        ri, ci = self.agentLocation[0] + DIRECTION[i][0], self.agentLocation[1] + DIRECTION[i][1]
                        if ri < 0 or ri >= self.size or ci < 0 or ci >= self.size:
                            continue
                        if (ri, ci) in self.explored:
                            continue
                        shootflag = True
                        if (ri, ci) != (r, c):
                            if not check(self.KB, 'S', self.explored, Not(W(ri, ci))):
                                for _ in range(3):
                                    if 'S' in self.WumpusWorld.getObject(self.agentLocation) and not check(self.KB, 'S', self.explored, Not(W(ri, ci))):
                                        if self.perceptStatus:
                                            self.addAction(f'check {(ri, ci)} have wumpus')
                                        newDirection = (ri - self.agentLocation[0], ci - self.agentLocation[1])
                                        if newDirection != self.agentDirection:
                                            if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                                                self.turnRight()
                                            elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                                                self.turnLeft()
                                            elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                                                self.turnRight()
                                                self.turnRight()
                                        shootflag = self.shoot()
                                        if shootflag == False:
                                            break
                                    else:
                                        break
                                if 'S' in self.WumpusWorld.getObject(self.agentLocation) and shootflag and not check(self.KB, 'S', self.explored, Not(W(ri, ci))):
                                    if self.perceptStatus:
                                        self.addAction(f'check {(ri, ci)} still have wumpus')
                                    self.PerceptWumpus.append((ri, ci))
                                    self.unexploreWumpus.append([])
                                    self.predictMap[ri][ci] = min(self.predictMap[ri][ci] - 1, -1)
                    if 'S' in self.WumpusWorld.getObject(self.agentLocation) and check(self.KB, 'S', self.explored, W(r, c)):
                        shootflag = True
                        for _ in range(3):
                            if 'S' in self.WumpusWorld.getObject(self.agentLocation) and check(self.KB, 'S', self.explored, W(r, c)):
                                if self.perceptStatus:
                                    self.addAction(f'check {(r, c)} may have wumpus')
                                newDirection = (r - self.agentLocation[0], c - self.agentLocation[1])
                                if newDirection != self.agentDirection:
                                    if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                                        self.turnRight()
                                    elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                                        self.turnLeft()
                                    elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                                        self.turnRight()
                                        self.turnRight()
                                shootflag = self.shoot()
                                if shootflag == False:
                                    break
                            else:
                                break
                        if 'S' in self.WumpusWorld.getObject(self.agentLocation) and shootflag and check(self.KB, 'S', self.explored, W(r, c)):
                            if self.perceptStatus:
                                self.addAction(f'check {(r, c)} may have wumpus')
                            unexplore = []
                            for u in range(-2, 3):
                                for v in range(-2, 3):
                                    if r + u < 0 or r + u >= self.size or c + v < 0 or c + v >= self.size:
                                        continue
                                    if (r + u, c + v) not in self.explored:
                                        unexplore.append((r + u, c + v))
                            self.PerdictWumpus.append((r, c))
                            self.unexploreWumpus.append(unexplore)
                            self.predictMap[r][c] = min(self.predictMap[r][c] - 1, -1)
                            while self.predictMap[r][c] >= 0:
                                self.canMoveCount()
                                self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
                                self.countMove = 1
                                r, c = self.predictPath[self.countMove]
                                if (r, c) in self.explored:
                                    break
                                shootflag = True
                                for _ in range(3):
                                    if 'S' in self.WumpusWorld.getObject(self.agentLocation) and check(self.KB, 'S', self.explored, W(r, c)):
                                        if self.perceptStatus:
                                            self.addAction(f'check {(r, c)} may have wumpus')
                                        newDirection = (r - self.agentLocation[0], c - self.agentLocation[1])
                                        if newDirection != self.agentDirection:
                                            if newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 1) % 4]:
                                                self.turnRight()
                                            elif newDirection == DIRECTION[(DIRECTION.index(self.agentDirection) + 3) % 4]:
                                                self.turnLeft()
                                            elif newDirection[0] + newDirection[1] + self.agentDirection[0] + self.agentDirection[1] == 0:
                                                self.turnRight()
                                                self.turnRight()
                                        shootflag = self.shoot()
                                        if shootflag == False:
                                            break
                                    else:
                                        break
                                if 'S' in self.WumpusWorld.getObject(self.agentLocation) and shootflag and check(self.KB, 'S', self.explored, W(r, c)):
                                    if not check(self.KB, 'S', self.explored, Not(W(r, c))):
                                        if self.perceptStatus:
                                            self.addAction(f'check {(r, c)} still have wumpus')
                                        self.PerceptWumpus.append((r, c))
                                        self.unexploreWumpus.append([])
                                        self.predictMap[r][c] = min(self.predictMap[r][c] - 1, -1)
                                    else:
                                        if self.perceptStatus:
                                            self.addAction(f'check {(r, c)} may have wumpus')
                                        unexplore = []
                                        for u in range(-2, 3):
                                            for v in range(-2, 3):
                                                if r + u < 0 or r + u >= self.size or c + v < 0 or c + v >= self.size:
                                                    continue
                                                if (r + u, c + v) not in self.explored:
                                                    unexplore.append((r + u, c + v))
                                    self.PerdictWumpus.append((r, c))
                                    self.unexploreWumpus.append(unexplore)
                                    self.predictMap[r][c] = min(self.predictMap[r][c] - 1, -1)
##                    self.canMoveCount()
##                    self.predictPath = self.DFS(self.agentLocation, self.agentDirection)
##                    self.countMove = 1
        if self.countMove >= len(self.predictPath):
            self.addAction('climb up')
            return False
        return True           


#for show map
#Agent.agentPercept: map that already explored
#Agent.WumpusWorld.map: entire map

#for get action
#Agent.action: list of actions/stats in 1 loop
    #please skip the first loop, see example
    #format of list: (agentPercept, agentLocation, agentDirection, score, agentHP, gold, potion, action), stats detail below
    #list of action: move foward, turn right, turn left, shoot, grap gold, grap potion, use healing potion, get poisoning, die, climb up
        #special action: SCREAM
#Agent.perceptStatus: set = True if want to add agent predict into action list, otherwise set = False. Default value: False

#for get specific stat
    #can only get stats before or after 1 loop, note that there can have many actions in 1 loop
#Agent.agentLocation: current location
#Agent.agentDirection: current direction
#Agent.score: current score
#Agent.agentHP: current HP
#Agent.gold: number of gold
#Agent.potion: number of healing potion

#example of using this stupid program:
##stats = ['map explored:', 'agentLocation:', 'agentDirection:', 'score:', 'agentHP:', 'gold:', 'potion:', 'action:']
##A = Agent()
##A.agentLogic() #skip this
##flag = True
##while flag:
##    #A.perceptStatus = True #use as you wish
##    flag = A.agentLogic()
##    for action in A.action:
##        for stat in range(8):
##            print(stats[stat], action[stat])
##        print('========================================')
##a = input()
