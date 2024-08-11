import pygame as pg
import program
import sys
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

print(map)
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

while(run):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    if (not run):
        pg.quit()
        sys.exit()
    pg.display.flip()
    pg.time.Clock().tick(60)