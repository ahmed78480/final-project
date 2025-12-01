import pygame
import os
##########################################################################
#VARIABLES an CONSTANTS
##########################################################################
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
ENEMY_WIDTH=36  
ENEMY_HEIGHT=30
BULLET_WIDTH = 16
BULLET_HEIGHT= 10
BULLET_VELOCITY= 8
ENEMY_BULLET_W= 12
ENEMY_BULLET_H=12
ENEMY_BULLET_VX=3
ENEMY_BULLET_VY=3


##########################################################################
#IMAGES
##########################################################################
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
enemy_image=pygame.image.load("images/metall-left.png")
enemy_image=pygame.transform.scale(enemy_image,(ENEMY_WIDTH,ENEMY_HEIGHT))
player_image_shoot_right = pygame.image.load("images/megaman-right-shoot.png")
player_image_shoot_right = pygame.transform.scale(player_image_shoot_right,(PLAYER_WIDTH,PLAYER_HEIGHT))
player_image_shoot_left = pygame.image.load("images/megaman-left-shoot.png")
player_image_shoot_left = pygame.transform.scale(player_image_shoot_left,(PLAYER_WIDTH,PLAYER_HEIGHT))
player_image_jump_shoot_right = pygame.image.load("images/megaman-right-jump-shoot.png")
player_image_jump_shoot_right = pygame.transform.scale(player_image_jump_shoot_right,(PLAYER_WIDTH,PLAYER_HEIGHT))
player_image_jump_shoot_left = pygame.image.load("images/megaman-left-jump-shoot.png")
player_image_jump_shoot_left = pygame.transform.scale(player_image_jump_shoot_left,(PLAYER_WIDTH,PLAYER_HEIGHT))
bullet_image= pygame.image.load("images/bullet.png")
bullet_image=pygame.transform.scale(bullet_image,(BULLET_WIDTH,BULLET_HEIGHT))
enemy_bullet_image= pygame.image.load("images/metall-bullet.png")
enemy_bullet_image=pygame.transform.scale(enemy_bullet_image,(ENEMY_BULLET_W,ENEMY_BULLET_H))
spike_image=pygame.image.load("images/spike.png")
spike_image=pygame.transform.scale(spike_image,(32,32))

##########################################################################
#GAME STATE
##########################################################################
game_started = False
game_over = False
tiles = []
enemies = []
spikes = []

#create my window####################################################################################
pygame.init() 
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Platformer") 
clock = pygame.time.Clock() 

##########################################################################
#Classes
##########################################################################
class Player(pygame.Rect):
    class Bullet(pygame.Rect):
        def __init__(self):
                if player.direction == "left":
                    pygame.Rect.__init__(self, player.x, player.y + TILE_SIZE/2,
                                        BULLET_WIDTH, BULLET_HEIGHT)
                    self.velocity_x = -BULLET_VELOCITY
                elif player.direction == "right":
                    pygame.Rect.__init__(self, player.x + player.width, player.y + TILE_SIZE/2,BULLET_WIDTH, BULLET_HEIGHT)
                    self.velocity_x = BULLET_VELOCITY
                self.image = bullet_image
                self.used= False
    def __init__(self):
        pygame.Rect.__init__(self,PLAYER_X,PLAYER_Y,PLAYER_WIDTH,PLAYER_HEIGHT)
        self.image= player_image
        self.velocity_y = 0
        self.velocity_x = 0
        self.jumping= 0
        self.max_health= 15
        self.health = self.max_health
        self.direction = "right"
        self.shooting=0
        self.bullets=[]
        self.shooting_timer=0
    def start_shooting(self):
        self.shooting=True
        self.shooting_timer=5
        self.bullets.append(Player.Bullet())

    def update_image(self):
        if self.jumping and self.shooting:
            if self.direction == "right":
                self.image = player_image_jump_shoot_right
            elif self.direction == "left":
                self.image = player_image_jump_shoot_left
        elif self.shooting:
            if self.direction == "right":
                self.image = player_image_shoot_right
            elif self.direction == "left":
                self.image = player_image_shoot_left
        elif self.jumping:
            if self.direction == "right":
                self.image = player_image_jump_right
            elif self.direction == "left":
                self.image = player_image_jump_left
        else:
            if self.direction == "right":
                self.image = player_image_right
            elif self.direction == "left":
                self.image = player_image_left

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image
class Enemy(pygame.Rect):
    class Bullet(pygame.Rect):
        def __init__(self, enemy, velocity_y):
            if enemy.direction=="left":
                pygame.Rect.__init__(self, enemy.x,enemy.y+TILE_SIZE/2,ENEMY_BULLET_W,ENEMY_BULLET_H)
                self.velocity_x= - ENEMY_BULLET_VX
                self.velocity_y= velocity_y
                self.image=enemy_bullet_image
                self.used= False
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.image = enemy_image
        self.velocity_y = 0
        self.direction = "left"
        self.health= 3
        self.bullets=[]
        self.shooting= False
        self.shoot_timer = 0

    def shoot(self):
        velocities = [-ENEMY_BULLET_VY, 0, ENEMY_BULLET_VY]

        for vy in velocities:
            bullet = Enemy.Bullet(self, vy)
            self.bullets.append(bullet)




##########################################################################
#GAME STATE FONTS
##########################################################################
menu_font = pygame.font.Font("assets/font.ttf", 48)
small_font = pygame.font.Font("assets/font.ttf", 24)

##########################################################################
#GAME FUNCTIONS
##########################################################################

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

def move_player(velocity_x):
    move_map(velocity_x)
    tile= check_tile_collision(player)
    if tile is not None:
        move_map(-velocity_x)

def move_map(velocity_x):
    for tile in tiles:
        tile.x+=velocity_x
    
    for enemy in enemies:
        enemy.x+= velocity_x
    
    for spike in spikes:
        spike.x+= velocity_x

def move():
    global enemies
    # Player falling
    #Y
    player.velocity_y += GRAVITY
    player.y += player.velocity_y
    check_tile_collision_y(player)
    # Spike collision

    for spike in spikes :
        if player.colliderect(spike):
            player.health=0
    #enemy
    for enemy in enemies:
        enemy.velocity_y +=GRAVITY 
        enemy.y +=enemy.velocity_y
        check_tile_collision_y(enemy)
        
        if player.colliderect(enemy):
            player.health -= 0.1

        enemy.shoot_timer += 1
        if enemy.shoot_timer >= 120:  
            enemy.shoot()
            enemy.shoot_timer = 0



#bullets
    for bullet in player.bullets:
        bullet.x += bullet.velocity_x
        for bullet in player.bullets[:]:
            bullet.x += (bullet.velocity_x)*0.01
        if bullet.x < 0 or bullet.x > GAME_WIDTH:
            player.bullets.remove(bullet)
        for enemy in enemies:
            if enemy.health >0 and not bullet.used and bullet.colliderect(enemy):
                enemy.health-= 1
                bullet.used= True

    player.bullets=[bullet for bullet in player.bullets if not bullet.used]
    if player.shooting_timer > 0:
        player.shooting_timer -= 1
    else:
        player.shooting = False
    enemies =[enemy for enemy in enemies if enemy.health>0]
#ENEMY BULLETS
    for enemy in enemies:
        for bullet in enemy.bullets[:]:
            bullet.x += bullet.velocity_x
            bullet.y += bullet.velocity_y

            if bullet.x < 0 or bullet.x > GAME_WIDTH or bullet.y < 0 or bullet.y > GAME_HEIGHT:
                enemy.bullets.remove(bullet)
                continue

            if not bullet.used and bullet.colliderect(player):
                player.health -= 1
                bullet.used = True
                enemy.bullets.remove(bullet)

def draw():
    window.fill((50,50,50))
    window.blit(Background_image, (0,50))
    window.blit(player.image, player)
    for enemy in enemies:
        window.blit(enemy.image, enemy)
    for tile in tiles:
        window.blit(tile.image, tile)
    for spike in spikes:
        window.blit(spike.image, spike)
    player.update_image()
    for bullet in player.bullets:
        window.blit(bullet.image, bullet)
    for enemy in enemies:
        for bullet in enemy.bullets:
            window.blit(enemy_bullet_image, bullet)
    pygame.draw.rect(window, "red", (20,20, 20*player.max_health, 10))
    pygame.draw.rect(window, "green", (20,20, 20*player.health, 10))
#COLLISIONS

def check_tile_collision(character):
    for tile in tiles:
        if character.colliderect(tile):
            return tile
    return None

def check_tile_collision_x(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_x < 0: 
            character.x = tile.x + tile.width 
        elif character.velocity_x > 0:
            character.x = tile.x - character.width 
        character.velocity_x = 0

def check_tile_collision_y(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_y < 0:  
                character.y = tile.y + tile.height 
        elif character.velocity_y > 0: 
            character.y = tile.y - character.height 
            character.jumping = False
        character.velocity_y = 0


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



#CREATE MY MAP FUNCTION
def create_map():
    for i in range(60):
        tile = Tile(i * TILE_SIZE, player.y + TILE_SIZE * 4, floor_tile_image)
        tiles.append(tile)

    for h in range(20):
        tile = Tile(0, player.y + TILE_SIZE * 4 - h * TILE_SIZE, floor_tile_image)
        tiles.append(tile)
    right_wall_x = 59 * TILE_SIZE
    for h in range(20):
        tile = Tile(right_wall_x, player.y + TILE_SIZE * 4 - h * TILE_SIZE, floor_tile_image)
        tiles.append(tile)

    
    spike_positions = [1, 2,22,23, 24, 25,38]

    for pos in spike_positions:
        spike = Tile(pos * TILE_SIZE, player.y + TILE_SIZE * 3, spike_image)
        spikes.append(spike)


    for i in range(5):
        tile = Tile(10 * TILE_SIZE + i * TILE_SIZE, player.y + TILE_SIZE * 1, floor_tile_image)
        tiles.append(tile)


    enemies.append(Enemy(12 * TILE_SIZE, player.y + TILE_SIZE * 1 - ENEMY_HEIGHT))


    for i in range(4):
        tile = Tile(25 * TILE_SIZE + i * TILE_SIZE, player.y + TILE_SIZE * 2, floor_tile_image)
        tiles.append(tile)


    for i in range(6):
        tile = Tile(40 * TILE_SIZE + i * TILE_SIZE, player.y + TILE_SIZE * 1, floor_tile_image)
        tiles.append(tile)

    enemies.append(Enemy(42 * TILE_SIZE, player.y + TILE_SIZE * 1 - ENEMY_HEIGHT))

    extra_enemy_positions = [
        (5 * TILE_SIZE,  player.y + TILE_SIZE * 3),  
        (18 * TILE_SIZE, player.y + TILE_SIZE * 3),  
        (33 * TILE_SIZE, player.y + TILE_SIZE * 2),   
        (50 * TILE_SIZE, player.y + TILE_SIZE * 3),   
        (46 * TILE_SIZE, player.y + TILE_SIZE * 1 - ENEMY_HEIGHT),
        (55 * TILE_SIZE, player.y + TILE_SIZE * 3),
        (48 * TILE_SIZE, player.y + TILE_SIZE * 3),
        (57 * TILE_SIZE, player.y + TILE_SIZE * 3) 
    ]

    for x, y in extra_enemy_positions:
        enemies.append(Enemy(x, y))
#INITIALIZE THE GAME
player= Player()
tiles=[]
enemies=[]
spikes=[]
create_map()


#GAME MAIN LOOP
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
        move_player(PLAYER_VELOCITY_X)
        player.direction = "left"

    if keys[pygame.K_RIGHT] or keys[pygame.K_d] and player.x + PLAYER_WIDTH <= GAME_WIDTH:
        move_player(-PLAYER_VELOCITY_X)
        player.direction = "right"
    if not game_over and keys[pygame.K_o] or player.health==0: 
        game_over = True
    if not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        player.velocity_x = 0
    if keys[pygame.K_x] and len(player.bullets) <= 1 :
        player.start_shooting()
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
    #RESTART MY GAME(press R)
        if keys[pygame.K_r]:
                player.x = PLAYER_X
                player.y = PLAYER_Y
                player.health = player.max_health
                player.velocity_y = 0
                player.bullets.clear()
                tiles.clear()
                enemies.clear()
                spikes.clear()
                create_map()
                game_over = False
        continue
    
    move()
    draw()
    pygame.display.update()
    clock.tick(60)
    
