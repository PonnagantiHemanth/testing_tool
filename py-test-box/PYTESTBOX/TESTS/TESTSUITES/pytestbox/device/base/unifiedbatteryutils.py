#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.unifiedbatteryutils
:brief:  Helpers for unified battery feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/07/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from time import time

from pychannel.blechannel import BleChannel
from pyharness.extensions import WarningLevel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.unifiedbattery import BatteryStatusEventV0ToV3
from pyhid.hidpp.features.common.unifiedbattery import BatteryStatusEventV4
from pyhid.hidpp.features.common.unifiedbattery import BatteryStatusEventV5
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV0ToV1
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV3
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV4
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV5
from pyhid.hidpp.features.common.unifiedbattery import GetStatusResponseV0ToV3
from pyhid.hidpp.features.common.unifiedbattery import GetStatusResponseV4
from pyhid.hidpp.features.common.unifiedbattery import GetStatusResponseV5
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryFactory
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytransport.ble.bleinterfaceclasses import BatteryLevelStatus


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UnifiedBatteryTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers on unified battery feature.
    """
    # Timing during which the battery measurement are suspended after a change notification
    BATTERY_MEASURE_BLIND_WINDOW = 16

    # Timing for the PWS battery SoC update in second
    PWS_BATTERY_SOC_UPDATE_TIME = 4

    # Timing for discharging the supercap in second
    DISCHARGE_SUPERCAP_TIME = 15

    # Timing: The time for the battery status update in second
    BATTERY_STATUS_UPDATE_TIME = 4

    # Timing: 60s delay.
    # It's also a criteria for Non-Rechargeable Wireless Powered(NRWP) device. As long as wireless charging starts to
    # charge the supercap, then the NRWP device must be able to be powered up within 60s.
    MINUTE = 60

    # Voltage unit convert (EX: v to mv, mv to v)
    V_UNIT_CONVERT = 1000

    # Transition time of entering charging mode in seconds
    TRANSITION_TIME_OF_ENTERING_CHARGING_MODE = 3

    # Constant current charging mode sampling time in seconds
    CC_SAMPLING_TIME = 8

    # Tolerance time for receiving battery status event report from devices
    REPORT_TOLERANCE_TIME = 2

    # Full charge voltage for Crush Pad charging, unit: Volt
    FULL_CHARGE_VOLTAGE_CP = 4.12

    # Restart charging voltage for Crush Pad charging, unit: Volt
    RESTART_CHARGE_VOLTAGE_CP = 4.0

    # Default voltage threshold in Volt
    # cf https://docs.google.com/document/d/1ArpYWbkJ2YVWhJLxjY016YT_C718-xCIhWZXoCNAPD0/edit# (SoC section)
    DEFAULT_VOLTAGE_THRESHOLD = 4.138

    # Wireless charging table offset voltage, unit: Volt
    WIRELESS_CHARGING_VOLTAGE_OFFSET = 0.045

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetCapabilities`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetCapabilitiesResponseV0ToV1`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY
            check_map = {
                "rfu_1": (cls.check_rfu_1, 0),
                "supported_level_full": (cls.check_full_level, config.F_SupportedLevels[0]),
                "supported_level_good": (cls.check_good_level, config.F_SupportedLevels[1]),
                "supported_level_low": (cls.check_low_level, config.F_SupportedLevels[2]),
                "supported_level_critical": (cls.check_critical_level, config.F_SupportedLevels[3]),
                "rfu_2": (cls.check_rfu_2, 0),
                "removable_battery_capability_flag": (
                    cls.check_removable_battery_capability_flag, config.F_CapabilitiesFlags[5] if len(
                        config.F_CapabilitiesFlags) > UnifiedBattery.Flags.REMOVABLE_BATTERY else 0),
                "fast_charging_capability_flag": (
                    cls.check_fast_charging_capability_flag, config.F_CapabilitiesFlags[4] if len(
                        config.F_CapabilitiesFlags) > UnifiedBattery.Flags.FAST_CHARGING else 0),
                "battery_src_idx_capability_flag": (cls.check_src_capability_flag, config.F_CapabilitiesFlags[3]),
                "show_capability_flag": (cls.check_show_capability_flag, config.F_CapabilitiesFlags[2]),
                "soc_capability_flag": (cls.check_soc_capability_flag, config.F_CapabilitiesFlags[1]),
                "rchg_capability_flag": (cls.check_rchg_capability_flag, config.F_CapabilitiesFlags[0]),
                "battery_source_index": (cls.check_battery_source_index, config.F_BatterySourceIndex),
            }
            return check_map
        # end def get_default_check_map

        @staticmethod
        def check_rfu_1(test_case, response, expected):
            """
            Check Rfu_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0ToV1 | GetCapabilitiesResponseV2 | GetCapabilitiesResponseV3 |
            GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert rfu_1 that raise an exception
            """
            test_case.assertEqual(
                obtained=to_int(response.rfu_1),
                expected=to_int(expected),
                msg="The rfu_1 field differs from the one expected")
        # end def check_rfu_1

        @staticmethod
        def check_rfu_2(test_case, response, expected):
            """
            Check Rfu_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0ToV1 | GetCapabilitiesResponseV2 | GetCapabilitiesResponseV3 |
            GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert rfu_2 that raise an exception
            """
            test_case.assertEqual(
                obtained=to_int(response.rfu_2),
                expected=to_int(expected),
                msg="The rfu_2 field differs from the one expected")
        # end def check_rfu_2

        @staticmethod
        def check_full_level(test_case, response, expected):
            """
            Check full level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0ToV1 | GetCapabilitiesResponseV2 | GetCapabilitiesResponseV3 |
            GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``str``

            :raise ``AssertionError``: Assert supported_level_full that raise an exception
            """
            test_case.assertEqual(
                obtained=to_int(response.supported_level_full),
                expected=1 if expected != '-1' else 0,
                msg="The supported_level_full parameter differs from the one expected")
        # end def check_full_level

        @staticmethod
        def check_good_level(test_case, response, expected):
            """
            Check good level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0ToV1 | GetCapabilitiesResponseV2 | GetCapabilitiesResponseV3 |
            GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``str``

            :raise ``AssertionError``: Assert supported_level_good that raise an exception
            """
            test_case.assertEqual(
                obtained=to_int(response.supported_level_good),
                expected=1 if expected != '-1' else 0,
                msg="The supported_level_good parameter differs from the one expected")
        # end def check_good_level

        @staticmethod
        def check_low_level(test_case, response, expected):
            """
            Check low level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0ToV1 | GetCapabilitiesResponseV2 | GetCapabilitiesResponseV3 |
            GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``str``

            :raise ``AssertionError``: Assert supported_level_low that raise an exception
            """
            test_case.assertEqual(
                obtained=to_int(response.supported_level_low),
                expected=1 if expected != '-1' else 0,
                msg="The supported_level_low parameter differs from the one expected")
        # end def check_low_level

        @staticmethod
        def check_critical_level(test_case, response, expected):
            """
            Check full level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0ToV1 | GetCapabilitiesResponseV2 | GetCapabilitiesResponseV3 |
            GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``str``

            :raise ``AssertionError``: Assert supported_level_critical that raise an exception
            """
            test_case.assertEqual(
                obtained=to_int(response.supported_level_critical),
                expected=1 if expected != '-1' else 0,
                msg="The supported_level_critical parameter differs from the one expected")
        # end def check_critical_level

        @staticmethod
        def check_removable_capability_flag(test_case, response, expected):
            """
            Check removable_battery_capability_flag capability flag field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``str``

            :raise ``AssertionError``: Assert removable_battery_capability_flag that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.removable_battery_capability_flag),
                                  expected=int(expected),
                                  msg="The removable_battery_capability_flag parameter differs from the one "
                                      "expected")
        # end def check_removable_capability_flag

        @staticmethod
        def check_src_capability_flag(test_case, response, expected):
            """
            Check battery_src_idx capability flag field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV3 | GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``str``

            :raise ``AssertionError``: Assert battery_src_idx_capability_flag that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.battery_src_idx_capability_flag),
                                  expected=int(expected),
                                  msg="The battery_src_idx_capability_flag parameter differs from the one "
                                      "expected")
        # end def check_src_capability_flag

        @staticmethod
        def check_show_capability_flag(test_case, response, expected):
            """
            Check show capability flag field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV2 | GetCapabilitiesResponseV3 | GetCapabilitiesResponseV4 |
            GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``str``

            :raise ``AssertionError``: Assert show_capability_flag that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.show_capability_flag),
                                  expected=int(expected),
                                  msg="The show_capability_flag parameter differs from the one expected")
        # end def check_show_capability_flag

        @staticmethod
        def check_soc_capability_flag(test_case, response, expected):
            """
            Check soc capability flag field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0ToV1 | GetCapabilitiesResponseV2 | GetCapabilitiesResponseV3 |
            GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``str``

            :raise ``AssertionError``: Assert soc_capability_flag that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.soc_capability_flag),
                                  expected=int(expected),
                                  msg="The soc_capability_flag parameter differs from the one expected")
        # end def check_soc_capability_flag

        @staticmethod
        def check_rchg_capability_flag(test_case, response, expected):
            """
            Check rchg capability flag field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV0ToV1 | GetCapabilitiesResponseV2 | GetCapabilitiesResponseV3 |
            GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``str``

            :raise ``AssertionError``: Assert rchg_capability_flag that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.rchg_capability_flag),
                                  expected=int(expected),
                                  msg="The rchg_capability_flag parameter differs from the one expected")
        # end def check_rchg_capability_flag

        @staticmethod
        def check_removable_battery_capability_flag(test_case, response, expected):
            """
            Check removable_battery_capability_flag field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert removable_battery_capability_flag that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The removable_battery_capability_flag shall be (a) defined in the DUT settings (b) passed as "
                    "an argument")
            test_case.assertEqual(
                expected=int(expected),
                obtained=to_int(response.removable_battery_capability_flag),
                msg="The removable_battery_capability_flag parameter differs from the one expected")
        # end def check_removable_battery_capability_flag

        @staticmethod
        def check_fast_charging_capability_flag(test_case, response, expected):
            """
            Check fast_charging_capability_flag field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert fast_charging_capability_flag that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The fast_charging_capability_flag shall be (a) defined in the DUT settings (b) passed as an "
                    "argument")
            test_case.assertEqual(
                expected=int(expected),
                obtained=to_int(response.fast_charging_capability_flag),
                msg="The fast_charging_capability_flag parameter differs from the one expected")
        # end def check_fast_charging_capability_flag

        @staticmethod
        def check_battery_source_index(test_case, response, expected):
            """
            Check battery source index field response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponseV3 | GetCapabilitiesResponseV4 | GetCapabilitiesResponseV5``
            :param expected: Expected battery source index
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert battery_source_index that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.battery_source_index),
                                  expected=to_int(expected),
                                  msg="The battery_source_index parameter differs from the one expected")
        # end def check_battery_source_index
    # end class GetCapabilitiesResponseChecker

    class GetStatusResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetStatus`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetStatus`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "state_of_charge": (cls.check_state_of_charge, 100),
                "rfu_1": (cls.check_rfu_1, 0),
                "battery_level_full": (cls.check_full_battery_level, 0),
                "battery_level_good": (cls.check_good_battery_level, 0),
                "battery_level_low": (cls.check_low_battery_level, 0),
                "battery_level_critical": (cls.check_critical_battery_level, 0),
                "charging_status": (cls.check_charging_status, UnifiedBattery.ChargingStatus.DISCHARGING),
                "external_power_status": (cls.check_external_power_status, UnifiedBattery.ExternalPowerStatus.NO_POWER),
                "rfu_2": (cls.check_rfu_2, 0),
                "fast_charging_status": (cls.check_fast_charging_status, 0),
                "rfu_3": (cls.check_rfu_3, 0),
                "removable_battery_status": (cls.check_removable_battery_status, 0),
            }
        # end def get_default_check_map

        @staticmethod
        def check_rfu_1(test_case, response, expected):
            """
            Check Rfu_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert rfu_1 that raise an exception
            """
            test_case.assertEqual(
                obtained=to_int(response.rfu_1),
                expected=to_int(expected),
                msg="The rfu_1 field differs from the one expected")
        # end def check_rfu_1

        @staticmethod
        def check_state_of_charge(test_case, response, expected):
            """
            Check state of charge field response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected state of charge
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert state_of_charge that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.state_of_charge),
                                  expected=to_int(expected),
                                  msg="The state_of_charge parameter differs from the one expected")
        # end def check_state_of_charge

        @staticmethod
        def check_state_of_charge_in_range(test_case, response, expected):
            """
            Check the state of charge field value is in a range around the expected value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected state of charge
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert state_of_charge that raise an exception
            """
            test_case.assertAlmostEqual(first=to_int(response.state_of_charge),
                                        second=to_int(expected),
                                        delta=test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_StateOfChargeStep,
                                        msg="The state_of_charge parameter differs more than the given delta from the "
                                            "expected value")
        # end def check_state_of_charge_in_range

        @staticmethod
        def check_full_battery_level(test_case, response, expected):
            """
            Check full battery level field response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert full_battery_level that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.battery_level_full),
                                  expected=to_int(expected),
                                  msg=f"Full battery level parameter differs from the one expected, it should"
                                      f" be {expected}, instead of {to_int(response.battery_level_full)}")
        # end def check_full_battery_level

        @staticmethod
        def check_good_battery_level(test_case, response, expected):
            """
            Check good battery level field response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert good_battery_level that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.battery_level_good),
                                  expected=to_int(expected),
                                  msg=f"Good battery level parameter differs from the one expected, it should"
                                      f" be {expected}, instead of {to_int(response.battery_level_good)}")
        # end def check_good_battery_level

        @staticmethod
        def check_low_battery_level(test_case, response, expected):
            """
            Check low battery level field response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert low_battery_level that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.battery_level_low),
                                  expected=to_int(expected),
                                  msg=f"Low battery level parameter differs from the one expected, it should"
                                      f" be {expected}, instead of {to_int(response.battery_level_low)}")
        # end def check_low_battery_level

        @staticmethod
        def check_critical_battery_level(test_case, response, expected):
            """
            Check critical battery level field response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert critical_battery_level that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.battery_level_critical),
                                  expected=to_int(expected),
                                  msg=f"Critical battery level parameter differs from the one expected, it should"
                                      f" be {expected}, instead of {to_int(response.battery_level_critical)}")
        # end def check_critical_battery_level

        @staticmethod
        def check_charging_status(test_case, response, expected):
            """
            Check charging status field response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected charging status
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert charging_status that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.charging_status),
                                  expected=to_int(expected),
                                  msg="The charging status parameter differs from the one expected, "
                                      f"charging status should be {expected}, instead of {response.charging_status}")
        # end def check_charging_status

        @staticmethod
        def check_external_power_status(test_case, response, expected):
            """
            Check external power status field response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected external power status
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert external_power_status that raise an exception
            """
            test_case.assertEqual(obtained=to_int(response.external_power_status),
                                  expected=to_int(expected),
                                  msg="The external power status parameter differs from the one expected, "
                                      f"external_power_status should be {expected}, "
                                      f"instead of {response.external_power_status}")
        # end def check_external_power_status

        @staticmethod
        def check_rfu_2(test_case, response, expected):
            """
            Check Rfu_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV4 | BatteryStatusEventV5 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert rfu_2 that raise an exception
            """
            test_case.assertEqual(
                obtained=to_int(response.rfu_2),
                expected=to_int(expected),
                msg="The rfu_2 field differs from the one expected")
        # end def check_rfu_2

        @staticmethod
        def check_fast_charging_status(test_case, response, expected):
            """
            Check fast_charging_status field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV4 | BatteryStatusEventV5 | GetStatusResponseV4 | GetStatusResponseV5``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert fast_charging_status that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The fast_charging_status shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.fast_charging_status),
                msg="The fast_charging_status parameter differs from the one expected")
        # end def check_fast_charging_status

        @staticmethod
        def check_rfu_3(test_case, response, expected):
            """
            Check Rfu_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV5 | GetStatusResponseV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert rfu_3 that raise an exception
            """
            test_case.assertEqual(
                obtained=to_int(response.rfu_3),
                expected=to_int(expected),
                msg="The rfu_3 field differs from the one expected")
        # end def check_rfu_3

        @staticmethod
        def check_removable_battery_status(test_case, response, expected):
            """
            Check removable_battery_status field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: BatteryStatusEvent or GetStatusResponse to check
            :type response: ``BatteryStatusEventV5 | GetStatusResponseV5``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert removable_battery_status that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The removable_battery_status shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.removable_battery_status),
                msg="The removable_battery_status parameter differs from the one expected")
        # end def check_removable_battery_status
    # end class GetStatusResponseChecker

    class BatteryStatusEventChecker(GetStatusResponseChecker):
        """
        Check ``BatteryStatus`` event
        """
    # end class BatteryStatusEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case, feature_id=UnifiedBattery.FEATURE_ID, factory=UnifiedBatteryFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None):
            """
            Send a GetCapabilities and wait for its response.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: The GetCapabilities response
            :rtype: ``GetCapabilitiesResponseV0ToV1``
            """
            feature_1004_index, feature_1004, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)
            get_capabilities = feature_1004.get_capabilities_cls(
                device_index=device_index, feature_index=feature_1004_index)

            return ChannelUtils.send(
                test_case=test_case,
                report=get_capabilities,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1004.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_status(cls, test_case, device_index=None, port_index=None):
            """
            Send a GetStatus and wait for its response.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: The GetStatus response
            :rtype: ``GetStatusResponseV0ToV3``
            """
            feature_1004_index, feature_1004, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)
            get_status = feature_1004.get_status_cls(
                device_index=device_index, feature_index=feature_1004_index)

            return ChannelUtils.send(
                        test_case=test_case,
                        report=get_status,
                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=feature_1004.get_status_response_cls)
        # end def get_status

        @classmethod
        def show_battery_status(cls, test_case, device_index=None, port_index=None):
            """
            Send a ShowBatteryStatus and wait for its response.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: The Show Battery Status response
            :rtype: ``ShowBatteryStatusResponseV1ToV2``
            """
            feature_1004_index, feature_1004, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)
            show_battery_status = feature_1004.show_battery_status_cls(
                device_index=device_index, feature_index=feature_1004_index)

            return ChannelUtils.send(
                        test_case=test_case,
                        report=show_battery_status,
                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=feature_1004.show_battery_status_response_cls)
        # end def show_battery_status
    # end class HIDppHelper

    class GamingDevicesHelper:
        """
        Gaming devices helper class
        """

        @staticmethod
        def wait_soc_computation(test_case):
            """
            Collect ``BatteryStatusEventV0ToV3`` notifications and return the last one with the most up-to-date SoC
            value.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Battery status notification
            :rtype: ``BatteryStatusEventV0ToV3``
            """
            # Gaming FW need at least 8 ~ 16 seconds to average voltage samples (anti-jitter) then start the SoC update.
            test_case.button_stimuli_emulator.user_action()  # Keep device in run mode
            sleep(UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
            battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(test_case)

            retry = 1
            while battery_status_event:
                response = UnifiedBatteryTestUtils.wait_for_battery_status_event(test_case)
                if response is None:
                    if retry:
                        retry -= 1
                        test_case.button_stimuli_emulator.user_action()  # Keep device in run mode
                        sleep(UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
                        continue
                    else:
                        break
                    # end if
                else:
                    battery_status_event = response
                # end if
            # end while

            return battery_status_event
        # end def wait_soc_computation

        @staticmethod
        def wait_soc_computation_const_current_charging(test_case, continuously_receive=True,
                                                        external_power_status=UnifiedBattery.ExternalPowerStatus.WIRED):
            """
            Collect ``BatteryStatusEventV0ToV3`` notifications and return the last one with the most up-to-date SoC
            value.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param continuously_receive: Flag indicating if battery notification
                                         should be received continuously - OPTIONAL
            :type continuously_receive: ``bool``
            :param external_power_status: The power source reported by the device - OPTIONAL
            :type external_power_status: ``int`` or ``HexList``

            :return: Battery status notification
            :rtype: ``BatteryStatusEventV0ToV3``
            """
            _, feature_1004, _, _ = UnifiedBatteryTestUtils.HIDppHelper.get_parameters(test_case)

            # Gaming FW need at least 8 ~ 16 seconds to average voltage samples (anti-jitter) then start the SoC update.
            test_case.button_stimuli_emulator.user_action()  # Keep device in run mode

            battery_status_event = None
            loop_iterations = 0

            sampling_time = UnifiedBatteryTestUtils.CC_SAMPLING_TIME if \
                external_power_status == UnifiedBattery.ExternalPowerStatus.WIRED else \
                UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW

            while loop_iterations <= sampling_time:
                response = ChannelUtils.get_only(
                    test_case=test_case, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
                    class_type=feature_1004.battery_status_event_cls,
                    timeout=1, check_first_message=False, allow_no_message=True)
                if response is not None:
                    battery_status_event = response
                    loop_iterations = 0
                    if not continuously_receive:
                        break
                    # end if
                # end if
                loop_iterations += 1
            # end while

            return battery_status_event
        # end def wait_soc_computation_const_current_charging

        @staticmethod
        def wait_soc_computation_const_voltage_charging(test_case, expected_soc, is_first_report=False):
            """
            Collect ``BatteryStatusEventV0ToV3`` notifications and return the last one with the most up-to-date SoC
            value.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param expected_soc: Expected state of charge
            :type expected_soc: ``int``
            :param is_first_report: Flag indicating that we shall wait 8 more seconds to receive the first
                                    battery status event - OPTIONAL
            :type is_first_report: ``bool``

            :return: Battery status notification, elapsed time of receiving battery notification
            :rtype: ``tuple[BatteryStatusEventV0ToV3, int]``
            """
            _, feature_1004, _, _ = UnifiedBatteryTestUtils.HIDppHelper.get_parameters(test_case)

            # Keep device in run mode
            test_case.button_stimuli_emulator.user_action()

            battery_status_event = None
            elapsed_time = 0

            if is_first_report:
                # The first report might need additional 8 seconds for sampling, adding 8 seconds delay when the
                # program is waiting for the first report of battery status event.
                sleep(UnifiedBatteryTestUtils.CC_SAMPLING_TIME)
            # end if

            init_time = time()
            upper_bound_counter = BatteryFiveSegmentCounterInfo.get_upper_bound_counter(test_case,
                                                                                        expected_soc)
            while elapsed_time < upper_bound_counter + UnifiedBatteryTestUtils.REPORT_TOLERANCE_TIME:
                battery_status_event = ChannelUtils.get_only(
                    test_case=test_case, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
                    class_type=feature_1004.battery_status_event_cls,
                    timeout=1, check_first_message=False, allow_no_message=True)
                if battery_status_event is not None:
                    break
                # end if
                elapsed_time = time() - init_time
            # end while

            return battery_status_event, int(elapsed_time)
        # end def wait_soc_computation_const_voltage_charging

        @staticmethod
        def check_battery_report_time_interval(test_case, state_of_charge, elapsed_time, is_first_report=False):
            """
            Check the reporting time interval is in valid range

            :param test_case: Current test case
            :type test_case: ``pytestbox.device.hidpp20.common.feature_1004.unifiedbattery.UnifiedBatteryGenericTest``
            :param state_of_charge: Battery state of charge
            :type state_of_charge: ``int`` or ``HexList``
            :param elapsed_time: Elapsed time of receiving battery notification
            :type elapsed_time: ``int``
            :param is_first_report: Flag indicating that had waited a few more seconds to receive the first
                                    battery status event - OPTIONAL
            :type is_first_report: ``bool``

            :raise ``AssertionError``: Assert check_battery_report_time_interval that raise an exception
            """
            upper_bound_counter = BatteryFiveSegmentCounterInfo.get_upper_bound_counter(test_case,
                                                                                        state_of_charge)
            lower_bound_counter = BatteryFiveSegmentCounterInfo.get_lower_bound_counter(test_case,
                                                                                        state_of_charge)

            if to_int(state_of_charge) == 100:
                lower_bound_counter = 0
                upper_bound_counter = UnifiedBatteryTestUtils.REPORT_TOLERANCE_TIME
            elif is_first_report:
                """
                The first report might have following latency between FW constant_v_counter and the 
                elapsed_time, so need to ignore these difference. 
                """
                lower_bound_counter = lower_bound_counter \
                                      - UnifiedBatteryTestUtils.TRANSITION_TIME_OF_ENTERING_CHARGING_MODE \
                                      - UnifiedBatteryTestUtils.CC_SAMPLING_TIME \
                                      - UnifiedBatteryTestUtils.REPORT_TOLERANCE_TIME
                upper_bound_counter = upper_bound_counter + UnifiedBatteryTestUtils.REPORT_TOLERANCE_TIME
            elif to_int(state_of_charge) == test_case.constant_v_threshold + 1:
                """
                If the expected SoC equals constant_v_threshold SoC + 1%, then skip reporting time check. 
                When the DUT is entering constant voltage charging mode, its report time is floated. The root 
                cause of this behavior might be the FW limitation and the difference between program implementation and
                the real-world used case.
                """
                lower_bound_counter = 0
            else:
                lower_bound_counter = lower_bound_counter - UnifiedBatteryTestUtils.REPORT_TOLERANCE_TIME
                upper_bound_counter = upper_bound_counter + UnifiedBatteryTestUtils.REPORT_TOLERANCE_TIME
            # end if

            test_case.assertGreaterEqual(elapsed_time, lower_bound_counter,
                                         msg=f"Reporting time {elapsed_time} seconds is not in valid range")
            test_case.assertLessEqual(elapsed_time, upper_bound_counter,
                                      msg=f"Reporting time {elapsed_time} seconds is not in valid range")
        # end def check_battery_report_time_interval
    # end class GamingDevicesHelper

    @staticmethod
    def wait_for_battery_status_event(test_case, timeout=0, **kwargs):
        """
        Wait for a battery status event.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param timeout: The timeout value to use to wait - OPTIONAL
        :type timeout: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: The received battery status event
        :rtype: ``BatteryStatusEventV0ToV3``
        """
        _, feature_1004, _, _ = UnifiedBatteryTestUtils.HIDppHelper.get_parameters(test_case)

        # Warning if there are some unused arguments after we popped those needed
        if len(kwargs) > 0:
            test_case.log_warning(f"Too many arguments for "
                                  f"{test_case.__class__.__name__}.wait_for_battery_status_event: {kwargs}",
                                  warning_level=WarningLevel.ROBUSTNESS)
        # end if

        return ChannelUtils.get_only(
            test_case=test_case, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
            class_type=feature_1004.battery_status_event_cls,
            timeout=timeout, check_first_message=False, allow_no_message=True)
    # end def wait_for_battery_status_event

    @staticmethod
    def wait_soc_computation(test_case, check_battery_event_on_core_dut=True, timeout_for_core_dut=None):
        """
        Wait SoC computation until it's update-to-date.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param check_battery_event_on_core_dut: Wait and check the battery status events if True, do nothing
                                                otherwise. - OPTIONAL
        :type check_battery_event_on_core_dut: ``bool``
        :param timeout_for_core_dut: Set None to use default timeout = BATTERY_MEASURE_BLIND_WINDOW - OPTIONAL
        :type timeout_for_core_dut: ``int``

        :return: The last and the penultimate (if it exists) battery status notifications
        :rtype: ``tuple(BatteryStatusEventV0ToV3, BatteryStatusEventV0ToV3 | None)``
        """
        battery_status_event = None
        penultimate_event = None
        if test_case.f.PRODUCT.F_IsGaming:
            battery_status_event = \
                UnifiedBatteryTestUtils.GamingDevicesHelper.wait_soc_computation(test_case)
        else:
            if check_battery_event_on_core_dut:
                if timeout_for_core_dut is None:
                    timeout_for_core_dut = UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW
                # end if
                sleep(timeout_for_core_dut)
                while True:
                    # Retrieve the last available battery event sent by the DUT
                    event = UnifiedBatteryTestUtils.wait_for_battery_status_event(test_case)
                    if event is None:
                        break
                    else:
                        penultimate_event = battery_status_event
                        battery_status_event = event
                    # end if
                # end while
            else:
                sleep(UnifiedBatteryTestUtils.MINUTE)
            # end if
        # end if
        return battery_status_event, penultimate_event
    # end def wait_soc_computation

    @staticmethod
    def power_reset_device_wait_wireless_status(test_case, starting_voltage=None):
        """
        Power reset device and check the x1D4B wireless status notification.
        - If the starting_voltage = None, it will be replaced with maximum voltage value.
        - Including a workaround to ignore Gaming DUT sends a redundant wireless status event issue

        Jira ticket: https://jira.logitech.io/browse/ARBL-24

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param starting_voltage: The output voltage while turning on device - OPTIONAL
        :type starting_voltage: ``float``
        """
        UnifiedBatteryTestUtils.set_voltage_wait_wireless_status(test_case, starting_voltage)
        # TODO: remove below check after FW fixed the P2 issue
        if test_case.f.PRODUCT.F_IsGaming:
            ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end if
    # end def power_reset_device_wait_wireless_status

    @staticmethod
    def get_state_of_charge_by_name(test_case, level_name):
        """
        Get the SOC based on the given level.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param level_name: 'full', 'good', 'low' or 'critical'
        :type level_name: ``str``

        :return: battery percentage
        :rtype: ``int``
        """
        index = UnifiedBatteryTestUtils.get_index_from_level(test_case=test_case, level_name=level_name)
        state_of_charge = int(test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[index])
        return state_of_charge
    # end def get_state_of_charge_by_name

    @staticmethod
    def get_voltage_by_state_of_charge(test_case, state_of_charge, discharge=True):
        """
        Get the voltage matching the given SOC and the charging mode (optional).

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param state_of_charge: battery percentage
        :type state_of_charge: ``int``
        :param discharge: discharge or recharge mode - OPTIONAL
        :type discharge: ``bool``

        :return: battery value in Volt
        :rtype: ``float``
        """
        soc_index = (100 - state_of_charge) // test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_StateOfChargeStep
        if discharge:
            battery_value = round(int(test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_DischargeSOCmV[soc_index]) /
                                  UnifiedBatteryTestUtils.V_UNIT_CONVERT, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
        else:
            battery_value = round(int(test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_RechargeSOCmV[soc_index]) /
                                  UnifiedBatteryTestUtils.V_UNIT_CONVERT, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
        # end if
        return battery_value
    # end def get_voltage_by_state_of_charge

    @staticmethod
    def set_voltage_wait_wireless_status(test_case, voltage=None):
        """
        Set the battery emulator voltage to the given value.
         - Turn off the battery emulation
         - Clean up the possible Battery events notified by the device during the previous turn off
         - Set the voltage value to its maximum then turn on the battery emulation
         - wait for the Wireless Device Status Broadcast event returned by the device

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param voltage: new voltage value to apply (default is maximum supported voltage) - OPTIONAL
        :type voltage: ``float`` or ``None``
        """
        _, feature_1004, _, _ = UnifiedBatteryTestUtils.HIDppHelper.get_parameters(test_case)
        if voltage is None:
            voltage = test_case.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage
        # end if
        test_case.power_supply_emulator.turn_off()
        sleep(.2)
        # Empty event_message_queue from BatteryStatusEvent notifications sent by the device
        ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT,
                                    class_type=feature_1004.battery_status_event_cls)
        test_case.power_supply_emulator.restart_device(starting_voltage=voltage)

        if isinstance(test_case.current_channel, BleChannel): # BLE channel doesn't automatically reconnect
            test_case.current_channel.wait_device_connection_state(connected=True, timeout=2)
        # end if
        DeviceBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(test_case=test_case)
    # end def set_voltage_wait_wireless_status

    @staticmethod
    def adapt_soc(test_case, input_soc, expected_soc, deviation=5):
        """
        Adapt SoC value to the expected SoC value if the difference is less than the deviation value.

        Note:
        - This function is used for Gaming devices only and by pass input SoC for PWS device.
        - The valid deviation value is 5% (for all SoC checking) and 3% (for supported battery level).

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param input_soc: Be adapted SoC value
        :type input_soc: ``int | HexList``
        :param expected_soc: The expected SoC
        :type expected_soc: ``int``
        :param deviation: The deviation allowed to adapt the SoC value - OPTIONAL
        :type deviation: ``int``

        :return: Adapted SoC value
        :rtype: ``int``

        :raise ``AssertionError``: If the deviation value is invalid
        """
        assert deviation in [3, 5], f"Invalid deviation value: {deviation}"

        int_soc = to_int(input_soc)
        adapted_soc = int_soc
        if test_case.f.PRODUCT.F_IsGaming:
            if abs(int_soc - expected_soc) <= deviation:
                adapted_soc = expected_soc
            # end if
        # end if
        return adapted_soc
    # end def adapt_soc

    @staticmethod
    def compare_status(test_case, first_event_response, second_event_response, previous_event_response=None, **kwargs):
        """
        Compare status from event and response.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param first_event_response: The first battery status event or GetStatus response, MANDATORY
        :type first_event_response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
        :param second_event_response: The second battery status event or GetStatus response, MANDATORY
        :type second_event_response: ``BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
        :param previous_event_response: The previous battery status event - OPTIONAL
        :type previous_event_response: ``None | BatteryStatusEventV0ToV3 | BatteryStatusEventV4 | BatteryStatusEventV5 |
            GetStatusResponseV0ToV3 | GetStatusResponseV4 | GetStatusResponseV5``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :raise ``AssertionError``: If the battery status parameters differ from the one expected
        """
        _, feature_1004, _, _ = UnifiedBatteryTestUtils.HIDppHelper.get_parameters(test_case)
        test_case.assertTrue(
            expr=(isinstance(first_event_response, feature_1004.battery_status_event_cls) or
                  isinstance(first_event_response, feature_1004.get_status_response_cls)),
            msg=f"first_event_response wrong type: {first_event_response.__class__.__name__}, "
                f"should be {feature_1004.battery_status_event_cls} or "
                f"{feature_1004.get_status_response_cls}")
        test_case.assertTrue(
            expr=(isinstance(first_event_response, feature_1004.battery_status_event_cls) or
                  isinstance(first_event_response, feature_1004.get_status_response_cls)),
            msg=f"second_event_response wrong type: {second_event_response.__class__.__name__}, "
                f"should be {feature_1004.battery_status_event_cls} or "
                f"{feature_1004.get_status_response_cls}")
        test_case.assertEqual(obtained=to_int(second_event_response.battery_level_full),
                              expected=to_int(first_event_response.battery_level_full),
                              msg="The battery_level_full parameter differs from the one expected")
        test_case.assertEqual(obtained=to_int(second_event_response.battery_level_good),
                              expected=to_int(first_event_response.battery_level_good),
                              msg="The battery_level_good parameter differs from the one expected")
        test_case.assertEqual(obtained=to_int(second_event_response.battery_level_low),
                              expected=to_int(first_event_response.battery_level_low),
                              msg="The battery_level_low parameter differs from the one expected")
        test_case.assertEqual(obtained=to_int(second_event_response.battery_level_critical),
                              expected=to_int(first_event_response.battery_level_critical),
                              msg="The battery_level_critical parameter differs from the one expected")
        test_case.assertEqual(obtained=to_int(second_event_response.state_of_charge),
                              expected=to_int(first_event_response.state_of_charge),
                              msg="The state_of_charge parameter differs from the one expected")
        test_case.assertEqual(obtained=to_int(second_event_response.charging_status),
                              expected=to_int(first_event_response.charging_status),
                              msg="The charging_status parameter differs from the one expected")
        test_case.assertEqual(obtained=to_int(second_event_response.external_power_status),
                              expected=to_int(first_event_response.external_power_status),
                              msg="The external_power_status parameter differs from the one expected")

        if previous_event_response is not None:
            test_case.assertTrue(
                expr=isinstance(previous_event_response, feature_1004.battery_status_event_cls),
                msg=f"previous_event_response wrong type: {previous_event_response.__class__.__name__}, should be "
                    f"{feature_1004.battery_status_event_cls}")
            test_case.assertEqual(
                obtained=to_int(
                                previous_event_response.state_of_charge +
                                test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_StateOfChargeStep),
                expected=to_int(first_event_response.state_of_charge),
                msg="The state_of_charge parameter differs from the one expected")
        # end if
        # Warning if there are some unused arguments after we popped those needed
        if len(kwargs) > 0:
            test_case.log_warning(f"Too many arguments for {test_case.__class__.__name__}.compare_status: {kwargs}",
                                  warning_level=WarningLevel.ROBUSTNESS)
        # end if
    # end def compare_status

    @staticmethod
    def get_level_from_index(test_case, index, **kwargs):
        """
        Get level name from the index in BATTERY_LEVELS_V0ToV5.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param index: The level index in BATTERY_LEVELS_V0ToV5, can be [0..3], MANDATORY
        :type index: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: The battery level name, can be 'full', 'good', 'low' or 'critical'
        :rtype: ``str``
        """

        # Warning if there are some unused arguments after we popped those needed
        if len(kwargs) > 0:
            test_case.log_warning(f"Too many arguments for {test_case.__class__.__name__}.get_level_from_index: "
                                  f"{kwargs}",
                                  warning_level=WarningLevel.ROBUSTNESS)
        # end if

        return UnifiedBattery.BATTERY_LEVELS_V0ToV5[index]
    # end def get_level_from_index

    @staticmethod
    def get_index_from_level(test_case, level_name, **kwargs):
        """
        Get level index in BATTERY_LEVELS_V0ToV5 from its name.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param level_name: 'full', 'good', 'low' or 'critical'
        :type level_name: ``str``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: The battery level index, can be [0..3]
        :rtype: ``int``
        """
        # Warning if there are some unused arguments after we popped those needed
        if len(kwargs) > 0:
            test_case.log_warning(f"Too many arguments for {test_case.__class__.__name__}.get_index_from_level: "
                                  f"{kwargs}",
                                  warning_level=WarningLevel.ROBUSTNESS)
        # end if

        return UnifiedBattery.BATTERY_LEVELS_V0ToV5.index(level_name)
    # end def get_index_from_level

    @staticmethod
    def get_padding_size_for_get_capabilities(test_case, **kwargs):
        """
        Get the padding size of GetCapabilitiesV0ToV3.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: The padding size of GetCapabilitiesV0ToV3
        :rtype: ``int``
        """
        _, feature_1004, _, _ = UnifiedBatteryTestUtils.HIDppHelper.get_parameters(test_case)
        # Warning if there are some unused arguments after we popped those needed
        if len(kwargs) > 0:
            test_case.log_warning(f"Too many arguments for "
                                  f"{test_case.__class__.__name__}.get_padding_size_for_get_capabilities: {kwargs}",
                                  warning_level=WarningLevel.ROBUSTNESS)
        # end if

        return feature_1004.get_capabilities_cls.LEN.PADDING // 8
    # end def get_padding_size_for_get_capabilities

    @classmethod
    def get_battery_level_status(cls, test_case, soc):
        """
        Parse battery level from battery status event or get status response

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param soc: State of charge
        :type soc: ``int`` or ``HexList``

        :return: battery level status [full, good, low, critical]
        :rtype: ``list[int]``

        :raise ``ValueError``: If get invalid battery level from test settings
        """
        battery_level = None

        for i in range(len(test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels)):
            supported_level = int(test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[i])
            if supported_level == -1:
                continue
            # end if
            good_level = int(test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[1])
            if to_int(soc) > good_level or (to_int(soc) == good_level and test_case.f.PRODUCT.F_IsGaming):
                # If the current soc is greater than or equal to (Gaming specific) the 'good' battery level soc,
                # the battery level is set to 'full'.
                # For details please refer to 'Battery charging flow in gaming platform' doc's 'Battery Level' section
                # cf https://docs.google.com/document/d/1ArpYWbkJ2YVWhJLxjY016YT_C718-xCIhWZXoCNAPD0/edit#
                battery_level = 'full'
                break
            elif to_int(soc) > supported_level:
                battery_level = cls.get_level_from_index(test_case=test_case, index=i-1)
                break
            else:
                if i == len(test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels) - 1:
                    battery_level = cls.get_level_from_index(test_case=test_case, index=i)
                # end if
            # end if
        # end for

        if battery_level == 'full':
            battery_level_status = [1, 0, 0, 0]
        elif battery_level == 'good':
            battery_level_status = [0, 1, 0, 0]
        elif battery_level == 'low':
            battery_level_status = [0, 0, 1, 0]
        elif battery_level == 'critical':
            battery_level_status = [0, 0, 0, 1]
        else:
            raise ValueError(f'Invalid battery level: {battery_level}')
        # end if

        return battery_level_status
    # end def get_battery_level_status

    @staticmethod
    def is_the_capability_supported(test_case, capability):
        """
        Return True if the input capability is supported on the device.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param capability: Flag indicating the battery capability on the device
        :type capability: ``UnifiedBattery.Flags``

        :return: True if the input capability of battery is supported on the device, otherwise False
        :rtype: ``bool``
        """
        if len(test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_CapabilitiesFlags) > capability:
            if int(test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_CapabilitiesFlags[capability]) == 1:
                return True
            else:
                return False
            # end if
        else:
            return False
        # end if
    # end def is_the_capability_supported

    @classmethod
    def get_ble_bas_battery_level_status(cls, unified_battery_status):
        """
        Get the battery level status for BAS 1.1 of BLE Gatt table

        :param unified_battery_status: status from the 1004 feature
        :type unified_battery_status: ``UnifiedBattery``

        :return: battery level status structure
        :rtype: ``BatteryLevelStatus``

        :raise ``ValueError``: Value error on unsupported levels
        """
        if unified_battery_status.external_power_status == UnifiedBattery.ExternalPowerStatus.WIRED:
            wired_power = 1
            wireless_power = 0
        elif unified_battery_status.external_power_status == UnifiedBattery.ExternalPowerStatus.WIRELESS:
            wired_power = 0
            wireless_power = 1
        else:
            wired_power = 0
            wireless_power = 0
        # end if
        charging_status = unified_battery_status.charging_status.toLong()
        if charging_status in [UnifiedBattery.ChargingStatus.CHARGING,
                               UnifiedBattery.ChargingStatus.CHARGING_AT_SLOW_RATE,
                               UnifiedBattery.ChargingStatus.CHARGE_ERROR]:
            status = 1
        elif charging_status == UnifiedBattery.ChargingStatus.DISCHARGING:
            status = 2
        elif charging_status == UnifiedBattery.ChargingStatus.CHARGE_COMPLETE:
            status = 3
        else:
            status = 0
        # end if

        if (unified_battery_status.battery_level_full or
                unified_battery_status.battery_level_good or
                unified_battery_status.battery_level_low):
            level = 1
        elif unified_battery_status.battery_level_critical and unified_battery_status.state_of_charge != 0:
            level = 2
        elif unified_battery_status.battery_level_critical and unified_battery_status.state_of_charge == 0:
            level = 3
        else:
            raise ValueError(f"unsupported level for {unified_battery_status}")
        # end if

        fault = 0b100 if charging_status == UnifiedBattery.ChargingStatus.CHARGE_ERROR else 0

        return BatteryLevelStatus(
            flags=0,
            battery_present=1,
            wired_external_power_source_connected=wired_power,
            wireless_external_power_source_connected=wireless_power,
            battery_charge_state=status,
            battery_charge_level=level,
            charging_type=0,
            charging_fault_reasons=fault,
            rfu=0,
        )
    # end def get_ble_bas_battery_level_status

    @classmethod
    def check_bas_alignment(cls, test_case, status_1004, ble_bas_status_message, ble_bas_level_message=None):
        """
        Check the BAS Battery Level Status value correspond to the status from Unified Battery (feature 1004)
        and  check the BAS Battery Level characteristic value too.

        Both check can be disabled by passing None as the corresponding ble message

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param status_1004:  status from the 1004 feature
        :type status_1004: ``UnifiedBattery``
        :param ble_bas_status_message: Battery Level Status value of the BLE BAS
        :type ble_bas_status_message: ``BleMessage | None``
        :param ble_bas_level_message: Battery Level value of the BLE BAS. - OPTIONAL
        :type ble_bas_level_message: ``BleMessage | None``

        :raise ``AssertionError``: If the value of the BAS Battery Level Status characteristic is not aligned
        """
        derived_status_value = cls.get_ble_bas_battery_level_status(status_1004)
        if ble_bas_status_message is None:
            ble_status_value = BatteryLevelStatus.fromHexList(ble_bas_status_message.data)

            test_case.assertEqual(expected=derived_status_value, obtained=ble_status_value,
                                  msg="The value of the BAS Battery Level Status characteristic is not aligned "
                                      "with the corresponding 1004 status")
        # end if
        if ble_bas_level_message is not None:
            ble_level = ble_bas_level_message.data
            test_case.assertEqual(expected=status_1004.state_of_charge, obtained=ble_level,
                                  msg="The value of the BAS Battery Level characteristic is not aligned "
                                      "with the corresponding 1004 status")
        # end if
    # end def check_bas_alignment

# end class UnifiedBatteryTestUtils


class BatteryFiveSegmentCounterInfo:
    """
    Battery five segment counter info, it's used in constant voltage charging mode
    """
    # ------------------------------------------------------------------------------------------------------------------
    # Synergy battery 5 segment counter info
    # ------------------------------------------------------------------------------------------------------------------
    # The SoC value in the 5 segments counter interval are used in constant voltage charging
    SYNERGY_5_SEGMENT_COUNTER_TO_SOC = (76, 83, 91, 96, 99)
    # The (lower bound, upper bound) time tolerance range for the 5 segments counter
    # Unit: second
    SYNERGY_5_SEGMENT_COUNTER_INTERVAL = ((32, 32), (44, 48), (72, 72), (169, 176), (305, 312))

    SYNERGY = {
        SYNERGY_5_SEGMENT_COUNTER_TO_SOC[0]: SYNERGY_5_SEGMENT_COUNTER_INTERVAL[0],
        SYNERGY_5_SEGMENT_COUNTER_TO_SOC[1]: SYNERGY_5_SEGMENT_COUNTER_INTERVAL[1],
        SYNERGY_5_SEGMENT_COUNTER_TO_SOC[2]: SYNERGY_5_SEGMENT_COUNTER_INTERVAL[2],
        SYNERGY_5_SEGMENT_COUNTER_TO_SOC[3]: SYNERGY_5_SEGMENT_COUNTER_INTERVAL[3],
        SYNERGY_5_SEGMENT_COUNTER_TO_SOC[4]: SYNERGY_5_SEGMENT_COUNTER_INTERVAL[4]
    }

    # ------------------------------------------------------------------------------------------------------------------
    # High Power battery 5 segment counter info
    # ------------------------------------------------------------------------------------------------------------------
    # The SoC value in the 5 segments counter interval are used in constant voltage charging
    HIGH_POWER_5_SEGMENT_TIMER_TO_SOC = (71, 81, 88, 96, 99)
    # The (lower bound, upper bound) time tolerance range for the 5 segments counter
    # Unit: second
    HIGH_POWER_5_SEGMENT_TIMER_INTERVAL = ((42, 48), (66, 72), (82, 88), (188, 192), (547, 552))

    HIGH_POWER = {
        HIGH_POWER_5_SEGMENT_TIMER_TO_SOC[0]: HIGH_POWER_5_SEGMENT_TIMER_INTERVAL[0],
        HIGH_POWER_5_SEGMENT_TIMER_TO_SOC[1]: HIGH_POWER_5_SEGMENT_TIMER_INTERVAL[1],
        HIGH_POWER_5_SEGMENT_TIMER_TO_SOC[2]: HIGH_POWER_5_SEGMENT_TIMER_INTERVAL[2],
        HIGH_POWER_5_SEGMENT_TIMER_TO_SOC[3]: HIGH_POWER_5_SEGMENT_TIMER_INTERVAL[3],
        HIGH_POWER_5_SEGMENT_TIMER_TO_SOC[4]: HIGH_POWER_5_SEGMENT_TIMER_INTERVAL[4]
    }

    @staticmethod
    def get_battery_mapping_table(test_case):
        """
        Get the battery mapping table.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Battery mapping table of 5 segment counter and corresponding state of charge
        :rtype: ``dict[int, tuple[int, int]]``

        :raise ``ValueError``: If the index of battery source is not supported
        """
        config = test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY

        if config.F_BatterySourceIndex == 1:
            battery_mapping_table = BatteryFiveSegmentCounterInfo.SYNERGY
        elif config.F_BatterySourceIndex == 2:
            battery_mapping_table = BatteryFiveSegmentCounterInfo.HIGH_POWER
        else:
            raise ValueError(f'Unsupported index of battery source: {config.F_BatterySourceIndex}')
        # end if
        return battery_mapping_table
    # end def get_battery_mapping_table

    @staticmethod
    def get_counter_segment_soc(test_case, state_of_charge):
        """
        Get the index of counter segment

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param state_of_charge: Battery state of charge
        :type state_of_charge: ``int`` or ``HexList``

        :return: The corresponding soc of the counter segment
        :rtype: ``int``
        """
        for counter_soc in BatteryFiveSegmentCounterInfo.get_battery_mapping_table(test_case).keys():
            if to_int(state_of_charge) <= counter_soc:
                return counter_soc
            # end if
        # end for
    # end def get_counter_segment_soc

    @staticmethod
    def get_upper_bound_counter(test_case, state_of_charge):
        """
        Get the upper bound counter value

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param state_of_charge: Battery state of charge
        :type state_of_charge: ``int`` or ``HexList``

        :return: The upper bound counter of the counter segment index
        :rtype: ``int``
        """
        counter_soc = BatteryFiveSegmentCounterInfo.get_counter_segment_soc(test_case, state_of_charge)
        return BatteryFiveSegmentCounterInfo.get_battery_mapping_table(test_case)[counter_soc][1]
    # end def get_upper_bound_counter

    @staticmethod
    def get_lower_bound_counter(test_case, state_of_charge):
        """
        Get the lower bound counter value

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param state_of_charge: Battery state of charge
        :type state_of_charge: ``int`` or ``HexList``

        :return: The lower bound counter of the counter segment index
        :rtype: ``int``
        """
        counter_soc = BatteryFiveSegmentCounterInfo.get_counter_segment_soc(test_case, state_of_charge)
        return BatteryFiveSegmentCounterInfo.get_battery_mapping_table(test_case)[counter_soc][0]
    # end def get_lower_bound_counter
# end class BatteryFiveSegmentCounterInfo

# ----------------------------------------------------------------------------------------------------------------------
# End of file
# ----------------------------------------------------------------------------------------------------------------------
