import pytest
from claude_gran_cassa.models import Pattern, SongConfig, Composition


def test_pattern_initialization():
    pattern = Pattern(
        hits=[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        divisions=16,
        triplet=False,
        channel=1,
        note=36,
        name="kick",
    )

    assert len(pattern.velocities) == 4
    assert all(v == 100 for v in pattern.velocities)
    assert all(p == 64 for p in pattern.panning)


def test_composition_serialization():
    config = SongConfig(bpm=135)
    pattern = Pattern(hits=[1, 0, 0, 0], divisions=4, name="test")
    comp = Composition(config=config, patterns=[pattern])

    data = comp.to_dict()
    restored = Composition.from_dict(data)

    assert restored.config.bpm == 135
    assert restored.patterns[0].hits == [1, 0, 0, 0]
