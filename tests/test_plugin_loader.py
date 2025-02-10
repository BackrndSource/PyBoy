#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#

from pyboy import PyBoy
from pyboy.plugins.loader import PluginLoader


def test_plugin_loader_plugin_keyword_arguments(default_rom):
    assert "debug" in PluginLoader().keyword_arguments()


def test_plugin_loader_non_existing_argv(default_rom):
    try:
        PyBoy(default_rom, window="null", non_existing_argv_r4nd0m=True)
    except Exception as e:
        assert type(e) == KeyError
    else:
        raise AssertionError("Expected a KeyError")
