#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#
from pyboy.plugins.base_plugin import PyBoyPlugin
from importlib_metadata import entry_points

# imports
from pyboy.plugins.window_sdl2 import WindowSDL2 # isort:skip
from pyboy.plugins.window_open_gl import WindowOpenGL # isort:skip
from pyboy.plugins.window_null import WindowNull # isort:skip
from pyboy.plugins.debug import Debug # isort:skip
from pyboy.plugins.disable_input import DisableInput # isort:skip
from pyboy.plugins.auto_pause import AutoPause # isort:skip
from pyboy.plugins.record_replay import RecordReplay # isort:skip
from pyboy.plugins.rewind import Rewind # isort:skip
from pyboy.plugins.screen_recorder import ScreenRecorder # isort:skip
from pyboy.plugins.screenshot_recorder import ScreenshotRecorder # isort:skip
from pyboy.plugins.debug_prompt import DebugPrompt # isort:skip
from pyboy.plugins.game_wrapper_super_mario_land import GameWrapperSuperMarioLand # isort:skip
from pyboy.plugins.game_wrapper_tetris import GameWrapperTetris # isort:skip
from pyboy.plugins.game_wrapper_kirby_dream_land import GameWrapperKirbyDreamLand # isort:skip
from pyboy.plugins.game_wrapper_pokemon_gen1 import GameWrapperPokemonGen1 # isort:skip
from pyboy.plugins.game_wrapper_pokemon_pinball import GameWrapperPokemonPinball # isort:skip
# imports end


class PluginLoader:
    entry_point_group = "pyboy_plugins"

    def __init__(self):
        self._load_plugins()

    def _load_plugins(self):
        self.plugins = []
        # plugins_available
        self.plugins.append(WindowSDL2)
        self.plugins.append(WindowOpenGL)
        self.plugins.append(WindowNull)
        self.plugins.append(Debug)
        self.plugins.append(DisableInput)
        self.plugins.append(AutoPause)
        self.plugins.append(RecordReplay)
        self.plugins.append(Rewind)
        self.plugins.append(ScreenRecorder)
        self.plugins.append(ScreenshotRecorder)
        self.plugins.append(DebugPrompt)
        self.plugins.append(GameWrapperSuperMarioLand)
        self.plugins.append(GameWrapperTetris)
        self.plugins.append(GameWrapperKirbyDreamLand)
        self.plugins.append(GameWrapperPokemonGen1)
        self.plugins.append(GameWrapperPokemonPinball)
        # plugins_available end
        for plugin_entry_point in entry_points(group=self.entry_point_group):
            plugin_cls = plugin_entry_point.load()
            if issubclass(plugin_cls, PyBoyPlugin):
                self.plugins.append(plugin_cls)

    def parser_arguments(self):
        return [plugin.argv for plugin in self.plugins]

    def keyword_arguments(self):
        keywords = []
        for x in self.parser_arguments():
            if not x:
                continue
            keywords.extend(z.strip("-").replace("-", "_") for y in x for z in y[:-1])
        return keywords
