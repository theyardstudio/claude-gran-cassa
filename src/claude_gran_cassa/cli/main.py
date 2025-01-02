import click
import pygame.midi


@click.group()
@click.option("--debug/--no-debug", default=False, help="Enable debug output")
def cli(debug):
    """Claude Gran Cassa Pattern Generator CLI"""
    if debug:
        click.echo("Debug mode enabled")


@cli.command()
def list_devices():
    """List available MIDI output devices"""
    pygame.midi.init()
    for i in range(pygame.midi.get_count()):
        info = pygame.midi.get_device_info(i)
        if info[3] == 1:
            click.echo(f"Device {i}: {info[1].decode()}")
    pygame.midi.quit()


def main():
    from .generate import generate
    from .evolve import evolve
    from .play import play

    cli.add_command(generate)
    cli.add_command(evolve)
    cli.add_command(play)
    cli.add_command(list_devices)
    cli()


if __name__ == "__main__":
    main()
