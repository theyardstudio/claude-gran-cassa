import click
import json
from pathlib import Path
from ..composer import Composer
from ..config import config
from .play import play_pattern
from .utils import get_versioned_filename


@click.command()
@click.argument("prompt")
@click.argument("output", type=click.Path())
@click.option("--play/--no-play", default=False, help="Play pattern after generation")
@click.option(
    "--audio/--midi", default=False, help="Use audio playback instead of MIDI"
)
@click.option(
    "--samples",
    type=click.Path(),
    help="Sound bank configuration for audio playback",
)
@click.option("--version/--no-version", default=True, help="Enable filename versioning")
def generate(prompt, output, play, audio, samples, version):
    """Generate a new pattern from a prompt"""
    composer = Composer(api_key=config.api_key)
    composition = composer.generate_pattern(prompt)

    output_path = Path(output)
    if version:
        output_path = get_versioned_filename(output_path)

    with open(output_path, "w") as f:
        json.dump(composition.to_dict(), f, indent=2)
    click.echo(f"Generated pattern saved to {output_path}")

    if play:
        play_pattern(composition, audio, samples)
