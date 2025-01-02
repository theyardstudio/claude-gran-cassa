import os
import pytest
import tempfile
from claude_gran_cassa.midi import MIDIConverter
from claude_gran_cassa.models import Composition, Pattern, SongConfig


def test_basic_midi_conversion():
    config = SongConfig(bpm=130)
    pattern = Pattern(
        hits=[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        divisions=16,
        channel=1,
        note=36,
        name="kick",
        velocities=[127, 120, 127, 120],
        panning=[64, 64, 64, 64],
    )

    composition = Composition(config=config, patterns=[pattern])
    converter = MIDIConverter()

    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp:
        converter.convert(composition, tmp.name)

        assert os.path.exists(tmp.name)
        assert os.path.getsize(tmp.name) > 0

        os.unlink(tmp.name)


def test_triplet_conversion():
    config = SongConfig(bpm=130)
    pattern = Pattern(
        hits=[1, 0, 1, 0, 1, 0],
        divisions=6,
        triplet=True,
        channel=1,
        note=42,
        name="hihat",
        velocities=[100, 80, 90],
        panning=[45, 80, 64],
    )

    composition = Composition(config=config, patterns=[pattern])
    converter = MIDIConverter()

    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp:
        converter.convert(composition, tmp.name)
        # TODO: Additional MIDI file validation
        os.unlink(tmp.name)
