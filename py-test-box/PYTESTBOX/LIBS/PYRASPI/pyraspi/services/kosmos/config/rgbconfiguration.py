#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.rgbconfiguration
:brief: RGB effect configuration per product
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/02/14
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyraspi.services.kosmos.config.rgbconfigurations.topazconfiguration.topaz import TopazRgbConfiguration
from pyraspi.services.kosmos.config.rgbconfigurations.cinderellawirelessconfiguration.cinderellawireless import \
    CinderellaWirelessRgbConfiguration

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
GET_RGB_CONFIGURATION_BY_ID = {
    'MPK17': TopazRgbConfiguration,
    'MPK25': CinderellaWirelessRgbConfiguration,
}

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
