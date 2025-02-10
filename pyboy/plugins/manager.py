#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#
from pyboy.plugins.base_plugin import PyBoyPlugin, PyBoyDebugPlugin, PyBoyWindowPlugin, PyBoyGameWrapper


class PluginManager:
    def __init__(self, pyboy, mb, plugin_loader, pyboy_argv):
        self.pyboy = pyboy
        self.plugin_loader = plugin_loader

        self.plugins_enabled = []
        self.window_plugins_enabled = []
        self.debug_plugins_enabled = []
        self.game_wrapper: PyBoyGameWrapper = None

        for plugin_cls in self.plugin_loader.plugins:
            plugin = plugin_cls(pyboy, mb, pyboy_argv)
            if plugin.enabled():
                if issubclass(plugin_cls, PyBoyWindowPlugin):
                    self.window_plugins_enabled.append(plugin)
                    continue
                if issubclass(plugin_cls, PyBoyDebugPlugin):
                    self.debug_plugins_enabled.append(plugin)
                    continue
                if issubclass(plugin_cls, PyBoyGameWrapper):
                    self.game_wrapper = plugin
                    continue
                self.plugins_enabled.append(plugin)

        # TODO: Assign a default window plugin if none is enabled or let the plugins handle this (as it is now)?
        # if len(self.window_plugins_enabled) == 0:
        #     self.window_plugins_enabled.append(WindowSDL2(pyboy, mb, pyboy_argv))

        if self.game_wrapper is None:
            self.game_wrapper = PyBoyGameWrapper(pyboy, mb, pyboy_argv)

    def handle_events(self, events):
        for plugin in (
            self.window_plugins_enabled + self.plugins_enabled + self.debug_plugins_enabled + [self.game_wrapper]
        ):
            events = plugin.handle_events(events)
        return events

    def post_tick(self):
        for plugin in self.plugins_enabled + self.debug_plugins_enabled + [self.game_wrapper]:
            plugin.post_tick()
        self._post_tick_windows()

    def _set_title(self):
        for plugin in self.window_plugins_enabled:
            plugin.set_title(self.pyboy.window_title)

    def _post_tick_windows(self):
        for plugin in self.window_plugins_enabled:
            plugin.post_tick()

    def frame_limiter(self, speed):
        if speed <= 0:
            return
        for plugin in self.window_plugins_enabled:
            done = plugin.frame_limiter(speed)
            if done:
                return

    def window_title(self):
        title = ""
        for plugin in (
            self.window_plugins_enabled + self.plugins_enabled + self.debug_plugins_enabled + [self.game_wrapper]
        ):
            title += plugin.window_title()
        return title

    def stop(self):
        for plugin in (
            self.window_plugins_enabled + self.plugins_enabled + self.debug_plugins_enabled + [self.game_wrapper]
        ):
            plugin.stop()

    def handle_breakpoint(self):
        for plugin in self.debug_plugins_enabled:
            plugin.handle_breakpoint()
