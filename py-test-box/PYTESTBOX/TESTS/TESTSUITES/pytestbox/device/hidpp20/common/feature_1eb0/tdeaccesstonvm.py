#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1eb0.tdeaccesstonvm
:brief: Validate HID++ 2.0 ``TdeAccessToNvm`` feature
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/07/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvm
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.tdeaccesstonvmutils import TdeAccessToNvmTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TdeAccessToNvmTestCase(DeviceBaseTestCase):
    """
    Validate ``TdeAccessToNvm`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1EB0 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1eb0_index, self.feature_1eb0, _, _ = TdeAccessToNvmTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.COMMON.TDE_ACCESS_TO_NVM
        self.tde_buffer_size = self.config.F_TdeBufferSize
        self.starting_position = self.config.F_TdeStartingPosition
        self.tde_max_size = self.config.F_TdeMaxSize
    # end def setUp

    @staticmethod
    def get_read_parameters(err_code=None, expected=None):
        """
        Get the read api parameters

        :param err_code: error code on read api - OPTIONAL
        :type err_code: ``int``
        :param expected: read response value - OPTIONAL
        :type expected: ``list``

        :return: read parameters
        :rtype: ``dict``
        """
        if not expected and not err_code:
            expected = [0] * (TdeAccessToNvm.MAX_PACKET_SIZE + 2)
        # end if
        return dict(response=dict(error_code=err_code, expected=expected))
    # end def get_read_parameters

    @staticmethod
    def get_write_parameters(err_code=None, payload=None):
        """
        Get write api parameters

        :param err_code: error code on read api - OPTIONAL
        :type err_code: ``int``
        :param payload: read response value - OPTIONAL
        :type payload: ``list``

        :return: read parameters
        :rtype: ``dict``
        """
        if not payload:
            payload = RandHexList(TdeAccessToNvm.MAX_PACKET_SIZE)
        # end if
        return dict(response=dict(error_code=err_code), payload=payload)
    # end def get_write_parameters

    def get_parameters(self, starting_position=None,
                       number_of_bytes=0x01,
                       write_dict=None,
                       read_dict=None):
        """
        Get default parameters for read/write/clear tde api

        :param starting_position: starting position of data byte - OPTIONAL
        :type starting_position: ``int`` or ``HexList``
        :param number_of_bytes: number of bytes to read/write - OPTIONAL
        :type number_of_bytes: ``int`` or ``HexList``
        :param write_dict: write api params - OPTIONAL
        :type write_dict: ``dict``
        :param read_dict: read api params - OPTIONAL
        :type read_dict: ``dict``

        :return: default values
        :rtype: ``dict``
        """
        if starting_position is None:
            if self.starting_position is None:
                starting_position = 0x00
            else:
                starting_position = self.starting_position
            # end if
        # end if
        if write_dict:
            write_dict["starting_position"] = starting_position
            write_dict["number_of_bytes"] = number_of_bytes
        # end if
        if read_dict:
            read_dict["starting_position"] = starting_position
            read_dict["number_of_bytes"] = number_of_bytes
            if not read_dict["response"]["error_code"]:
                # what is written is expected back
                read_dict["response"]["expected"][0] = starting_position
                read_dict["response"]["expected"][1] = number_of_bytes
                for i in range(number_of_bytes):
                    read_dict["response"]["expected"][i + 2] = write_dict["payload"][i]
                # end for
            # end if
        # end if

        params = dict(
            write=write_dict,
            read=read_dict
        )

        return params
    # end def get_parameters

    def process_api(self, params):
        """
        Process the api based on params

        :param params: parameters
        :type params: ``dict``

        :return: None
        """
        if params["write"]:
            payload = params["write"]["payload"]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send TdeWriteData (sp = {HexList(params["write"]["starting_position"])}) '
                                     f'(nb = {HexList(params["write"]["number_of_bytes"])}) (payload = {payload})')
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1eb0.tde_write_data_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1eb0_index,
                starting_position=HexList(params["write"]["starting_position"]),
                number_of_bytes_to_read_or_write=HexList(params["write"]["number_of_bytes"]),
                data_byte_0=HexList(payload[0]),
                data_byte_1=HexList(payload[1]),
                data_byte_2=HexList(payload[2]),
                data_byte_3=HexList(payload[3]),
                data_byte_4=HexList(payload[4]),
                data_byte_5=HexList(payload[5]),
                data_byte_6=HexList(payload[6]),
                data_byte_7=HexList(payload[7]),
                data_byte_8=HexList(payload[8]),
                data_byte_9=HexList(payload[9]),
                data_byte_10=HexList(payload[10]),
                data_byte_11=HexList(payload[11]),
                data_byte_12=HexList(payload[12]),
                data_byte_13=HexList(payload[13])
            )
            if params["write"]["response"]["error_code"]:
                TdeAccessToNvmTestUtils.HIDppHelper.send_report_wait_error(
                    test_case=self,
                    report=report,
                    error_codes=[params["write"]["response"]["error_code"]])
            else:
                ChannelUtils.send(
                    test_case=self,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=self.feature_1eb0.tde_write_data_response_cls)
            # end if
        # end if

        if "clear_api" in params:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send TdeClearData to delete TDE memory")
            # ----------------------------------------------------------------------------------------------------------
            response = TdeAccessToNvmTestUtils.HIDppHelper.tde_clear_data(self)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check TdeClearData fields")
            # ------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1eb0.tde_clear_data_response_cls, {})

        # end if

        if ("device_reset_by_feature_1802" in params) or ("device_reset_by_power_emulator" in params):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Reset the device")
            # ----------------------------------------------------------------------------------------------------------
            if "device_reset_by_feature_1802" in params:
                DeviceTestUtils.ResetHelper.hidpp_reset(self)
            elif "device_reset_by_power_emulator" in params:
                self.reset(LinkEnablerInfo.HID_PP_MASK, hardware_reset=True, recover_time_needed=True)
                sleep(2)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "after reset, once again enable hidden features")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        # end if

        if params["read"]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send TdeReadData (sp = {HexList(params["read"]["starting_position"])}) '
                                     f'(nb = {HexList(params["read"]["number_of_bytes"])})')
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1eb0.tde_read_data_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1eb0_index,
                starting_position=HexList(params["read"]["starting_position"]),
                number_of_bytes_to_read=HexList(params["read"]["number_of_bytes"])
            )

            if params["read"]["response"]["error_code"]:
                TdeAccessToNvmTestUtils.HIDppHelper.send_report_wait_error(
                    test_case=self,
                    report=report,
                    error_codes=[params["read"]["response"]["error_code"]])
            else:
                response = ChannelUtils.send(
                    test_case=self,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=self.feature_1eb0.tde_read_data_response_cls)

                expected = params["read"]["response"]["expected"]
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Validate TdeReadData.dataValues ({HexList(expected)})")
                # ------------------------------------------------------------------------------------------------------
                checker = TdeAccessToNvmTestUtils.TdeReadDataResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "starting_position": (checker.check_starting_position, expected[0]),
                    "number_of_bytes_to_read_or_write": (checker.check_number_of_bytes_to_read_or_write, expected[1]),
                    "data_byte_0": (checker.check_data_byte_0, expected[2]),
                    "data_byte_1": (checker.check_data_byte_1, expected[3]),
                    "data_byte_2": (checker.check_data_byte_2, expected[4]),
                    "data_byte_3": (checker.check_data_byte_3, expected[5]),
                    "data_byte_4": (checker.check_data_byte_4, expected[6]),
                    "data_byte_5": (checker.check_data_byte_5, expected[7]),
                    "data_byte_6": (checker.check_data_byte_6, expected[8]),
                    "data_byte_7": (checker.check_data_byte_7, expected[9]),
                    "data_byte_8": (checker.check_data_byte_8, expected[10]),
                    "data_byte_9": (checker.check_data_byte_9, expected[11]),
                    "data_byte_10": (checker.check_data_byte_10, expected[12]),
                    "data_byte_11": (checker.check_data_byte_11, expected[13]),
                    "data_byte_12": (checker.check_data_byte_12, expected[14]),
                    "data_byte_13": (checker.check_data_byte_13, expected[15]),
                })
                checker.check_fields(self, response, self.feature_1eb0.tde_read_data_response_cls, check_map)
            # end if
        # end if
    # end def process_api
# end class TdeAccessToNvmTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
