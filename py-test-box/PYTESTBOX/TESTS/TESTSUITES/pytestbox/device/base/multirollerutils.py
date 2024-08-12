#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.multirollerutils
:brief: Helpers for ``MultiRoller`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.multiroller import GetCapabilitiesResponse
from pyhid.hidpp.features.keyboard.multiroller import GetModeResponse
from pyhid.hidpp.features.keyboard.multiroller import GetRollerCapabilitiesResponseV0
from pyhid.hidpp.features.keyboard.multiroller import GetRollerCapabilitiesResponseV1
from pyhid.hidpp.features.keyboard.multiroller import MultiRoller
from pyhid.hidpp.features.keyboard.multiroller import MultiRollerFactory
from pyhid.hidpp.features.keyboard.multiroller import RotationEventV1
from pyhid.hidpp.features.keyboard.multiroller import SetModeResponse
from pyhid.hidpp.features.keyboard.multiroller import NumRoller
from pyhid.hidpp.features.keyboard.multiroller import RollerId
from pyhid.hidpp.features.keyboard.multiroller import RollerMode
from pyhid.hidpp.features.keyboard.multiroller import CapabilitiesV0
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiRollerTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``MultiRoller`` feature
    """

    class NumRollerChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``NumRoller``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.MULTI_ROLLER
            return {
                "reserved": (cls.check_reserved, 0),
                "num_rollers": (cls.check_num_rollers, config.F_NumRollers)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: NumRoller to check
            :type bitmap: ``NumRoller``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_num_rollers(test_case, bitmap, expected):
            """
            Check num_rollers field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: NumRoller to check
            :type bitmap: ``NumRoller``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert num_rollers that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.num_rollers),
                msg="The num_rollers parameter differs from the one expected")
        # end def check_num_rollers
    # end class NumRollerChecker

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "num_roller": (cls.check_num_roller,
                               MultiRollerTestUtils.NumRollerChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_num_roller(test_case, message, expected):
            """
            Check ``num_roller``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetCapabilitiesResponse to check
            :type message: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            MultiRollerTestUtils.NumRollerChecker.check_fields(
                test_case, message.num_roller, NumRoller, expected)
        # end def check_num_roller
    # end class GetCapabilitiesResponseChecker

    class CapabilitiesChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``Capabilities``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case=test_case, roller_id=0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, roller_id):
            """
            Get the check methods and expected values for a given roller index

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param roller_id: The roller index
            :type roller_id: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.MULTI_ROLLER
            return {
                "reserved": (cls.check_reserved, 0),
                "timestamp_report": (cls.check_timestamp_report, int(config.F_TimestampReport[roller_id])),
                "lightbar_id": (cls.check_lightbar_id, int(config.F_LightbarId[roller_id]))
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``MultiRoller.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_timestamp_report(test_case, bitmap, expected):
            """
            Check timestamp_report field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``MultiRoller.CapabilitiesV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert timestamp_report that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.timestamp_report),
                msg="The timestamp_report parameter differs from the one expected")
        # end def check_timestamp_report

        @staticmethod
        def check_lightbar_id(test_case, bitmap, expected):
            """
            Check lightbar_id field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``MultiRoller.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert lightbar_id that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.lightbar_id),
                msg="The lightbar_id parameter differs from the one expected")
        # end def check_lightbar_id
    # end class CapabilitiesChecker

    class GetRollerCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetRollerCapabilitiesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case=test_case, roller_id=0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, roller_id):
            """
            Get the check methods and expected values for a given roller index

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param roller_id: The roller index
            :type roller_id: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.MULTI_ROLLER
            roller_capabilities_checker = MultiRollerTestUtils.CapabilitiesChecker
            roller_capabilities_check_map = roller_capabilities_checker.get_check_map(test_case=test_case,
                                                                                      roller_id=roller_id)
            return {
                "increments_per_rotation": (cls.check_increments_per_rotation,
                                            int(config.F_IncrementsPerRotation[roller_id])),
                "increments_per_ratchet": (cls.check_increments_per_ratchet,
                                           int(config.F_IncrementsPerRatchet[roller_id])),
                "capabilities": (
                    cls.check_capabilities, roller_capabilities_check_map)
            }
        # end def get_check_map

        @staticmethod
        def check_increments_per_rotation(test_case, response, expected):
            """
            Check increments_per_rotation field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRollerCapabilitiesResponse to check
            :type response: ``GetRollerCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert increments_per_rotation that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.increments_per_rotation),
                msg="The increments_per_rotation parameter differs from the one expected")
        # end def check_increments_per_rotation

        @staticmethod
        def check_increments_per_ratchet(test_case, response, expected):
            """
            Check increments_per_ratchet field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRollerCapabilitiesResponse to check
            :type response: ``GetRollerCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert increments_per_ratchet that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.increments_per_ratchet),
                msg="The increments_per_ratchet parameter differs from the one expected")
        # end def check_increments_per_ratchet

        @staticmethod
        def check_capabilities(test_case, message, expected):
            """
            Check ``capabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetRollerCapabilitiesResponse to check
            :type message: ``GetRollerCapabilitiesResponseV0 | GetRollerCapabilitiesResponseV1``
            :param expected: Expected value
            :type expected: ``dict``
            """
            MultiRollerTestUtils.CapabilitiesChecker.check_fields(
                test_case, message.capabilities, CapabilitiesV0, expected)
        # end def check_capabilities
    # end class GetRollerCapabilitiesResponseChecker

    class RollerModeChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``RollerMode``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(divert=RollerMode.DEFAULT_MODE)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, divert):
            """
            Get the check methods with given expected values

            :param divert: Roller mode
            :type divert: ``RollerMode | int``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "reserved": (cls.check_reserved, 0),
                "divert": (cls.check_divert, divert)
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: RollerMode to check
            :type bitmap: ``RollerMode``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_divert(test_case, bitmap, expected):
            """
            Check divert field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: RollerMode to check
            :type bitmap: ``RollerMode``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert divert that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.divert),
                msg="The divert parameter differs from the one expected")
        # end def check_divert
    # end class RollerModeChecker

    class GetModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(divert=RollerMode.DEFAULT_MODE)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, divert):
            """
            Get the check methods with given expected value

            :param divert: Roller mode
            :type divert: ``RollerMode | int``

            :return: Check map
            :rtype: ``dict``
            """
            roller_mode_checker = MultiRollerTestUtils.RollerModeChecker
            roller_mode_check_map = roller_mode_checker.get_check_map(divert=divert)
            return {
                "roller_mode": (cls.check_roller_mode, roller_mode_check_map)
            }
        # end def get_check_map

        @staticmethod
        def check_roller_mode(test_case, message, expected):
            """
            Check ``roller_mode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetModeResponse to check
            :type message: ``GetModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            MultiRollerTestUtils.RollerModeChecker.check_fields(
                test_case, message.roller_mode, RollerMode, expected)
        # end def check_roller_mode
    # end class GetModeResponseChecker

    class RollerIdChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``RollerId``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(roller_id=0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, roller_id):
            """
            Get the check methods with given expected value

            :param roller_id: The roller index
            :type roller_id: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "reserved": (cls.check_reserved, 0),
                "roller_id": (cls.check_roller_id, roller_id)
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: RollerId to check
            :type bitmap: ``RollerId``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_roller_id(test_case, bitmap, expected):
            """
            Check roller_id field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: RollerId to check
            :type bitmap: ``RollerId``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert roller_id that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.roller_id),
                msg="The roller_id parameter differs from the one expected")
        # end def check_roller_id
    # end class RollerIdChecker

    class SetModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(roller_id=0, divert=RollerMode.DEFAULT_MODE)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, roller_id, divert):
            """
            Get the check methods and expected values for a given roller index and roller mode

            :param roller_id: Roller index
            :type roller_id: ``int``
            :param divert: Roller mode
            :type divert: ``RollerMode | int``

            :return: Check map
            :rtype: ``dict``
            """
            roller_id_checker = MultiRollerTestUtils.RollerIdChecker
            roller_id_check_map = roller_id_checker.get_check_map(roller_id=roller_id)
            roller_mode_checker = MultiRollerTestUtils.RollerModeChecker
            roller_mode_check_map = roller_mode_checker.get_check_map(divert=divert)
            return {
                "roller_id": (cls.check_roller_id, roller_id_check_map),
                "roller_mode": (cls.check_roller_mode, roller_mode_check_map)
            }
        # end def get_check_map

        @staticmethod
        def check_roller_id(test_case, message, expected):
            """
            Check ``roller_id``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: SetModeResponse to check
            :type message: ``SetModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            MultiRollerTestUtils.RollerIdChecker.check_fields(
                test_case, message.roller_id, RollerId, expected)
        # end def check_roller_id

        @staticmethod
        def check_roller_mode(test_case, message, expected):
            """
            Check ``roller_mode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: SetModeResponse to check
            :type message: ``SetModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            MultiRollerTestUtils.RollerModeChecker.check_fields(
                test_case, message.roller_mode, RollerMode, expected)
        # end def check_roller_mode
    # end class SetModeResponseChecker

    class RotationEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``RotationEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(roller_id=0, delta=0, report_timestamp=0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, roller_id, delta, report_timestamp):
            """
            Get the check methods with given expected values

            :param roller_id: Roller index
            :type roller_id: ``int``
            :param delta: Roller rotation increments since last report
            :type delta: ``int``
            :param report_timestamp: Report timestamp in ms
            :type report_timestamp: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            roller_id_checker = MultiRollerTestUtils.RollerIdChecker
            roller_id_check_map = roller_id_checker.get_check_map(roller_id=roller_id)
            return {
                "roller_id": (cls.check_roller_id, roller_id_check_map),
                "delta": (cls.check_delta, delta),
                "report_timestamp": (cls.check_report_timestamp, report_timestamp)
            }
        # end def get_check_map

        @staticmethod
        def check_roller_id(test_case, message, expected):
            """
            Check ``roller_id``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: RotationEvent to check
            :type message: ``RotationEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            MultiRollerTestUtils.RollerIdChecker.check_fields(
                test_case, message.roller_id, RollerId, expected)
        # end def check_roller_id

        @staticmethod
        def check_delta(test_case, event, expected):
            """
            Check delta field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: RotationEvent to check
            :type event: ``RotationEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert delta that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.delta),
                msg="The delta parameter differs from the one expected")
        # end def check_delta

        @staticmethod
        def check_report_timestamp(test_case, event, expected):
            """
            Check report_timestamp field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: RotationEvent to check
            :type event: ``RotationEventV1``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert report_timestamp that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(event.report_timestamp),
                msg="The report_timestamp parameter differs from the one expected")
        # end def check_report_timestamp
    # end class RotationEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=MultiRoller.FEATURE_ID,
                           factory=MultiRollerFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetCapabilitiesResponse (if not error)
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_4610_index, feature_4610, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4610.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_4610_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4610.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_capabilities_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_4610_index, feature_4610, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4610.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_4610_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def get_roller_capabilities(cls, test_case, roller_id, reserved=None, device_index=None, port_index=None,
                                    software_id=None, padding=None):
            """
            Process ``GetRollerCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param roller_id: Roller Id
            :type roller_id: ``int | HexList``
            :param reserved: Reserved bits of roller id - OPTIONAL
            :type reserved: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetRollerCapabilitiesResponse (if not error)
            :rtype: ``GetRollerCapabilitiesResponseV0 | GetRollerCapabilitiesResponseV1``
            """
            feature_4610_index, feature_4610, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4610.get_roller_capabilities_cls(
                device_index=device_index,
                feature_index=feature_4610_index,
                roller_id=roller_id)

            if reserved is not None:
                report.reserved = reserved
            # end if

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4610.get_roller_capabilities_response_cls)
        # end def get_roller_capabilities

        @classmethod
        def get_roller_capabilities_and_check_error(
                cls, test_case, error_codes, roller_id, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``GetRollerCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param roller_id: Roller Id
            :type roller_id: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_4610_index, feature_4610, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4610.get_roller_capabilities_cls(
                device_index=device_index,
                feature_index=feature_4610_index,
                roller_id=roller_id)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_roller_capabilities_and_check_error

        @classmethod
        def get_mode(cls, test_case, roller_id, reserved=None, device_index=None, port_index=None, software_id=None,
                     padding=None):
            """
            Process ``GetMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param roller_id: Roller Id
            :type roller_id: ``int``
            :param reserved: Reserved bits of roller id - OPTIONAL
            :type reserved: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetModeResponse (if not error)
            :rtype: ``GetModeResponse``
            """
            feature_4610_index, feature_4610, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4610.get_mode_cls(
                device_index=device_index,
                feature_index=feature_4610_index,
                roller_id=roller_id)

            if reserved is not None:
                report.reserved = reserved
            # end if

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4610.get_mode_response_cls)
        # end def get_mode

        @classmethod
        def get_mode_and_check_error(
                cls, test_case, error_codes, roller_id, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``GetMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param roller_id: Roller Id
            :type roller_id: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_4610_index, feature_4610, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4610.get_mode_cls(
                device_index=device_index,
                feature_index=feature_4610_index,
                roller_id=roller_id)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_mode_and_check_error

        @classmethod
        def set_mode(cls, test_case, roller_id, divert, device_index=None, port_index=None, software_id=None,
                     padding=None):
            """
            Process ``SetMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param roller_id: Roller Id
            :type roller_id: ``int | HexList``
            :param divert: divert
            :type divert: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetModeResponse (if not error)
            :rtype: ``SetModeResponse``
            """
            feature_4610_index, feature_4610, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4610.set_mode_cls(
                device_index=device_index,
                feature_index=feature_4610_index,
                roller_id=roller_id,
                divert=divert)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4610.set_mode_response_cls)
        # end def set_mode

        @classmethod
        def set_mode_and_check_error(
                cls, test_case, error_codes, roller_id, divert, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SetMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param roller_id: Roller Id
            :type roller_id: ``int | HexList``
            :param divert: divert
            :type divert: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_4610_index, feature_4610, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4610.set_mode_cls(
                device_index=device_index,
                feature_index=feature_4610_index,
                roller_id=roller_id,
                divert=divert)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_mode_and_check_error

        @classmethod
        def rotation_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``RotationEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: RotationEvent
            :rtype: ``RotationEvent``
            """
            _, feature_4610, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_4610.rotation_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def rotation_event
    # end class HIDppHelper
# end class MultiRollerTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
