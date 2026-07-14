import time
import threading
import click
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .transcriber import transcribe_file
from .formatter import write_note

AUDIO_EXTENSIONS = {".mp3", ".aac", ".wav", ".m4a"}


class AudioHandler(FileSystemEventHandler):
    def __init__(self, output_path: Path, model: str):
        self.output_path = output_path
        self.model = model
        self._processing: set = set()
        self._lock = threading.Lock()

    def on_created(self, event):
        if event.is_directory:
            return
        self._dispatch(Path(event.src_path))

    def on_moved(self, event):
        # Catches files AirDropped or moved into the watched folder
        if event.is_directory:
            return
        self._dispatch(Path(event.dest_path))

    def _dispatch(self, path: Path):
        if path.suffix.lower() not in AUDIO_EXTENSIONS:
            return
        with self._lock:
            if path in self._processing:
                return
            self._processing.add(path)
        threading.Thread(target=self._process, args=(path,), daemon=True).start()

    def _process(self, path: Path):
        try:
            self._wait_stable(path)
            click.echo(f"Transcribing: {path.name}")
            text = transcribe_file(path, self.model)
            note_path = write_note(text, path, self.output_path)
            click.echo(f"Saved: {note_path.name}")
        except FileNotFoundError:
            click.echo(f"File disappeared before processing: {path.name}", err=True)
        except Exception as e:
            click.echo(f"Error processing {path.name}: {e}", err=True)
        finally:
            with self._lock:
                self._processing.discard(path)

    def _wait_stable(self, path: Path, stable_needed: int = 3, interval: float = 1.0):
        """Wait until file size stops changing — ensures the write is complete."""
        prev_size = -1
        stable_count = 0
        while stable_count < stable_needed:
            size = path.stat().st_size
            if size == prev_size and size > 0:
                stable_count += 1
            else:
                stable_count = 0
            prev_size = size
            time.sleep(interval)


def start_watching(input_path: Path, output_path: Path, model: str):
    handler = AudioHandler(output_path, model)
    observer = Observer()
    observer.schedule(handler, str(input_path), recursive=False)
    observer.start()
    click.echo(f"Watching {input_path}")
    click.echo("Press Ctrl+C to stop.")
    try:
        while observer.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\nStopping watcher...")
        observer.stop()
    observer.join()
