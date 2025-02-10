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

from pyboy.plugin_manager import keyword_arguments, window_names


def test_plugin_manager_basics(default_rom):
    pyboy = PyBoy(default_rom, window="null")
    pyboy.set_emulation_speed(0)
    pyboy.tick(60, False)
    pyboy.stop()


@pytest.mark.parametrize(
    "plugin_name, debug",
    [
        ("Debug", True),
        ("ScreenRecorder", False),
        ("ScreenshotRecorder", False),
    ],
)
def test_plugin_manager_get_plugin(default_rom, plugin_name, debug):
    pyboy = PyBoy(default_rom, window="null", debug=debug)
    assert pyboy._plugin_manager.get_plugin(plugin_name) is not None


def test_plugin_manager_get_plugin_key_error(default_rom):
    pyboy = PyBoy(default_rom, window="null")
    assert pyboy._plugin_manager.get_plugin("non_existing_plugin_r4nd0m") is None


@pytest.mark.parametrize(
    "keyword_arg",
    [
        "autopause",
        "breakpoints",
        "d",
        "debug",
        "no_input",
        "record_input",
        "rewind",
    ],
)
def test_plugin_manager_keyword_arguments_builtin_plugins(keyword_arg):
    assert keyword_arg in keyword_arguments()


def test_plugin_manager_non_existing_argv(default_rom):
    try:
        PyBoy(default_rom, window="null", non_existing_argv_r4nd0m=True)
    except Exception as e:
        assert type(e) == KeyError
    else:
        raise AssertionError("Expected a KeyError")


def test_plugin_manager_non_existing_window_name(default_rom):
    try:
        PyBoy(default_rom, window="non_existing_window_name_r4nd0m")
    except Exception as e:
        assert type(e) == KeyError
    else:
        raise AssertionError("Expected a KeyError")


def test_plugin_manager_generic_game_wrapper(default_rom):
    pyboy = PyBoy(default_rom, window="null")
    generic_wrapper = pyboy._plugin_manager.game_wrapper
    assert type(generic_wrapper) == PyBoyGameWrapper


@pytest.mark.parametrize(
    "window_name",
    ["SDL2", "OpenGL", "null"],
)
def test_plugin_manager_builtin_window_plugins_names(window_name):
    assert window_name in window_names()


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
def test_plugin_manager_builtin_window_plugins(default_rom, window_arg, window_cls, debug):
    if os.environ.get("TEST_NO_UI") and window_arg in ["SDL2", "OpenGL"]:
        pytest.skip("Skipping test, as there is no UI")

    pyboy = PyBoy(default_rom, window=window_arg, debug=debug)
    enabled_window_plugins = pyboy._plugin_manager.enabled_window_plugins

    if debug:
        assert len(enabled_window_plugins) == 2
        assert type(enabled_window_plugins[0]) != type(enabled_window_plugins[1])
        for plugin in enabled_window_plugins:
            assert type(plugin) == window_cls or type(plugin) == Debug
    else:
        assert len(enabled_window_plugins) == 1
        assert type(enabled_window_plugins[0]) == window_cls
