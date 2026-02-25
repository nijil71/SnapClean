import typer
from snapclean.core import create_snapshot

app = typer.Typer()

@app.command()
def main(
    path: str = typer.Option(".", help="Project path"),
    output: str = typer.Option("dist", help="Output directory"),
    build: bool = typer.Option(False, help="Run build before snapshot"),
    dry_run: bool = typer.Option(False, help="Preview without creating zip")
):
    """
    Create a clean project snapshot.
    """
    create_snapshot(path, output, build, dry_run)

