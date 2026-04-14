import pygame

# Colors
FEATHER_COLOR = (255, 255, 240)
FEATHER_OUTLINE = (180, 180, 180)
CORK_COLOR = (200, 60, 60)
LABEL_COLOR = (255, 255, 100)


def draw_shuttlecock(surface, x, y, label=None, scale=1.0):
    """Draw a shuttlecock at the given position with an optional label.

    The shuttlecock is drawn as a triangular feather cone with a cork circle.
    scale: multiplier relative to the base 700px design height.
    """
    r = int(18 * scale)   # feather radius
    cork_r = int(7 * scale)
    line_w = max(1, int(1 * scale))
    outline_w = max(2, int(2 * scale))

    # Feather cone (triangle pointing down into the cork)
    points = [
        (x - r, y - r),
        (x + r, y - r),
        (x, y + r),
    ]
    pygame.draw.polygon(surface, FEATHER_COLOR, points)
    pygame.draw.polygon(surface, FEATHER_OUTLINE, points, outline_w)

    # Feather lines for detail
    for i in range(1, 4):
        lx = x - r + i * (2 * r) // 4
        pygame.draw.line(surface, FEATHER_OUTLINE,
                         (lx, y - r), (x, y + r), line_w)

    # Cork (circle at the tip of the cone)
    pygame.draw.circle(surface, CORK_COLOR, (x, y + r), cork_r)
    pygame.draw.circle(surface, (160, 40, 40), (x, y + r), cork_r, line_w)

    # Position label
    if label:
        font = pygame.font.SysFont(None, int(22 * scale))
        text = font.render(label, True, LABEL_COLOR)
        text_rect = text.get_rect(centerx=x, top=y + r + cork_r + int(4 * scale))
        surface.blit(text, text_rect)
