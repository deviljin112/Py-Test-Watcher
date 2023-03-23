from src.utils.watcher import extract_file_name, change_cb


def test_should_extract_file_name_from_path():
    assert extract_file_name("test/test.py") == "test.py"


def test_should_extract_file_name_from_path_with_multiple_slashes():
    assert extract_file_name("test/test/test.py") == "test.py"


def test_should_print_changed_file(capfd):
    changes = [("modified", "test/test_file.py")]
    change_cb(changes)
    out, err = capfd.readouterr()
    assert out == "File change detected: test_file.py\n"


def test_should_print_changed_files(capfd):
    changes = [("modified", "test/test_file.py"), ("modified", "test/test_file2.py")]
    change_cb(changes)
    out, err = capfd.readouterr()
    assert (
        out
        == "File change detected: test_file.py\nFile change detected: test_file2.py\n"
    )
