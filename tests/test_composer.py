import os
import pytest
from claude_gran_cassa.composer import Composer
from claude_gran_cassa.models import Composition


@pytest.fixture
def composer():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    return Composer(api_key)


def test_pattern_generation(composer):
    prompt = """Create a simple techno pattern with:
    - Basic kick on every quarter note
    - Hi-hats on 16th notes
    Set BPM to 130"""

    composition = composer.generate_pattern(prompt)

    assert hasattr(composition, "config")
    assert hasattr(composition, "patterns")

    assert composition.config.bpm == 130

    kick = next(p for p in composition.patterns if p.name == "kick")
    assert kick.hits.count(1) == 4

    hihat = next(p for p in composition.patterns if "hat" in p.name.lower())
    assert len(hihat.hits) == 16


def test_pattern_evolution(composer):
    initial_pattern = {
        "config": {"bpm": 130, "time_signature": [4, 4]},
        "patterns": [
            {
                "name": "kick",
                "hits": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                "divisions": 16,
                "triplet": False,
                "channel": 1,
                "note": 36,
                "velocities": [127, 127, 127, 127],
                "panning": [64, 64, 64, 64],
                "bars": 1,
            }
        ],
    }

    composition = Composition.from_dict(initial_pattern)

    evolved = composer.evolve_pattern(
        composition, "Add velocity variation to make it more dynamic"
    )

    kick = next(p for p in evolved.patterns if p.name == "kick")
    assert len(set(kick.velocities)) > 1
