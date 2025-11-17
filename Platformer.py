import pygame
import os
#VARIABLES
GAME_WIDTH = 512
GAME_HEIGHT = 512
PLAYER_X= GAME_WIDTH//2
PLAYER_Y= GAME_HEIGHT//2
PLAYER_WIDTH= 42
PLAYER_HEIGHT=48
PLAYER_SPEED= 5
GAME_FLOOR= GAME_HEIGHT
PLAYER_VELOCITY_Y=-10
GRAVITY= 0.5

#IMAGES
Background_image= pygame.image.load("images/background.png")
player_image=pygame.image.load("images/megaman-right.png")
player_image=pygame.transform.scale(player_image,(PLAYER_WIDTH,PLAYER_HEIGHT))
pygame.init() 
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Platformer") 
clock = pygame.time.Clock() 

class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,PLAYER_X,PLAYER_Y,PLAYER_WIDTH,PLAYER_HEIGHT)
        self.image= player_image
        self.velocity_y = 0
        self.jumping= 0
        self.max_health= 5
        self.health = self.max_health


#MY PLAYER 
player= Player()
game_started = False
game_over = False

#FONTS/ GAME START AND OVER
menu_font = pygame.font.Font("assets/font.ttf", 48)
small_font = pygame.font.Font("assets/font.ttf", 24)

def draw_start_menu():
    window.fill((20, 20, 20))

    title = menu_font.render("Platformer", True, (255, 255, 255))
    start_text = small_font.render("Press SPACE to Start", True, (200, 200, 200))

    window.blit(title, (GAME_WIDTH//2 - title.get_width()//2, 150))
    window.blit(start_text, (GAME_WIDTH//2 - start_text.get_width()//2, 260))
    
def draw_game_over():
    window.fill((0, 0, 0))
    over_text = menu_font.render("GAME OVER", True, (255, 0, 0))
    restart_text = small_font.render("press R to Restart", True, (200, 200, 100))

    window.blit(over_text, (GAME_WIDTH//2 - over_text.get_width()//2, 100))
    window.blit(restart_text, (GAME_WIDTH//2 - restart_text.get_width()//2, 200))


def move():
    player.velocity_y += GRAVITY
    player.y += player.velocity_y
    if player.y + player.height > GAME_FLOOR:
        player.y= GAME_FLOOR - player.height
        player.jumping= 0
def draw():
    window.fill((50,50,50))
    window.blit(Background_image, (0,50))
    window.blit(player.image, player)
    pygame.draw.rect(window, "red", (20,20, 20*player.max_health, 10))
    pygame.draw.rect(window, "green", (20,20, 20*player.health, 10))

#SCREENSHOT
def take_screenshot():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    index = 1
    filename = f"screenshots/screenshot_{index}.png"
    while os.path.exists(filename):
        index += 1
        filename = f"screenshots/screenshot_{index}.png"

    # Save the screenshot
    pygame.image.save(window, filename)

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                take_screenshot()
    #MOVE MY PLAYER USING KEYS

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping :
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping= 1
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and player.x>=0:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d] and player.x + PLAYER_WIDTH <= GAME_WIDTH:
        player.x += PLAYER_SPEED
    if not game_over and keys[pygame.K_o]:
        game_over = True

    #draw my start menu
    if not game_started:
        draw_start_menu()
        pygame.display.update()

        if keys[pygame.K_SPACE]:
            game_started = True
        continue
    #DRAW GAME OVER
    if game_over:
        draw_game_over()
        pygame.display.update()
    #RESTART MY GAME(press space)
        if keys[pygame.K_r]:
                player.x = PLAYER_X
                player.y = PLAYER_Y
                player.health = player.max_health
                player.velocity_y = 0
                game_over = False
        continue
    
    move()
    draw()
    pygame.display.update()
    clock.tick(60)
    
