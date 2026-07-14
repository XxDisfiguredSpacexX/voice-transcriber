import click
from pathlib import Path
from .watcher import start_watching
from .transcriber import transcribe_file
from .formatter import write_note

DEFAULT_OUTPUT = str(Path.home() / "Documents" / "Welcome-obsidian-main" / "Voice Notes")


@click.group()
def cli():
    """Transcribes audio files into Obsidian vault notes using local Whisper."""
    pass


@cli.command()
@click.option(
    "--input", "-i",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Folder to watch for new audio files.",
)
@click.option(
    "--output", "-o",
    default=DEFAULT_OUTPUT,
    show_default=True,
    type=click.Path(file_okay=False, dir_okay=True),
    help="Obsidian folder to write transcript notes into.",
)
@click.option(
    "--model", "-m",
    default="base",
    show_default=True,
    type=click.Choice(["tiny", "base", "small", "medium", "large"]),
    help="Whisper model size. Larger = more accurate but slower.",
)
def watch(input, output, model):
    """Watch a folder and transcribe any new audio file automatically."""
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    start_watching(Path(input), output_path, model)


@cli.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--output", "-o",
    default=DEFAULT_OUTPUT,
    show_default=True,
    type=click.Path(file_okay=False, dir_okay=True),
    help="Obsidian folder to write the transcript note into.",
)
@click.option(
    "--model", "-m",
    default="base",
    show_default=True,
    type=click.Choice(["tiny", "base", "small", "medium", "large"]),
    help="Whisper model size. Larger = more accurate but slower.",
)
def transcribe(file, output, model):
    """Transcribe a single audio FILE immediately."""
    audio_path = Path(file)
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    click.echo(f"Transcribing {audio_path.name}...")
    text = transcribe_file(audio_path, model)
    note_path = write_note(text, audio_path, output_path)
    click.echo(f"Saved: {note_path}")
