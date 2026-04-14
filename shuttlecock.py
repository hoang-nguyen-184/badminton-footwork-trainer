import pygame

# Colors
FEATHER_COLOR = (255, 255, 240)
FEATHER_OUTLINE = (180, 180, 180)
CORK_COLOR = (200, 60, 60)
LABEL_COLOR = (255, 255, 100)


def draw_shuttlecock(surface, x, y, label=None):
    """Draw a shuttlecock at the given position with an optional label.

    The shuttlecock is drawn as a triangular feather cone with a cork circle.
    """
    r = 18  # feather radius

    # Feather cone (triangle pointing up)
    points = [
        (x, y - r),
        (x - r, y + r),
        (x + r, y + r),
    ]
    pygame.draw.polygon(surface, FEATHER_COLOR, points)
    pygame.draw.polygon(surface, FEATHER_OUTLINE, points, 2)

    # Feather lines for detail
    for i in range(1, 4):
        lx = x - r + i * (2 * r) // 4
        pygame.draw.line(surface, FEATHER_OUTLINE,
                         (x, y - r), (lx, y + r), 1)

    # Cork (circle at bottom of feathers)
    pygame.draw.circle(surface, CORK_COLOR, (x, y + r), 7)
    pygame.draw.circle(surface, (160, 40, 40), (x, y + r), 7, 1)

    # Position label
    if label:
        font = pygame.font.SysFont(None, 22)
        text = font.render(label, True, LABEL_COLOR)
        text_rect = text.get_rect(centerx=x, top=y + r + 12)
        surface.blit(text, text_rect)
