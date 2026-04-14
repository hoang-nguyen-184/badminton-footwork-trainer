import array
import math

import pygame


def generate_hit_sound(frequency=880, duration_ms=120, volume=0.6, sample_rate=44100):
    """Generate a short percussive 'hit' sound programmatically.

    Returns a pygame.mixer.Sound with a sharp attack and fast decay,
    simulating a badminton shuttle hit.
    """
    n_samples = int(sample_rate * duration_ms / 1000)
    max_val = int(32767 * volume)
    samples = array.array("h", [0] * n_samples)

    for i in range(n_samples):
        t = i / sample_rate
        # Mix two frequencies for a richer "thwack" sound
        wave = (
            0.6 * math.sin(2 * math.pi * frequency * t)
            + 0.3 * math.sin(2 * math.pi * (frequency * 1.5) * t)
            + 0.1 * math.sin(2 * math.pi * (frequency * 3) * t)
        )
        # Exponential decay envelope for percussive feel
        decay = math.exp(-8.0 * (i / n_samples))
        samples[i] = int(max_val * wave * decay)

    sound = pygame.mixer.Sound(buffer=bytes(samples))
    return sound
