from src.utils.configure import Config


def test_config_should_be_singleton():
    config1 = Config("test")
    config2 = Config("test")
    assert config1 is config2
