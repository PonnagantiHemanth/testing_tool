#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.configurabledevicepropertiesutils
:brief: Helpers for ConfigurableDeviceProperties feature
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/02/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep
from warnings import warn

from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDeviceProperties
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesFactory
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigurableDevicePropertiesTestUtils(object):
    """
    This class provides helpers for common checks on ConfigurableDeviceProperties feature
    """
    class GetDeviceNameMaxCountHelper(object):
        """
        GetDeviceNameMaxCount helper
        """
        class MessageChecker(CommonBaseTestUtils.MessageChecker):
            """
            GetDeviceNameMaxCount MessageChecker
            """
            @classmethod
            def get_default_check_map(cls, test_case):
                """
                Get the default check methods and expected values for the GetDeviceNameMaxCount API

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``

                :return: Default check map
                :rtype: ``dict``
                """
                v = test_case.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_DEVICE_PROPERTIES
                return {
                        "device_name_max_count": (cls.check_device_name_max_count, v.F_DeviceNameMaxCount),
                }
            # end def get_default_check_map

            @staticmethod
            def check_device_name_max_count(test_case, response, expected):
                """
                Check device_name_max_count field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: GetDeviceNameMaxCountResponse to check
                :type response: ``GetDeviceNameMaxCountResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                value = int(Numeral(response.device_name_max_count))
                max_value = int(Numeral(expected))

                # -------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate deviceNameMaxCount ({value} == {max_value})")
                # -------------------------------------------------------------------------------------
                test_case.assertEqual(expected=max_value, obtained=value,
                                      msg="The device_name_max_count parameter differs from the one expected")
            # end def check_device_name_max_count
        # end class MessageChecker

        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            GetDeviceNameMaxCount HIDppHelper
            """
            @classmethod
            def read(cls, test_case):
                """
                Process GetDeviceNameMaxCount

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``

                :return: GetDeviceNameMaxCountResponse
                :rtype: ``GetDeviceNameMaxCountResponse``
                """
                # -----------------------------------------------------------------
                LogHelper.log_step(test_case, "Send GetDeviceNameMaxCount request")
                # -----------------------------------------------------------------
                report = test_case.feature_1806.get_device_name_max_count_cls(
                        test_case.deviceIndex, test_case.feature_1806_index)
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_1806.get_device_name_max_count_response_cls)
                return response
            # end def read
        # end class HIDppHelper
    # end class GetDeviceNameMaxCountHelper

    class SetDeviceNameHelper(object):
        """
        SetDeviceName helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            SetDeviceName HIDppHelper
            """
            @classmethod
            def write(cls, test_case, char_index, device_name):
                """
                Process SetDeviceName

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param char_index: parameter index
                :type char_index: ``int`` or ``HexList``
                :param device_name: device name
                :type device_name: ``str`` or ``HexList``

                :return: SetDeviceNameResponse
                :rtype: ``SetDeviceNameResponse``
                """
                # -------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case,
                                   f"Send SetDeviceName request with char_index:{char_index} & name:{device_name}")
                # -------------------------------------------------------------------------------------------------
                if isinstance(device_name, str):
                    # Note: When string is directly passed, it throws error
                    # pylibrary.tools.hexlist.HexListError: Odd-length string
                    # Because, every character should be of equal size.
                    # string.encode() will convert to bytes which is of size 2 per char.
                    device_name = device_name.encode()
                # end if
                report = test_case.feature_1806.set_device_name_cls(
                        test_case.deviceIndex, test_case.feature_1806_index,
                        HexList(char_index), HexList(device_name))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_1806.set_device_name_response_cls)
                return response
            # end def write
        # end class HIDppHelper
    # end class SetDeviceNameHelper

    class SetDeviceNameCommitHelper(object):
        """
        SetDeviceNameCommit helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            SetDeviceNameCommit HIDppHelper
            """
            @classmethod
            def write(cls, test_case, length):
                """
                Process SetDeviceNameCommit

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param length: length of device name
                :type length: ``int`` or ``HexList``

                :return: SetDeviceNameCommitResponse
                :rtype: ``SetDeviceNameCommitResponse``
                """
                # -------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f"Send SetDeviceNameCommit request with length:{length}")
                # -------------------------------------------------------------------------------------
                report = test_case.feature_1806.set_device_name_commit_cls(
                        test_case.deviceIndex, test_case.feature_1806_index, HexList(length))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_1806.set_device_name_commit_response_cls)
                return response
            # end def write

            @classmethod
            def write_with_wrong_length(cls, test_case, length):
                """
                Process SetDeviceNameCommit

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param length: length of device name
                :type length: ``int`` or ``HexList``
                """
                # -------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f"Send SetDeviceNameCommit request with wrong length:{length}")
                # -------------------------------------------------------------------------------------------
                report = test_case.feature_1806.set_device_name_commit_cls(
                        test_case.deviceIndex, test_case.feature_1806_index, HexList(length))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_1806.set_device_name_commit_response_cls)

                # ------------------------------------------------------------
                LogHelper.log_check(test_case, "Validate successful response")
                # ------------------------------------------------------------
                test_case.assertEqual(obtained=response.padding,
                                      expected=HexList("00" * 16),
                                      msg="The padding parameter differs from the one expected")
            # end def write_with_wrong_length
        # end class HIDppHelper
    # end class SetDeviceNameCommitHelper

    class SetDeviceExtendModelIDHelper(object):
        """
        SetDeviceExtendModelID helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            SetDeviceExtendModelID HIDppHelper
            """
            @classmethod
            def write(cls, test_case, extended_model_id):
                """
                Process SetDeviceExtendModelID

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param extended_model_id: extended model id
                :type extended_model_id: ``int`` or ``HexList``

                :return: SetDeviceExtendModelIDResponse
                :rtype: ``SetDeviceExtendModelIDResponse``
                """
                # ---------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                        test_case, f"Send SetDeviceExtendModelID request with extended_model_id:{extended_model_id}")
                # ---------------------------------------------------------------------------------------------------
                report = test_case.feature_1806.set_device_extended_model_id_cls(
                        test_case.deviceIndex, test_case.feature_1806_index, HexList(extended_model_id))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_1806.set_device_extended_model_id_response_cls)
                return response
            # end def write

            @classmethod
            def read(cls, test_case, extended_model_id):
                """
                Read SetDeviceExtendModelID using feature 0003.

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param extended_model_id: extended model id
                :type extended_model_id: ``int`` or ``HexList``

                :return: device extend model id
                :rtype: ``int``
                """
                # ---------------------------------------------------------
                LogHelper.log_step(test_case, "Send GetDeviceInfo request")
                # ---------------------------------------------------------
                get_device_info_report = test_case.feature_1806.get_device_info_cls(
                        test_case.deviceIndex, test_case.feature_0003_index)

                test_case.send_report_wait_response(
                        report=get_device_info_report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_1806.get_device_info_response_cls)

                # ----------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, "Wait for GetDeviceInfo response and check product-specific constants")
                # ----------------------------------------------------------------------------------------------------

                # ---------------------------------------------------------
                LogHelper.log_step(test_case, "Send GetDeviceInfo request")
                # ---------------------------------------------------------
                report = test_case.feature_1806.set_device_extend_model_id_cls(
                        test_case.deviceIndex, test_case.feature_1806_index, HexList(extended_model_id))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_1806.set_device_extend_model_id_response_cls)
                return response
            # end def read
        # end class HIDppHelper
    # end class SetDeviceExtendModelIDHelper

    class SetDevicePropertiesHelper(object):
        """
        SetDeviceProperties helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            SetDeviceProperties HIDppHelper
            """
            @classmethod
            def write(cls, test_case, property_id, flag, sub_data_index, property_data):
                """
                Process SetDeviceProperties

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param property_id: property id
                :type property_id: ``int`` or ``HexList``
                :param flag: flag
                :type flag: ``int`` or ``HexList``
                :param sub_data_index: sub data index
                :type sub_data_index: ``int`` or ``HexList``
                :param property_data: property data
                :type property_data: ``int`` or ``str`` or ``HexList``

                :return: SetDevicePropertiesResponse
                :rtype: ``SetDevicePropertiesResponse``
                """
                # ---------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                        test_case, f"Send SetDeviceProperties request with property_id:{property_id}, flag:{flag}, "
                                   f"sub_data_index:{sub_data_index} & property_data:{property_data}")
                # ---------------------------------------------------------------------------------------------------
                if isinstance(property_data, str):
                    # Note: When string is directly passed, it throws error
                    # pylibrary.tools.hexlist.HexListError: Odd-length string
                    # Because, every character should be of equal size.
                    # string.encode() will convert to bytes which is of size 2 per char.
                    property_data = property_data.encode()
                # end if
                report = test_case.feature_1806.set_device_properties_cls(
                        test_case.deviceIndex, test_case.feature_1806_index,
                        HexList(property_id), flag,
                        sub_data_index, HexList(property_data))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_1806.set_device_properties_response_cls)
                return response
            # end def write

            @classmethod
            def write_with_invalid_argument(cls, test_case, property_id, flag, sub_data_index, property_data):
                """
                Process SetDeviceProperties

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param property_id: property id
                :type property_id:``int`` or ``HexList``
                :param flag: flag
                :type flag:``int`` or ``HexList``
                :param sub_data_index: sub data index
                :type sub_data_index: ``int`` or ``HexList``
                :param property_data: property data
                :type property_data: ``int`` or ``str`` or ``HexList``
                """
                # --------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                        test_case, f"Send SetDeviceProperties request with property_id:{property_id}, flag:{flag}, "
                                   f"sub_data_index:{sub_data_index} & property_data:{property_data}")
                # --------------------------------------------------------------------------------------------------
                if isinstance(property_data, str):
                    # Note: When string is directly passed, it throws error
                    # pylibrary.tools.hexlist.HexListError: Odd-length string
                    # Because, every character should be of equal size.
                    # string.encode() will convert to bytes which is of size 2 per char.
                    property_data = property_data.encode()
                # end if
                report = test_case.feature_1806.set_device_properties_cls(
                        test_case.deviceIndex, test_case.feature_1806_index, HexList(property_id), flag,
                        sub_data_index, HexList(property_data))
                error_response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.error_message_queue,
                        response_class_type=ErrorCodes)
                # ----------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate error code:{ErrorCodes.INVALID_ARGUMENT}")
                # ----------------------------------------------------------------------------------
                test_case.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                                      expected=ErrorCodes.INVALID_ARGUMENT,
                                      msg="The error_code parameter differs from the one expected")
            # end def write_with_invalid_argument
        # end class HIDppHelper
    # end class SetDevicePropertiesHelper

    class GetDevicePropertiesHelper(object):
        """
        GetDeviceProperties helper
        """
        class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
            """
            GetDeviceProperties HIDppHelper
            """
            @classmethod
            def get_parameters(cls, test_case,
                               feature_id=ConfigurableDeviceProperties.FEATURE_ID,
                               factory=ConfigurableDevicePropertiesFactory,
                               device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
                # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
                return super().get_parameters(
                    test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
            # end def get_parameters

            @classmethod
            def read(cls, test_case, property_id, flag, sub_data_index):
                """
                Process GetDeviceProperties

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param property_id: property id
                :type property_id: ``int`` or ``HexList``
                :param flag: flag
                :type flag: ``int`` or ``HexList``
                :param sub_data_index: sub data index
                :type sub_data_index: ``int`` or ``HexList``

                :return: GetDevicePropertiesResponse
                :rtype: ``GetDevicePropertiesResponse``
                """
                feature_1806_index, feature_1806, device_index, _ = cls.get_parameters(test_case)
                # ---------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                        test_case, f"Send GetDeviceProperties request with property_id:{property_id} flag:{flag} "
                                   f"sub_data_index:{sub_data_index}")
                # ---------------------------------------------------------------------------------------------------
                report = feature_1806.get_device_properties_cls(
                        device_index, feature_1806_index, HexList(property_id), flag, sub_data_index)
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=feature_1806.get_device_properties_response_cls)
                return response
            # end def read

            @classmethod
            def read_with_invalid_argument(cls, test_case, property_id, flag, sub_data_index):
                """
                Process GetDeviceProperties

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param property_id: property id
                :type property_id: ``int`` or ``HexList``
                :param flag: flag
                :type flag: ``int`` or ``HexList``
                :param sub_data_index: sub data index
                :type sub_data_index: ``int`` or ``HexList``
                """
                # ----------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                        test_case, f"Send GetDeviceProperties request with property_id:{property_id}, flag:{flag} & "
                                   f"sub_data_index:{sub_data_index}")
                # ----------------------------------------------------------------------------------------------------
                report = test_case.feature_1806.get_device_properties_cls(
                        test_case.deviceIndex, test_case.feature_1806_index, HexList(property_id),
                        flag, sub_data_index)
                error_response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.error_message_queue,
                        response_class_type=ErrorCodes)
                # ------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate error code:{ErrorCodes.INVALID_ARGUMENT}")
                # ------------------------------------------------------------------------------------------------
                test_case.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                                      expected=ErrorCodes.INVALID_ARGUMENT,
                                      msg="The error_code parameter differs from the one expected")
            # end def read_with_invalid_argument
        # end class HIDppHelper
    # end class GetDevicePropertiesHelper

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=ConfigurableDeviceProperties.FEATURE_ID,
                           factory=ConfigurableDevicePropertiesFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def force_device_reset_and_activate_features(cls, test_case):
            """
            Perform force device reset with the help of 0x1802 and activate hidden feature after reset

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: None
            :rtype: ``None``
            """
            # ---------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Reset the device using feature x1802")
            # ---------------------------------------------------------------------------------
            test_case.set_feature_1802()
            force_device_reset = ForceDeviceReset(deviceIndex=test_case.deviceIndex,
                                                  featureId=test_case.feature_1802_index)
            test_case.send_report_to_device(report=force_device_reset)

            # Wait DUT to complete reset procedure
            # It seems that in Unifying it is not happening.
            # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
            #  interesting to investigate a better solution
            if not isinstance(test_case.current_channel, ThroughEQuadReceiverChannel):
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=test_case)
            # end if

            # ------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "After reset, once again enable manufacturing features")
            # ------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(test_case, manufacturing=True)
        # end def force_device_reset_and_activate_features

        @classmethod
        def power_device_reset_and_activate_features(cls, test_case):
            """
            Perform force device reset with the help of power supply and activate hidden feature after reset

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: None
            :rtype: ``None``
            """
            # ------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Reset the device using power supply board")
            # ------------------------------------------------------------------------
            test_case.reset(LinkEnablerInfo.HID_PP_MASK, hardware_reset=True, recover_time_needed=True)
            sleep(2)

            # ------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "After reset, once again enable manufacturing features")
            # ------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(test_case, manufacturing=True)
        # end def power_device_reset_and_activate_features

        @classmethod
        def validate_supported_property_ids(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate the supported property ids

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            pid = ConfigurableDeviceProperties.PropertyIdV8
            _formatter_map = {
                    pid.EXTENDED_MODEL_ID: cls.validate_property_id_1,
                    pid.KEYBOARD_INTERNATIONAL_LAYOUT: cls.validate_property_id_2,
                    pid.RGB_LEDBIN_INFORMATION_BACKUP_ZONE0: cls.validate_property_id_3,
                    pid.RGB_LEDBIN_INFORMATION_BACKUP_ZONE1: cls.validate_property_id_4,
                    pid.EQUAD_SHORT_NAME: cls.validate_property_id_5,
                    pid.BLE_SHORT_NAME: cls.validate_property_id_6,
                    pid.BLE_AD_SERVICE_DATA: cls.validate_property_id_7,
                    pid.BLE_AD_TX_OUTPUT_POWER_DBM: cls.validate_property_id_8,
                    pid.RGB_LEDBIN_INFORMATION_BACKUP_ZONE2: cls.validate_property_id_9,
                    pid.BLE_LONG_NAME: cls.validate_property_id_10,
                    pid.SERIAL_NUMBER: cls.validate_property_id_11,
                    pid.CAR_SIMULATOR_PEDALS_TYPES: cls.validate_property_id_12,
            }

            for property_id in test_case.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_DEVICE_PROPERTIES.F_SupportedPropertyIds:
                if property_id is None or property_id == "":
                    continue
                # end if
                _formatter_map[int(property_id)](test_case, device_reset, read_by_other_feature)
            # end for
        # end def validate_supported_property_ids

        @classmethod
        def validate_property_id_1(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 1 (EXTENDED_MODEL_ID)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            max_size = 1
            property_id = ConfigurableDeviceProperties.PropertyIdV8.EXTENDED_MODEL_ID
            flag = 0
            sub_data_index = 0
            property_data = RandHexList(max_size)

            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            if read_by_other_feature:
                # -----------------------------------------------------------------------------
                LogHelper.log_step(test_case, "Send GetDeviceInfo request")
                # -----------------------------------------------------------------------------
                output_value = DeviceInformationTestUtils.HIDppHelper.get_extended_model_id(test_case)
                # -----------------------------------------------------------------------------
                LogHelper.log_check(
                        test_case, f"Validate SetDeviceProperties.data ({property_data})"
                                   f" == DeviceInformation.extended_model_id ({output_value})")
                # -----------------------------------------------------------------------------
                test_case.assertEqual(expected=HexList(property_data),
                                      obtained=output_value,
                                      msg="The extended model id obtained is not as expected")
            # end if
        # end def validate_property_id_1

        @classmethod
        def validate_property_id_2(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 2 (KEYBOARD_INTERNATIONAL_LAYOUT)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            max_size = 1
            property_id = ConfigurableDeviceProperties.PropertyIdV8.KEYBOARD_INTERNATIONAL_LAYOUT
            flag = 0
            sub_data_index = 0
            property_data = RandHexList(max_size)

            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            if read_by_other_feature:
                # TODO: (Suresh Thiyagarajan) Read the feature
                pass
            # end if
        # end def validate_property_id_2

        @classmethod
        def validate_property_id_3(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 3 (RGB_LEDBIN_INFORMATION_BACKUP_ZONE0)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            property_id = ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE0
            max_size = 64
            size = 14
            (q, r) = divmod(max_size, size)
            for i in range(q):
                flag = 1
                sub_data_index = i * q
                property_data = RandHexList(size)

                cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index,
                                                  property_data, device_reset)
            # end for

            if r > 0:
                flag = 1
                sub_data_index = q * size
                property_data = RandHexList(r)
                cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index,
                                                  property_data, device_reset)
            # end if

            if read_by_other_feature:
                # TODO: (Suresh Thiyagarajan) Read the feature
                pass
            # end if
        # end def validate_property_id_3

        @classmethod
        def validate_property_id_4(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 4(RGB_LEDBIN_INFORMATION_BACKUP_ZONE1)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            property_id = ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE1
            max_size = 64
            size = 14
            (q, r) = divmod(max_size, size)
            for i in range(q):
                flag = 1
                sub_data_index = i * q
                property_data = RandHexList(size)

                cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index,
                                                  property_data, device_reset)
            # end for

            if r > 0:
                flag = 1
                sub_data_index = q * size
                property_data = RandHexList(r)
                cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index,
                                                  property_data, device_reset)
            # end if

            if read_by_other_feature:
                # TODO: (Suresh Thiyagarajan) Read the feature
                pass
            # end if
        # end def validate_property_id_4

        @classmethod
        def validate_property_id_5(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 5 (EQUAD_SHORT_NAME)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            property_id = ConfigurableDeviceProperties.PropertyIdV8.EQUAD_SHORT_NAME
            flag = 0
            sub_data_index = 0
            property_data = "EquadShortName"

            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            if read_by_other_feature:
                # TODO: (Suresh Thiyagarajan) Read the feature
                pass
            # end if
        # end def validate_property_id_5

        @classmethod
        def validate_property_id_6(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 6 (BLE_SHORT_NAME)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            property_id = ConfigurableDeviceProperties.PropertyIdV8.BLE_SHORT_NAME
            flag = 0
            sub_data_index = 0
            property_data = "BLE_SHORT_NAME"

            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            if read_by_other_feature:
                test_case.set_feature_0007()

                response = DeviceFriendlyNameTestUtils.GetFriendlyNameLenHelper.get_friendly_name_len(test_case)
                output_value = DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.get_full_name(
                        test_case, response.name_len)

                # ------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                        test_case,
                        f"Validate SetDeviceProperties ({property_data}) == DeviceFriendlyName ({output_value})")
                # ------------------------------------------------------------------------------------------------
                test_case.assertEqual(expected=property_data,
                                      obtained=output_value,
                                      msg="The extended model id obtained is not as expected")
                # end if
            # end if
        # end def validate_property_id_6

        @classmethod
        def validate_property_id_7(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 7 (BLE_AD_SERVICE_DATA)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            max_size = 14
            property_id = ConfigurableDeviceProperties.PropertyIdV8.BLE_AD_SERVICE_DATA
            flag = 0
            sub_data_index = 0
            property_data = RandHexList(max_size)

            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            if read_by_other_feature:
                # TODO: (Suresh Thiyagarajan) Read the feature
                pass
            # end if
        # end def validate_property_id_7

        @classmethod
        def validate_property_id_8(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 8 (BLE_AD_TX_OUTPUT_POWER_DBM)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            max_size = 1
            property_id = ConfigurableDeviceProperties.PropertyIdV8.BLE_AD_TX_OUTPUT_POWER_DBM
            flag = 0
            sub_data_index = 0
            property_data = RandHexList(max_size)

            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            if read_by_other_feature:
                # TODO: (Suresh Thiyagarajan) Read the feature
                pass
            # end if
        # end def validate_property_id_8

        @classmethod
        def validate_property_id_9(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 9 (RGB_LEDBIN_INFORMATION_BACKUP_ZONE2)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            property_id = ConfigurableDeviceProperties.PropertyIdV8.RGB_LEDBIN_INFORMATION_BACKUP_ZONE2
            max_size = 64
            size = 14
            (q, r) = divmod(max_size, size)
            for i in range(q):
                flag = 1
                sub_data_index = i * q
                property_data = RandHexList(size)

                cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index,
                                                  property_data, device_reset)
            # end for

            if r > 0:
                flag = 1
                sub_data_index = q * size
                property_data = RandHexList(r)
                cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index,
                                                  property_data, device_reset)
            # end if

            if read_by_other_feature:
                # TODO: (Suresh Thiyagarajan) Read the feature
                pass
            # end if
        # end def validate_property_id_9

        @classmethod
        def validate_property_id_10(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 10 (BLE_LONG_NAME)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            property_id = ConfigurableDeviceProperties.PropertyIdV8.BLE_LONG_NAME
            size = 14
            name = "BLE_LONG_NAME_TEST"
            flag = 1
            sub_data_index = 0
            property_data = name[0:size]
            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            sub_data_index = size
            property_data = name[size:]
            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            if read_by_other_feature:
                test_case.set_feature_0007()

                response = DeviceFriendlyNameTestUtils.GetFriendlyNameLenHelper.get_friendly_name_len(test_case)
                output_value = DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.get_full_name(
                        test_case, response.name_len)

                # --------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                        test_case, f"Validate SetDeviceProperties ({name}) == DeviceFriendlyName ({output_value})")
                # --------------------------------------------------------------------------------------------------
                test_case.assertEqual(expected=name,
                                      obtained=output_value,
                                      msg="The extended model id obtained is not as expected")
                # end if
            # end if
        # end def validate_property_id_10

        @classmethod
        def validate_property_id_11(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 11 (SERIAL_NUMBER)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            property_id = ConfigurableDeviceProperties.PropertyIdV7.SERIAL_NUMBER
            flag = 0
            sub_data_index = 0
            property_data = "123456789CBA"

            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            if read_by_other_feature:
                # -------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, "Send GetDeviceSerialNumber request")
                # -------------------------------------------------------------------------------------
                output_value = DeviceInformationTestUtils.HIDppHelper.get_device_serial_number(test_case)
                # -----------------------------------------------------------------------------
                LogHelper.log_check(
                        test_case, f"Validate SetDeviceProperties.data ({property_data})"
                                   f" == DeviceInformation.serial_number ({output_value})")
                # -----------------------------------------------------------------------------
                if isinstance(property_data, str):
                    # Note: When string is directly passed, it throws error
                    # pylibrary.tools.hexlist.HexListError: Odd-length string
                    # Because, every character should be of equal size.
                    # string.encode() will convert to bytes which is of size 2 per char.
                    property_data = property_data.encode()
                # end if
                test_case.assertEqual(expected=HexList(property_data),
                                      obtained=output_value,
                                      msg="The serial number obtained is not as expected")
            # end if
        # end def validate_property_id_11

        @classmethod
        def validate_property_id_12(cls, test_case, device_reset=None, read_by_other_feature=False):
            """
            Validate property id 12 (CAR_SIMULATOR_PEDALS_TYPES)

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            :param read_by_other_feature: value to read the data using other feature - Optional
            :type read_by_other_feature: ``bool``
            """
            max_size = 3
            property_id = ConfigurableDeviceProperties.PropertyIdV8.CAR_SIMULATOR_PEDALS_TYPES
            flag = 0
            sub_data_index = 0
            property_data = RandHexList(max_size)

            cls.validate_property_set_and_get(test_case, property_id, flag, sub_data_index, property_data, device_reset)

            if read_by_other_feature:
                # TODO: (Suresh Thiyagarajan) Read the feature
                pass
            # end if
        # end def validate_property_id_12

        @classmethod
        def validate_property_set_and_get(cls, test_case, property_id, flag, sub_data_index,
                                          property_data, device_reset=None):
            """
            Process SetDeviceProperties & GetDeviceProperties

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param property_id: property id
            :type property_id: ``int`` or ``HexList``
            :param flag: flag
            :type flag: ``int`` or ``HexList``
            :param sub_data_index: sub data index
            :type sub_data_index: ``int`` or ``HexList``
            :param property_data: property data
            :type property_data: ``int`` or ``str`` or ``HexList``
            :param device_reset: value to reset the device - Optional
            :type device_reset: ``str`` or ``None``
            """
            ConfigurableDevicePropertiesTestUtils.SetDevicePropertiesHelper.HIDppHelper.write(
                    test_case,
                    property_id=property_id,
                    flag=flag,
                    sub_data_index=sub_data_index,
                    property_data=property_data)

            if device_reset == "byFeature":
                ConfigurableDevicePropertiesTestUtils.HIDppHelper.force_device_reset_and_activate_features(test_case)
            elif device_reset == "byPowerSupply":
                ConfigurableDevicePropertiesTestUtils.HIDppHelper.power_device_reset_and_activate_features(test_case)
            # end if

            # -----------------------------------------------------------------------------------------
            LogHelper.log_step(
                    test_case, f"Send GetDeviceProperties request with property_id:{property_id}"
                               f" flag:{flag} & sub_data_index:{sub_data_index}")
            # -----------------------------------------------------------------------------------------
            response = ConfigurableDevicePropertiesTestUtils.GetDevicePropertiesHelper.HIDppHelper.read(
                    test_case,
                    property_id=property_id,
                    flag=flag,
                    sub_data_index=sub_data_index)

            # -----------------------------------------------------------------------------
            LogHelper.log_check(
                    test_case, f"Validate SetDeviceProperties.data ({property_data})"
                               f" == GetDeviceProperties.data ({response.property_data})")
            # -----------------------------------------------------------------------------
            if isinstance(property_data, str):
                # Note: When string is directly passed, it throws error
                # pylibrary.tools.hexlist.HexListError: Odd-length string
                # Because, every character should be of equal size.
                # string.encode() will convert to bytes which is of size 2 per char.
                property_data = property_data.encode()
            # end if
            test_case.assertEqual(expected=HexList(property_data),
                                  obtained=response.property_data,
                                  msg="The property_data is different the one expected")
        # end def validate_property_set_and_get
    # end class HIDppHelper

    class NvsHelper(object):
        """
        Non Volatile Storage helper
        """

        @classmethod
        def validate_nvs_chunk(cls, test_case):
            """
            Check NVS device tde chunk content.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            """
            if test_case.memory_manager is None:
                # No memory manager for this device
                return None
            # end if
            # Dump receiver NVS
            test_case.memory_manager.read_nvs()
            # Extract TDE chunks
            chunks = test_case.memory_manager.get_chunks_by_name("NVS_CONF_DEV_PROP_ID")
            chunk_size = len(chunks)
            if chunk_size == 0:
                warn("No CONF_DEV_PROP chunk found")
                return None
            # end if
            for i in range(chunk_size):
                if i == 0:
                    continue
                # end if
                if i + 1 == chunk_size:
                    break
                # end if
                test_case.assertNotEqual(
                        unexpected=chunks[i],
                        obtained=chunks[i + 1],
                        msg=f"The previous chunk ({i}) and current chunk ({i + 1}) are same ({chunks[i]})")
            # end for
            return True
        # end def validate_nvs_chunk
    # end class NvsHelper
# end class ConfigurableDevicePropertiesTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
