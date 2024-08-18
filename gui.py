import pygame as pg
import program
import sys
import agent 

class GUI:
    def __init__(self, map = "map1.txt") -> None:
        self.agent = agent.Agent(map)
        self.mapSize = self.agent.WumpusWorld.size
        self.screenW =  1200
        self.screenH = 800
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
            

sim = GUI("map2.txt")
sim.run()