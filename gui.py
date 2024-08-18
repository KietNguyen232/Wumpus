import pygame as pg
import program
import sys
import agent 
map = [["-","-","-","P"],
    ["W", "G H_P", "P", "-"],
    ["-", "-", "-",'-'],
    ["A","-","P","-"]]

winW, winH = 1200,1000 


_agent =  pg.transform.scale(pg.image.load(".\img\\agent.png"), (40, 40))
_gas =  pg.transform.scale(pg.image.load(".\img\\gas.png"), (40, 40))
_healingpotion = pg.transform.scale(pg.image.load(".\img\\healingpotion.png"), (40, 40))
_goal =  pg.transform.scale(pg.image.load(".\img\\goal.png"), (40, 40))
_pit = pg.transform.scale(pg.image.load(".\img\\pit.png"), (40, 40))
_wumpus =  pg.transform.scale(pg.image.load(".\img\\wumpus.png"), (40, 40))
_stench = pg.transform.scale_by(pg.image.load(".\img\stench.png"), 0.5)
_breeze = pg.transform.scale_by(pg.image.load(".\img\\breeze.png"), 0.5)
_glow = pg.transform.scale_by(pg.image.load(".\img\glow.png"), 0.5)
_whiff = pg.transform.scale_by(pg.image.load(".\img\whiff.png"), 0.5)
_hud = pg.image.load(".\img\hud.png")

window = pg.display.set_mode((winW, winH))

images = {"P": _pit, "W": _wumpus, "G": _goal,
           "H_P": _healingpotion, "S": _stench, "G_L": _glow, 
           "W_H": _whiff, "P_G": _gas, "A": _agent, "B":_breeze}


_program = program.Program("map1.txt")
map, start, size = _program.StartingStateRepresentation()

# print(map)
cellW = 100
cellH = 100
offsetX = 400
offsetY = 0
def generateGrid():
    window.fill((0,0,0))
    gut = 4
    canvasW = size*100 + (1+size)*gut
    canvasH = size*100 + (1+size)*gut
    offsetX = (winW - canvasW)/2
    offsetY = (winH - canvasH)/2
    for i in range(size):
        for j in range(size):
            posx = gut + offsetX + j*(cellW + gut)
            posy = gut + offsetY + i*(cellH + gut) 
            pg.draw.rect(window, (255,255,255), pg.Rect(posx, posy, cellW, cellH))
    pg.display.flip()
    img = images[str("A")]
    posx = offsetX + start[1]*(cellW + 2) + (cellW - img.get_rect().size[0])/2
    posy = offsetY + start[0]*(cellH + 2) + (cellH - img.get_rect().size[1])/2
    window.blit(img,(posx, posy))
    for i in range(size):
        for j in range(size):
            items = set(map[i][j])
            items = list(items)
            items.sort()
            indent_y = 10
            indent_x = 10
            for k in range(len(items)):
                if (items[k] == '-'):
                    continue
                img = images[str(items[k])]
                posx = offsetX + j*(cellW + 2) + indent_x
                posy = offsetY + i*(cellH + 2) + indent_y
                if (k % 2 == 1):
                    indent_x = 10
                    indent_y = indent_y + images[str(items[k if k < 2 else k - 2])].get_rect().size[1] 
                else:
                    indent_x = indent_x + images[str(items[k if k < 2 else k - 2])].get_rect().size[0] 
                window.blit(img,(posx, posy))
    pg.display.flip()
    return offsetX, offsetY


def printMap(map):
    # window.blit(_hud, (0,0))
    img = images[str("A")]
    posx = offsetX + start[1]*(cellW + 2) + (cellW - img.get_rect().size[0])/2
    posy = offsetY + start[0]*(cellH + 2) + (cellH - img.get_rect().size[1])/2
    window.blit(img,(posx, posy))
    for i in range(size):
        for j in range(size):
            for k in range(len(map[i][j])):
                if (map[i][j][k] == '-'):
                    continue
                img = images[str(map[i][j][0])]
                posx = offsetX + j*(cellW + 2) + (cellW - img.get_rect().size[0])/2
                posy = offsetY + i*(cellH + 2) + (cellH - img.get_rect().size[1])/2
                window.blit(img,(posx, posy))
    pg.display.flip()
window.fill((255,255,255))
run = True
offsetX , offsetX = generateGrid()
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
# while(run):
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             run = False
#     if (not run):
#         pg.quit()
#         sys.exit()
#     pg.display.flip()
#     pg.time.Clock().tick(60)

class GUI:
    def __init__(self, map = "map1.txt") -> None:
        self.agent = agent.Agent(map)
        self.mapSize = self.agent.WumpusWorld.size
        self.screenW =  1200
        self.screenH = 1000
        self.screen = pg.display.set_mode((self.screenW, self.screenH))
        self.statusCell = [0,0,400, 200] #left, top, width, height        self.currentCell = [0,0,400, 200]
        self.currentCell = [0, 200, 400, 200]
        self.topCell = [0,400,400, 200]
        self.leftCell = [0,600,400, 200]
        self.rightCell = [400,800,400, 200]
        self.buttomCell = [800,800,400, 200]
        self.board = [400, 0, 800, 800]
        self.cellW = 80
        self.cellH = 80
        self._agent =  [pg.transform.scale(pg.image.load(".\img\\agent_up.png"), (70, 70)), 
                        pg.transform.scale(pg.image.load(".\img\\agent_right.png"), (70, 70)), 
                        pg.transform.scale(pg.image.load(".\img\\agent_down.png"), (70, 70)), 
                        pg.transform.scale(pg.image.load(".\img\\agent_left.png"), (70, 70)),
                        pg.transform.scale(pg.image.load(".\img\\agent_pass.png"), (70, 70))]
        self._gas =  pg.transform.scale(pg.image.load(".\img\\gas.png"), (40, 40))
        self._healingpotion = pg.transform.scale(pg.image.load(".\img\\healingpotion.png"), (40, 40))
        self._goal =  pg.transform.scale(pg.image.load(".\img\\goal.png"), (40, 40))
        self._pit = pg.transform.scale(pg.image.load(".\img\\pit.png"), (40, 40))
        self._wumpus =  pg.transform.scale(pg.image.load(".\img\\wumpus.png"), (40, 40))
        self._stench = pg.transform.scale_by(pg.image.load(".\img\stench.png"), 0.5)
        self._breeze = pg.transform.scale_by(pg.image.load(".\img\\breeze.png"), 0.5)
        self._glow = pg.transform.scale_by(pg.image.load(".\img\glow.png"), 0.5)
        self._whiff = pg.transform.scale_by(pg.image.load(".\img\whiff.png"), 0.5)
        self._hud = pg.image.load(".\img\hud.png")
    def getAgentPicture(self, direction:tuple):
        match direction:
            case (-1, 0):
                return self._agent[0]

            case (0, 1):
                return self._agent[1]
            case (1, 0):
                return self._agent[2]
            case (0, -1):
                return self._agent[3]
        return self._agent[4]
    def drawAgent(self, location:tuple, direction:tuple):
        agentImage = self.getAgentPicture(direction)
        posx = self.board[0] + location[1]*(self.cellW) + (self.cellW - agentImage.get_rect().size[0])/2
        posy = self.board[1] + location[0]*(self.cellH) + (self.cellH - agentImage.get_rect().size[1])/2
        self.screen.blit(agentImage, (posx,posy))
        pg.display.flip()
    def run(self): 
        run = True
        flag = True
        actionListIndex = 0
        self.screen.blit(self._hud, (0,0))
        self.agent.agentLogic()
        # agentPercept, agentLocation, agentDirection, score, agentHP, gold, potion, action 
        actionList = []
        # print (actionList[0][1], actionList[0][2])
        # self.drawAgent(actionList[0][1], actionList[0][2])
        oldPos = (-1, -1)
        while(run):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            if (not run):
                pg.quit()
                sys.exit()
            if actionListIndex >= len(actionList):
                flag = self.agent.agentLogic()
                if not flag:
                    return
                actionList = self.agent.action
                actionListIndex = 0
            else:
                agentPos = actionList[actionListIndex][1]
                try:
                    print("top: ", actionList[actionListIndex][0][agentPos[0] -1 ][agentPos[1]])
                except:
                    print("out of range")    
                try:
                    print("right: ", actionList[actionListIndex][0][agentPos[0]][agentPos[1] + 1])
                except:
                    print("out of range")    
                try:
                    print("left: ", actionList[actionListIndex][0][agentPos[0] ][agentPos[1] -1])
                except:
                    print("out of range")    
                try:
                    print("bottom: ", actionList[actionListIndex][0][agentPos[0] +1 ][agentPos[1]])
                except:
                    print("out of range")    
                print(actionList[actionListIndex][0][agentPos[0]][agentPos[1]])
                print("===================================")
                if oldPos !=  (-1,-1):
                    self.drawAgent(oldPos, (-1, -1))
                self.drawAgent(actionList[actionListIndex][1], actionList[actionListIndex][2])
                oldPos = actionList[actionListIndex][1]
                actionListIndex += 1
            pg.display.flip()
            pg.time.Clock().tick(8)
            

sim = GUI()
sim.run()