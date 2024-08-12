#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.important.testrunner
:brief: Device HID++ 2.0 Important features testrunner implementation
:author: Christophe Roquebert
:date: 2018/02/02
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import PyHarnessSuite
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.hidpp20.important.feature_0000 import ApplicationIRootDirectBleTestCase
from pytestbox.device.hidpp20.important.feature_0000 import ApplicationIRootTestCase
from pytestbox.device.hidpp20.important.feature_0000 import ApplicationIRootUsbTestCase
from pytestbox.device.hidpp20.important.feature_0000 import BootloaderIRootDirectBleTestCase
from pytestbox.device.hidpp20.important.feature_0000 import BootloaderIRootTestCase
from pytestbox.device.hidpp20.important.feature_0000 import BootloaderIRootUsbTestCase
from pytestbox.device.hidpp20.important.feature_0001 import ApplicationIFeatureDirectBleTestCase
from pytestbox.device.hidpp20.important.feature_0001 import ApplicationIFeatureSetTestCase
from pytestbox.device.hidpp20.important.feature_0001 import ApplicationIFeatureUsbTestCase
from pytestbox.device.hidpp20.important.feature_0001 import BootloaderIFeatureSetDirectBleTestCase
from pytestbox.device.hidpp20.important.feature_0001 import BootloaderIFeatureSetTestCase
from pytestbox.device.hidpp20.important.feature_0001 import BootloaderIFeatureSetUsbTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceImportantHidpp20TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 important tests
    """
    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, ApplicationIRootTestCase)
        self.runTest(result, context, BootloaderIRootTestCase)
        self.runTest(result, context, ApplicationIFeatureSetTestCase)
        self.runTest(result, context, BootloaderIFeatureSetTestCase)

        features = context.getFeatures()
        fw_info = features.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION
        default_protocol = features.PRODUCT.PROTOCOLS.F_DefaultProtocol
        if default_protocol is not None:
            assert default_protocol in LogitechProtocol, \
                f"Unknown F_DefaultProtocol = {default_protocol}, is should be part of LogitechProtocol " \
                "(either a name of or a value in the enum)"
            default_protocol = LogitechProtocol(default_protocol)
            # If the default protocol is specified (and a known value), it should just not be the protocol of the
            # specific testsuite (and the specific protocol should be supported)
            do_usb_specific_testsuites = fw_info.F_TransportUsb and default_protocol != LogitechProtocol.USB
            do_ble_specific_testsuites = fw_info.F_TransportBTLE and default_protocol != LogitechProtocol.BLE
        else:
            # If the default protocol is not specified, another protocol than the protocol of the specific testsuite
            # should exist (and the specific protocol should be supported)
            do_usb_specific_testsuites = fw_info.F_TransportUsb and (fw_info.F_TransportEQuad or
                                                                     fw_info.F_TransportBTLE or fw_info.F_TransportBT)
            do_ble_specific_testsuites = fw_info.F_TransportBTLE and (fw_info.F_TransportEQuad or
                                                                      fw_info.F_TransportBT or fw_info.F_TransportUsb)
        # end if

        if do_usb_specific_testsuites:
            self.runTest(result, context, ApplicationIRootUsbTestCase)
            self.runTest(result, context, BootloaderIRootUsbTestCase)
            self.runTest(result, context, ApplicationIFeatureUsbTestCase)
            self.runTest(result, context, BootloaderIFeatureSetUsbTestCase)
        # end if
        if do_ble_specific_testsuites:
            self.runTest(result, context, ApplicationIRootDirectBleTestCase)
            self.runTest(result, context, ApplicationIFeatureDirectBleTestCase)

            config_manager = ConfigurationManager(context.getFeatures())
            if config_manager.feature_value_map[config_manager.ID.TRANSPORT_BTLE][config_manager.MODE.BOOTLOADER]:
                self.runTest(result, context, BootloaderIRootDirectBleTestCase)
                self.runTest(result, context, BootloaderIFeatureSetDirectBleTestCase)
            # end if
        # end if
    # end def runTests
# end class DeviceImportantHidpp20TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
