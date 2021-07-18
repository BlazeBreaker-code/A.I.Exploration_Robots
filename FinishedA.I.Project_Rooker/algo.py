import sys, os, random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
robots = []
spots = []
movement = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'R']


def main():
    global CLOCK, SCREEN, robots, spots
    quit = "N"

    while quit == 'N' or quit == "n":
        robots = []
        spots = []
        robotNum = input("Pick the number of robots you would like to use(integer): ")
        if robotNum.isdigit():
            robotNum = int(robotNum)
        else:
            robotNum = "k"
        while not isinstance(robotNum, int):
            print("WRONG INPUT!!! Please choose an integer!")
            robotNum = input("Now what number of robots you would like to use(integer): ")
            if robotNum.isdigit():
                robotNum = int(robotNum)
            else:
                robotNum = "k"
        askRange = input("Pick the range you would like to use(integer): ")
        if askRange.isdigit():
            askRange = int(askRange)
        else:
            askRange = "k"
        while not isinstance(askRange, int):
            print("WRONG INPUT!!! Please choose an integer!")
            askRange = input("Now what range you would like to use(integer): ")
            if askRange.isdigit():
                askRange = int(askRange)
            else:
                askRange = "k"
        print(f'You have picked {robotNum} number of robots with the range of {askRange}.')
        print("The solution is now being visualized.")
        print("If there are any faulty spawns with the robots please restart the program.")
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()
        SCREEN.fill(WHITE)
        drawGrid(robotNum)
        algorithm1(askRange)
        # CLOCK.tick(30)
        quit1 = input("Do you wish to exit (Y if yes, N if no)? ")
        while (quit1 != 'N' and quit1 != 'n') and (quit1 != 'Y' and quit1 != 'y'):
            print("WRONG INPUT!!! Please choose either N or Y!")
            quit1 = input("Do you wish to exit (Y if yes, N if no)? ")
            quit1 = str(quit1)
        quit = quit1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


# Makes an environment with random obstacles and random starting positions for the robots
def drawGrid(robotNum):
    blockSize = 20
    i = 0
    pop = 0
    start = random.randint(1, 1000)
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            value = random.randint(1, 7)
            if value == 3:
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(SCREEN, BLACK, rect)
                spots.append(Spot(x, y, 1, 0, 0, 0))
            else:
                if start == pop and i < robotNum:
                    rect = pygame.Rect(x, y, blockSize, blockSize)
                    pygame.draw.rect(SCREEN, RED, rect)
                    robots.append(Robot(x, y))
                    spots.append(Spot(x, y, 0, 1, 1, 0))
                    i = i + 1
                else:
                    pop = pop + 1
                    rect = pygame.Rect(x, y, blockSize, blockSize)
                    pygame.draw.rect(SCREEN, GREY, rect, 1)
                    spots.append(Spot(x, y, 0, 0, 0, 0))


def update(x1, y1, x2, y2, q):
    s = len(spots)
    rect1 = pygame.Rect(x1, y1, 20, 20)
    pygame.draw.rect(SCREEN, GREEN, rect1)
    rect2 = pygame.Rect(x2, y2, 20, 20)
    pygame.draw.rect(SCREEN, RED, rect2)
    robots[q].x = x2
    robots[q].y = y2
    for w in range(s):
        if spots[w].x == x1 and spots[w].y == y1:
            spots[w].occupied = 0
    for e in range(s):
        if spots[e].x == x2 and spots[e].y == y2:
            spots[e].occupied = 1
            spots[e].visited = 1
            spots[e].fron = 0


class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Spot:
    def __init__(self, x, y, obstacle, occupied, visited, fron):
        self.x = x
        self.y = y
        self.obstacle = obstacle
        self.occupied = occupied
        self.visited = visited
        self.fron = fron


# Communication Exploration
def algorithm1(r):
    t = 0
    T = 80000
    # k < 9^n n being number of robots
    k = int((9 ** (len(robots))) / (3 ** (len(robots))))
    if k > 15:
        k = 10
    n = len(robots)
    # Range
    # r = 15
    while t < T:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.event.get()
        pop = []
        for i in range(k):
            cfg = []
            for j in range(n):
                value = random.randint(0, 8)
                cfg.append(movement[value])
            pop.append(cfg)
        cfg_max = pop[0]
        for l in range(k):
            if utility(pop[l], r) >= utility(cfg_max, r):
                cfg_max = pop[l]
        listCo = []
        l1 = []
        for y in range(n):
            ran = True
            second = move(cfg_max[y], y)
            listCo.append(second)
            tempx, tempy = second
            for u in range(n):
                if ((abs(robots[u].x - second[0]) + abs(robots[u].y - second[1])) / 20) > r:
                    ran = False
            for i in listCo:
                if i not in l1:
                    if (findCoorCell(second) and ran):
                        update(robots[y].x, robots[y].y, tempx, tempy, y)
                        l1.append(i)
            pygame.time.delay(-50)
            pygame.display.flip()
        t = t + 1


def move(m, i):
    if m == "N":
        coord = tuple([robots[i].x, robots[i].y - 20])
        return coord
    if m == "NE":
        coord = tuple([robots[i].x + 20, robots[i].y - 20])
        return coord
    if m == "E":
        coord = tuple([robots[i].x + 20, robots[i].y])
        return coord
    if m == "SE":
        coord = tuple([robots[i].x + 20, robots[i].y + 20])
        return coord
    if m == "S":
        coord = tuple([robots[i].x, robots[i].y + 20])
        return coord
    if m == "SW":
        coord = tuple([robots[i].x - 20, robots[i].y + 20])
        return coord
    if m == "W":
        coord = tuple([robots[i].x - 20, robots[i].y])
        return coord
    if m == "NW":
        coord = tuple([robots[i].x - 20, robots[i].y - 20])
        return coord
    if m == "R":
        coord = tuple([robots[i].x, robots[i].y])
        return coord


def findCoorCell(coord):
    s = len(spots)
    for x in range(s):
        if spots[x].x == coord[0] and spots[x].y == coord[1] and spots[x].obstacle != 1 and spots[x].occupied != 1:
            return True

    return False


def findVisited(coord):
    s = len(spots)
    for x in range(s):
        if spots[x].x == coord[0] and spots[x].y == coord[1] and spots[x].visited == 0:
            return True

    return False


def makeSureNotSame(cfg):
    n = len(robots)
    Checker = []
    for x in range(n):
        coord2 = move(cfg[x], x)
        Checker.append(coord2)
    m = len(Checker)
    for j in range(m):
        for k in range(m):
            if Checker[j] == Checker[k]:
                return False
    return True


def utility(cfg, r):
    total = 0
    n = len(robots)
    limit = 0
    for x in range(n):
        coord2 = move(cfg[x], x)
        if not findCoorCell(coord2):
            total = total - 3000000
        else:
            for u in range(n):
                if limit == 0:
                    if ((abs(robots[u].x - coord2[0]) + abs(robots[u].y - coord2[1])) / 20) > r:
                        total = total - 300000
                        limit = 1
                    else:
                        # Check the frontier and see what is the lowest value to a frontier node
                        currentRobot = tuple([robots[x].x, robots[x].y])
                        checkFrontier(currentRobot)
                        great = makeFrontArray()
                        if great:
                            dist = []
                            for q in great:
                                dist.append((abs(q[0] - coord2[0]) + abs(q[1] - coord2[1])) / 20)
                            total = total - min(dist)
                        if not great:
                            print("Program has been completed!")
                            sys.exit(0)

    return total


# Checks nodes around current to see if they are visited or not, if not, they go into a frontier node array
def checkFrontier(check):
    sp = len(spots)
    nearby = [tuple([check[0], check[1] - 20]), tuple([check[0] + 20, check[1] - 20]), tuple([check[0] + 20, check[1]]),
              tuple([check[0] + 20, check[1] + 20]), tuple([check[0], check[1] + 20]),
              tuple([check[0] - 20, check[1] + 20]), tuple([check[0] - 20, check[1]]),
              tuple([check[0] - 20, check[1] - 20]), tuple([check[0], check[1]])]
    for u in nearby:
        for i in range(sp):
            if spots[i].x == u[0] and spots[i].y == u[1] and spots[i].obstacle == 0 and spots[i].visited == 0:
                spots[i].fron = 1


def makeFrontArray():
    frontier = []
    sp = len(spots)
    for i in range(sp):
        if spots[i].fron == 1:
            fill = tuple([spots[i].x, spots[i].y])
            frontier.append(fill)
    return frontier


main()
