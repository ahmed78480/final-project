import pygame
import os
#VARIABLES
TILE_SIZE= 32
GAME_WIDTH = 512
GAME_HEIGHT = 512
PLAYER_X= GAME_WIDTH//2
PLAYER_Y= GAME_HEIGHT//2
PLAYER_WIDTH= 42
PLAYER_HEIGHT=48
PLAYER_SPEED= 5
PLAYER_VELOCITY_Y=-11
PLAYER_VELOCITY_X = 5
GRAVITY= 0.5

#IMAGES
Background_image= pygame.image.load("images/background.png")
floor_tile_image=pygame.image.load("images/floor-tile.png")
floor_tile_image=pygame.transform.scale(floor_tile_image,(TILE_SIZE,TILE_SIZE))
player_image=pygame.image.load("images/megaman-right.png")
player_image=pygame.transform.scale(player_image,(PLAYER_WIDTH,PLAYER_HEIGHT))
player_image_right = pygame.image.load("images/megaman-right.png")
player_image_right=pygame.transform.scale(player_image_right,(PLAYER_WIDTH,PLAYER_HEIGHT))
player_image_left = pygame.image.load("images/megaman-left.png")
player_image_left=pygame.transform.scale(player_image_left,(PLAYER_WIDTH,PLAYER_HEIGHT))
player_image_jump_right = pygame.image.load("images/megaman-right-jump.png")
player_image_jump_right=pygame.transform.scale(player_image_jump_right,(PLAYER_WIDTH,PLAYER_HEIGHT))
player_image_jump_left = pygame.image.load("images/megaman-left-jump.png")
player_image_jump_left=pygame.transform.scale(player_image_jump_left,(PLAYER_WIDTH,PLAYER_HEIGHT))

pygame.init() 
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Platformer") 
clock = pygame.time.Clock() 

class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,PLAYER_X,PLAYER_Y,PLAYER_WIDTH,PLAYER_HEIGHT)
        self.image= player_image
        self.velocity_y = 0
        self.velocity_x = 0
        self.jumping= 0
        self.max_health= 5
        self.health = self.max_health
        self.direction = "right"

    def update_image(self):
        if self.jumping:
            if self.direction == "right":
                self.image = player_image_jump_right
            elif self.direction == "left":
                self.image = player_image_jump_left
        else:
            if self.direction == "right":
                self.image = player_image_right
            elif self.direction == "left":
                self.image = player_image_left


#MY PLAYER 
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
    #X
    player.x += player.velocity_x
    if player.x < 0:
        player.x = 0
    elif player.x + player.width > GAME_WIDTH:
        player.x = GAME_WIDTH - player.width
    check_tile_collision_x()

    #Y
    player.velocity_y += GRAVITY
    player.y += player.velocity_y
    check_tile_collision_y()

    
def draw():
    window.fill((50,50,50))
    window.blit(Background_image, (0,50))
    window.blit(player.image, player)
    for tile in tiles:
        window.blit(tile.image, tile)
    player.update_image()
    pygame.draw.rect(window, "red", (20,20, 20*player.max_health, 10))
    pygame.draw.rect(window, "green", (20,20, 20*player.health, 10))
#COLLISIONS
tiles=[]

def check_tile_collision():
    for tile in tiles:
        if player.colliderect(tile):
            return tile
    return None

def check_tile_collision_x():
    tile = check_tile_collision()
    if tile is not None:
        if player.velocity_x < 0: 
            player.x = tile.x + tile.width 
        elif player.velocity_x > 0:
            player.x = tile.x - player.width 
        player.velocity_x = 0

def check_tile_collision_y():
    tile = check_tile_collision()
    if tile is not None:
        if player.velocity_y < 0:  
                player.y = tile.y + tile.height 
        elif player.velocity_y > 0: 
            player.y = tile.y - player.height 
            player.jumping = False
        player.velocity_y = 0


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



class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

def create_map():
    for i in range(4):
        tile = Tile(player.x + i*TILE_SIZE, player.y + TILE_SIZE, floor_tile_image)
        tiles.append(tile)
    
    for i in range(16):
        tile = Tile(i*TILE_SIZE, player.y + TILE_SIZE*4, floor_tile_image)
        tiles.append(tile)

    for i in range(3):
        tile = Tile(TILE_SIZE*3, (i+9)*TILE_SIZE, floor_tile_image)
        tiles.append(tile)

#START THE GAME
player= Player()
create_map()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                take_screenshot()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping :
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping= 1
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and player.x>=0:
        player.velocity_x = -PLAYER_VELOCITY_X
        player.direction = "left"

    if keys[pygame.K_RIGHT] or keys[pygame.K_d] and player.x + PLAYER_WIDTH <= GAME_WIDTH:
        player.velocity_x = PLAYER_VELOCITY_X
        player.direction = "right"
    if not game_over and keys[pygame.K_o]:
        game_over = True
    if not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        player.velocity_x = 0

    #draw my start menu
    if not game_started:
        draw_start_menu()
        pygame.display.update()

        if keys[pygame.K_SPACE]:
            game_started = True
        continue
    #MOVE MY PLAYER USING KEYS

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
    
