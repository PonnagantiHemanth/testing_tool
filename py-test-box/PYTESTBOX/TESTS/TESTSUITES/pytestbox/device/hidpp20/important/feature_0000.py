#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.important.feature_0000
:brief: Device HID++ 2.0 IRoot Important Package
:author: Christophe Roquebert
:date: 2018/12/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.bootloadertest import DeviceBootloaderTestCase
from pytestbox.shared.hidpp20.important.feature_0000 import ApplicationOnlyIRootTestCase
from pytestbox.shared.hidpp20.important.feature_0000 import IRootTestCaseMixin
from pytestbox.shared.hidpp20.important.feature_0000 import SharedIRootTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ApplicationIRootTestCase(ApplicationOnlyIRootTestCase, DeviceBaseTestCase):
    """
    Validate Important Root TestCases in Application mode
    """
# end class ApplicationIRootTestCase


@features.class_decorator("BootloaderAvailable", inheritance=SharedIRootTestCase)
class BootloaderIRootTestCase(SharedIRootTestCase, DeviceBootloaderTestCase):
    """
    Validate Important Root TestCases in Bootloader mode
    """
# end class BootloaderIRootTestCase


class ApplicationIRootUsbTestCase(IRootTestCaseMixin, DeviceBaseTestCase):
    """
    Validate Important Root TestCases in Application mode while the DUT is connected thru USB protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB
# end class ApplicationIRootUsbTestCase


@features.class_decorator("BootloaderAvailable", inheritance=IRootTestCaseMixin)
class BootloaderIRootUsbTestCase(IRootTestCaseMixin, DeviceBootloaderTestCase):
    """
    Validate Important Root TestCases in Bootloader mode while the DUT is connected thru USB protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB
# end class BootloaderIRootUsbTestCase


@services.class_decorator("BleContext", inheritance=IRootTestCaseMixin)
class ApplicationIRootDirectBleTestCase(IRootTestCaseMixin, DeviceBaseTestCase):
    """
    Validate Important Root TestCases in Application mode while the DUT is connected through direct BLE protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE
# end class ApplicationIRootDirectBleTestCase


@services.class_decorator("BleContext", inheritance=IRootTestCaseMixin)
class BootloaderIRootDirectBleTestCase(IRootTestCaseMixin, DeviceBootloaderTestCase):
    """
    Validate Important Root TestCases in Bootloader mode while the DUT is connected through direct BLE protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE
# end class BootloaderIRootDirectBleTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
