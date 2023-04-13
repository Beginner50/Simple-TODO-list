import pygame


class FontRenderer:
    def __init__(
        self,
        font_size: int,
        font_style: str,
        center: tuple = None,
        topleft: tuple = None,
        max_width: int = 250,
    ) -> None:
        self.original_font_size = self.font_size = font_size
        self.font_style = font_style
        self.font = pygame.font.SysFont(self.font_style, self.font_size, True)

        self.surfs = []
        self.rects = []

        self.max_width = max_width

        if center is not None:
            self.placement = "center"
            self.current_coords = center
        if topleft is not None:
            self.placement = "topleft"
            self.current_coords = topleft
        self.original_coords = self.current_coords

        self.line_padding_y = lambda x: self.font_size * 2 if x else self.font_size + 6

    def render_text(self, text):
        if type(text) != list:
            while (
                self.create_rect(self.font.render(text, True, "Black")).width
                > self.max_width
            ):
                self.font_size -= 1
                self.font = pygame.font.SysFont(self.font_style, self.font_size, True)

            self.current_coords = self.original_coords
            self.surfs.append(self.font.render(text, True, "Black"))
            self.rects.append(self.create_rect(self.surfs[-1]))
            return

        for line in text:
            while (
                self.create_rect(
                    self.font.render(line["line"], True, "Black"),
                    separate_point=line["separate_point"],
                ).width
                > self.max_width
            ):
                self.font_size -= 1
                self.font = pygame.font.SysFont(self.font_style, self.font_size, True)

        self.current_coords = self.original_coords
        for line in text:
            self.surfs.append(
                self.font.render(line["line"][:-1], True, "Black"),
            )
            self.rects.append(
                self.create_rect(self.surfs[-1], separate_point=line["separate_point"])
            )

        if self.rects[-1].bottom > 350:
            self.surfs.clear()
            self.rects.clear()

            self.font_size -= 1
            self.render_text(text)

    def create_rect(self, surf, separate_point=True):
        self.current_coords = (
            self.current_coords[0],
            self.current_coords[1] + self.line_padding_y(separate_point),
        )
        if self.placement == "center":
            return surf.get_rect(center=self.current_coords)
        elif self.placement == "topleft":
            return surf.get_rect(topleft=self.current_coords)

    def get_surfaces(self):
        return self.surfs

    def get_rects(self):
        return self.rects

    def reset(self):
        self.font_size = self.original_font_size
        self.font = pygame.font.SysFont("Arial", self.font_size, True)
        self.surfs.clear()
        self.rects.clear()


class TextRenderer:
    def __init__(self) -> None:
        self.disp_surf = pygame.display.get_surface()
        self.title_renderer = FontRenderer(
            40, "Arial", center=(205, -40), max_width=350
        )
        self.paragraph_renderer = FontRenderer(
            30, "Arial", topleft=(40, 50), max_width=300
        )

        self.render()

    @staticmethod
    def get_file_contents():
        lines = []
        with open("/home/prashant/Desktop/pygame/TODO/list/list.txt") as f:
            title = f.readline()[:-1]

            while True:
                separate_point = True
                line = f.readline()

                while len(line) > 21:
                    index = 22
                    while line[index] not in ("\n", " "):
                        index -= 1
                    lines.append(
                        {"line": line[: index + 1], "separate_point": separate_point}
                    )
                    separate_point = False
                    line = line[index + 1 :]
                else:
                    lines.append({"line": line, "separate_point": separate_point})

                if lines[-1]["line"] == "":
                    break

        return title, lines

    def render(self):
        self.title_renderer.reset()
        self.paragraph_renderer.reset()

        title, paragraph = self.get_file_contents()
        self.title_renderer.render_text(title)
        self.paragraph_renderer.render_text(paragraph)

    def run(self):
        surfaces = (
            self.title_renderer.get_surfaces() + self.paragraph_renderer.get_surfaces()
        )
        rects = self.title_renderer.get_rects() + self.paragraph_renderer.get_rects()
        for i in range(len(surfaces)):
            self.disp_surf.blit(surfaces[i], rects[i])
