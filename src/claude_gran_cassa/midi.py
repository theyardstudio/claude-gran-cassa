from midiutil import MIDIFile
from .models import Composition


class MIDIConverter:
    def __init__(self, ppqn: int = 480):
        self.ppqn = ppqn  # Pulses Per Quarter Note - high resolution for triplets

    def convert(self, composition: Composition, filename: str):
        midi = MIDIFile(1)  # Single track
        track = 0
        time = 0

        midi.addTempo(track, time, composition.config.bpm)

        for pattern in composition.patterns:
            if pattern.triplet:
                beat_length = self.ppqn * 4  # Length of a whole note in ticks
                division_length = beat_length // (pattern.divisions // pattern.bars)
                division_length = int(division_length * 2 / 3)  # Adjust for triplet
            else:
                # Regular timing
                beat_length = self.ppqn * 4
                division_length = beat_length // (pattern.divisions // pattern.bars)

            hit_index = 0
            for i, hit in enumerate(pattern.hits):
                if hit == "1":
                    tick_time = time + (i * division_length)
                    midi.addNote(
                        track=track,
                        channel=pattern.channel - 1,  # MIDI channels are 0-based
                        pitch=pattern.note,
                        time=tick_time / self.ppqn,  # Convert ticks to beats
                        duration=division_length
                        / self.ppqn
                        / 2,  # Short duration for percussion
                        volume=pattern.velocities[hit_index],
                    )
                    # Pan control
                    midi.addControllerEvent(
                        track=track,
                        channel=pattern.channel - 1,
                        time=tick_time / self.ppqn,
                        controller_number=10,  # Pan controller
                        parameter=pattern.panning[hit_index],
                    )
                    hit_index += 1

        with open(filename, "wb") as f:
            midi.writeFile(f)
