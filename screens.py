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

# Design base height — all sizes are authored for this and then scaled
BASE_HEIGHT = 700


class InputBox:
    """A simple numeric text input field for Pygame."""

    def __init__(self, x, y, w, h, label, default_value="", scale=1.0):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.text = default_value
        self.active = False
        self.scale = scale
        self.font = pygame.font.SysFont(None, int(28 * scale))
        self.label_font = pygame.font.SysFont(None, int(24 * scale))

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
        s = self.scale
        # Label above the box
        label_surf = self.label_font.render(self.label, True, GRAY)
        surface.blit(label_surf, (self.rect.x, self.rect.y - int(25 * s)))
        # Box border
        color = ACTIVE_BOX if self.active else INACTIVE_BOX
        pygame.draw.rect(surface, color, self.rect, max(2, int(2 * s)))
        # Text inside
        text_surf = self.font.render(self.text, True, WHITE)
        surface.blit(text_surf, (self.rect.x + int(8 * s), self.rect.y + int(6 * s)))

    def get_value(self):
        try:
            return float(self.text)
        except ValueError:
            return None


class Button:
    """A clickable button for Pygame."""

    def __init__(self, x, y, w, h, text, scale=1.0):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont(None, int(32 * scale))
        self.hovered = False
        self.scale = scale

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        border_w = max(2, int(2 * self.scale))
        radius = int(6 * self.scale)
        color = BTN_HOVER if self.hovered else BTN_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=radius)
        pygame.draw.rect(surface, WHITE, self.rect, border_w, border_radius=radius)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


def run_start_screen(surface, clock):
    """Display the start screen with input fields. Returns config dict or None if quit."""
    w = surface.get_width()
    h = surface.get_height()
    s = h / BASE_HEIGHT  # scale factor

    title_font = pygame.font.SysFont(None, int(44 * s))
    subtitle_font = pygame.font.SysFont(None, int(24 * s))
    error_font = pygame.font.SysFont(None, int(22 * s))

    box_w = int(200 * s)
    box_h = int(35 * s)
    box_x = (w - box_w) // 2
    spacing = int(80 * s)
    start_y = int(h * 0.30)  # start fields at 30% down the screen

    input_duration = InputBox(box_x, start_y, box_w, box_h,
                              "Training Duration (seconds)", "60", scale=s)
    input_interval = InputBox(box_x, start_y + spacing, box_w, box_h,
                              "Reappear Interval (seconds)", "3", scale=s)
    input_display = InputBox(box_x, start_y + spacing * 2, box_w, box_h,
                             "Display Duration (seconds)", "1", scale=s)
    inputs = [input_duration, input_interval, input_display]

    btn_w = int(160 * s)
    btn_h = int(50 * s)
    start_button = Button((w - btn_w) // 2, start_y + spacing * 3 + int(10 * s),
                           btn_w, btn_h, "START", scale=s)

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
        surface.blit(title, title.get_rect(centerx=w // 2, y=int(h * 0.09)))

        subtitle = subtitle_font.render("Configure your training session:", True, GRAY)
        surface.blit(subtitle, subtitle.get_rect(centerx=w // 2, y=int(h * 0.20)))

        for inp in inputs:
            inp.draw(surface)

        start_button.draw(surface)

        if error_msg:
            err_surf = error_font.render(error_msg, True, ERROR_COLOR)
            surface.blit(err_surf, err_surf.get_rect(
                centerx=w // 2, y=start_y + spacing * 3 + btn_h + int(25 * s)))

        pygame.display.flip()
        clock.tick(30)


def run_end_screen(surface, clock, stats):
    """Display the end screen with training stats. Returns 'restart' or 'quit'."""
    w = surface.get_width()
    h = surface.get_height()
    s = h / BASE_HEIGHT

    title_font = pygame.font.SysFont(None, int(48 * s))
    stats_font = pygame.font.SysFont(None, int(30 * s))

    btn_w = int(130 * s)
    btn_h = int(50 * s)
    btn_y = int(h * 0.68)
    restart_btn = Button(w // 2 - btn_w - int(10 * s), btn_y, btn_w, btn_h, "Restart", scale=s)
    quit_btn = Button(w // 2 + int(10 * s), btn_y, btn_w, btn_h, "Quit", scale=s)

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
        surface.blit(title, title.get_rect(centerx=w // 2, y=int(h * 0.14)))

        stat_lines = [
            f"Total Time: {stats['duration']:.1f} seconds",
            f"Shuttlecocks Shown: {stats['shuttle_count']}",
            f"Interval: {stats['interval']:.1f}s  |  Visible: {stats['display_duration']:.1f}s",
        ]
        line_spacing = int(50 * s)
        stats_start_y = int(h * 0.33)
        for i, line in enumerate(stat_lines):
            surf = stats_font.render(line, True, WHITE)
            surface.blit(surf, surf.get_rect(centerx=w // 2, y=stats_start_y + i * line_spacing))

        restart_btn.draw(surface)
        quit_btn.draw(surface)

        pygame.display.flip()
        clock.tick(30)
