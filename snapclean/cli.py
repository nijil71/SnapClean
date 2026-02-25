import typer
from rich.console import Console
from snapclean.core import create_snapshot
from snapclean import __version__

console = Console()
app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    path: str = typer.Option(".", help="Project path"),
    output: str = typer.Option("dist", help="Output directory"),
    build: bool = typer.Option(False, help="Run build before snapshot"),
    dry_run: bool = typer.Option(False, help="Preview without creating zip")
):
    """
    Create a clean project snapshot.
    """
    if ctx.invoked_subcommand is None:
        create_snapshot(path, output, build, dry_run)


@app.command()
def version():
    """
    Show snapclean version.
    """
    console.print(f"[bold green]snapclean version {__version__}[/bold green]")