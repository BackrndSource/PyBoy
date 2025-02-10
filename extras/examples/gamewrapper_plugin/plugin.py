from pyboy.plugins.base_plugin import PyBoyGameWrapper


class ExamplePyBoyGameWrapperPlugin(PyBoyGameWrapper):
    cartridge_title = "EXAMPLE GAME WRAPPER" # If set to None plugin will be treated as a generic game wrapper
