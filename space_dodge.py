import pygame
import time
import random 
import shelve
import shelve
pygame.init()

""" Setting up Window """
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

""" Loading Background """
BG = pygame.transform.scale(pygame.image.load("space.jpeg"), (WIDTH, HEIGHT))

""" Player Characteristics """
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 100
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("spaceship.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_VEL = 5

""" Asteroid Characteristics """
ASTEROID_WIDTH = 20
ASTEROID_HEIGHT = 20
ASTEROID_IMAGE = pygame.transform.scale(pygame.image.load("asteroid.png"), (ASTEROID_WIDTH, ASTEROID_HEIGHT))
ASTEROID_VEL = 3

""" Font Initialization """
FONT = pygame.font.SysFont("comicsans", 30)
BIG_FONT = pygame.font.SysFont("comicsans", 60)
MED_FONT = pygame.font.SysFont("comicsans", 45)
SMALL_FONT =pygame.font.SysFont("comicsans", 20)
TITLE_FONT = pygame.font.SysFont("comicsans", 100)

""" Game Status Variable (signifies to game loop to repeat or terminate game)"""
game_over = False

""" Draw Function """
def draw(player, elapsed_time, high_score, asteroids):
    high_score_text = FONT.render(f"High Score: {high_score}s", 1, "white")
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    
    WIN.blit(BG, (0, 0))     
    WIN.blit(time_text, (10, 10))
    WIN.blit(high_score_text, (10, 50))
    WIN.blit(PLAYER_IMAGE, (player.x, player.y))
    
    for asteroid in asteroids:
        WIN.blit(ASTEROID_IMAGE, (asteroid.x, asteroid.y))
    
    pygame.display.update()

""" Starting Screen """
def start_game(high_score):
    global game_over
    
    author_text = SMALL_FONT.render("Made by Jermaine Pina", 1, "white")
    title_text = TITLE_FONT.render("SPACE DODGE", 1, "white")
    start_text = MED_FONT.render("Press SPACE to start", 1, "white")       
    quit_text = FONT.render("Press Q to quit", 1, "white")       
    high_score_text = FONT.render(f"High Score: {high_score}s", 1, "white")
    
    WIN.blit(BG, (0, 0))
    WIN.blit(author_text, (10, 10))
    WIN.blit(high_score_text, (10, 40))
    WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2,
                            HEIGHT/2 - title_text.get_height()/2 - 100))
    WIN.blit(start_text, (WIDTH/2 - start_text.get_width()/2,
                            HEIGHT/2 - start_text.get_height()/2 + 100))
    WIN.blit(quit_text, (10, HEIGHT - 50))
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_q:
                    game_over = True
                    waiting = False

""" Ending Screen """
def end_game(elapsed_time, high_score):
    lost_text = BIG_FONT.render("You Lost!", 1, "white")
    score_text = FONT.render(f"Score: {round(elapsed_time)}s", 1, "white")
    
    if elapsed_time > high_score:
        new_score_text = MED_FONT.render("New High Score!", 1, "white")
        WIN.blit(new_score_text, (WIDTH/2 - new_score_text.get_width()/2,
                                 HEIGHT/2 - new_score_text.get_height()/2 - 50))
        
    WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2,
                                 HEIGHT/2 - lost_text.get_width()/2 - 100))
    WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2,
                                 HEIGHT/2 - score_text.get_width()/2 + 100))
    
    pygame.display.update()
    pygame.time.delay(5000)
    main()

""" Resets high score to 0 """
def reset_score():
    d = shelve.open('score.txt')
    d['score'] = 0  
    d.close()


""" Main Game Loop """
def main():
    d = shelve.open('score.txt')
    high_score = d.get('score', 0) 
    d.close()
    
    start_game(high_score) 
    
    run = True    
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    asteroid_add_increment = 2000
    asteroid_count = 0
    asteroids = []
    hit = False
    level = 0
    amount = 3
    
    while run and not game_over:
        asteroid_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        if elapsed_time > high_score:
            d = shelve.open('score.txt')
            d['score'] = round(elapsed_time)
            d.close()
            high_score = round(elapsed_time)
        
        if asteroid_count > asteroid_add_increment:
            level += 1
            if level % 5 == 0:
                amount += 1
            for _ in range(amount):
                asteroid_x = random.randint(0, WIDTH - ASTEROID_WIDTH)     
                asteroid = pygame.Rect(asteroid_x, -ASTEROID_HEIGHT, ASTEROID_WIDTH, ASTEROID_HEIGHT)       
                asteroids.append(asteroid)
                
            asteroid_add_increment = max(200, asteroid_add_increment - 30)
            asteroid_count = 0    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
            
        for asteroid in asteroids[:]:
            asteroid.y += ASTEROID_VEL
            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)
            elif asteroid.y + asteroid.height >= player.y and asteroid.colliderect(player):
                asteroids.remove(asteroid)
                hit = True
                break
            
        if hit:
            end_game(elapsed_time, high_score)
            break
        draw(player, elapsed_time, high_score, asteroids)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()
