import pygame

#VARIABLES
GAME_WIDTH = 512
GAME_HEIGHT = 512

#BACKGROUND
Background_image= pygame.image.load("images/background.png")

pygame.init() 
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Platformer") 
clock = pygame.time.Clock() 


def draw():
    window.fill((50,50,50))
    window.blit(Background_image, (0,50))
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    draw()
    pygame.display.update()
    clock.tick(60)
    
