import click
import json
import pygame.midi
import tempfile
from pathlib import Path
from ..models import Composition
from ..midi import MIDIConverter
from ..audio.engine import AudioEngine


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--audio/--midi", default=False, help="Use audio playback instead of MIDI"
)
@click.option(
    "--samples",
    type=click.Path(),
    help="Sound bank configuration for audio playback",
)
@click.option("--loop/--no-loop", default=False, help="Loop playback")
def play(input_file, audio, samples, loop):
    """Play a pattern from a file"""
    with open(input_file) as f:
        composition = Composition.from_dict(json.load(f))

    click.echo("Press Ctrl+C to stop looping")
    while True:
        play_pattern(composition, audio, samples)
        if not loop:
            break


def play_pattern(composition: Composition, use_audio: bool, samples: str):
    """Play a pattern using either MIDI or audio"""
    if use_audio:
        if not samples:
            click.echo("Error: Sound configuration required for audio playback")
            return

        engine = AudioEngine()
        engine.load_sound_bank(Path(samples))
        engine.play_pattern(composition)
    else:
        converter = MIDIConverter()
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp:
            converter.convert(composition, tmp.name)

            pygame.midi.init()
            player = pygame.midi.Output(pygame.midi.get_default_output_device_id())

            try:
                # TODO: MIDI playback implementation
                pass
            finally:
                player.close()
                pygame.midi.quit()
