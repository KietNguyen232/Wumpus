import pygame as pg
import sys
map = [["-","-","-","P"],
    ["W", "G H_P", "P", "-"],
    ["-", "-", "-",'-'],
    ["A","-","P","-"]]

winW, winH = 1000, 1000


_agent =  pg.transform.scale(pg.image.load(".\img\\agent.png"), (100, 100))
_gas =  pg.transform.scale(pg.image.load(".\img\\gas.png"), (100, 100))
_healingpotion = pg.transform.scale(pg.image.load(".\img\\healingpotion.png"), (100, 100))
_goal =  pg.transform.scale(pg.image.load(".\img\\goal.png"), (100, 100))
_pit = pg.transform.scale(pg.image.load(".\img\\pit.png"), (100, 100))
_wumpus =  pg.transform.scale(pg.image.load(".\img\\wumpus.png"), (100, 100))

window = pg.display.set_mode((winW, winH))

run = True
while(run):
    window.fill((255,255,255))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    if (not run):
        pg.quit()
        sys.exit()
    window.blit(_agent, (0,0))
    window.blit(_gas, (100,0))
    window.blit(_goal, (200,0))
    window.blit(_healingpotion, (0,100))
    window.blit(_pit, (100,100))
    window.blit(_wumpus, (200, 100))
    pg.display.flip()
    pg.time.Clock().tick(60)