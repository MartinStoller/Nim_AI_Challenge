import os.path
import pygame
import pygame.locals as pl
import itertools
from pygame_textinput import *

pygame.font.init()
WIDTH, HEIGHT = 960, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30
BLOCKSIZE = 60
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont('bahnschrift', 30)


class Block:
    def __init__(self,id,colour,position,size):
        self.size = size  # int: edge length
        self.colour = colour  # (R, G, B)
        self.id = id  # int
        self.position = position  # (x, y)

    def render(self,screen):
        pygame.draw.rect(screen,self.colour,(self.position[0], self.position[1], self.size, self.size))




def main():
    pygame.display.set_caption("Marty´s Coding Palace: Nim Challenge")
    # Create TextInput-object
    textinput = TextInput()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    piles = [1, 3, 5, 7]
    # Load Text displays:
    textsurface = []
    text0 = FONT.render('How many blocks do you want to', True, (0, 0, 0))
    text1 = FONT.render('remove and from which Line?', True, (0, 0, 0))
    text2 = FONT.render("Line:", True, (255, 255, 255))
    text3 = FONT.render("Amount of blocks:", True, (255, 255, 255))
    textsurface.append((text0, (80, 20)))
    textsurface.append((text1, (80, 55)))
    textsurface.append((text2, (600, 20)))
    textsurface.append((text3, (600, 55)))

    while True:
        screen.fill(WHITE)
        pygame.draw.rect(SCREEN, BLACK, (593, 0, 1000, 1000))
        pygame.draw.rect(SCREEN, WHITE, (850, 55, 50, 35), 2)
        pygame.draw.rect(SCREEN, WHITE, (675, 18, 50, 35), 2)

        for text in textsurface:
            SCREEN.blit(text[0], text[1])

        drawAllBlocks(SCREEN, piles)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Blit input surface onto the screen
        screen.blit(textinput.get_surface(), (690, 25))

        pygame.display.update()
        clock.tick(FPS)
        if textinput.update(events):
            print(textinput.get_text())


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()