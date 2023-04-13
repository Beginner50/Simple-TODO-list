#!/home/prashant/Desktop/pygame/.venv/bin/python3
import pygame
from renderer import Renderer
import os


class Main:
    def __init__(self) -> None:
        posx, posy = 1000, 400
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{posx},{posy}"

        pygame.init()

        self.window = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Todo list")

        self.renderer = Renderer()
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60)

            self.renderer.run()

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()
