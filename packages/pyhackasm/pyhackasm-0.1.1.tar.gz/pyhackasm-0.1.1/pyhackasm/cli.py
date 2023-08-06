from pathlib import Path

import typer

cli = typer.Typer()


@cli.command(name="assemble")
def assemble(
        filepth: Path = typer.Argument(
            ...,
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        )
):
    typer.echo(filepth)


if __name__ == "__main__":
    cli()
