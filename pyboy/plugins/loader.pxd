#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#

cimport cython

cdef class PluginLoader:
    cdef readonly list plugins
    cdef readonly str entry_point_group

    cdef list parser_arguments(self) noexcept
    cdef list keyword_arguments(self) noexcept
