#  Copyright (C) 2011  Equinor ASA, Norway.
#
#  The file '__init__.py' is part of ERT - Ensemble based Reservoir Tool.
#
#  ERT is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
#  for more details.
"""
Ert - Ensemble Reservoir Tool - a package for reservoir modeling.
"""
import os.path
import sys
import platform
import ecl

import warnings
warnings.filterwarnings(
    action='always',
    category=DeprecationWarning,
    module=r'res|ert'
)

from cwrap import Prototype

from ._version import version as __version__


def _load_lib():
    import ctypes

    # Find and dlopen libres
    lib_path = os.path.join(os.path.dirname(__file__), ".libs")
    if platform.system() == "Linux":
        lib_path = os.path.join(lib_path, "libres.so")
    elif platform.system() == "Darwin":
        lib_path = os.path.join(lib_path, "libres.dylib")
    else:
        raise NotImplementedError("Invalid platform")

    lib = ctypes.CDLL(lib_path, ctypes.RTLD_GLOBAL)

    # Configure site_config to be a ctypes.CFUNCTION with type:
    # void set_site_config(char *);
    site_config = lib.set_site_config
    site_config.restype = None
    site_config.argtypes = (ctypes.c_char_p,)

    # Set site-config to point to [CURRENT DIR]/.data/site-config
    path = os.path.join(os.path.dirname(__file__), ".data", "site-config")
    if sys.version_info.major >= 3:
        path = bytes(path, "utf8")
    site_config(path)

    return lib


class ResPrototype(Prototype):
    lib = _load_lib()

    def __init__(self, prototype, bind=True):
        super(ResPrototype, self).__init__(ResPrototype.lib, prototype, bind=bind)


RES_LIB = ResPrototype.lib

from res.util import ResVersion
from ecl.util.util import updateAbortSignals

updateAbortSignals( )

def root():
    """
    Will print the filesystem root of the current ert package.
    """
    return os.path.abspath( os.path.join( os.path.dirname( __file__ ) , "../"))
