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


def test_plugin_manager_generic_game_wrapper(default_rom):
    pyboy = PyBoy(default_rom, window="null")
    generic_wrapper = pyboy._plugin_manager.game_wrapper
    assert type(generic_wrapper) == PyBoyGameWrapper


def test_plugin_manager_window_sdl2_plugin(default_rom):
    pyboy = PyBoy(default_rom, window="SDL2", debug=False)
    window_plugin = pyboy._plugin_manager.window_plugins_enabled[0]
    assert type(window_plugin) == WindowSDL2


def test_plugin_manager_window_sdl2_debug_plugin(default_rom):
    pyboy = PyBoy(default_rom, window="SDL2", debug=True)
    window_plugins = pyboy._plugin_manager.window_plugins_enabled
    assert len(window_plugins) == 2
    assert type(window_plugins[0]) != type(window_plugins[1])
    for plugin in window_plugins:
        assert type(plugin) == WindowSDL2 or type(plugin) == Debug


def test_plugin_manager_window_opengl_plugin(default_rom):
    pyboy = PyBoy(default_rom, window="OpenGL", debug=False)
    window_plugin = pyboy._plugin_manager.window_plugins_enabled[0]
    assert type(window_plugin) == WindowOpenGL


def test_plugin_manager_window_null_plugin(default_rom):
    pyboy = PyBoy(default_rom, window="null", debug=False)
    window_plugin = pyboy._plugin_manager.window_plugins_enabled[0]
    assert type(window_plugin) == WindowNull


def test_plugin_manager_window_null_debug_plugin(default_rom):
    pyboy = PyBoy(default_rom, window="null", debug=True)
    window_plugins = pyboy._plugin_manager.window_plugins_enabled
    assert len(window_plugins) == 2
    assert type(window_plugins[0]) != type(window_plugins[1])
    for plugin in window_plugins:
        assert type(plugin) == WindowNull or type(plugin) == Debug
