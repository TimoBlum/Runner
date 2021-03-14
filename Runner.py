import pygame, random, math

pygame.init()

WHITE = [255, 255, 255]
xy = 800
win = pygame.display.set_mode((xy, xy))
pygame.display.set_caption("Runner game!")
win.fill((255, 255, 255))
Frame = 0
difficulty = 50
isLost = False
rows = 40
run = True
spacebtwn = xy // rows
clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 255, 0)
        self.radius = 15
        self.vel = 1.8
        self.health = 180
        self.HB = (self.x - 27, self.y - 37, 54, 14)
        self.barcolor = [255 - self.health, 75 + self.health, 0]
        self.wh = 20

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.y >= self.radius:
            self.y -= self.vel
        if keys[pygame.K_s] and self.y <= xy - self.radius:
            self.y += self.vel
        if keys[pygame.K_a] and self.x >= self.radius:
            self.x -= self.vel
        if keys[pygame.K_d] and self.x <= xy - self.radius:
            self.x += self.vel

    def drawP(self):
        d = detectZones()
        if d:
            self.health -= 1
            pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius, self.wh)
            self.healthBar()
        elif not d:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, self.wh)
            self.healthBar()

    def updateHB(self):
        global isLost
        if self.HB[2] == 0:
            isLost = True
        self.barcolor = [255 - self.health, 75 + self.health, 0]
        self.HB = (self.x - 27, self.y - 37, (3 * self.health / 10), 14)

    def healthBar(self):
        """draws a health bar above the green player"""
        self.updateHB()
        pygame.draw.rect(win, (230, 230, 230), (self.x - 30, self.y - 40, 60, 20))
        pygame.draw.rect(win, self.barcolor, self.HB)


class Zone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1
        self.m = 1
        self.color = [255, 0, 0]

    def bigger(self):
        if self.radius >= 100:
            self.m = -1
        elif self.radius < 0:
            del Zones[0]
        self.radius += self.m

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


P = Player(xy // 2, xy // 2)
Zones = [Zone(random.randint(20, xy - 20),
              random.randint(20, xy - 20))]


def detectZones():
    for z in Zones:
        if euclidian(z.x, z.y, P.x, P.y) - (z.radius + P.radius) < 0:
            return True
    return False


def redrawGameWin():
    global Frame, difficulty
    win.fill(WHITE)
    drawGrid()

    # Zones
    for zone in Zones:
        zone.draw()
        zone.bigger()

    # Player
    P.move()
    P.drawP()

    # Difficulty
    Frame += 1
    print("Frame Nr.", Frame, "  Score: ", pygame.time.get_ticks() // 1000)
    # These are regulators for Red Zone spawns, because the game runs at 50 FPS, and difficulty = 50 at first
    # a red zone spawns every second. The yn() function means: doing something everytime
    # (first argument) / (second argument) is a float with no decimal values
    if yn(Frame, difficulty):
        Zones.append(Zone(random.randint(20, xy - 20), random.randint(20, xy - 20)))
    if yn(Frame, 40) and difficulty > 2:
        difficulty -= 0.5

    score = pygame.time.get_ticks() // 1000
    if isLost:
        win.fill((255, 0, 0))
        pygame.time.wait(2000)
        with open('highscore', 'a') as f:
            f.write('\n')
            f.write(gamer)
            f.write('\n')
            f.write(str(score))
        pygame.quit()
    pygame.display.update()


def drawGrid():
    """Draw a grid"""
    global win, xy
    x = 0
    y = 0
    for l in range(rows):
        pygame.draw.line(win, (240, 240, 240), (x, 0), (x, xy))
        pygame.draw.line(win, (240, 240, 240), (0, y), (xy, y))

        x = x + spacebtwn
        y = y + spacebtwn


def euclidian(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1) ** 2) + (y2 - y1) ** 2)


def yn(a, c):
    # decide if something, whether float or int is the same number
    b = a // c
    bb = a / c
    if b - bb == 0:
        return True
    else:
        return False


def main():
    global run
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redrawGameWin()


gamer = input('Whos playing: ')
try:
    main()
except:
    pass
