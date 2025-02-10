#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#

from pyboy import PyBoy
from pyboy.plugins.base_plugin import PyBoyGameWrapper
from pyboy.plugins.window_sdl2 import WindowSDL2
from pyboy.plugins.window_open_gl import WindowOpenGL
from pyboy.plugins.window_null import WindowNull
from pyboy.plugins.debug import Debug
import pytest
import os


def test_plugin_manager_basics(default_rom):
    pyboy = PyBoy(default_rom, window="null")
    pyboy.set_emulation_speed(0)
    pyboy.tick(60, False)
    pyboy.stop()


def test_plugin_manager_generic_game_wrapper(default_rom):
    pyboy = PyBoy(default_rom, window="null")
    generic_wrapper = pyboy._plugin_manager.game_wrapper
    assert type(generic_wrapper) == PyBoyGameWrapper


@pytest.mark.parametrize(
    "window_arg, window_cls, debug",
    [
        ("SDL2", WindowSDL2, True),
        ("SDL2", WindowSDL2, False),
        ("OpenGL", WindowOpenGL, True),
        ("OpenGL", WindowOpenGL, False),
        ("null", WindowNull, True),
        ("null", WindowNull, False),
    ],
)
def test_plugin_manager_window_plugin(default_rom, window_arg, window_cls, debug):
    if os.environ.get("TEST_NO_UI") and window_arg in ["SDL2", "OpenGL"]:
        pytest.skip("Skipping test, as there is no UI")

    pyboy = PyBoy(default_rom, window=window_arg, debug=debug)
    window_plugins_enabled = pyboy._plugin_manager.window_plugins_enabled

    if debug:
        assert len(window_plugins_enabled) == 2
        assert type(window_plugins_enabled[0]) != type(window_plugins_enabled[1])
        for plugin in window_plugins_enabled:
            assert type(plugin) == window_cls or type(plugin) == Debug
    else:
        assert len(window_plugins_enabled) == 1
        assert type(window_plugins_enabled[0]) == window_cls
