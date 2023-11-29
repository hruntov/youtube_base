from website import __version__


def test_version():
    assert __version__ == "0.1.0"
    print(f"Version {__version__} is correct.")
