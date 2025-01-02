import json
import pygame.midi
import pygame.mixer
import time
from pathlib import Path
from ..models import Composition


class AudioEngine:
    def __init__(self):
        pygame.mixer.init(44100, -16, 2, 2048)
        self.sounds = {}

    def load_sound_bank(self, config_path: Path):
        with open(config_path) as f:
            self.sound_config = json.load(f)
            for note, sound_file in self.sound_config.items():
                self.sounds[int(note)] = pygame.mixer.Sound(sound_file)

    def play_pattern(self, composition: Composition):
        bpm = composition.config.bpm
        ms_per_tick = (60000 / bpm) / 4  # ms per 16th note

        # Group events by time
        timeline = {}
        for pattern in composition.patterns:
            hit_count = 0
            for i, hit in enumerate(pattern.hits):
                if hit == 1:
                    tick = i * ms_per_tick
                    if tick not in timeline:
                        timeline[tick] = []
                    timeline[tick].append(
                        {
                            "note": pattern.note,
                            "velocity": pattern.velocities[hit_count],
                            "pan": pattern.panning[hit_count],
                        }
                    )
                    hit_count += 1

        # Play events
        start_time = time.time() * 1000
        for tick, events in sorted(timeline.items()):
            while (time.time() * 1000 - start_time) < tick:
                time.sleep(0.001)
            for event in events:
                if event["note"] in self.sounds:
                    sound = self.sounds[event["note"]]
                    velocity = event["velocity"] / 127
                    # Convert pan (0-127) to stereo balance (-1.0 to 1.0)
                    pan = (event["pan"] - 64) / 64.0
                    sound.set_volume(velocity)
                    # sound.set_volume(velocity * (1 - pan), velocity * (1 + pan))
                    sound.play()
