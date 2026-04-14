# Badminton Footwork Trainer

A Python application that helps you practise badminton footwork by displaying a 2D court and flashing a shuttlecock at the six standard court corners. Place your laptop or screen court-side, watch for the shuttlecock, and move to the indicated position on a real court.

## How It Works

1. **Start screen** -- configure three settings (or keep the defaults) and press **START**.
2. **Training** -- a shuttlecock appears at a random corner, a hit sound plays, and the shuttlecock disappears after the display duration. After the reappear interval it shows up at a different corner. A countdown timer is shown at the top.
3. **End screen** -- see your session stats (total time, number of shuttlecocks shown) and choose to **Restart** or **Quit**.

### The Six Court Positions

```
         ┌─────────────────────┐
         │        NET          │
         ├─────────────────────┤
         │  Front L   Front R  │
         │                     │
         │  Mid L       Mid R  │
         │                     │
         │  Back L     Back R  │
         └─────────────────────┘
              (Baseline)
```

The shuttlecock never appears at the same position twice in a row.

## Requirements

- Python 3.8 or later
- [Pygame](https://www.pygame.org/) 2.0+

## Installation

```bash
git clone https://github.com/hoang-nguyen-184/badminton-footwork-trainer.git
cd badminton-footwork-trainer
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

On the start screen you can configure:

| Setting | Description | Default |
|---|---|---|
| Training Duration | Total session length in seconds | 60 |
| Reappear Interval | Seconds between shuttlecock appearances | 3 |
| Display Duration | How long the shuttlecock stays visible (must be less than the interval) | 1 |

### Controls

- **Click** an input field to edit it, **Tab** to move to the next field.
- **Enter** or click **START** to begin training.
- **Esc** to quit at any time (training will end early and stats will still be shown).

## Project Structure

```
main.py          Entry point and training game loop
court.py         Court drawing and position mapping
shuttlecock.py   Shuttlecock rendering
sound.py         Programmatic hit-sound generation (no external audio files)
screens.py       Start screen and end screen UI
requirements.txt Python dependencies
```

## License

See [LICENSE](LICENSE) for details.
