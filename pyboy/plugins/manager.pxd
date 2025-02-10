#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#

cimport cython
from pyboy.plugins.base_plugin cimport PyBoyGameWrapper

cdef class PluginManager:
    cdef object pyboy
    cdef object plugin_loader
    cdef readonly list plugins_enabled
    cdef readonly list window_plugins_enabled
    cdef readonly list debug_plugins_enabled
    cdef public PyBoyGameWrapper game_wrapper

    cdef list handle_events(self, list) noexcept
    cpdef void post_tick(self) noexcept
    cdef void _post_tick_windows(self) noexcept
    cdef void frame_limiter(self, int) noexcept
    cdef str window_title(self) noexcept
    cdef void stop(self) noexcept
    cdef void _set_title(self) noexcept
    cdef void handle_breakpoint(self) noexcept
