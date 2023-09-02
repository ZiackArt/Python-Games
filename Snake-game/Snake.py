import pygame
from random import randint
from pygame import *
import button
# init window
W = 640
H = 480
wind = pygame.display.set_mode((W,H), pygame.RESIZABLE)
bg_color = pygame.Color(22,41,85)
pygame.display.set_caption("The Snake - Ziack Art")
pygame_icon = pygame.image.load('asserts/icon.jpg')
pygame.display.set_icon(pygame_icon)

## Fonctions
def drawFood():
    
    food_color = pygame.Color(210, 45, 60)
    food_rect = pygame.Rect((food[0] * tiles_w, food[1] * tiles_h), (tiles_w,tiles_h))
    pygame.draw.rect(wind, food_color, food_rect)


def drawSnake():
    snk_color = pygame.Color(60, 215, 60)
    for cell in snake:
        cell_rect = pygame.Rect((cell[0] * tiles_w, cell[1] * tiles_h), (tiles_w,tiles_h))
        pygame.draw.rect(wind, snk_color, cell_rect)

def updateSnake(direction):
    global food, snake
    global diff
    global i, scores
    dirX, dirY = direction
    head = snake[0].copy()
    head[0] = (head[0]+ dirX)%tiles_x
    head[1] = (head[1]+ dirY)%tiles_y
    if head in snake[1:]:
        die_s.play()
        return True
    elif head == food:
        eat_s.play()
        scores += 1
        i += 1
        if i == 5:
            point_s.play()
            diff += 5
            i=0
        food = None
        while food is None:
            newFood = [
                randint(0, tiles_x-1),
                randint (0, tiles_y-1)
            ]
            food = newFood if newFood not in snake else None
    else:
        snake.pop()

    snake.insert(0, head)
    return False

def format_score(text):
    if text <= 9:
        text = '000'+str(text)
    elif  text <= 99:
        text = '00'+str(text)
    elif text <= 999 :
        text = "0"+str(text)
    else :
        text = str(text)
    return text

def lire_score():
    fichier = open("score.txt","r+")
    content=fichier.readlines()
    ls = ""
    for line in content:
        for i in line:
            if i.isdigit() == True:
                ls+=i
    fichier.close()
    return ls
   

def score(text, font, tex_col, x):
    text = format_score(text)
    text = font.render(text, True, tex_col)
    wind.blit(text,x)

def gameOver(text, font, tex_col,score):
    global running,snake,die,direction,diff,scores,i,hs
    text = font.render(text, True, tex_col)
    text_rect = text.get_rect(center=(W/2-5, H/2))
    wind.blit(text,text_rect)

    ls = lire_score()

    if int(ls) < score:
        # fichier.truncate(0)
        fichier = open("score.txt",'w')
        fichier.write(format_score(score))
        fichier.close()

    #load button images
    start_img = pygame.image.load('asserts/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('asserts/exit_btn.png').convert_alpha()
    #create button instances
    start_button = button.Button(W//2-150, H//2 + 50, start_img, 0.5)
    exit_button = button.Button(W//2+50, H//2 + 50, exit_img, 0.5)
    start = start_button.draw(wind)
    if start:
        snk_x, snk_y = tiles_x // 4, tiles_y // 2
        direction = [1,0]
        scores,i,diff = 0,0,10
        hs = lire_score()
        snake = [
            [snk_x, snk_y],
            [snk_x-1, snk_y],
            [snk_x-2, snk_y]
        ]
        die = False

    exit = exit_button.draw(wind)
    if exit:
        running = False


## Define the playground
tiles_x = W // 20
tiles_y = H // 20

tiles_w = W // tiles_x
tiles_h = H // tiles_y

## Define the snake
snk_x, snk_y = tiles_x // 4, tiles_y // 2

snake = [
    [snk_x, snk_y],
    [snk_x-1, snk_y],
    [snk_x-2, snk_y]
]

# Initialisation du mixer
pygame.mixer.init()
# Chargement des sons
die_s = pygame.mixer.Sound("asserts/die.wav")
eat_s = pygame.mixer.Sound("asserts/eat.wav")
point_s = pygame.mixer.Sound("asserts/point.wav")

# Initialisation des polices de caractÃ¨res
pygame.font.init()
# Chargement de la police pour afficher le score
font = pygame.font.SysFont('monospace', 30)
font_ls = pygame.font.SysFont('monospace', 15)
GomeOverFont = pygame.font.SysFont('monospace', 50)
## Define the food
food = [tiles_x//2, tiles_y//2]
clock = pygame.time.Clock()
scores,i,diff = 0,0,10
die = False
hs = lire_score()
## Game loop
running = True
direction = [1,0]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT and not direction == [-1,0] :
                direction = [1,0]
            elif event.key == pygame.K_LEFT and not direction == [1,0]:
                direction = [-1,0]
            elif event.key == pygame.K_UP and not direction == [0,1]:
                direction = [0,-1]
            elif event.key == pygame.K_DOWN and not direction == [0,-1]:
                direction = [0,1]
    # Draw
    wind.fill(bg_color)
    
    if die == False: 
        die = updateSnake(direction)
  
    drawFood()
    drawSnake()

    W, H = pygame.display.get_surface().get_size()
    tiles_x = W // 20
    tiles_y = H // 20

    if die == False:
        score(scores ,font, (255,255,255), [15, 15])
        score(int(hs) ,font_ls, (255,255,255), [45, 44])
    elif die == True:
        score(scores ,GomeOverFont, (255,255,255), [W//2-55, H//3])
        gameOver("Game Over" ,GomeOverFont, (255,255,255),scores)
    
    

    pygame.display.flip()
    clock.tick(diff)

# pygame.time.delay(4000)
pygame.quit()