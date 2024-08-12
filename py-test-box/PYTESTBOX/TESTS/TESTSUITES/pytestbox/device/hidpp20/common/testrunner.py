#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.testrunner
:brief: Device HID++ 2.0 Common features testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/03/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import PyHarnessSuite
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.hidpp20.common.feature_0003 import ApplicationDeviceInformationTestCase
from pytestbox.device.hidpp20.common.feature_0003 import ApplicationDeviceInformationUsbTestCase
from pytestbox.device.hidpp20.common.feature_0003 import BootloaderDeviceInformationTestCase
from pytestbox.device.hidpp20.common.feature_0003 import BootloaderDeviceInformationUsbTestCase
from pytestbox.device.hidpp20.common.feature_0005 import ApplicationDeviceTypeAndNameTestCase
from pytestbox.device.hidpp20.common.feature_0005 import ApplicationDeviceTypeAndNameUsbTestCase
from pytestbox.device.hidpp20.common.feature_0005 import BootloaderDeviceTypeAndNameTestCase
from pytestbox.device.hidpp20.common.feature_0007.testrunner import DeviceHidpp20Feature0007TestSuite
from pytestbox.device.hidpp20.common.feature_0008.testrunner import DeviceHidpp20Feature0008TestSuite
from pytestbox.device.hidpp20.common.feature_0011.testrunner import DeviceHidpp20Feature0011TestSuite
from pytestbox.device.hidpp20.common.feature_0020 import ApplicationConfigChangeTestCase
from pytestbox.device.hidpp20.common.feature_0021 import ApplicationUniqueIdentifier32BytesMultiReceiverTestCase
from pytestbox.device.hidpp20.common.feature_0021 import ApplicationUniqueIdentifier32BytesSpecificFirmwareTestCase
from pytestbox.device.hidpp20.common.feature_0021 import ApplicationUniqueIdentifier32BytesTestCase
from pytestbox.device.hidpp20.common.feature_00C2 import ApplicationDfuControlTestCase
from pytestbox.device.hidpp20.common.feature_00D0_business import BleppDfuDirectBleTestCaseBusiness
from pytestbox.device.hidpp20.common.feature_00D0_business import DfuDirectBleTestCaseBusiness
from pytestbox.device.hidpp20.common.feature_00D0_business import DfuOnTagDirectBleTestCaseBusiness
from pytestbox.device.hidpp20.common.feature_00D0_business import DfuOnTagTestCaseBusiness
from pytestbox.device.hidpp20.common.feature_00D0_business import DfuTestCaseBusiness
from pytestbox.device.hidpp20.common.feature_00D0_change_flag import DfuTestCaseChangeFlag
from pytestbox.device.hidpp20.common.feature_00D0_change_security_level import DfuTestCaseChangeSecurityLevel
from pytestbox.device.hidpp20.common.feature_00D0_errorhandling import DfuTestCaseErrorHandling
from pytestbox.device.hidpp20.common.feature_00D0_functionality import DfuTestCaseFunctionality
from pytestbox.device.hidpp20.common.feature_00D0_interface import DfuTestCaseInterface
from pytestbox.device.hidpp20.common.feature_00D0_robustness import DfuTestCaseRobustness
from pytestbox.device.hidpp20.common.feature_00D0_security import DfuTestCaseSecurity
from pytestbox.device.hidpp20.common.feature_00c3.testrunner import DeviceHidpp20Feature00C3TestSuite
from pytestbox.device.hidpp20.common.feature_1000 import ApplicationBatteryUnifiedLevelStatusTestCase
from pytestbox.device.hidpp20.common.feature_1004.testrunner import DeviceHidpp20Feature1004TestSuite
from pytestbox.device.hidpp20.common.feature_1602.testrunner import DeviceHidpp20Feature1602TestSuite
from pytestbox.device.hidpp20.common.feature_1801.testrunner import DeviceHidpp20Feature1801TestSuite
from pytestbox.device.hidpp20.common.feature_1802 import ApplicationDeviceResetTestCase
from pytestbox.device.hidpp20.common.feature_1803.testrunner import DeviceHidpp20Feature1803TestSuite
from pytestbox.device.hidpp20.common.feature_1805.testrunner import DeviceHidpp20Feature1805TestSuite
from pytestbox.device.hidpp20.common.feature_1806.testrunner import DeviceHidpp20Feature1806TestSuite
from pytestbox.device.hidpp20.common.feature_1807.testrunner import DeviceHidpp20Feature1807TestSuite
from pytestbox.device.hidpp20.common.feature_180b.testrunner import DeviceHidpp20Feature180BTestSuite
from pytestbox.device.hidpp20.common.feature_1814.testrunner import DeviceHidpp20Feature1814TestSuite
from pytestbox.device.hidpp20.common.feature_1815.testrunner import DeviceHidpp20Feature1815TestSuite
from pytestbox.device.hidpp20.common.feature_1816.testrunner import DeviceHidpp20Feature1816TestSuite
from pytestbox.device.hidpp20.common.feature_1817.testrunner import DeviceHidpp20Feature1817TestSuite
from pytestbox.device.hidpp20.common.feature_1830 import ApplicationPowerModesTestCase
from pytestbox.device.hidpp20.common.feature_1861.testrunner import DeviceHidpp20Feature1861TestSuite
from pytestbox.device.hidpp20.common.feature_18a1.testrunner import DeviceHidpp20Feature18A1TestSuite
from pytestbox.device.hidpp20.common.feature_18b0.testrunner import DeviceHidpp20Feature18B0TestSuite
from pytestbox.device.hidpp20.common.feature_1982.testrunner import DeviceHidpp20Feature1982TestSuite
from pytestbox.device.hidpp20.common.feature_1D4B import ApplicationWirelessDeviceStatusTestCase
from pytestbox.device.hidpp20.common.feature_1D4B import BootloaderWirelessDeviceStatusTestCase
from pytestbox.device.hidpp20.common.feature_1DF3 import ApplicationEquadDJDebugInfoTestCase
from pytestbox.device.hidpp20.common.feature_1E00 import ApplicationEnableHiddenTestCase
from pytestbox.device.hidpp20.common.feature_1E01_functionality import ManageDeactivatableFeaturesFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1E01_robustness import ManageDeactivatableFeaturesRobustnessTestCase
from pytestbox.device.hidpp20.common.feature_1b04.testrunner import DeviceHidpp20Feature1B04TestSuite
from pytestbox.device.hidpp20.common.feature_1b05.testrunner import DeviceHidpp20Feature1B05TestSuite
from pytestbox.device.hidpp20.common.feature_1b08.testrunner import DeviceHidpp20Feature1B08TestSuite
from pytestbox.device.hidpp20.common.feature_1b10.testrunner import DeviceHidpp20Feature1B10TestSuite
from pytestbox.device.hidpp20.common.feature_1e02.testrunner import DeviceHidpp20Feature1e02TestSuite
from pytestbox.device.hidpp20.common.feature_1e22.testrunner import DeviceHidpp20Feature1E22TestSuite
from pytestbox.device.hidpp20.common.feature_1e30.testrunner import DeviceHidpp20Feature1E30TestSuite
from pytestbox.device.hidpp20.common.feature_1eb0.testrunner import DeviceHidpp20Feature1EB0TestSuite
from pytestbox.device.hidpp20.common.feature_1f30.testrunner import DeviceHidpp20Feature1F30TestSuite


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceCommonHidpp20TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 common tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.

        :param result: The test result that will collect the results.
        :type result: ``TestResult``
        :param context: The context in which the tests are run.
        :type context: ``Context``

        :raise ``AssertionError``: If the default protocol is not supported by the specific testsuites
        """
        self.runTest(result, context, ApplicationDeviceInformationTestCase)
        self.runTest(result, context, BootloaderDeviceInformationTestCase)
        self.runTest(result, context, ApplicationDeviceTypeAndNameTestCase)
        self.runTest(result, context, BootloaderDeviceTypeAndNameTestCase)

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
        else:
            # If the default protocol is not specified, another protocol than the protocol of the specific testsuite
            # should exist (and the specific protocol should be supported)
            do_usb_specific_testsuites = fw_info.F_TransportUsb and (fw_info.F_TransportEQuad or
                                                                     fw_info.F_TransportBTLE or fw_info.F_TransportBT)
        # end if

        if do_usb_specific_testsuites:
            self.runTest(result, context, ApplicationDeviceInformationUsbTestCase)
            self.runTest(result, context, BootloaderDeviceInformationUsbTestCase)
            self.runTest(result, context, ApplicationDeviceTypeAndNameUsbTestCase)
        # end if

        self.runTest(result, context, DfuTestCaseBusiness)
        self.runTest(result, context, DfuOnTagTestCaseBusiness)

        config_manager = ConfigurationManager(context.getFeatures())
        if config_manager.feature_value_map[config_manager.ID.TRANSPORT_BTLE][config_manager.MODE.BOOTLOADER]:
            self.runTest(result, context, DfuDirectBleTestCaseBusiness)
            self.runTest(result, context, DfuOnTagDirectBleTestCaseBusiness)
            self.runTest(result, context, BleppDfuDirectBleTestCaseBusiness)
        # end if

        self.runTest(result, context, DfuTestCaseInterface)
        self.runTest(result, context, DfuTestCaseFunctionality)
        self.runTest(result, context, DfuTestCaseChangeFlag)
        self.runTest(result, context, DfuTestCaseRobustness)
        self.runTest(result, context, DfuTestCaseErrorHandling)
        self.runTest(result, context, DfuTestCaseSecurity)
        self.runTest(result, context, DfuTestCaseChangeSecurityLevel)
        self.runTest(result, context, ApplicationWirelessDeviceStatusTestCase)
        self.runTest(result, context, BootloaderWirelessDeviceStatusTestCase)
        self.runTest(result, context, ApplicationConfigChangeTestCase)
        self.runTest(result, context, ApplicationUniqueIdentifier32BytesTestCase)
        self.runTest(result, context, ApplicationUniqueIdentifier32BytesSpecificFirmwareTestCase)
        self.runTest(result, context, ApplicationUniqueIdentifier32BytesMultiReceiverTestCase)
        self.runTest(result, context, ApplicationBatteryUnifiedLevelStatusTestCase)

        self.runTest(result, context, ApplicationPowerModesTestCase)
        self.runTest(result, context, ApplicationEnableHiddenTestCase)
        self.runTest(result, context, ManageDeactivatableFeaturesFunctionalityTestCase)
        self.runTest(result, context, ManageDeactivatableFeaturesRobustnessTestCase)
        self.runTest(result, context, ApplicationDfuControlTestCase)
        self.runTest(result, context, ApplicationEquadDJDebugInfoTestCase)

        self.runTest(result, context, DeviceHidpp20Feature0007TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature0008TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature0011TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature00C3TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1004TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1602TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1801TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1803TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1805TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1806TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1807TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature180BTestSuite)
        self.runTest(result, context, DeviceHidpp20Feature18A1TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1814TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1815TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1816TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1817TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1861TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature18B0TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1982TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1B04TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1B05TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1B08TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1B10TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1e02TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1E22TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1E30TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1EB0TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature1F30TestSuite)

        # For Demo purpose only - to be removed
        self.runTest(result, context, ApplicationDeviceResetTestCase)
    # end def runTests
# end class DeviceCommonHidpp20TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
