import pygame
import sys
import json
import os


class Renderer:
    def __init__(self) -> None:
        self.get_file_settings()
        self.disp_surf = pygame.display.get_surface()

        # All outer frames (Changes made when buttons get clicked, etc)
        self.outer_frame_normal = pygame.image.load(
            "graphics/Outer-Frame1.png"
        ).convert_alpha()
        self.outer_frame_edit_clicked = pygame.image.load(
            "graphics/Outer-Frame2.png"
        ).convert_alpha()
        self.outer_frame_bg_clicked = pygame.image.load(
            "graphics/Outer-Frame3.png"
        ).convert_alpha()

        # background_surface is the surface on which the background image
        # will be drawn.
        self.bg_path = self.settings["background"]["bg_path"]
        self.background_surf = pygame.surface.Surface((400, 400))
        self.background_surf.set_colorkey("gray")
        self.background_surf.set_alpha(150)
        self.draw_background_image()

        self.current_frame = self.outer_frame_normal

        self.edit_button_rect = pygame.Rect(22, 342, 70, 38)
        self.bg_button_rect = pygame.Rect(210, 342, 170, 39)

        self.ticks = 0

    def change_background(self):
        initial_dir = "/home/prashant/Desktop/pygame/TODO/graphics/background"
        files = os.listdir(initial_dir)

        self.bg_path = (
            "/home/prashant/Desktop/pygame/TODO/graphics/background/"
            + files[(self.settings["background"]["index"] + 1) % (len(files))]
        )

        self.settings["background"]["index"] = (
            self.settings["background"]["index"] + 1
        ) % (len(files))
        self.settings["background"]["bg_path"] = self.bg_path
        self.modify_settings_file()
        self.draw_background_image()

    def get_file_settings(self):
        with open("/home/prashant/Desktop/pygame/TODO/settings/settings.json") as f:
            self.settings = json.load(f)

    def modify_settings_file(self):
        with open(
            "/home/prashant/Desktop/pygame/TODO/settings/settings.json", "w"
        ) as f:
            json.dump(self.settings, f)

    def draw_background_image(self):
        self.bg_image = pygame.image.load(self.bg_path).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (400, 400))
        self.background_surf.blit(self.bg_image, (0, 0))

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.button_events()

    def button_events(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.edit_button_rect.collidepoint(*mouse_pos):
            self.current_frame = self.outer_frame_edit_clicked
            # Open up editor

        if self.bg_button_rect.collidepoint(*mouse_pos):
            self.current_frame = self.outer_frame_bg_clicked

            # Changes background if button clicked
            if self.ticks < 0:
                if pygame.mouse.get_pressed()[0]:
                    self.ticks = 60
                    self.change_background()
            else:
                self.ticks -= 1

    def draw(self):
        self.disp_surf.fill("gray")
        self.disp_surf.blit(self.background_surf, (0, 0))
        self.disp_surf.blit(self.current_frame, (0, 0))

        self.current_frame = self.outer_frame_normal

    def run(self, dt):
        self.event_loop()
        self.draw()
