import yaml
import typer

from rich import print
from rich.table import Table
from rich.console import Console
from typing import List, Optional

app = typer.Typer()
console = Console()

config_template = {
    "verbose": {
        "type": bool,
        "default": False,
        "description": "Enable verbose mode",
    },
    "autoClear": {
        "type": bool,
        "default": False,
        "description": "Automatically clear the terminal after each test",
    },
    "passthrough": {
        "type": list,
        "default": [],
        "description": "Enter passthrough args (separated by spaces)",
    },
    "onPass": {
        "type": str,
        "default": "",
        "description": "Enter a shell command to run when tests pass",
    },
    "onFail": {
        "type": str,
        "default": "",
        "description": "Enter a shell command to run when tests fail",
    },
}


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=Singleton):
    def __init__(
        self,
        path: str,
        verbose: Optional[bool] = None,
        autoClear: Optional[bool] = None,
        passthrough: Optional[List[str]] = None,
        useConfig: Optional[bool] = False,
    ):
        self.path = path
        self.onPass = None
        self.onFail = None

        if useConfig:
            config = load_config()
            self.verbose = verbose or config["verbose"]
            self.autoClear = autoClear or config["autoClear"]
            self.passthrough = passthrough or config["passthrough"]
            self.onPass = config["onPass"] or None
            self.onFail = config["onFail"] or None
        else:
            self.verbose = verbose
            self.autoClear = autoClear
            self.passthrough = passthrough

    def to_dict(self):
        return {
            "path": self.path,
            "verbose": self.verbose,
            "autoClear": self.autoClear,
            "passthrough": self.passthrough,
        }


def display_table(data: dict):
    table = Table()
    table.add_column("Key")
    table.add_column("Value")
    for key, value in data.items():
        table.add_row(key, str(value))
    console.print(table)


def load_config():
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
            return config
    except FileNotFoundError:
        print("Config file not found")
        raise typer.Exit()


@app.command()
def create():
    """
    Create a config file for PyTest-Watcher.

    \b
    Use the [cyan]create[/cyan] command to create a config file that will be used for testing.

    [underline magenta]Note:[/underline magenta] This command will overwrite any existing config file.

    [underline magenta]Note:[/underline magenta] If you use the configure command, you can use the -c flag to use the config file for testing.
    """

    print("Enter values for the config.")

    config = {}
    for key, value in config_template.items():
        config[key] = typer.prompt(
            value["description"], default=value["default"], type=value["type"]
        )

    display_table(config)
    confirmation = typer.confirm("Are all the values correct?", abort=True)

    if confirmation:
        with open("config.yaml", "w") as f:
            yaml.dump(config, f)

        print("Config created successfully")
    else:
        print("Config creation aborted")


@app.command()
def edit():
    """
    Edit the config file for PyTest-Watcher.

    \b
    Use the [cyan]edit[/cyan] command to edit an existing config file that will be used for testing.

    [underline magenta]Note:[/underline magenta] This command will overwrite any existing config file.

    [underline magenta]Note:[/underline magenta] If you use the configure command, you can use the -c flag to use the config file for testing.
    """
    config = load_config()

    print("Enter new values for the config. Leave blank to keep the current value.")
    for key, value in config_template.items():
        new_value = typer.prompt(
            value["description"], default=config[key], type=value["type"]
        )

        if value["type"] == "list":
            new_value = new_value.split(" ")

        if new_value:
            config[key] = new_value

    display_table(config)
    confirmation = typer.confirm("Are all the values correct?", abort=True)

    if confirmation:
        with open("config.yaml", "w") as f:
            yaml.dump(config, f)

        print("Config edited successfully")
    else:
        print("Config edit aborted")


@app.command()
def show():
    """
    Show the config file for PyTest-Watcher.

    \b
    Use the [cyan]show[/cyan] command to show the current config file that will be used for testing.
    """
    config = load_config()
    display_table(config)
