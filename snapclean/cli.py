import typer
from snapclean.core import create_snapshot

def main(
    path: str = ".",
    output: str = "dist",
    build: bool = False
):
    """
    Create a clean project snapshot.
    """
    create_snapshot(path, output, build)

if __name__ == "__main__":
    typer.run(main)