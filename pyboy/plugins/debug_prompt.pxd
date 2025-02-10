#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#

from pyboy.logging.logging cimport Logger
from pyboy.plugins.base_plugin cimport PyBoyDebugPlugin


cdef Logger logger

cdef class DebugPrompt(PyBoyDebugPlugin):
    cdef dict rom_symbols