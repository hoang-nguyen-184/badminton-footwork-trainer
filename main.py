import random
import time

import pygame

from court import Court, POSITIONS
from screens import run_start_screen, run_end_screen
from shuttlecock import draw_shuttlecock
from sound import generate_hit_sound

# Design base resolution (all sizes are relative to this)
BASE_HEIGHT = 700
DARK_BG = (30, 30, 60)
WHITE = (255, 255, 255)


def run_training(surface, clock, config, hit_sound):
    """Run the training session. Returns stats dict."""
    w = surface.get_width()
    h = surface.get_height()
    scale = h / BASE_HEIGHT

    court = Court(w, h)
    position_names = list(POSITIONS.keys())

    duration = config["duration"]
    interval = config["interval"]
    display_dur = config["display_duration"]

    timer_font = pygame.font.SysFont(None, int(36 * scale))
    count_font = pygame.font.SysFont(None, int(24 * scale))

    shuttle_count = 0
    current_pos = None
    shuttle_visible = False

    training_start = time.time()
    # Set last_hide_time so the first shuttlecock appears immediately
    last_hide_time = training_start - interval
    shuttle_show_time = 0

    while True:
        now = time.time()
        elapsed = now - training_start
        remaining = max(0, duration - elapsed)

        # Check if training is over
        if remaining <= 0:
            return {
                "duration": duration,
                "interval": interval,
                "display_duration": display_dur,
                "shuttle_count": shuttle_count,
            }

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {
                    "duration": elapsed,
                    "interval": interval,
                    "display_duration": display_dur,
                    "shuttle_count": shuttle_count,
                }
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return {
                    "duration": elapsed,
                    "interval": interval,
                    "display_duration": display_dur,
                    "shuttle_count": shuttle_count,
                }

        # Shuttlecock timing logic
        if not shuttle_visible:
            wait_time = interval - display_dur
            if now - last_hide_time >= wait_time:
                # Show new shuttlecock at a different position
                available = [p for p in position_names if p != current_pos]
                current_pos = random.choice(available)
                shuttle_visible = True
                shuttle_show_time = now
                shuttle_count += 1
                hit_sound.play()
        else:
            if now - shuttle_show_time >= display_dur:
                shuttle_visible = False
                last_hide_time = now

        # Draw
        surface.fill(DARK_BG)

        # Timer at top
        mins = int(remaining) // 60
        secs = int(remaining) % 60
        timer_text = timer_font.render(f"Time Remaining: {mins:02d}:{secs:02d}", True, WHITE)
        surface.blit(timer_text, timer_text.get_rect(centerx=w // 2, y=int(15 * scale)))

        # Court
        court.draw(surface)

        # Shuttlecock
        if shuttle_visible and current_pos:
            px, py = court.get_position(current_pos)
            draw_shuttlecock(surface, px, py, label=current_pos, scale=scale)

        # Shuttle count at bottom
        count_text = count_font.render(f"Shuttles shown: {shuttle_count}", True, WHITE)
        surface.blit(count_text, (int(10 * scale), h - int(30 * scale)))

        pygame.display.flip()
        clock.tick(60)


def main():
    # Initialize mixer before pygame.init() for mono sound support
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    # Use the full native display resolution
    display_info = pygame.display.Info()
    screen_w = display_info.current_w
    screen_h = display_info.current_h
    surface = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Badminton Footwork Trainer")
    clock = pygame.time.Clock()

    # Generate the hit sound (may fail in environments without audio)
    try:
        hit_sound = generate_hit_sound()
    except Exception:
        class _SilentSound:
            def play(self):
                pass
        hit_sound = _SilentSound()

    while True:
        # Start screen
        config = run_start_screen(surface, clock)
        if config is None:
            break

        # Training
        stats = run_training(surface, clock, config, hit_sound)

        # End screen
        result = run_end_screen(surface, clock, stats)
        if result == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    main()
