from src.watcher import extract_file_name, callback_wrapper


class MockConfig:
    def __init__(self, autoClear: bool):
        self.autoClear = autoClear


def test_should_extract_file_name_from_path():
    assert extract_file_name("test/test.py") == "test.py"


def test_should_extract_file_name_from_path_with_multiple_slashes():
    assert extract_file_name("test/test/test.py") == "test.py"


def test_should_print_changed_file(capfd):
    change_callback = callback_wrapper(MockConfig(False))

    changes = [("modified", "test/test_file.py")]
    change_callback(changes)

    out, err = capfd.readouterr()
    assert out == "File change detected: test_file.py\n"


def test_should_print_changed_files(capfd):
    change_callback = callback_wrapper(MockConfig(False))

    changes = [("modified", "test/test_file.py"), ("modified", "test/test_file2.py")]
    change_callback(changes)

    out, err = capfd.readouterr()
    assert (
        out
        == "File change detected: test_file.py\nFile change detected: test_file2.py\n"
    )
