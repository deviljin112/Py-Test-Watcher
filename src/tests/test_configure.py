import yaml
from typer.testing import CliRunner

from src.configure import app, Config, get_optional_fields, load_config


runner = CliRunner()


def test_should_get_optional_fields():
    fields = get_optional_fields(Config)

    assert "verbose" in fields.keys()
    assert "autoClear" in fields.keys()
    assert "passthrough" in fields.keys()
    assert "ignore" in fields.keys()
    assert "extensions" in fields.keys()
    assert "onPass" in fields.keys()
    assert "onFail" in fields.keys()


def test_should_load_config(tmpdir):
    config_path = tmpdir.join("config.yaml")

    with open(config_path.strpath, "w") as f:
        yaml.dump(
            {
                "onPass": "loadPass",
                "onFail": "loadFail",
                "verbose": True,
                "autoClear": True,
            },
            f,
        )

    config = load_config(config_path.strpath)

    assert config["onPass"] == "loadPass"
    assert config["onFail"] == "loadFail"
    assert config["verbose"] is True
    assert config["autoClear"] is True


def test_should_create_config_file(tmpdir):
    config_path = tmpdir.join("config.yaml")

    result = runner.invoke(
        app,
        ["create", "-c", config_path.strpath],
        input="createPass\ncreateFail\n\n\n\n\n\ny\n",
    )

    assert result.exit_code == 0

    with open(config_path.strpath, "r") as f:
        config = yaml.safe_load(f)

        assert config["onPass"] == "createPass"
        assert config["onFail"] == "createFail"


def test_should_create_config_with_lists(tmpdir):
    config_path = tmpdir.join("config.yaml")

    result = runner.invoke(
        app,
        ["create", "-c", config_path.strpath],
        input='\n\n\n\n"a1" "a2"\n"b1" "b2\n"c1" "c2"\ny\n',
    )

    assert result.exit_code == 0

    with open(config_path.strpath, "r") as f:
        config = yaml.safe_load(f)

        assert config["ignore"] == ["a1", "a2"]
        assert config["extensions"] == ["b1", "b2"]
        assert config["passthrough"] == ["c1", "c2"]


def test_should_edit_config(tmpdir):
    config_path = tmpdir.join("config.yaml")

    with open(config_path.strpath, "w") as f:
        yaml.dump(
            {
                "onPass": "onPass",
                "onFail": "onFail",
            },
            f,
        )

    result = runner.invoke(
        app,
        ["edit", "-c", config_path.strpath],
        input="editPass\neditFail\n\n\n\n\n\ny\n",
    )

    assert result.exit_code == 0

    with open(config_path.strpath, "r") as f:
        config = yaml.safe_load(f)

        assert config["onPass"] == "editPass"
        assert config["onFail"] == "editFail"


def test_should_show_config_table(tmpdir):
    config_path = tmpdir.join("config.yaml")

    with open(config_path.strpath, "w") as f:
        yaml.dump(
            {
                "onPass": "onPass",
                "onFail": "onFail",
                "verbose": True,
                "autoClear": True,
                "ignore": [],
                "extensions": [],
                "passthrough": [],
            },
            f,
        )

    result = runner.invoke(app, ["show", "-c", config_path.strpath])

    assert result.exit_code == 0
    assert "onPass" in result.stdout
    assert "onFail" in result.stdout
    assert "verbose" in result.stdout
    assert "autoClear" in result.stdout
    assert "ignore" in result.stdout
    assert "extensions" in result.stdout
    assert "passthrough" in result.stdout
