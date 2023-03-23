import os
import logging
import subprocess

from rich import print
from watchfiles import run_process, PythonFilter

from src.utils.configure import Config

logger = logging.getLogger("watchfiles.main")
logger.setLevel(logging.ERROR)


def extract_file_name(file_path: str):
    return file_path.split("/")[-1]


def change_cb(changes):
    config = Config()
    if config.autoClear:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    for change in list(changes):
        print(
            f"File change detected: [bold red]{extract_file_name(change[1])}[/bold red]"
        )


def watch_files():
    config = Config()
    target_path = os.getcwd() + "/" + config.path

    run_process(
        target_path,
        target=test_runner,
        target_type="function",
        watch_filter=PythonFilter(),
        callback=change_cb,
        args=[config],
    )


def test_runner(config: Config):
    args = ["pytest", config.path]

    if config.verbose:
        args.append("-v")

    if config.passthrough:
        args.extend(config.passthrough)

    try:
        process = subprocess.Popen(args)
        process.wait()
    except KeyboardInterrupt:
        process.kill()
    else:
        if process.poll() == 0:
            if config.onPass:
                subprocess.call(config.onPass, shell=True)
        else:
            if config.onFail:
                subprocess.call(config.onFail, shell=True)
