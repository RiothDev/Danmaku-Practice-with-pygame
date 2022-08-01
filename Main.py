import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, math, random

class sizes:
    def __init__(self, width, height):
        self.Width = width
        self.Height = height

currentCount = 0
currentAnim = 1
animLimit = False

playerX = 800 / 2
playerY = 450

lastBullet = 0
bulletLimit = 50
totalBullets = 0

toX = 0
toY = 0

bullets = []
bulletsDirection = [1]
bulletsY = []
bulletsX = []

def main():
    global bullets
    global bulletsX
    global bulletsY

    pygame.init

    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Song.mp3")
    pygame.mixer.music.play()

    screenSizes = sizes(800, 600)
    screen = pygame.display.set_mode((screenSizes.Width, screenSizes.Height))

    startBullet = pygame.image.load("Assets/Bullet.png")
    startBullet = screen.blit(startBullet, (450, 300))

    bullets.append(startBullet)
    bulletsX.append(450)
    bulletsY.append(300)

    pygame.display.set_caption("Danmaku Practice")
    pygame.display.set_icon(pygame.image.load("Assets/Icon.png"))

    background = pygame.image.load("Assets/Background.jpg")
    background = pygame.transform.scale(background, (screenSizes.Width, screenSizes.Height))

    def getPlayerDirection():
        global animLimit

        if toX == 0:
            animLimit = bool(False)
            return "Idle"
        elif toX >= 1:
            animLimit = bool(True)
            return "Right"
        elif toX <= -1:
            animLimit = bool(True)
            return "Left"

    def getAnimation():
        global currentCount
        global currentAnim

        if currentCount >= 150:
            if currentAnim <= 7:
                currentCount = 0
                currentAnim += 1
            else:
                if animLimit == False:
                    currentCount = 0
                    currentAnim = 1

    def loadBullet(x, y):
        newBullet = pygame.image.load("Assets/Bullet.png")
        newBullet = screen.blit(newBullet, (x, y))

    def bullet(x, y):
        global bullets
        global bulletsX
        global bulletsY

        newBullet = pygame.image.load("Assets/Bullet.png")
        newBullet = screen.blit(newBullet, (x, y))
        
        bulletsDirection.append(random.randint(1, 2))
        bullets.append(newBullet)
        bulletsX.append(x)
        bulletsY.append(y)

    def editDirection():
        global playerY
        global playerX

        if toY <= -1:
            if playerY <= 0:
                pass
            else:
                playerY -= 1

        elif toY >= 1:
            if playerY >= (screenSizes.Height - 60):
                pass
            else:
                playerY += 1

        if toX <= -1:
            if playerX <= 0:
                pass
            else:
                playerX -= 1

        elif toX >= 1:
            if playerX >= (screenSizes.Width - 25):
                pass
            else:
                playerX += 1

    def gameOver():
        pass
        #Soon maybe

    def isCollision(bulletX, bulletY):
        distance = math.sqrt(math.pow(playerX - bulletX, 2) + (math.pow(playerY - bulletY, 2)))
        if distance < 12:
            return True
        else:
            return False

    def makePlayer(posX, posY):
        getAnimation()
        editDirection()

        getDir = getPlayerDirection()
        screen.blit(pygame.image.load(f"Assets/Character/{getDir}/Reimu{getDir}{currentAnim}.png"), (posX, posY))
    
    screen.fill((24, 24, 24))
    pygame.display.update()

    isGameRunning = True

    while isGameRunning:
        #screen.fill((25, 25, 25))
        screen.blit(background, (0, 0))

        global currentAnim
        global currentCount
        global lastBullet
        global totalBullets
        global toX
        global toY

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGameRunning = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    toX = -1
                    currentAnim = 1

                elif event.key == pygame.K_RIGHT:
                    toX = 1
                    currentAnim = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    toY = 1

                elif event.key == pygame.K_UP:
                    toY = -1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if toX <= -1:
                        toX = 0

                elif event.key == pygame.K_RIGHT:
                    if toX >= 1:
                        toX = 0

                elif event.key == pygame.K_UP:
                    if toY <= -1:
                        toY = 0

                elif event.key == pygame.K_DOWN:
                    if toY >= 1:
                        toY = 0

        currentCount += 1
        lastBullet += 1

        for x in range(0, len(bullets)):

            if lastBullet >= 5:
                lastBullet = 0
                if totalBullets <= bulletLimit:
                    totalBullets += 1
                    bullet(random.randint(0, 800), 0)

            try:
                if bulletsDirection[x] == 1:
                    bulletsX[x] += 0.2
                    
                elif bulletsDirection[x] == 2:
                    bulletsX[x] -= 0.2
                    
                bulletsY[x] += 1.5
                loadBullet(bulletsX[x], bulletsY[x])

                if bulletsY[x] >= 600:
                    totalBullets -= 1
                    bullets.pop(x)
                    bulletsX.pop(x)
                    bulletsY.pop(x)
            except:
                pass

            try:
                if isCollision(bulletsX[x], bulletsY[x]) == True:
                    totalBullets -= 1
                    gameOver()
                    bullets.pop(x)
                    bulletsX.pop(x)
                    bulletsY.pop(x)
            except:
                pass
            
        makePlayer(playerX, playerY)
        pygame.display.update()

if __name__ == "__main__":
    main()