#  Copyright (C) 2013  Equinor ASA, Norway.
#
#  The file 'history.py' is part of ERT - Ensemble based Reservoir Tool.
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

from cwrap import BaseCClass
from res import ResPrototype
from res.sched import HistorySourceEnum
from ecl.summary import EclSum

class History(BaseCClass):
    TYPE_NAME = "history"

    _alloc_from_refcase    = ResPrototype("void* history_alloc_from_refcase(ecl_sum, bool)", bind = False)
    _get_source_string     = ResPrototype("char* history_get_source_string(history_source_enum)", bind = False)
    _free                  = ResPrototype("void  history_free( history )")

    def __init__(self, refcase = None, use_history = False, sched_file = None):
        """
        @type refcase: EclSum
        @type use_history: bool
        @rtype: HistoryType
        """
        if sched_file is not None:
            raise ValueError("Cannot create history from sched_file.")

        if refcase is None:
            ValueError('Refcase cannot be None when creating a History.')

        self._init_from = 'refcase'
        self._init_val  = str(refcase)
        c_ptr = self._alloc_from_refcase(refcase, use_history)
        if c_ptr:
            super(History, self).__init__(c_ptr)
        else:
            raise ValueError('Invalid input.  Failed to create History.')

    @staticmethod
    def get_source_string(history_source_type):
        """
        @type history_source_type: HistorySourceEnum
        @rtype: str
        """
        return self._get_source_string(history_source_type)

    def free(self):
        self._free( self )

    def __repr__(self):
        fr = self._init_from
        va = self._init_val
        ad = self._ad_str()
        return 'History(init_from = %s: %s) %s' % (fr,va,ad)
