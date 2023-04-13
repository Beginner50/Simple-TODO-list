import pygame
import os
import json
from pathlib import Path

class Background:
    def __init__(self) -> None:
        self.background_surf = pygame.surface.Surface((400, 400))
        self.background_surf.set_alpha(150)
        self.background_surf.set_colorkey("gray")

    def get_background_image(self):
        self.get_file_settings()
        self.bg_path = self.settings["background"]["bg_path"]

    def change_background(self):
        initial_dir = Path("graphics/background")
        files = os.listdir(initial_dir)

        self.settings["background"]["index"] = (
            self.settings["background"]["index"] + 1
        ) % (len(files))

        self.bg_path = (
            "graphics/background/" + files[self.settings["background"]["index"]]
        )
        self.settings["background"]["bg_path"] = self.bg_path
        self.modify_settings_file()
        self.draw_background_image()

    def get_file_settings(self):
        with open(Path("settings/settings.json")) as f:
            self.settings = json.load(f)

    def modify_settings_file(self):
        with open(Path("settings/settings.json"), "w") as f:
            json.dump(self.settings, f)

    def draw_background_image(self):
        self.bg_image = pygame.image.load(Path(self.bg_path)).convert_alpha()
        self.bg_image = pygame.transform.smoothscale(self.bg_image, (380, 380))
        self.background_surf.blit(self.bg_image, (10, 10))

    def get_surface(self):
        return self.background_surf
