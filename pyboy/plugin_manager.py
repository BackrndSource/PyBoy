#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#
import inspect
import importlib
import importlib_metadata
from pkgutil import iter_modules

from pyboy import plugins
from pyboy.logging import get_logger
from pyboy.plugins.base_plugin import PyBoyDebugPlugin, PyBoyGameWrapper, PyBoyPlugin, PyBoyWindowPlugin


logger = get_logger(__name__)

registered_plugins = []
registered_debug_plugins = []
registered_window_plugins = []
registered_gamewrappers = []

builtin_modules = [importlib.import_module("pyboy.plugins." + m.name) for m in iter_modules(plugins.__path__)]
external_modules = [entry_point for entry_point in importlib_metadata.entry_points(group="pyboy")]

for module in builtin_modules + [m.load() for m in external_modules]:

    if hasattr(module, "_export_plugins"):
        plugin_names = getattr(module, "_export_plugins")
    else:
        plugin_names = [attr for attr in dir(module) if not attr.startswith("_")]

    for attr_name in plugin_names:
        module_cls = getattr(module, attr_name)
        if not inspect.isclass(module_cls):
            continue
        if not issubclass(module_cls, PyBoyPlugin):
            continue
        if module_cls in [PyBoyPlugin, PyBoyWindowPlugin, PyBoyGameWrapper, PyBoyDebugPlugin]:
            continue
        if issubclass(module_cls, PyBoyDebugPlugin):
            registered_debug_plugins.append(module_cls)
            continue
        if issubclass(module_cls, PyBoyWindowPlugin):
            registered_window_plugins.append(module_cls)
            continue
        if issubclass(module_cls, PyBoyGameWrapper):
            registered_gamewrappers.append(module_cls)
            continue
        registered_plugins.append(module_cls)


def parser_arguments():
    for plugin_cls in (
        registered_plugins + registered_debug_plugins + registered_window_plugins + registered_gamewrappers
    ):
        yield plugin_cls.argv


def keyword_arguments():
    keywords = []
    for x in parser_arguments():
        if not x:
            continue
        keywords.extend(z.strip("-").replace("-", "_") for y in x for z in y[:-1])
    return keywords


def window_names():
    for plugin_cls in registered_window_plugins:
        if plugin_cls.name:
            yield plugin_cls.name


def external_module_names():
    return ", ".join([f"{m.dist.name}-{m.dist.version}" for m in external_modules])


class PluginManager:
    def __init__(self, pyboy, mb, pyboy_argv):
        self.pyboy = pyboy

        if external_modules:
            logger.info(f"External modules loaded: {external_module_names()}")
        else:
            logger.info("No external modules found")

        self.enabled_plugins = self._instantiate_plugins(registered_plugins, pyboy, mb, pyboy_argv)
        self.enabled_window_plugins = self._instantiate_plugins(registered_window_plugins, pyboy, mb, pyboy_argv)
        self.enabled_debug_plugins = self._instantiate_plugins(registered_debug_plugins, pyboy, mb, pyboy_argv)
        self.game_wrapper = self._instantiate_gamewrapper(registered_gamewrappers, pyboy, mb, pyboy_argv)

        self.plugin_mapping = {}
        for plugin in (
            self.enabled_window_plugins + self.enabled_plugins + self.enabled_debug_plugins + [self.game_wrapper]
        ):
            self.plugin_mapping[plugin.__class__.__name__] = plugin

    @staticmethod
    def _instantiate_plugins(plugin_cls_list, pyboy, mb, pyboy_argv):
        return [
            plugin_cls(pyboy, mb, pyboy_argv) for plugin_cls in plugin_cls_list if plugin_cls.enabled(pyboy, pyboy_argv)
        ]

    @staticmethod
    def _instantiate_gamewrapper(gamewrapper_cls_list, pyboy, mb, pyboy_argv):
        enabled_gamewrappers_cls_list = [
            plugin_cls for plugin_cls in gamewrapper_cls_list if plugin_cls.enabled(pyboy, pyboy_argv)
        ]

        if len(enabled_gamewrappers_cls_list) == 0:
            return PyBoyGameWrapper(pyboy, mb, pyboy_argv)

        if len(enabled_gamewrappers_cls_list) > 1:
            logger.warning(
                "More than one game wrapper can be enabled. Selected: " + enabled_gamewrappers_cls_list[0].__name__
            )

        return enabled_gamewrappers_cls_list[0](pyboy, mb, pyboy_argv)

    def list_plugins(self):
        return list(self.plugin_mapping.keys())

    def get_plugin(self, name):
        try:
            return self.plugin_mapping[name]
        except KeyError:
            logger.error("Trying to get unavailable plugin: " + name)
        return None

    def handle_events(self, events):
        for plugin in (
            self.enabled_window_plugins + self.enabled_plugins + self.enabled_debug_plugins + [self.game_wrapper]
        ):
            events = plugin.handle_events(events)
        return events

    def post_tick(self):
        for plugin in self.enabled_plugins + self.enabled_debug_plugins + [self.game_wrapper]:
            plugin.post_tick()
        self._post_tick_windows()

    def _post_tick_windows(self):
        for plugin in self.enabled_window_plugins:
            plugin.post_tick()

    def _set_title(self):
        for plugin in self.enabled_window_plugins:
            plugin.set_title(self.pyboy.window_title)

    def frame_limiter(self, speed):
        if speed <= 0:
            return
        for plugin in self.enabled_window_plugins:
            if plugin.frame_limiter(speed):
                return

    def window_title(self):
        title = ""
        for plugin in (
            self.enabled_window_plugins + self.enabled_plugins + self.enabled_debug_plugins + [self.game_wrapper]
        ):
            title += plugin.window_title()
        return title

    def stop(self):
        for plugin in (
            self.enabled_window_plugins + self.enabled_plugins + self.enabled_debug_plugins + [self.game_wrapper]
        ):
            plugin.stop()

    def handle_breakpoint(self):
        for plugin in self.enabled_debug_plugins:
            plugin.handle_breakpoint()
