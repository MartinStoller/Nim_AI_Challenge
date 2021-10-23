import pygame
import sys
import gui
import time


class Button:
    def __init__(self, text0, text1, width, height, position, screen, training_iterations, clock, elevation, faces):
        # Core attributes
        self.pressed = False
        self.faces = faces  # which face pictures should be shown on top of Blocks
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = position[1]
        self.screen = screen
        self.clock = clock
        self.training_iterations = training_iterations

        # top rectangle
        self.top_rect = pygame.Rect(position, (width,height))
        self.top_color = "#475F77"
        self.button_font = pygame.font.Font(None, 22)

        # bottom rectangle
        self.bottom_rect = pygame.Rect(position, (width, elevation))
        self.bottom_color = "#354B5E"

        #text:
        self.text_surf0 = self.button_font.render(text0, True, "#FFFFFF")
        self.text_surf1 = self.button_font.render(text1, True, "#FFFFFF")
        self.text_rect0 = self.text_surf0.get_rect(center=(self.top_rect.center[0], self.top_rect.center[1] - 11))
        self.text_rect1 = self.text_surf1.get_rect(center=(self.top_rect.center[0], self.top_rect.center[1] + 11))

    def draw(self):
        # elevation logic:
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect0.center = (self.top_rect.center[0], self.top_rect.center[1] - 11)
        self.text_rect1.center = (self.top_rect.center[0], self.top_rect.center[1] + 11)

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=16)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=16)
        self.screen.blit(self.text_surf0, self.text_rect0)
        self.screen.blit(self.text_surf1, self.text_rect1)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "#D74B4B"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed is True:
                    self.pressed = False
                    gui.run_playingscreen(self.training_iterations, SCREEN=self.screen,
                                          clock=self.clock, faces=self.faces)
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#475F77"

