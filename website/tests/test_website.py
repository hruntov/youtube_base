from website import __version__


class TestClass:
    def test_version(self):
        assert __version__ == "0.2.0"
        print(f"Version {__version__} is correct.")
