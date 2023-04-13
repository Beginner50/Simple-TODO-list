import pygame


class Foreground:
    def __init__(self) -> None:
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

    def get_foreground_image(self):
        self.current_frame = self.outer_frame_normal

    def draw_foreground_image(self):
        pass

    def change_foreground(self, edit_button_clicked=False, bg_button_clicked=False):
        if edit_button_clicked:
            self.current_frame = self.outer_frame_edit_clicked

        if bg_button_clicked:
            self.current_frame = self.outer_frame_bg_clicked

    def get_surface(self):
        surf = self.current_frame
        self.current_frame = self.outer_frame_normal
        return surf
