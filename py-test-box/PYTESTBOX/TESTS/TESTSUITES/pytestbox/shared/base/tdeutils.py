#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.tdeutils
:brief:  Helpers for TDE feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/06/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import RFRegisterAccess
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import SetRFRegisterAccessRequest
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import SetRFRegisterAccessResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import GetTestModeControlRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import GetTestModeControlResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import SetTestModeControlRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import SetTestModeControlResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class TDETestUtils(CommonBaseTestUtils):
    """
    Provide helpers for common checks on TDE features
    """

    @classmethod
    def set_check_test_mode(cls, test_case, test_mode_enable, log_step=0, log_check=0):
        """
        Enable the build-in test mode and verify the acknowledgement

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param test_mode_enable: Enable Manufacturing Test Mode
        :type test_mode_enable: ``bool`` or ``IntEnum``
        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``
        :param log_check: Log check number, if <= 0 no log printed
        :type log_check: ``int``
        """
        # Send Write Test Mode Control
        set_test_mode_control_resp = cls.set_test_mode_control(test_case, test_mode_enable, log_step)
        # Check Write Test Mode Control response
        if log_check > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Check Write Test Mode Control response')
            # ---------------------------------------------------------------------------
        # end if
        TDETestUtils.MessageChecker.check_fields(test_case, set_test_mode_control_resp, SetTestModeControlResponse, {})
    # end def set_check_test_mode

    @staticmethod
    def set_test_mode_control(test_case, test_mode_enable=TestModeControl.TestModeEnable.DISABLE_TEST_MODE, log_step=0):
        """
        Send Enable Test Mode Control

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param test_mode_enable: Flag to enable / disable the manufactring test mode
        :type test_mode_enable: ``int``
        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``

        :return: Response to Write command
        :rtype: ``SetTestModeControlResponse``
        """
        if log_step > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Send Write Test Mode Control')
            # ---------------------------------------------------------------------------
        # end if
        return ChannelUtils.send(
            test_case=test_case, report=SetTestModeControlRequest(test_mode_enable),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetTestModeControlResponse)
    # end def set_test_mode_control

    @classmethod
    def get_check_test_mode(cls, test_case, test_mode_enable, log_step=0, log_check=0):
        """
        Enable the build-in test mode and verify the acknowledgement

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param test_mode_enable: Enable Manufacturing Test Mode
        :type test_mode_enable: ``bool``
        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``
        :param log_check: Log check number, if <= 0 no log printed
        :type log_check: ``int``
        """
        # Send Read Test Mode Control
        get_test_mode_control_resp = cls.get_test_mode_control(test_case, test_mode_enable, log_step)
        # Check Read Test Mode Control response
        if log_check > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Check Read Test Mode Control response')
            # ---------------------------------------------------------------------------
        # end if
        checks = TDETestUtils.GetTestModeControlResponseChecker.get_default_check_map(test_case)
        checks["test_mode_enable"] = (TDETestUtils.GetTestModeControlResponseChecker.check_test_mode_enable,
                                      test_mode_enable)
        TDETestUtils.GetTestModeControlResponseChecker.check_fields(
            test_case, get_test_mode_control_resp, GetTestModeControlResponse, checks)
    # end def set_check_test_mode

    @staticmethod
    def get_test_mode_control(test_case, test_mode_enable=TestModeControl.TestModeEnable.DISABLE_TEST_MODE, log_step=0):
        """
        Send Enable Test Mode Control

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param test_mode_enable: Flag to enable / disable the manufactring test mode
        :type test_mode_enable: ``int``
        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``

        :return: Response to Read command
        :rtype: ``GetTestModeControlResponse``
        """
        if log_step > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Send Read Test Mode Control')
            # ---------------------------------------------------------------------------
        # end if
        return ChannelUtils.send(
            test_case=test_case, report=GetTestModeControlRequest(),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetTestModeControlResponse)
    # end def get_test_mode_control

    @staticmethod
    def set_rf_test_mode_enable(test_case, test_mode=RFRegisterAccess.TestModeEnableDisable.RF_OFF):
        """
        Send RF Register Access Page 0 - Test Mode Enable/Disable write request
        """
        rf_register_access_req = SetRFRegisterAccessRequest(RFRegisterAccess.RFPageRegister.PAGE_0,
                                                            RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
                                                            test_mode)
        return ChannelUtils.send(
            test_case=test_case, report=rf_register_access_req,
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetRFRegisterAccessResponse)
    # end def set_rf_test_mode_enable

    class GetTestModeControlResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on Test Mode Control read response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Default checks on each field
            """
            return {
                "test_mode_enable": (cls.check_test_mode_enable, TestModeControl.TestModeEnable.DISABLE_TEST_MODE),
                "test_mode_reserved": (cls.check_test_mode_reserved, 0),
            }
        # end def get_default_check_map

        @staticmethod
        def check_test_mode_enable(test_case, message, expected):
            """
            Check test mode enable value
            """
            test_case.assertEqual(obtained=int(Numeral(message.test_mode_enable)), expected=expected,
                                  msg="Test Mode Enable is not as expected")
        # end def check_test_mode_enable

        @staticmethod
        def check_test_mode_reserved(test_case, message, expected):
            """
            Check test mode reserved value
            """
            test_case.assertEqual(obtained=int(Numeral(message.test_mode_reserved)), expected=expected,
                                  msg="Test Mode reserved bits are not as expected")
        # end def check_test_mode_reserved

        @staticmethod
        def check_test_mode_kill(test_case, message, expected):
            """
            Check test mode kill value
            """
            test_case.assertEqual(obtained=int(Numeral(message.test_mode_kill)), expected=expected,
                                  msg="Test Mode Kill is not as expected")
        # end def check_test_mode_kill
    # end class GetTestModeControlResponseChecker

    class GetNonVolatileMemoryAccessResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on Non Volatile Memory Access read response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Default checks on each field
            """
            return cls.get_check_map(0x00, 0x00, 0x00)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, expected_nvm_address_lsb, expected_nvm_address_msb, expected_data):
            """
            Get check map for given set of expected values
            """
            return {
                "nvm_address_lsb": (cls.check_nvm_address_lsb, expected_nvm_address_lsb),
                "nvm_address_msb": (cls.check_nvm_address_msb, expected_nvm_address_msb),
                "data": (cls.check_data, expected_data)
            }
        # end def get_check_map

        @staticmethod
        def check_nvm_address_lsb(test_case, message, expected):
            """
            Check NVM Address LSB field
            """
            test_case.assertEqual(expected, int(Numeral(message.nvm_address_lsb)), "Address LSB should be as expected")
        # end def check_nvm_address_lsb

        @staticmethod
        def check_nvm_address_msb(test_case, message, expected):
            """
            Check NVM Address MSB field
            """
            test_case.assertEqual(expected, int(Numeral(message.nvm_address_msb)), "Address MSB should be as expected")
        # end def check_nvm_address_lsb

        @staticmethod
        def check_data(test_case, message, expected):
            """
            Check Data field
            """
            test_case.assertEqual(expected, int(Numeral(message.data)), "Data should be as expected")
        # end def check_data
    # end class GetNonVolatileMemoryAccessResponseChecker
# end class TDETestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
