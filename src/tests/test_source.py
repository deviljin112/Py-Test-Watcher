from typer.testing import CliRunner

from src.utils.source import app

runner = CliRunner()


def test_source_code():
    result = runner.invoke(app, ["code"])
    assert result.exit_code == 0
    assert "Opening source code in browser..." in result.stdout


def test_source_update():
    result = runner.invoke(app, ["update"])
    assert result.exit_code == 0
    assert "Checking for updates..." in result.stdout
