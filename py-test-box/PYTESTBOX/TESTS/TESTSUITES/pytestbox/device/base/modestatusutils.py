#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.modestatusutils
:brief: Helpers for ``ModeStatus`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2022/08/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.modestatus import GetDevConfigResponseV1
from pyhid.hidpp.features.gaming.modestatus import GetDevConfigResponseV2ToV3
from pyhid.hidpp.features.gaming.modestatus import GetModeStatusResponse
from pyhid.hidpp.features.gaming.modestatus import GetModeStatusResponseV3
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pyhid.hidpp.features.gaming.modestatus import ModeStatusBroadcastingEvent
from pyhid.hidpp.features.gaming.modestatus import ModeStatusFactory
from pyhid.hidpp.features.gaming.modestatus import SetModeStatusResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ModeStatusTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ModeStatus`` feature
    """

    class ModeStatus0Checker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ModeStatus0``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.MODE_STATUS
            return cls.get_check_map(mode_status_0=config.F_ModeStatus0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, mode_status_0):
            """
            Get the check methods and expected values

            :param mode_status_0: Mode Status 0
            :type mode_status_0: ``ModeStatus.ModeStatus0|int``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "mode_status_0": (
                    cls.check_mode_status_0,
                    mode_status_0)
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ModeStatus0 to check
            :type bitmap: ``ModeStatus.ModeStatus0``
            :param expected: Expected value
            :type expected: ``int|HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg=f"The reserved parameter differs (expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_mode_status_0(test_case, bitmap, expected):
            """
            Check mode_status_0 field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ModeStatus0 to check
            :type bitmap: ``ModeStatus.ModeStatus0``
            :param expected: Expected value
            :type expected: ``bool|HexList``
            """
            test_case.assertNotNone(
                expected, msg="ModeStatus0 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.mode_status_0),
                msg=f"The mode_status_0 parameter differs (expected:{expected}, obtained:{bitmap.mode_status_0})")
        # end def check_mode_status_0
    # end class ModeStatus0Checker

    class ModeStatus1Checker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ModeStatus1``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.MODE_STATUS
            return cls.get_check_map(mode_status_1=config.F_ModeStatus1)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, mode_status_1):
            """
            Get the check methods and expected values

            :param mode_status_1: Mode Status 1
            :type mode_status_1: ``ModeStatus.ModeStatus1|int``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "power_mode": (
                    cls.check_power_mode,
                    HexList(mode_status_1).testBit(ModeStatus.ModeStatus1.POS.POWER_MODE)),
                "force_gaming_surface_mode": (
                    cls.check_force_gaming_surface_mode,
                    HexList(mode_status_1).testBit(ModeStatus.ModeStatus1.POS.GAMING_SURFACE))
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ModeStatus1 to check
            :type bitmap: ``ModeStatus.ModeStatus1``
            :param expected: Expected value
            :type expected: ``int|HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg=f"The reserved parameter differs (expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_power_mode(test_case, bitmap, expected):
            """
            Check power_mode field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ModeStatus1 to check
            :type bitmap: ``ModeStatus.ModeStatus1``
            :param expected: Expected value
            :type expected: ``bool|HexList``
            """
            test_case.assertNotNone(
                expected, msg="ModeStatus1 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.power_mode),
                msg=f"The power_mode parameter differs (expected:{expected}, obtained:{bitmap.power_mode})")
        # end def check_power_mode

        @staticmethod
        def check_force_gaming_surface_mode(test_case, bitmap, expected):
            """
            Check force_gaming_surface_mode field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ModeStatus1 to check
            :type bitmap: ``ModeStatus.ModeStatus1``
            :param expected: Expected value
            :type expected: ``bool|HexList``
            """
            test_case.assertNotNone(
                expected, msg="ModeStatus1 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.force_gaming_surface_mode),
                msg=f"The force_gaming_surface_mode parameter differs (expected:{expected}, "
                    f"obtained:{bitmap.force_gaming_surface_mode})")
        # end def check_force_gaming_surface_mode
    # end class ModeStatus1Checker

    class GetModeStatusResponseChecker(ModeStatus0Checker, ModeStatus1Checker):
        """
        Define Helper to check ``GetModeStatusResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "mode_status_0": (
                    cls.check_mode_status_0_bit_map,
                    ModeStatusTestUtils.ModeStatus0Checker.get_default_check_map(test_case)),
                "mode_status_1": (
                    cls.check_mode_status_1_bit_map,
                    ModeStatusTestUtils.ModeStatus1Checker.get_default_check_map(test_case)),
            }
        # end def get_default_check_map

        @classmethod
        def check_mode_status_0_bit_map(cls, test_case, message, expected):
            """
            Check mode_status_0 bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetModeStatusResponse to check
            :type message: ``GetModeStatusResponse``
            :param expected: Expected bit map check map
            :type expected: ``dict``
            """
            ModeStatusTestUtils.ModeStatus0Checker.check_fields(
                test_case, message.mode_status_0, ModeStatus.ModeStatus0, expected)
        # end def check_mode_status_0_bit_map

        @classmethod
        def check_mode_status_1_bit_map(cls, test_case, message, expected):
            """
            Check mode_status_1 bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetModeStatusResponse to check
            :type message: ``GetModeStatusResponse``
            :param expected: Expected bit map check map
            :type expected: ``dict``
            """
            if isinstance(message, GetModeStatusResponseV3):
                expected_cls = ModeStatus.ModeStatus1V3
            elif isinstance(message, GetModeStatusResponse):
                expected_cls = ModeStatus.ModeStatus1
            else:
                raise TypeError("Wrong message type. Should be GetModeStatusResponseV3 or GetModeStatusResponse")
            # end if
            ModeStatusTestUtils.ModeStatus1Checker.check_fields(
                test_case, message.mode_status_1, expected_cls, expected)
        # end def check_mode_status_1_bit_map
    # end class GetModeStatusResponseChecker

    class DevCapabilityChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``DevCapability``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.MODE_STATUS
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "mode_status_0_changed_by_hw": (
                    cls.check_mode_status_0_changed_by_hw,
                    config.F_ModeStatus0ChangedByHw),
                "mode_status_0_changed_by_sw": (
                    cls.check_mode_status_0_changed_by_sw,
                    config.F_ModeStatus0ChangedBySw),
                "power_save_mode": (
                    cls.check_power_save_mode,
                    config.F_PowerSaveModeSupported),
                "surface_mode": (
                    cls.check_surface_mode,
                    config.F_NonGamingSurfaceModeSupported)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: DevCapability to check
            :type bitmap: ``ModeStatus.DevCapabilityV1`` or ``ModeStatus.DevCapabilityV2ToV3``
            :param expected: Expected value
            :type expected: ``int|HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg=f"The reserved parameter differs (expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_mode_status_0_changed_by_hw(test_case, bitmap, expected):
            """
            Check mode_status_0_changed_by_hw field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: DevCapability to check
            :type bitmap: ``ModeStatus.DevCapabilityV1|ModeStatus.DevCapabilityV2ToV3``
            :param expected: Expected value
            :type expected: ``bool|HexList``
            """
            test_case.assertNotNone(
                expected,
                msg="ModeStatus0ChangedByHw shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.mode_status_0_changed_by_hw),
                msg="The mode_status_0_changed_by_hw parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.mode_status_0_changed_by_hw})")
        # end def check_mode_status_0_changed_by_hw

        @staticmethod
        def check_mode_status_0_changed_by_sw(test_case, bitmap, expected):
            """
            Check mode_status_0_changed_by_sw field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: DevCapability to check
            :type bitmap: ``ModeStatus.DevCapabilityV1|ModeStatus.DevCapabilityV2ToV3``
            :param expected: Expected value
            :type expected: ``bool|HexList``
            """
            test_case.assertNotNone(
                expected,
                msg="ModeStatus0ChangedBySw shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.mode_status_0_changed_by_sw),
                msg="The mode_status_0_changed_by_sw parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.mode_status_0_changed_by_sw})")
        # end def check_mode_status_0_changed_by_sw

        @staticmethod
        def check_power_save_mode(test_case, bitmap, expected):
            """
            Check power_save_mode field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: DevCapability to check
            :type bitmap: ``ModeStatus.DevCapabilityV2ToV3``
            :param expected: Expected value
            :type expected: ``bool|HexList``
            """
            test_case.assertNotNone(
                expected,
                msg="PowerSaveModeSupported shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.power_save_mode),
                msg="The power_save_mode parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.power_save_mode})")
        # end def check_power_save_mode

        @staticmethod
        def check_surface_mode(test_case, bitmap, expected):
            """
            Check surface_mode field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: DevCapability to check
            :type bitmap: ``ModeStatus.DevCapabilityV2ToV3``
            :param expected: Expected value
            :type expected: ``bool|HexList``
            """
            test_case.assertNotNone(
                expected,
                msg="NonGamingSurfaceModeSupported shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.surface_mode),
                msg="The surface_mode parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.surface_mode})")
        # end def check_surface_mode
    # end class DevCapabilityChecker

    class GetDevConfigResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetDevConfigResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "dev_capability": (
                    cls.check_dev_capability,
                    ModeStatusTestUtils.DevCapabilityChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_dev_capability(test_case, message, expected):
            """
            Check ``dev_capability``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetDevConfigResponse to check
            :type message: ``GetDevConfigResponseV1|GetDevConfigResponseV2ToV3``
            :param expected: Expected value
            :type expected: ``dict``

            :raise ``TypeError``: If input message type is invalid
            """
            if isinstance(message, GetDevConfigResponseV1):
                expected_cls = ModeStatus.DevCapabilityV1
            elif isinstance(message, GetDevConfigResponseV2ToV3):
                expected_cls = ModeStatus.DevCapabilityV2ToV3
            else:
                raise TypeError("Wrong message type. Should be GetDevConfigResponseV1 or GetDevConfigResponseV2ToV3")
            # end if
            ModeStatusTestUtils.DevCapabilityChecker.check_fields(
                test_case, message.dev_capability, expected_cls, expected)
        # end def check_dev_capability
    # end class GetDevConfigResponseChecker

    class ModeStatusBroadcastingEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ModeStatusBroadcastingEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "mode_status_0": (
                    cls.check_mode_status_0,
                    ModeStatusTestUtils.ModeStatus0Checker.get_default_check_map(test_case)),
                "mode_status_1": (
                    cls.check_mode_status_1,
                    ModeStatusTestUtils.ModeStatus1Checker.get_default_check_map(test_case)),
                "changed_mask_0": (cls.check_changed_mask_0, 0),
                "changed_mask_1": (cls.check_changed_mask_1, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_mode_status_0(test_case, message, expected):
            """
            Check ``mode_status_0``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetModeStatusResponse to check
            :type message: ``GetModeStatusResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ModeStatusTestUtils.ModeStatus0Checker.check_fields(
                test_case, message.mode_status_0, ModeStatus.ModeStatus0, expected)
        # end def check_mode_status_0

        @staticmethod
        def check_mode_status_1(test_case, message, expected):
            """
            Check ``mode_status_1``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetModeStatusResponse to check
            :type message: ``GetModeStatusResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ModeStatusTestUtils.ModeStatus1Checker.check_fields(
                test_case, message.mode_status_1, ModeStatus.ModeStatus1, expected)
        # end def check_mode_status_1

        @staticmethod
        def check_changed_mask_0(test_case, message, expected):
            """
            Check ``changed_mask_0``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: ModeStatusBroadcastingEvent to check
            :type message: ``ModeStatusBroadcastingEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(message.changed_mask_0),
                msg=f"The changed_mask_0 parameter differs (expected:{expected}, obtained:{message.changed_mask_0})")
        # end def check_changed_mask_0

        @staticmethod
        def check_changed_mask_1(test_case, message, expected):
            """
            Check ``changed_mask_1``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: ModeStatusBroadcastingEvent to check
            :type message: ``ModeStatusBroadcastingEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(message.changed_mask_1),
                msg=f"The changed_mask_0 parameter differs (expected:{expected}, obtained:{message.changed_mask_1})")
        # end def check_changed_mask_1
    # end class ModeStatusBroadcastingEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=ModeStatus.FEATURE_ID, factory=ModeStatusFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_mode_status(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetModeStatus``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetModeStatusResponse
            :rtype: ``GetModeStatusResponse``
            """
            feature_8090_index, feature_8090, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8090.get_mode_status_cls(
                device_index=device_index,
                feature_index=feature_8090_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8090.get_mode_status_response_cls)
            return response
        # end def get_mode_status

        @classmethod
        def set_mode_status(cls, test_case, mode_status_0, mode_status_1, changed_mask_0, changed_mask_1,
                            device_index=None, port_index=None):
            """
            Process ``SetModeStatus``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param mode_status_0: Mode Status 0
            :type mode_status_0: ``int|HexList``
            :param mode_status_1: Mode Status 1
            :type mode_status_1: ``int|HexList``
            :param changed_mask_0: Changed Mask 0
            :type changed_mask_0: ``int|HexList``
            :param changed_mask_1: Changed Mask 1
            :type changed_mask_1: ``int|HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetModeStatusResponse
            :rtype: ``SetModeStatusResponse``
            """
            feature_8090_index, feature_8090, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8090.set_mode_status_cls(
                device_index=device_index,
                feature_index=feature_8090_index,
                mode_status_0=mode_status_0,
                mode_status_1=mode_status_1,
                changed_mask_0=HexList(changed_mask_0),
                changed_mask_1=HexList(changed_mask_1))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8090.set_mode_status_response_cls)
            return response
        # end def set_mode_status

        @classmethod
        def get_dev_config(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetDevConfig``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetDevConfigResponse
            :rtype: ``GetDevConfigResponse``
            """
            feature_8090_index, feature_8090, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8090.get_dev_config_cls(
                device_index=device_index,
                feature_index=feature_8090_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8090.get_dev_config_response_cls)
            return response
        # end def get_dev_config

        @classmethod
        def mode_status_broadcasting_event(cls, test_case, timeout=2,
                                           check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``ModeStatusBroadcastingEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: ModeStatusBroadcastingEvent
            :rtype: ``ModeStatusBroadcastingEvent``
            """
            _, feature_8090, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8090.mode_status_broadcasting_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def mode_status_broadcasting_event
    # end class HIDppHelper

    @staticmethod
    def get_dev_config(test_case):
        """
        Get device capability from product settings

        :return: The configuration value supported by the device.
        :rtype: ``int``
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.MODE_STATUS

        return config.F_ModeStatus0ChangedByHw * 1 + config.F_ModeStatus0ChangedBySw * 2 + \
            config.F_PowerSaveModeSupported * 4 + config.F_NonGamingSurfaceModeSupported * 8
    # end def get_dev_config

    @staticmethod
    def set_low_latency_mode(test_case):
        """
        Force hybrid switch low latency mode

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            test_case,
            f"Send setModeStatus request with ModeStatus1 = {ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.HIDppHelper.set_mode_status(
            test_case=test_case, mode_status_0=0, mode_status_1=ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE,
            changed_mask_0=0, changed_mask_1=ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case, "Check the configured power mode")
        # --------------------------------------------------------------------------------------------------------------
        test_case.assertEqual(
            expected=ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE,
            obtained=response.mode_status_1.power_mode,
            msg=f"The low latency mode was not configured")
    # end def set_low_latency_mode

    @staticmethod
    def flip_hybrid_switch_mode(test_case):
        """
        Flip the hybrid switch mode from the default to the other supported mode

        Remark from Richard P.: "The default value may change from one NPI to another.
        However, as far as I know, it has always been in power save mode for now."

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, "Get default hybrid switch mode ")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=test_case)

        flipped_mode = ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE if (
                response.mode_status_1.power_mode == ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE) else (
            ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, f"Send setModeStatus request with ModeStatus1 = {flipped_mode}")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.HIDppHelper.set_mode_status(
            test_case=test_case, mode_status_0=0, mode_status_1=flipped_mode,
            changed_mask_0=0, changed_mask_1=ModeStatus.ModeStatus1.Mask.POWER_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case, "Check the configured power mode")
        # --------------------------------------------------------------------------------------------------------------
        test_case.assertEqual(
            expected=flipped_mode,
            obtained=response.mode_status_1.power_mode,
            msg=f"The requested mode was not configured")
    # end def flip_hybrid_switch_mode
# end class ModeStatusTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
