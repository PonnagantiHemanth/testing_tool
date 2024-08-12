#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.devicetypeandnameutils
:brief: Helpers for DeviceTypeAndName feature
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/03/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndName
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameFactory
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceTypeAndNameTestUtils(object):
    """
    This class provides helpers for common checks on DeviceTypeAndName feature
    """
    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=DeviceTypeAndName.FEATURE_ID, factory=DeviceTypeAndNameFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_device_name_count(cls, test_case, device_index=None, port_index=None):
            """
            Get Device Name Count

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: device name count response
            :rtype: ``GetDeviceNameCountResponse``
            """
            feature_0005_index, feature_0005, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            # ---------------------------------------------------------
            LogHelper.log_info(test_case, "Send GetDeviceNameCount request")
            # ---------------------------------------------------------
            report = feature_0005.get_device_name_count_cls(device_index=device_index, feature_index=feature_0005_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_0005.get_device_name_count_response_cls
            )

            return response
        # end def get_device_name_count

        @classmethod
        def get_device_name(cls, test_case, char_index, device_index=None, port_index=None):
            """
            Get device name

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param char_index: Char Index
            :type char_index: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: device name response
            :rtype: ``GetDeviceNameResponse``
            """
            feature_0005_index, feature_0005, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            # ---------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"Send GetDeviceName request with char_index:{char_index}")
            # ---------------------------------------------------------------------------------------
            report = feature_0005.get_device_name_cls(
                device_index=device_index, feature_index=feature_0005_index, char_index=HexList(char_index))

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_0005.get_device_name_response_cls)

            return response
        # end def get_device_name

        @classmethod
        def get_full_device_name(cls, test_case, device_name_max_count):
            """
            Get full device name

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_name_max_count: device name size
            :type device_name_max_count: ``int``

            :return: device full name
            :rtype: ``str``
            """
            _, feature_0005, _, _ = cls.get_parameters(test_case)
            # ------------------------------------------------------------------------
            LogHelper.log_step(test_case, "send GetDeviceName to read all characters")
            # ------------------------------------------------------------------------
            size = feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME // 8
            (q, r) = divmod(device_name_max_count, size)

            full_name = ""
            for index in range(q):
                output_value = ascii_converter(cls.get_device_name(test_case, char_index=(index * size)).device_name)
                full_name = f"{full_name}{output_value}"
            # end for
            if r > 0:
                output_value = ascii_converter(cls.get_device_name(test_case, char_index=(q * size)).device_name)
                full_name = f"{full_name}{output_value}"
            # end if

            return full_name
        # end def get_full_device_name

        @classmethod
        def get_device_type(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetDeviceType``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetDeviceTypeResponse
            :rtype: ``GetDeviceTypeResponse``
            """
            feature_0005_index, feature_0005, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0005.get_device_type_cls(
                device_index=device_index,
                feature_index=feature_0005_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_0005.get_device_type_response_cls)
            return response
        # end def get_device_type
    # end class HIDppHelper
# end class DeviceTypeAndNameTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
