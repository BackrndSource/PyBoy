#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#
cimport cython
from pyboy.plugins.base_plugin cimport PyBoyPlugin, PyBoyGameWrapper


cdef class PluginManager:
    cdef object pyboy

    cdef list enabled_plugins
    cdef list enabled_window_plugins
    cdef list enabled_debug_plugins
    cdef PyBoyGameWrapper game_wrapper

    cdef dict plugin_mapping
    cpdef list list_plugins(self)
    cpdef PyBoyPlugin get_plugin(self, str)

    cdef list handle_events(self, list)
    cdef void post_tick(self) noexcept
    cdef void _post_tick_windows(self) noexcept
    cdef void _set_title(self) noexcept
    cdef void frame_limiter(self, int) noexcept
    cdef str window_title(self) 
    cdef void stop(self) noexcept
    cdef void handle_breakpoint(self) noexcept