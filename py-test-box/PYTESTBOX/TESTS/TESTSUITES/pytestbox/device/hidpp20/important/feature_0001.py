#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.important.feature_0001
:brief: Device HID++ 2.0 FeatureSet Important Package
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.bootloadertest import DeviceBootloaderTestCase
from pytestbox.shared.hidpp20.important.feature_0001 import SharedIFeatureSetTestCase, IFeatureSetTestCaseMixin


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ApplicationIFeatureSetTestCase(SharedIFeatureSetTestCase, DeviceBaseTestCase):
    """
    Validate Device Important Feature Set TestCases in Application mode
    """
# end class ApplicationIFeatureSetTestCase


@features.class_decorator("BootloaderAvailable", inheritance=SharedIFeatureSetTestCase)
class BootloaderIFeatureSetTestCase(SharedIFeatureSetTestCase, DeviceBootloaderTestCase):
    """
    Validate Device Important Feature Set TestCases in Bootloader mode
    """
# end class BootloaderIFeatureSetTestCase


class ApplicationIFeatureUsbTestCase(IFeatureSetTestCaseMixin, DeviceBaseTestCase):
    """
    Validate Device Important Feature Set TestCases in Application mode while the DUT is connected thru USB protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB
# end class ApplicationIFeatureUsbTestCase


@features.class_decorator("BootloaderAvailable", inheritance=IFeatureSetTestCaseMixin)
class BootloaderIFeatureSetUsbTestCase(IFeatureSetTestCaseMixin, DeviceBootloaderTestCase):
    """
    Validate Device Important Feature Set TestCases in Bootloader mode while the DUT is connected thru USB protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB
# end class BootloaderIFeatureSetUsbTestCase


@services.class_decorator("BleContext", inheritance=IFeatureSetTestCaseMixin)
class ApplicationIFeatureDirectBleTestCase(IFeatureSetTestCaseMixin, DeviceBaseTestCase):
    """
    Validate Device Important Feature Set TestCases in Application mode while the DUT is connected through Direct BLE
    protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE
# end class ApplicationIFeatureDirectBleTestCase


@services.class_decorator("BleContext", inheritance=IFeatureSetTestCaseMixin)
class BootloaderIFeatureSetDirectBleTestCase(IFeatureSetTestCaseMixin, DeviceBootloaderTestCase):
    """
    Validate Device Important Feature Set TestCases in Bootloader mode while the DUT is connected through Direct BLE
    protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE
# end class BootloaderIFeatureSetDirectBleTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
