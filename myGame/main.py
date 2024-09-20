import pygame
import os
import random


pygame.font.init()
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 100)

pygame.mixer.init()
BULLET_SOUND = pygame.mixer.Sound(os.path.join('/Users/cole.lingo/Desktop/Python CEC 112/myGame/assets', 'gun.mp3'))
HIT_SOUND = pygame.mixer.Sound(os.path.join('/Users/cole.lingo/Desktop/Python CEC 112/myGame/assets', 'explode.mp3'))

#constants
WIDTH, HEIGHT = 800, 600
GAME_TITLE = "Space Battle!"
SHIP_WIDTH, SHIP_HEIGHT = 40,55
SABER_WIDTH = 80
FPS = 60
SHIP_VEL = 5
BULLET_VEL = 8
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
MAX_BULLETS = 3
MAX_HEALTH = 10

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPLASH = 1
PLAYING = 2
OVER = 3


#loading files
SPACE_IMAGE = pygame.image.load(os.path.join("/Users/cole.lingo/Desktop/Python CEC 112/myGame/assets", "space.jpg"))
SPACE_IMAGE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

YELLOW_SHIP = pygame.image.load(os.path.join("/Users/cole.lingo/Desktop/Python CEC 112/myGame/assets", "spaceship_yellow.png"))
YELLOW_SHIP = pygame.transform.rotate(YELLOW_SHIP, 90)
YELLOW_SHIP = pygame.transform.scale(YELLOW_SHIP, (SHIP_WIDTH, SHIP_HEIGHT))

RED_SHIP = pygame.image.load(os.path.join("/Users/cole.lingo/Desktop/Python CEC 112/myGame/assets", "spaceship_red.png"))
RED_SHIP = pygame.transform.rotate(RED_SHIP, 270)
RED_SHIP = pygame.transform.scale(RED_SHIP, (SHIP_WIDTH, SHIP_HEIGHT))

SABER = pygame.image.load(os.path.join("/Users/cole.lingo/Desktop/Python CEC 112/myGame/assets", "saber.png"))
SABER = pygame.transform.scale(SABER, (SABER_WIDTH, HEIGHT))
#window 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)

def move_yellow_ship(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]: #left
        yellow.x -= SHIP_VEL
        if yellow.x <= 0:
            yellow.x = 0
    if keys_pressed[pygame.K_d]: #right
        yellow.x += SHIP_VEL
        if yellow.x + SHIP_WIDTH> WIDTH //2:
            yellow.x = 10
            yellow.y = random.randrange(0, HEIGHT - SHIP_HEIGHT)
    if keys_pressed[pygame.K_w]: #up
        yellow.y -= SHIP_VEL
        if yellow.y <= 0:
            yellow.y = 0
    if keys_pressed[pygame.K_s]: #down
        yellow.y += SHIP_VEL
        if yellow.y >= HEIGHT - SHIP_HEIGHT:
            yellow.y = HEIGHT - SHIP_HEIGHT

def move_red_ship(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]: #left
        red.x -= SHIP_VEL
        if red.x + SHIP_WIDTH < WIDTH //2:
            red.x = WIDTH - 10 - SHIP_WIDTH
            red.y = random.randrange(0, HEIGHT - SHIP_HEIGHT)
    if keys_pressed[pygame.K_RIGHT]: #right
        red.x += SHIP_VEL
        if red.x >= WIDTH - SHIP_WIDTH:
            red.x = WIDTH - SHIP_WIDTH
    if keys_pressed[pygame.K_UP]: #up
        red.y -= SHIP_VEL
        if red.y <= 0:
            red.y = 0
    if keys_pressed[pygame.K_DOWN]: #down
        red.y += SHIP_VEL
        if red.y >= HEIGHT - SHIP_HEIGHT:
            red.y = HEIGHT - SHIP_HEIGHT

def move_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if bullet.x >= WIDTH:
            yellow_bullets.remove(bullet)
        elif red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
           
        
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if bullet.x <= 0:
            red_bullets.remove(bullet)
        elif yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))

def draw_over(winner):
    WIN.blit(SPACE_IMAGE, (0, 0))
    over_text = TITLE_FONT.render("GAME OVER", True, (255, 255, 255))
    if winner == "YELLOW WINS!":
        winner_text = HEALTH_FONT.render(winner, True, YELLOW)
    else:
        winner_text = HEALTH_FONT.render(winner, True, RED)
    WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - over_text.get_height()//2))
    WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 + winner_text.get_height()//2+ 20))
    pygame.display.update()

def draw_splash():
    WIN.blit(SPACE_IMAGE, (0, 0))
    title_text = TITLE_FONT.render("SPACE BATTLE", True, (255, 255, 255))
    subtitle_text = HEALTH_FONT.render("Press any key to start!!", True, (255, 255, 255))
    WIN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - title_text.get_height()//2))
    WIN.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//2 - subtitle_text.get_height()//2 + 100))
    pygame.display.update()

def draw_game(yellow, red, yellow_bullets, red_bullets, red_health, yellow_health):
    WIN.blit(SPACE_IMAGE, (0, 0))
    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SHIP, (red.x, red.y))
    WIN.blit(SABER, (WIDTH//2 - 40, 0))
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    yellow_health_text = HEALTH_FONT.render("Health: "+ str(yellow_health),True, YELLOW)
    red_health_text = HEALTH_FONT.render("Health: "+ str(red_health),True, RED)

    WIN.blit(yellow_health_text, (WIDTH//2 - yellow_health_text.get_width()*2, 10))
    WIN.blit(red_health_text, (WIDTH * 3 // 4 - red_health_text.get_width()//2, 10))

    pygame.display.update()



def main():
    clock = pygame.time.Clock()
    yellow = pygame.Rect(10, HEIGHT//2 - SHIP_HEIGHT//2, SHIP_WIDTH, SHIP_HEIGHT)

    red = pygame.Rect(WIDTH-10 - SHIP_WIDTH, HEIGHT//2 - SHIP_HEIGHT//2, SHIP_WIDTH, SHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_health = MAX_HEALTH
    red_health = MAX_HEALTH

    stage = SPLASH

    run = True
    while run:
        clock.tick(FPS)

        my_event = pygame.event.get()

        for event in my_event:
            if event.type == pygame.QUIT:
                run = False

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                HIT_SOUND.play()
                if yellow_health <= 0:
                    stage = OVER

            if event.type == RED_HIT:
                red_health -= 1
                HIT_SOUND.play()
                if red_health <= 0:
                    stage = OVER
            if event.type == pygame.KEYDOWN:
                if stage == SPLASH:
                    stage = PLAYING
                elif stage == OVER:
                    yellow_health = MAX_HEALTH
                    red_health = MAX_HEALTH
                    yellow.x = 10
                    yellow.y = HEIGHT//2 - SHIP_HEIGHT//2
                    red.x = WIDTH-10 - SHIP_WIDTH
                    red.y = HEIGHT//2 - SHIP_HEIGHT//2
                    yellow_bullets = []
                    red_bullets = []
                    stage = SPLASH

                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + SHIP_WIDTH, yellow.y + SHIP_HEIGHT//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_SOUND.play()
                    
                
                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - SHIP_WIDTH, red.y + SHIP_HEIGHT//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_SOUND.play()
                  
    
        if stage == SPLASH:
            draw_splash()
        elif stage == PLAYING:
            keys_pressed = pygame.key.get_pressed()
            move_yellow_ship(keys_pressed, yellow)
            move_red_ship(keys_pressed, red)
            move_bullets(yellow_bullets, red_bullets, yellow, red)
            draw_game(yellow, red, yellow_bullets, red_bullets, red_health, yellow_health)
        elif stage == OVER:
            if red_health <= 0:
                draw_over("YELLOW WINS!")
            else :
                draw_over("RED WINS!")


    pygame.quit()

if __name__ == "__main__":
    main()
