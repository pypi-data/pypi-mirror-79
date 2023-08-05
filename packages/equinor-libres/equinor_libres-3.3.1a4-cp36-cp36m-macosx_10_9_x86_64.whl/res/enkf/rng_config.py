#  Copyright (C) 2017  Equinor ASA, Norway.
#
#  The file 'rng_config.py' is part of ERT - Ensemble based Reservoir Tool.
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

from ecl.util.enums import RngAlgTypeEnum

from res import ResPrototype
from res.enkf import ConfigKeys

class RNGConfig(BaseCClass):

    TYPE_NAME = "rng_config"
    _alloc        = ResPrototype("void* rng_config_alloc(config_content)", bind=False)
    _alloc_full   = ResPrototype("void* rng_config_alloc_full(char*, char*, char*)", bind=False)
    _free         = ResPrototype("void rng_config_free(rng_config)")
    _rng_alg_type = ResPrototype("rng_alg_type_enum rng_config_get_type(rng_config)")
    _load_file    = ResPrototype("char* rng_config_get_seed_load_file(rng_config)")
    _store_file   = ResPrototype("char* rng_config_get_seed_store_file(rng_config)")
    _random_seed  = ResPrototype("char* rng_config_get_random_seed(rng_config)")

    def __init__(self, config_content=None, config_dict=None):
        if config_content and config_dict:
            raise ValueError('RNGConfig can not be instantiated with both config types')

        if not (config_content or config_dict):
            raise ValueError('RNGConfig can not be instantiated without any config objects')

        if config_content:
            c_ptr = self._alloc(config_content)

        elif config_dict:

            random_seed = config_dict.get(ConfigKeys.RANDOM_SEED)
            store_seed = config_dict.get(ConfigKeys.STORE_SEED) if random_seed is None else None
            load_seed = config_dict.get(ConfigKeys.LOAD_SEED) if random_seed is None else None

            if store_seed or load_seed:
                print("STORE_SEED/LOAD_SEED has been deprecated. Please use RANDOM_SEED instead!")

            c_ptr = self._alloc_full(random_seed, store_seed, load_seed)

        if c_ptr is None:
            raise ValueError('Failed to construct RNGConfig instance')

        super(RNGConfig, self).__init__(c_ptr)

    @property
    def alg_type(self):
        return self._rng_alg_type()

    @property
    def load_filename(self):
        return self._load_file()

    @property
    def store_filename(self):
        return self._store_file()

    @property
    def random_seed(self):
        return self._random_seed()

    def free(self):
        self._free()

    def __eq__(self, other):

        if self.random_seed != other.random_seed:
            return False

        if self.load_filename != other.load_filename:
            return False

        if self.store_filename != other.store_filename:
            return False

        if self.alg_type != other.alg_type:
            return False

        return True
