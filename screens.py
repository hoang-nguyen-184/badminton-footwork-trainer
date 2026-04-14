import pygame

# Colors
WHITE = (255, 255, 255)
DARK_BG = (30, 30, 60)
GRAY = (180, 180, 180)
ACTIVE_BOX = (100, 200, 255)
INACTIVE_BOX = (200, 200, 200)
BTN_COLOR = (60, 120, 60)
BTN_HOVER = (80, 160, 80)
ERROR_COLOR = (255, 100, 100)
SUCCESS_COLOR = (100, 255, 100)


class InputBox:
    """A simple numeric text input field for Pygame."""

    def __init__(self, x, y, w, h, label, default_value=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.text = default_value
        self.active = False
        self.font = pygame.font.SysFont(None, 28)
        self.label_font = pygame.font.SysFont(None, 24)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_TAB:
                return "next_field"
            elif event.unicode.isdigit() or (event.unicode == "." and "." not in self.text):
                self.text += event.unicode
        return None

    def draw(self, surface):
        # Label above the box
        label_surf = self.label_font.render(self.label, True, GRAY)
        surface.blit(label_surf, (self.rect.x, self.rect.y - 25))
        # Box border
        color = ACTIVE_BOX if self.active else INACTIVE_BOX
        pygame.draw.rect(surface, color, self.rect, 2)
        # Text inside
        text_surf = self.font.render(self.text, True, WHITE)
        surface.blit(text_surf, (self.rect.x + 8, self.rect.y + 6))

    def get_value(self):
        try:
            return float(self.text)
        except ValueError:
            return None


class Button:
    """A clickable button for Pygame."""

    def __init__(self, x, y, w, h, text, font_size=32):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        color = BTN_HOVER if self.hovered else BTN_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=6)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


def run_start_screen(surface, clock):
    """Display the start screen with input fields. Returns config dict or None if quit."""
    w = surface.get_width()

    title_font = pygame.font.SysFont(None, 44)
    subtitle_font = pygame.font.SysFont(None, 24)
    error_font = pygame.font.SysFont(None, 22)

    box_w = 200
    box_h = 35
    box_x = (w - box_w) // 2
    spacing = 80

    input_duration = InputBox(box_x, 220, box_w, box_h, "Training Duration (seconds)", "60")
    input_interval = InputBox(box_x, 220 + spacing, box_w, box_h, "Reappear Interval (seconds)", "3")
    input_display = InputBox(box_x, 220 + spacing * 2, box_w, box_h, "Display Duration (seconds)", "1")
    inputs = [input_duration, input_interval, input_display]

    start_button = Button((w - 160) // 2, 220 + spacing * 3 + 10, 160, 50, "START")

    error_msg = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None

            # Handle tab navigation between fields
            for i, inp in enumerate(inputs):
                result = inp.handle_event(event)
                if result == "next_field":
                    inp.active = False
                    inputs[(i + 1) % len(inputs)].active = True
                    break

            if start_button.handle_event(event):
                dur = input_duration.get_value()
                ivl = input_interval.get_value()
                disp = input_display.get_value()

                if dur is None or ivl is None or disp is None:
                    error_msg = "All fields must be valid numbers!"
                elif dur <= 0 or ivl <= 0 or disp <= 0:
                    error_msg = "All values must be greater than 0!"
                elif disp >= ivl:
                    error_msg = "Display duration must be less than interval!"
                else:
                    return {
                        "duration": dur,
                        "interval": ivl,
                        "display_duration": disp,
                    }

            # Handle enter key to start
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                dur = input_duration.get_value()
                ivl = input_interval.get_value()
                disp = input_display.get_value()

                if dur and ivl and disp and dur > 0 and ivl > 0 and disp > 0 and disp < ivl:
                    return {
                        "duration": dur,
                        "interval": ivl,
                        "display_duration": disp,
                    }

        # Draw
        surface.fill(DARK_BG)

        title = title_font.render("Badminton Footwork Trainer", True, WHITE)
        surface.blit(title, title.get_rect(centerx=w // 2, y=60))

        subtitle = subtitle_font.render("Configure your training session:", True, GRAY)
        surface.blit(subtitle, subtitle.get_rect(centerx=w // 2, y=140))

        for inp in inputs:
            inp.draw(surface)

        start_button.draw(surface)

        if error_msg:
            err_surf = error_font.render(error_msg, True, ERROR_COLOR)
            surface.blit(err_surf, err_surf.get_rect(centerx=w // 2, y=220 + spacing * 3 + 75))

        pygame.display.flip()
        clock.tick(30)


def run_end_screen(surface, clock, stats):
    """Display the end screen with training stats. Returns 'restart' or 'quit'."""
    w = surface.get_width()

    title_font = pygame.font.SysFont(None, 48)
    stats_font = pygame.font.SysFont(None, 30)

    restart_btn = Button(w // 2 - 150, 480, 130, 50, "Restart")
    quit_btn = Button(w // 2 + 20, 480, 130, 50, "Quit")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"

            if restart_btn.handle_event(event):
                return "restart"
            if quit_btn.handle_event(event):
                return "quit"

        # Draw
        surface.fill(DARK_BG)

        title = title_font.render("Training Complete!", True, SUCCESS_COLOR)
        surface.blit(title, title.get_rect(centerx=w // 2, y=100))

        stat_lines = [
            f"Total Time: {stats['duration']:.1f} seconds",
            f"Shuttlecocks Shown: {stats['shuttle_count']}",
            f"Interval: {stats['interval']:.1f}s  |  Visible: {stats['display_duration']:.1f}s",
        ]
        for i, line in enumerate(stat_lines):
            surf = stats_font.render(line, True, WHITE)
            surface.blit(surf, surf.get_rect(centerx=w // 2, y=230 + i * 50))

        restart_btn.draw(surface)
        quit_btn.draw(surface)

        pygame.display.flip()
        clock.tick(30)
