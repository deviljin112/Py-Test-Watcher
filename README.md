# Py Watcher

Py-Watcher is a tool that watches your files and runs your pytest tests automatically when it detects changes.

## Why?

I was tired of running `pytest` manually every time I made a change to my code. I wanted a tool that would watch my files and run my tests automatically when it detected changes.
\
While [pytest-watch](https://github.com/joeyespo/pytest-watch) is a great tool, it is simply not maintained anymore. It works for most things, but I wanted something simpler. I wanted to be able to create config files within my projects so I dont need to remember all the flags and commands I need to pass to pytest. That way I just need to run `pytest-w test` and it will do all the work for me.
\
Py-Watcher may not have all the features of pytest-watch (**yet**), but I plan to expand the functionality of this tool as needed.
\
You will find that Py-Watcher is quite opinionated. It is designed to work with my workflow. If you have any suggestions, please feel free to open an issue or a pull request. I am always open to suggestions.
\
I hope it helps someone else with managing a multi-project testing workflow.

## Disclaimer

This tool is still in development. It's not perfect by any means. It does what I need it to do, but it may not work for your use case. Please feel free to open an issue or a pull request if you find any bugs or have any suggestions. I only tested so many use cases, so I am sure there are many more that I have not thought of.

## Installation

```bash
pip install py-watcher
```

## Usage

Main entrypoint

```bash
pytest-w
```

You can run the `--help` command to see all available options.

```bash
pytest-w --help
```

or on any command.

```bash
pytest-w test --help
```

You can also view the `--version` of the tool.

```bash
pytest-w --version
```

### Global Flags

Py-Watcher supports the following global flags:

- `--verbose` or `-v`: Enable verbose mode.
- `--auto-clear` or `-a`: Automatically clear the terminal screen before each test run.
- `--config` or `-c`: Use a custom config file.

These flags need to be passed before the command.

```bash
pytest-w --verbose test
```

You can mix and max all the flags, and also write multiple flags in one (shorthanded)

```bash
pytest-w -va test
```

Which would apply the `--verbose` and `--auto-clear` flags.

### Test Watching

I strongly recommend using the `config.yaml` file to configure Py-Watcher. You can use the `configure` command to generate a `config.yaml` (see [#Config](#config)) file in the root of your project or if you prefer writing it yourself see [#Config (Advanced)](#config-advanced) section. As mentioned before this is quite opinionated. I personally do not like to pass many flags and commands when testing. Especially when those flags don't change, but it can be problematic to navigate a long line of shell command to edit something. Hence **use the config**.
\
Anyway... The `test` command is the real reason you are here. It will watch your files and run your tests automatically when it detects changes. You need to pass the path to the folder you want to watch. You can just pass `./` to watch all files in the current directory.

```bash
pytest-w test ./path/to/folder
```

You can also add parameters which will be passed to pytest with `--pass` or `-p`. You can only pass one parameter per flag. However, you can pass the flag multiple times. **Important**: You need to pass the parameter in quotes as a string (makes everything easier).

```bash
pytest-w test ./path/to/folder --pass "--maxfail=2" -p "-m test_marker"
```

Just to reiterate you can prepend global flags before the command.

```bash
pytest-w -ca test ./path/to/folder --pass "--maxfail=2" -p "-m test_marker"
```

In this case we will apply the `--config` flag to use our `config.yaml` file and the `--auto-clear` flag to Py-Watcher. But we also pass the extra parameters to pytest.

### Config

If you are not familiar with yaml files, you can use this option to generate a `config.yaml` file in the root of your project.

```bash
pytest-w configure create
```

You can also edit the `config.yaml` file.

```bash
pytest-w configure edit
```

And view the current configuration.

```bash
pytest-w configure view
```

### Config (Advanced)

Py-Watcher can be configured using a `config.yaml` file in the root of your project. Example of currently supported options:

```yaml
verbose: false
autoClear: true
onFail: shell-command
onPass: shell-command
passthrough:
  - "--maxfail=2"
  - "--tb=line"
```

This will likely change in the future, and be expanded further. I will do my best to keep the documentation up-to-date.

**Recommendation:** My daily driver is WSL2 within Windows 10. I have found myself running Py-Watcher in the background while doing other operations in another terminal tab and often forgetting to check the status of tests. I know that on linux you can use [notify-send](https://vaskovsky.net/notify-send/linux.html) to send notifications to your desktop. Well, on WSL you can use [wsl-notify-send](https://github.com/stuartleeks/wsl-notify-send) which essentially sends a notification to the Windows notification center. I have found this to be very useful and I highly recommend checking it out and using it in your own projects.
\
I have added the following to my `config.yaml` file:

```yaml
onPass: wsl-notify-send.exe --category "Py-Watcher" "All tests passed"
onFail: wsl-notify-send.exe --category "Py-Watcher" "A test has failed"
```

Now I can forget about Py-Watcher and it will notify me when it is done running tests. Not sure how this will work on other platforms, but I am sure there is a similar tool for MacOS.

## Manual Build

If you want to build the project manually, you can do so by cloning the repository. I recommend using a virtual environment.

```bash
python -m venv venv
source venv/bin/activate
```

Then install the dependencies.

```bash
pip install -r requirements.txt
```

And finally build the project.

```bash
pip install -e .
```

Then you can run the tool whenever you are in that virtual environment.

## Contributing

Contributions are welcome! Please feel free to open an issue or a pull request.

## Acknowledgements

- [pytest-watch](https://github.com/joeyespo/pytest-watch)
- [watchfiles](https://github.com/samuelcolvin/watchfiles)
- [typer](https://github.com/tiangolo/typer)

## Author

[Deviljin112](https://github.com/Deviljin112)

## License

MIT
