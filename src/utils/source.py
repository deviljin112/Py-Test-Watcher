import typer

app = typer.Typer()


@app.command()
def code():
    """
    Open the source code in your browser
    """
    # TODO: Implement
    print("Opening source code in browser...")


@app.command()
def update():
    """
    Check for updates
    """
    # TODO: Implement
    print("Checking for updates...")
