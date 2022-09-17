import pygame, random, sys
from pygame.locals import *

WINDOWCAPTION = "Coffin Dodger"
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
TEXTCOLOR = (229,225,0)
BACKGROUNDCOLOR = (0,0,0)
FPS = 50
COFFINMINSIZE = 20
COFFINMAXSIZE = 50
COFFINMINSPEED = 1
COFFINMAXSPEED = 8
ADDNEWCOFFINRATE = 15
PLAYERMOVERATE = 15

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPresskey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def playerHasHitcoffin(playerRect, coffins):
    for coffin in coffins:
        if playerRect.colliderect(coffin['rect']):
            return True
        return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainclock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption(WINDOWCAPTION)
pygame.mouse.set_visible(False)

#setting up fonts
font = pygame.font.SysFont(None,60)

#setting up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mp3')

#setting up images
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
coffinImage = pygame.image.load('coffin.png')

#dissplaying the start screen
drawText(WINDOWCAPTION, font, windowSurface, ((WINDOWWIDTH / 3) - 10), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3)-50, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPresskey()

#main code
topScore = 0
while True:
    #set up the start of the game
    coffins = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    coffinAddCounter = 0 #is to tell the program when to add new coffins
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == ord("z"):
                    reverseCheat = True
                if event.key == ord("x"):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:
                if event.key == ord('z'):
                     reverseCheat = False
                     score = 0 #The score reset is to discourage the player for using the cheats.
                if event.key == ord('x'):
                     slowCheat = False
                     score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                     moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                     moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                     moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                     moveDown = False
                
            if event.type == MOUSEMOTION:
                #If player uses mouse, move the player where the cursor is
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)
        if not reverseCheat and not slowCheat:
            coffinAddCounter += 1
        if coffinAddCounter == ADDNEWCOFFINRATE:
            coffinAddCounter = 0
            coffinSize = random.randint (COFFINMINSIZE,COFFINMAXSIZE)
            newCoffin = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-coffinSize), 0 - coffinSize, coffinSize, coffinSize),
            'speed': random.randint(COFFINMINSPEED, COFFINMAXSPEED),
            'surface':pygame.transform.scale(coffinImage, (coffinSize, coffinSize))}
            coffins.append(newCoffin)
            
            #move the player around
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1*PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

            #Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        for coffin in coffins:
            if not reverseCheat and not slowCheat:
                coffin['rect'].move_ip(0, coffin['speed'])
            elif reverseCheat:
                coffin['rect'].move_ip(0, -5)
            elif slowCheat:
                coffin['rect'].move_ip(0, 1)
            
            #loop through coffins list copy to clear coffins that have fallen already
        for coffin in coffins[:]:
            if coffin['rect'].top > WINDOWHEIGHT:
                coffins.remove(coffin)
                    
            windowSurface.fill(BACKGROUNDCOLOR)

            #Draw score
        drawText('Score: %s' %(score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' %(topScore), font, windowSurface, 10, 40)

        windowSurface.blit(playerImage, playerRect)

        for coffin in coffins:
            windowSurface.blit(coffin['surface'], coffin['rect'])
            
        pygame.display.update()

            #collison detection
        if playerHasHitcoffin(playerRect, coffins):
            if score > topScore:
                topScore = score #set new high score
            break

        mainclock.tick(FPS)

            #game ended
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPresskey()

    gameOverSound.stop()
