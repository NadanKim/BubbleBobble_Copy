import pygame
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((800, 600))

pygame.mixer.music.load("MainTheme.ogg")
pygame.mixer.music.play(-1, 0.0)

circle = pygame.draw.circle(window, (50,30,90), (90, 30), 16, 5)

window.blit(window, circle)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()