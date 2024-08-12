#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.backlightconfiguration
:brief: Backlight configuration per product
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/02/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.keybaordlayout import LAYOUT_MAX_COUNT
from pyraspi.services.kosmos.config.i2cbacklightconfiguration.commonbacklightconfiguration import \
    NonMechanicalBacklightConfiguration
from pyraspi.services.kosmos.config.i2cbacklightconfiguration.inga import IngaBacklightConfiguration
from pyraspi.services.kosmos.config.i2cbacklightconfiguration.inga import IngaJpnBacklightConfiguration
from pyraspi.services.kosmos.config.i2cbacklightconfiguration.inga import IngaUkBacklightConfiguration
from pyraspi.services.kosmos.config.i2cbacklightconfiguration.ingacs import IngaCsMacBacklightConfiguration
from pyraspi.services.kosmos.config.i2cbacklightconfiguration.ingacs import IngaCsMacJpnBacklightConfiguration
from pyraspi.services.kosmos.config.i2cbacklightconfiguration.ingacs import IngaCsMacUkBacklightConfiguration


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
GET_BACKLIGHT_CONFIGURATION_BY_ID = {
    # Pollux firmware on Inga hardware
    'RBO03': [IngaBacklightConfiguration, IngaBacklightConfiguration, IngaUkBacklightConfiguration,
              IngaBacklightConfiguration, IngaJpnBacklightConfiguration, ],
    'RBK71': [IngaBacklightConfiguration, IngaBacklightConfiguration, IngaUkBacklightConfiguration,
              IngaBacklightConfiguration, IngaJpnBacklightConfiguration, ],
    'RBK75': [IngaCsMacBacklightConfiguration, IngaCsMacBacklightConfiguration, IngaCsMacUkBacklightConfiguration,
              IngaCsMacBacklightConfiguration, IngaCsMacJpnBacklightConfiguration, ],
    'RBK81': [NonMechanicalBacklightConfiguration for _ in range(LAYOUT_MAX_COUNT)],
}

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
