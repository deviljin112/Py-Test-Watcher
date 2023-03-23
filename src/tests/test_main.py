from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Py-Watcher Version: 0.1.0" in result.stdout
