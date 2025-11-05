import pygame

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


#MY PLAYER 
player= Player()

#

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
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #MOVE MY PLAYER USING KEYS

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping :
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping= 1
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and player.x>=0:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d] and player.x + PLAYER_WIDTH <= GAME_WIDTH:
        player.x += PLAYER_SPEED

    move()
    draw()
    pygame.display.update()
    clock.tick(60)
    
