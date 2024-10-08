import pygame as pg
import program
import sys
import agent 
from copy import deepcopy
pg.font.init()
pg.display.init()
class GUI:
    def __init__(self, map = "map1.txt") -> None:
        self.output = "output.txt"
        self.agent = agent.Agent(map)
        self.mapSize = self.agent.WumpusWorld.size
        self.map = self.agent.WumpusWorld.map
        self.screenW =  1300
        self.screenH = 1000
        self.screen = pg.display.set_mode((self.screenW, self.screenH))
        self.statusCell = (25,100,255,700) #left, top, width, height        self.currentCell = [0,0,400, 200]
        self.board = (300, 0, 1000, 1000)
        self.cellW = 100
        self.cellH = 100
        self._agent =  [pg.transform.scale(pg.image.load(".\\img\\agent_up.png"), (96, 96)), 
                        pg.transform.scale(pg.image.load(".\\img\\agent_right.png"), (96, 96)), 
                        pg.transform.scale(pg.image.load(".\\img\\agent_down.png"), (96, 96)), 
                        pg.transform.scale(pg.image.load(".\\img\\agent_left.png"), (96, 96)),
                        pg.transform.scale(pg.image.load(".\\img\\agent_pass.png"), (96, 96))]
        self._gas =  pg.transform.scale(pg.image.load(".\\img\\gas.png"), (100, 100))
        self._healingpotion = pg.transform.scale(pg.image.load(".\\img\\healingpotion.png"), (100, 100))
        self._goal =  pg.transform.scale(pg.image.load(".\\img\\goal.png"), (100, 100))
        self._pit = pg.transform.scale(pg.image.load(".\\img\\pit.png"), (100, 100))
        self._wumpus =  pg.transform.scale(pg.image.load(".\\img\\wumpus.png"), (100, 100))
        self._stench = pg.transform.scale(pg.image.load(".\\img\stench.png"), (100, 100))
        self._breeze = pg.transform.scale(pg.image.load(".\\img\\breeze.png"), (100, 100))
        self._glow = pg.transform.scale(pg.image.load(".\\img\glow.png"), (100, 100))
        self._whiff = pg.transform.scale(pg.image.load(".\\img\whiff.png"),(100, 100))
        self._nothing = pg.transform.scale(pg.image.load(".\\img\\nothing.png"), (96, 96))
        self._hud = pg.image.load(".\\img\\newhud.png")
        self._review = pg.image.load(".\\img\\reviewhud.png")
    def clearOutput(self):
        file = open(self.output, 'w')
        file.write("")
        file.close()
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
    def getProperpyImage(self, key):
        match str(key):
            case "W":
                return self._wumpus
            case "P": 
                return self._pit
            case "P_G": 
                return self._gas
            case "H_P": 
                return self._healingpotion
            case "G":
                return self._goal
            case "S":
                return self._stench
            case "B": 
                return self._breeze
            case "W_H": 
                return self._whiff
            case "G_L": 
                return self._glow
        return self._nothing
    def showStatus(self, score, agentHP, gold, potion, action, percepts, location):
        offsetX, offsetY, width, height = self.statusCell
        posX = offsetX + 16
        posY = offsetY + 100
        eraser = pg.Rect(0,0,   width - 25, 34 )
        font = pg.font.Font("COMIC.TTF", 24)
        healthText = font.render(f"Health: {str(agentHP)}", True, (0,0,0))
        eraser.topleft = (posX, posY)
        pg.draw.rect(self.screen, (160,160,160), eraser)
        self.screen.blit(healthText, (posX, posY))
        posY += healthText.get_rect().size[1] + 2

        scoreText = font.render(f"Score: {str(score)}", True, (0,0,0))
        eraser.topleft = (posX, posY)
        pg.draw.rect(self.screen, (160,160,160), eraser)
        self.screen.blit(scoreText, (posX, posY))
        posY += scoreText.get_rect().size[1] + 2

        goldText = font.render(f"Gold: {str(gold)}", True, (0,0,0))
        eraser.topleft = (posX, posY)
        pg.draw.rect(self.screen, (160,160,160), eraser)
        self.screen.blit(goldText, (posX, posY))
        posY += goldText.get_rect().size[1] + 2

        potionText = font.render(f"Potion: {str(potion)}", True, (0,0,0))
        eraser.topleft = (posX, posY)
        pg.draw.rect(self.screen, (160,160,160), eraser)
        self.screen.blit(potionText, (posX, posY))
        posY += potionText.get_rect().size[1] + 2

        temp = str(action)
        if (temp == "SCREAM"):
            temp = "Hear scream"
        actionText = font.render(f"Action:", True, (0,0,0))
        eraser.topleft = (posX, posY)
        pg.draw.rect(self.screen, (160,160,160), eraser)
        self.screen.blit(actionText, (posX, posY))
        posY += actionText.get_rect().size[1] + 2

        actionText = font.render(f"{str(temp)}", True, (0,0,0))
        eraser.topleft = (posX, posY)
        pg.draw.rect(self.screen, (160,160,160), eraser)
        self.screen.blit(actionText, (posX, posY))
        posY += actionText.get_rect().size[1] + 2
        
        file = open(self.output, 'a')
        file.write(f"{self.mapSize - location[0], location[1] + 1}: {temp} \n")
        file.close()

        itemText = font.render(f"Items in cell:", True, (0,0,0))
        eraser.topleft = (posX, posY)
        pg.draw.rect(self.screen, (160,160,160), eraser)
        self.screen.blit(itemText, (posX, posY))
        posY += itemText.get_rect().size[1] + 2

        self.screen.blit(self._nothing, (posX, posY))
        for i in range(len(percepts)):
            img = self.getProperpyImage(percepts[i])
            posx = posX + (self.cellW - img.get_rect().size[0])/2
            posy = posY + (self.cellH - img.get_rect().size[1])/2
            self.screen.blit(img, (posx, posy))

        posY+= 100 + 2

        
        if (action.lower() == "climb up"):
            escapeText = font.render(f"Agent escaped!!!", True, (0,0,0))
            eraser.topleft = (posX, posY)
            pg.draw.rect(self.screen, (160,160,160), eraser)
            self.screen.blit(escapeText, (posX, posY))
            posY += escapeText.get_rect().size[1] + 2
            file = open(self.output, 'a')
            file.write(f"Final Score: {score} \n")
            file.close()
        
        if (str(agentHP) == "0"):
            deathText = font.render(f"Agent failed!!!", True, (0,0,0))
            eraser.topleft = (posX, posY)
            pg.draw.rect(self.screen, (160,160,160), eraser)
            self.screen.blit(deathText, (posX, posY))
            posY += deathText.get_rect().size[1] + 2
            file = open(self.output, 'a')
            file.write(f"Final Score: {score} \n")
            file.close()
        pg.display.flip()
    def drawItemInCell(self, location, items):
        posx = self.board[0] + location[1]*(self.cellW) + (self.cellW - self._nothing.get_rect().size[0])/2
        posy = self.board[1] + (location[0])*(self.cellH) + (self.cellH - self._nothing.get_rect().size[1])/2
        self.screen.blit(self._nothing, (posx, posy))
        for i in range(len(items)):
            img = self.getProperpyImage(items[i])
            posx = self.board[0] + location[1]*(self.cellW) + (self.cellW - img.get_rect().size[0])/2
            posy = self.board[1] + (location[0])*(self.cellH) + (self.cellH - img.get_rect().size[1])/2
            self.screen.blit(img, (posx, posy))
    def drawReviewMap(self):
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                # self.screen.blit(self._nothing, (i, j))
                items = self.map[i][j]
                self.drawItemInCell((i, j), items)
        pg.display.flip()
    def drawPerceptInfo(self, location:tuple, percepts:list):
        if (location[0] -  1 >= 0):
            if (percepts[location[0] -  1][location[1]]):
                percept = percepts[location[0] -  1][location[1]]
                self.drawItemInCell((location[0] -  1, location[1]), percept)
        if (location[0] +  1 < self.mapSize):
            if (percepts[location[0] +  1][location[1]]):
                percept = percepts[location[0] +  1][location[1]]
                self.drawItemInCell((location[0] +  1, location[1]), percept)
        if (location[1] -  1 >= 0):
            if (percepts[location[0]][location[1] - 1]):
                percept = percepts[location[0]][location[1] - 1]
                self.drawItemInCell((location[0], location[1] - 1), percept)
        if (location[1] +  1 < self.mapSize):
            if (percepts[location[0]][location[1] + 1]):
                percept = percepts[location[0]][location[1] + 1]
                self.drawItemInCell((location[0], location[1] + 1), percept)
    def run(self):
        self.clearOutput() 
        run = True
        flag = True
        stopNextLoop = 0
        review = False
        actionListIndex = 0
        initialAction = deepcopy(self.agent.action)
        self.screen.blit(self._review, (0,0))
        self.agent.agentLogic()
        # agentPercept, agentLocation, agentDirection, score, agentHP, gold, potion, action 
        actionList = []
        oldPos = (-1, -1)
        self.drawReviewMap()
        while(run):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_k and not review:
                        self.screen.blit(self._hud, (0,0))
                        review = True
                        continue
            if (not run):
                print("Quit by pygame")
                pg.quit()
                return
            if (review):
                if actionListIndex >= len(actionList):
                    if flag:
                        flag = self.agent.agentLogic()
                        actionList = self.agent.action
                        actionListIndex = 0
                else:
                    agentPos = actionList[actionListIndex][1]
                    if oldPos !=  (-1,-1):
                        self.drawAgent(oldPos, (-1, -1))
                    self.drawAgent(actionList[actionListIndex][1], actionList[actionListIndex][2])
                    self.drawPerceptInfo(agentPos, actionList[actionListIndex][0])
                    self.showStatus(actionList[actionListIndex][3], actionList[actionListIndex][4], 
                                    actionList[actionListIndex][5], actionList[actionListIndex][6],
                                    actionList[actionListIndex][7], actionList[actionListIndex][0][agentPos[0]][agentPos[1]], 
                                    actionList[actionListIndex][1])
                    oldPos = actionList[actionListIndex][1]
                    actionListIndex += 1
                     
            pg.display.flip()
            pg.time.Clock().tick(4)

                
def main():
    filename = input("Path to input map: ")
    while True:
        pg.init()
        pg.font.init()
        try:
            print("Initializing the GUI")
            print("Run the simulation")
            GUI(filename).run()
        except:
            print("File invalid!!!!")
        filename = input("PLease input file path for new simulation, or q to quit: ")
        if (filename.lower() == 'q'):
            sys.exit()

main()
