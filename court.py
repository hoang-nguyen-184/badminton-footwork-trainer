import pygame

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 120, 50)
NET_COLOR = (220, 220, 220)

# Real badminton court dimensions (meters)
COURT_WIDTH = 6.1       # doubles width
COURT_LENGTH = 13.4     # full court length
HALF_LENGTH = 6.7       # half court (baseline to net)

# Key distances from baseline (meters) for half-court
SHORT_SERVICE_LINE = 1.98  # from net = 6.7 - 1.98 = 4.72 from baseline
LONG_SERVICE_LINE = 0.76   # from baseline
SINGLES_SIDELINE_INSET = 0.46  # from each side

# Fractions of half-court height (from baseline = 0.0, net = 1.0)
FRAC_LONG_SERVICE = LONG_SERVICE_LINE / HALF_LENGTH          # ~0.113
FRAC_SHORT_SERVICE = (HALF_LENGTH - SHORT_SERVICE_LINE) / HALF_LENGTH  # ~0.704
FRAC_SINGLES_INSET = SINGLES_SIDELINE_INSET / COURT_WIDTH    # ~0.0754

# 6 standard positions as (x_fraction, y_fraction) of court rect
# x: 0=left, 1=right; y: 0=baseline(bottom), 1=net(top)
POSITIONS = {
    "Front Left":  (0.20, 0.85),
    "Front Right": (0.80, 0.85),
    "Mid Left":    (0.10, 0.50),
    "Mid Right":   (0.90, 0.50),
    "Back Left":   (0.20, 0.15),
    "Back Right":  (0.80, 0.15),
}


class Court:
    """Handles computing court dimensions and drawing the court."""

    def __init__(self, window_width, window_height, top_margin=60, bottom_margin=40, side_margin=30):
        self.window_width = window_width
        self.window_height = window_height
        self.rect = self._compute_rect(top_margin, bottom_margin, side_margin)

    def _compute_rect(self, top_margin, bottom_margin, side_margin):
        available_w = self.window_width - 2 * side_margin
        available_h = self.window_height - top_margin - bottom_margin
        aspect = HALF_LENGTH / COURT_WIDTH  # ~1.098

        court_w = min(available_w, available_h / aspect)
        court_h = court_w * aspect

        court_x = (self.window_width - court_w) / 2
        court_y = top_margin + (available_h - court_h) / 2

        return pygame.Rect(int(court_x), int(court_y), int(court_w), int(court_h))

    def get_position(self, name):
        """Convert a position name to pixel coordinates on the court.

        The court is drawn with the net at the top and baseline at the bottom.
        """
        fx, fy = POSITIONS[name]
        px = self.rect.left + self.rect.width * fx
        py = self.rect.bottom - self.rect.height * fy
        return int(px), int(py)

    def get_all_positions(self):
        """Return a dict of all position names to pixel coords."""
        return {name: self.get_position(name) for name in POSITIONS}

    def draw(self, surface):
        """Draw the badminton half-court on the given surface."""
        r = self.rect

        # Court surface
        pygame.draw.rect(surface, GREEN, r)

        # Outer boundary (doubles sidelines + baseline + net line)
        pygame.draw.rect(surface, WHITE, r, 2)

        # Singles sidelines
        inset = int(r.width * FRAC_SINGLES_INSET)
        pygame.draw.line(surface, WHITE,
                         (r.left + inset, r.top), (r.left + inset, r.bottom), 2)
        pygame.draw.line(surface, WHITE,
                         (r.right - inset, r.top), (r.right - inset, r.bottom), 2)

        # Short service line
        service_y = int(r.bottom - r.height * FRAC_SHORT_SERVICE)
        pygame.draw.line(surface, WHITE,
                         (r.left, service_y), (r.right, service_y), 2)

        # Long service line (doubles, near baseline)
        long_y = int(r.bottom - r.height * FRAC_LONG_SERVICE)
        pygame.draw.line(surface, WHITE,
                         (r.left, long_y), (r.right, long_y), 2)

        # Center line (from short service line to long service line)
        center_x = r.left + r.width // 2
        pygame.draw.line(surface, WHITE,
                         (center_x, service_y), (center_x, long_y), 2)

        # Net at top — drawn slightly wider and thicker
        net_extend = 10
        pygame.draw.line(surface, NET_COLOR,
                         (r.left - net_extend, r.top),
                         (r.right + net_extend, r.top), 4)

        # "NET" label
        font = pygame.font.SysFont(None, 20)
        label = font.render("NET", True, NET_COLOR)
        label_rect = label.get_rect(centerx=r.centerx, bottom=r.top - 4)
        surface.blit(label, label_rect)
