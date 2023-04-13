import pygame
import sys
from background import Background
from foreground import Foreground
from text_renderer import TextRenderer
import subprocess


class Renderer:
    def __init__(self) -> None:
        self.disp_surf = pygame.display.get_surface()

        # Initialises the background of the app
        self.background = Background()
        self.background.get_background_image()
        self.background.draw_background_image()

        # Initialises the foreground of the app
        self.foreground = Foreground()
        self.foreground.get_foreground_image()
        self.foreground.draw_foreground_image()

        # Initialises the text renderer
        self.text_renderer = TextRenderer()
        self.list_writing_proc = None

        self.edit_button_rect = pygame.Rect(22, 342, 70, 38)
        self.bg_button_rect = pygame.Rect(210, 342, 170, 39)

        self.ticks = 0

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.animate_buttons()

        if self.list_writing_proc is not None:
            if self.list_writing_proc.poll() == 0:
                self.list_writing_proc = None
                self.ticks = 0
                self.text_renderer.render()

    def animate_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.edit_button_rect.collidepoint(*mouse_pos):
            self.foreground.change_foreground(edit_button_clicked=True)

            # Ticks ensure that the edit button is not activated more than once during one click
            if self.ticks > 0:
                self.ticks -= 1
                return

            # Opens text editor
            if pygame.mouse.get_pressed()[0]:
                self.ticks = 20
                self.list_writing_proc = subprocess.Popen(["kate", "list/list.txt"])

        if self.bg_button_rect.collidepoint(*mouse_pos):
            self.foreground.change_foreground(bg_button_clicked=True)

            # Ticks ensure that the bg button is not activated more than once during one click
            if self.ticks > 0:
                self.ticks -= 1
                return

            # Changes background if button clicked
            if pygame.mouse.get_pressed()[0]:
                self.ticks = 20
                self.background.change_background()

    def draw(self):
        self.disp_surf.fill("gray")
        self.disp_surf.blit(self.background.get_surface(), (0, 0))
        self.disp_surf.blit(self.foreground.get_surface(), (0, 0))
        self.text_renderer.run()

    def run(self):
        self.event_loop()
        self.draw()
