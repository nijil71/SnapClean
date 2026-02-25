import typer
from snapclean.core import create_snapshot
from rich.console import Console

console = Console()
app = typer.Typer()

__version__ = "0.2.0"


@app.command()
def run(
    path: str = typer.Option(".", help="Project path"),
    output: str = typer.Option("dist", help="Output directory"),
    build: bool = typer.Option(False, help="Run build before snapshot"),
    dry_run: bool = typer.Option(False, help="Preview without creating zip")
):
    """
    Create a clean project snapshot.
    """
    create_snapshot(path, output, build, dry_run)

@app.command()
def version():
    """
    Show snapclean version.
    """
    console.print(f"[bold green]snapclean version {__version__}[/bold green]")