import click
import json
from pathlib import Path
from ..composer import Composer
from ..config import config
from ..models import Composition
from .play import play_pattern
from .utils import get_versioned_filename


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("prompt")
@click.argument("output", type=click.Path())
@click.option("--play/--no-play", default=False, help="Play evolved pattern")
@click.option(
    "--audio/--midi", default=False, help="Use audio playback instead of MIDI"
)
@click.option(
    "--samples",
    type=click.Path(),
    help="Sound bank configuration for audio playback",
)
@click.option("--version/--no-version", default=True, help="Enable filename versioning")
def evolve(input_file, prompt, output, play, audio, samples, version):
    """Evolve an existing pattern"""
    with open(input_file) as f:
        original = Composition.from_dict(json.load(f))

    composer = Composer(api_key=config.api_key)
    evolved = composer.evolve_pattern(original, prompt)

    output_path = Path(output)
    if version:
        output_path = get_versioned_filename(output_path)

    with open(output_path, "w") as f:
        json.dump(evolved.to_dict(), f, indent=2)
    click.echo(f"Evolved pattern saved to {output_path}")

    if play:
        play_pattern(evolved, audio, samples)
