import typer

from dataclasses import dataclass
from typing import List, Optional

from src.utils.watcher import watch_files
from src.utils.configure import app as configure, Config

app = typer.Typer(rich_markup_mode="rich", add_completion=False)
app.add_typer(configure, name="configure", help="Configure PyTest-Watcher")


@dataclass
class State:
    verbose: bool = False
    useConfig: bool = False
    autoClear: bool = False


def version_callback(value: bool):
    if value:
        typer.echo(f"Py-Watcher Version: {typer.style('0.1.0', fg='blue')}")
        raise typer.Exit()


@app.callback()
def main(
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        help="[red][GLOBAL][/red] Verbose testing mode",
    ),
    useConfig: bool = typer.Option(
        False,
        "-c",
        "--config",
        help="[red][GLOBAL][/red] Use config file for testing",
    ),
    autoClear: bool = typer.Option(
        False,
        "-a",
        "--auto-clear",
        help="[red][GLOBAL][/red] Automatically clear the terminal after each test",
    ),
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show current version",
    ),
):
    """
    PyTest-Watcher is a CLI tool that watches for changes in your code and runs pytest on the changed files.

    \b
    [underline magenta]Recommended:[/underline magenta] Use the configure command to create a config file that will be used for testing.
    [underline magenta]Note:[/underline magenta] If you use the configure command, you can use the -c flag to use the config file for testing.

    \b
    Any global option, [bold red]must[/bold red] be used before the command.

    [blue]Example:
        pytest-watcher -c test tests/[/blue]
    """
    State.verbose = verbose
    State.useConfig = useConfig
    State.autoClear = autoClear
    return


@app.command()
def test(
    path: str = typer.Argument(..., help="Path to a test folder"),
    passthrough: Optional[List[str]] = typer.Option(
        None, "-p", "--pass", help="Passes arguments to pytest."
    ),
):
    """
    Run pytest on a given path.

    [blue]
    Example:
        pytest-watcher test tests/
    [/blue]

    To pass arguments to pytests, use the -p flag.
    [italic] Note: You must use the flag for each argument you want to pass. [/italic]
    [blue]
    Example:
        pytest-watcher test tests/ -p "-k test_something" -p "-m slow"
    [/blue]
    """
    Config(
        path=path,
        passthrough=passthrough,
        verbose=State.verbose,
        useConfig=State.useConfig,
        autoClear=State.autoClear,
    )

    watch_files()


def cli():
    app()
