#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.fninversionformultihostdevicesutils
:brief: Helpers for ``FnInversionForMultiHostDevices`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/04/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FLockChangeEvent
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevices
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevicesFactory
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import GetGlobalFnInversionResponse
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import SetGlobalFnInversionResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FnInversionForMultiHostDevicesTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``FnInversionForMultiHostDevices`` feature
    """

    class GetGlobalFnInversionResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetGlobalFnInversionResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetGlobalFnInversionResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES
            return {
                "host_index": (cls.check_host_index, None),
                "fn_inversion_state": (cls.check_fn_inversion_state, config.F_FnInversionDefaultState),
                "fn_inversion_default_state": (cls.check_fn_inversion_default_state, config.F_FnInversionDefaultState),
                "capabilities_mask_reserved_bits": (cls.check_capabilities_mask_reserved_bits, 0),
                "capabilities_mask_fn_lock": (cls.check_capabilities_mask_fn_lock, config.F_HasFnLock)
            }
        # end def get_default_check_map

        @staticmethod
        def check_host_index(test_case, response, expected):
            """
            Check host_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGlobalFnInversionResponse to check
            :type response: ``GetGlobalFnInversionResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert host_index that raise an exception
            """
            test_case.assertNotNone(
                expected, msg="HostIndex shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.host_index),
                msg="The host_index parameter differs "
                    f"(expected:{expected}, obtained:{response.host_index})")
        # end def check_host_index

        @staticmethod
        def check_fn_inversion_state(test_case, response, expected):
            """
            Check fn_inversion_state field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGlobalFnInversionResponse to check
            :type response: ``GetGlobalFnInversionResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert fn_inversion_state that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.fn_inversion_state),
                msg="The fn_inversion_state parameter differs "
                    f"(expected:{expected}, obtained:{response.fn_inversion_state})")
        # end def check_fn_inversion_state

        @staticmethod
        def check_fn_inversion_default_state(test_case, response, expected):
            """
            Check fn_inversion_default_state field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGlobalFnInversionResponse to check
            :type response: ``GetGlobalFnInversionResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert fn_inversion_default_state that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.fn_inversion_default_state),
                msg="The fn_inversion_default_state parameter differs "
                    f"(expected:{expected}, obtained:{response.fn_inversion_default_state})")
        # end def check_fn_inversion_default_state

        @staticmethod
        def check_capabilities_mask_reserved_bits(test_case, response, expected):
            """
            Check capabilities_mask_reserved_bits field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGlobalFnInversionResponse to check
            :type response: ``GetGlobalFnInversionResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert capabilities_mask_reserved_bits that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.capabilities_mask_reserved_bits),
                msg="The capabilities_mask_reserved_bits parameter differs "
                    f"(expected:{expected}, obtained:{response.capabilities_mask_reserved_bits})")
        # end def check_capabilities_mask_reserved_bits

        @staticmethod
        def check_capabilities_mask_fn_lock(test_case, response, expected):
            """
            Check capabilities_mask_fn_lock field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetGlobalFnInversionResponse to check
            :type response: ``GetGlobalFnInversionResponse``
            :param expected: Expected value
            :type expected: ``bool|HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.capabilities_mask_fn_lock),
                msg="The capabilities_mask_fn_lock parameter differs "
                    f"(expected:{expected}, obtained:{response.capabilities_mask_fn_lock})")
        # end def check_capabilities_mask_fn_lock
    # end class GetGlobalFnInversionResponseChecker

    class SetGlobalFnInversionResponseChecker(GetGlobalFnInversionResponseChecker):
        """
        Define Helper to check ``SetGlobalFnInversionResponse``
        """
        pass
    # end class SetGlobalFnInversionResponseChecker

    class FLockChangeEventChecker(GetGlobalFnInversionResponseChecker):
        """
        Define Helper to check ``FLockChangeEventChecker``
        """
        pass
    # end class FLockChangeEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=FnInversionForMultiHostDevices.FEATURE_ID,
                           factory=FnInversionForMultiHostDevicesFactory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_global_fn_inversion(cls, test_case, host_index, device_index=None, port_index=None):
            """
            Process ``GetGlobalFnInversion``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param host_index: Host Index
            :type host_index: ``int|HexList|FnInversionForMultiHostDevices.HostIndex``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetGlobalFnInversionResponse
            :rtype: ``GetGlobalFnInversionResponse``
            """
            feature_40a3_index, feature_40a3, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_40a3.get_global_fn_inversion_cls(
                device_index=device_index,
                feature_index=feature_40a3_index,
                host_index=HexList(host_index))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_40a3.get_global_fn_inversion_response_cls)
            return response
        # end def get_global_fn_inversion

        @classmethod
        def set_global_fn_inversion(cls, test_case, host_index, fn_inversion_state, device_index=None, port_index=None):
            """
            Process ``SetGlobalFnInversion``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param host_index: Host Index
            :type host_index: ``int|HexList|FnInversionForMultiHostDevices.HostIndex``
            :param fn_inversion_state: Fn Inversion State
            :type fn_inversion_state: ``int|HexList|FnInversionForMultiHostDevices.FnInversionState``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetGlobalFnInversionResponse
            :rtype: ``SetGlobalFnInversionResponse``
            """
            feature_40a3_index, feature_40a3, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_40a3.set_global_fn_inversion_cls(
                device_index=device_index,
                feature_index=feature_40a3_index,
                host_index=HexList(host_index),
                fn_inversion_state=HexList(fn_inversion_state))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_40a3.set_global_fn_inversion_response_cls)
            return response
        # end def set_global_fn_inversion

        @classmethod
        def f_lock_change_event(cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                check_first_message=True, allow_no_message=False, skip_error_message=False,
                                device_index=None, port_index=None):
            """
            Process ``FLockChangeEvent``: get notification from event queue

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
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: FLockChangeEvent
            :rtype: ``FLockChangeEvent``
            """
            _, feature_40a3, _, _ = cls.get_parameters(test_case, device_index=device_index, port_index=port_index)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_40a3.f_lock_change_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def f_lock_change_event
    # end class HIDppHelper

    @classmethod
    def restore_fn_inversion_to_default_for_all_hosts(cls, test_case):
        """
        Restore fn inversion state to default setting

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        nb_host = test_case.f.PRODUCT.DEVICE.F_NbHosts if test_case.f.PRODUCT.DEVICE.F_NbHosts > 0 else 1
        default_fn_inversion_state = \
            test_case.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_FnInversionDefaultState
        for host in range(nb_host):
            get_global_fn_inversion_resp = cls.HIDppHelper.get_global_fn_inversion(test_case, host)
            if default_fn_inversion_state != to_int(get_global_fn_inversion_resp.fn_inversion_state):
                cls.HIDppHelper.set_global_fn_inversion(test_case, host, default_fn_inversion_state)
            # end if
        # end for
    # end def restore_fn_inversion_to_default_for_all_hosts

    @classmethod
    def enable_fn_inversion(cls, test_case, host=FnInversionForMultiHostDevices.HostIndex.HOST1):
        """
        Enable fn inversion state

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param host: Host index - OPTIONAL
        :type host: ``FnInversionForMultiHostDevices.HostIndex``
        """
        get_global_fn_inversion_resp = cls.HIDppHelper.get_global_fn_inversion(test_case, host)
        if to_int(get_global_fn_inversion_resp.fn_inversion_state) == \
                FnInversionForMultiHostDevices.FnInversionState.ON:
            cls.HIDppHelper.set_global_fn_inversion(test_case, host, FnInversionForMultiHostDevices.FnInversionState.ON)
        # end if
    # end def enable_fn_inversion

    @classmethod
    def restore_fn_inversion(cls, test_case, host=0):
        """
        Restore fn inversion to default setting

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param host: Host index - OPTIONAL
        :type host: ``int``
        """
        default_fn_inversion_state = \
            test_case.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_FnInversionDefaultState
        get_global_fn_inversion_resp = cls.HIDppHelper.get_global_fn_inversion(test_case, host)
        if default_fn_inversion_state != to_int(get_global_fn_inversion_resp.fn_inversion_state):
            cls.HIDppHelper.set_global_fn_inversion(test_case, host, default_fn_inversion_state)
        # end if
    # end def restore_fn_inversion
# end class FnInversionForMultiHostDevicesTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
