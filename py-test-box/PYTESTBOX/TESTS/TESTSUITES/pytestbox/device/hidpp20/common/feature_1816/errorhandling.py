#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1816.errorhandling
:brief: HID++ 2.0 BLEPro pre-pairing Error Handling test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/16
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleproprepairingutils import BleProPrePairingTestUtils
from pytestbox.device.hidpp20.common.feature_1816.bleproprepaing import BleProPrePairingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Christophe Roquebert"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BleProPrePairingErrorHandlingTestCase(BleProPrePairingTestCase):
    """
    Validate Device BLE Pro Pre-pairing Error Handling TestCases
    """
    @features('Feature1816')
    @level('ErrorHandling')
    def test_start_bad_prepairing_slot(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the prepairing slot is not available.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some interesting {bad_prepairing_slot} value in range [1..0xFF]")
        # ---------------------------------------------------------------------------
        for bad_prepairing_slot in compute_sup_values(
                self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send prepairing_data_management with prepairing_slot= {bad_prepairing_slot} "
                                     "and prepairing_management_control='Start'")
            # ---------------------------------------------------------------------------
            prepairing_data_management = self.feature_1816.prepairing_data_management_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
                prepairing_slot=bad_prepairing_slot,
                mode=self.feature_1816.prepairing_data_management_cls.MODE.START)
            prepairing_data_management_response = ChannelUtils.send(
                test_case=self, report=prepairing_data_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                             obtained=prepairing_data_management_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ERR_1816_0001")
    # end def test_start_bad_prepairing_slot

    @features('Feature1816')
    @level('ErrorHandling')
    def test_store_before_start(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the Store action is requested while
        no Start request has been sent.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send prepairing_data_management with prepairing_slot=0 and "
                                 "prepairing_management_control='Store'")
        # ---------------------------------------------------------------------------
        prepairing_management = self.feature_1816.prepairing_data_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            prepairing_slot=self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=self.feature_1816.prepairing_data_management_cls.MODE.STORE)
        prepairing_management_response = ChannelUtils.send(
            test_case=self, report=prepairing_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=prepairing_management_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ERR_1816_0002")
    # end def test_store_before_start

    @features('Feature1816')
    @level('ErrorHandling')
    def test_sequence_without_ltk(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the Long-Term Key (LTK) has not being set
        when the Store action is requested.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Roll out the Device Pre-pairing sequence without the ltk and the last 'Store' requests")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            long_term_key=None, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send prepairing_data_management with prepairing_slot=0 and "
                                 "prepairing_management_control='Store'")
        # ---------------------------------------------------------------------------
        prepairing_management = self.feature_1816.prepairing_data_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            prepairing_slot=self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=self.feature_1816.prepairing_data_management_cls.MODE.STORE)
        prepairing_management_response = ChannelUtils.send(
            test_case=self, report=prepairing_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=prepairing_management_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ERR_1816_0003")
    # end def test_sequence_without_ltk

    @features('Feature1816')
    @level('ErrorHandling')
    def test_sequence_without_remote_address(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the remote address has not being set
        when the Store action is requested.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Roll out the Device Pre-pairing sequence without the receiver address and the last 'Store' requests")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            receiver_address=None, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send prepairing_data_management with prepairing_slot=0 and "
                                 "prepairing_management_control='Store'")
        # ---------------------------------------------------------------------------
        prepairing_management = self.feature_1816.prepairing_data_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            prepairing_slot=self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=self.feature_1816.prepairing_data_management_cls.MODE.STORE)
        prepairing_management_response = ChannelUtils.send(
            test_case=self, report=prepairing_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=prepairing_management_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ERR_1816_0004")
    # end def test_sequence_without_remote_address

    @features('Feature1816')
    @level('ErrorHandling')
    def test_store_called_twice(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the Store action is called twice
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the mandatory part of thee Device Pre-pairing sequence including the "
                                 "last 'Store' requests")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Resend the prepairing_management request with prepairing_slot=0 and "
                                 "prepairing_management_control='Store'")
        # ---------------------------------------------------------------------------
        prepairing_management = self.feature_1816.prepairing_data_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            prepairing_slot=self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=self.feature_1816.prepairing_data_management_cls.MODE.STORE)
        prepairing_management_response = ChannelUtils.send(
            test_case=self, report=prepairing_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=prepairing_management_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ERR_1816_0005")
    # end def test_store_called_twice

    @features('Feature1816')
    @level('ErrorHandling')
    def test_store_bad_prepairing_slot(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the Store action is called on a
        not available pairing slot.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence without the last 'Store' requests")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some interesting {bad_prepairing_slot} value in range [1..0xFF]")
        # ---------------------------------------------------------------------------
        for bad_prepairing_slot in compute_sup_values(
                self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send prepairing_data_management with prepairing_slot={bad_prepairing_slot} and "
                                     "prepairing_management_control='Delete'")
            # ---------------------------------------------------------------------------
            prepairing_data_management = self.feature_1816.prepairing_data_management_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
                prepairing_slot=bad_prepairing_slot,
                mode=self.feature_1816.prepairing_data_management_cls.MODE.STORE)
            prepairing_data_management_response = ChannelUtils.send(
                test_case=self, report=prepairing_data_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                             obtained=prepairing_data_management_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ERR_1816_0006")
    # end def test_store_bad_prepairing_slot

    @features('Feature1816')
    @level('ErrorHandling')
    def test_delete_bad_prepairing_slot(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the Delete request is called on a not
        available pairing slot.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some interesting {bad_prepairing_slot} value in range [1..0xFF]")
        # ---------------------------------------------------------------------------
        for bad_prepairing_slot in compute_sup_values(
                self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send prepairing_data_management with prepairing_slot={bad_prepairing_slot} and "
                                     "prepairing_management_control='Delete'")
            # ---------------------------------------------------------------------------
            prepairing_data_management = self.feature_1816.prepairing_data_management_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
                prepairing_slot=bad_prepairing_slot,
                mode=self.feature_1816.prepairing_data_management_cls.MODE.DELETE)
            prepairing_data_management_response = ChannelUtils.send(
                test_case=self, report=prepairing_data_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                             obtained=prepairing_data_management_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ERR_1816_0007")
    # end def test_delete_bad_prepairing_slot

    @features('Feature1816')
    @level('ErrorHandling')
    def test_set_local_address(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the set pairing data data_type parameters is set
        to local address
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send prepairing_data_management with prepairing_slot=0 and "
                                 "prepairing_management_control='Start'")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data with data_type='Local'")
        # ---------------------------------------------------------------------------
        set_prepairing_data = self.feature_1816.set_prepairing_data_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            data_type=self.feature_1816.set_prepairing_data_cls.TYPE.LOCAL,
            local_address=BleProPrePairingTestUtils.generate_random_static_address(test_case=self))
        set_prepairing_data_response = ChannelUtils.send(
            test_case=self, report=set_prepairing_data, response_queue_name=HIDDispatcher.QueueName.ERROR,
            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=set_prepairing_data_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ERR_1816_0008")
    # end def test_set_local_address

    @features('Feature1816')
    @level('ErrorHandling')
    def test_set_pairing_data_rfu_data_type(self):
        """
        Check an HID++ error code INVALID_ARGUMENT (2) is raised if the set pairing data data_type parameters is set
        to its RFU values
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send prepairing_data_management with prepairing_slot=0 and "
                                 "prepairing_management_control='Start'")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some interesting {rfu_data_type} value in range [2..0xFF]")
        # ---------------------------------------------------------------------------
        for rfu_data_type in compute_sup_values(self.feature_1816.set_prepairing_data_cls.TYPE.RFU, True):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send set_prepairing_data with data_type={rfu_data_type}")
            # ---------------------------------------------------------------------------
            set_prepairing_data = self.feature_1816.set_prepairing_data_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
                data_type=rfu_data_type,
                local_address=BleProPrePairingTestUtils.generate_random_static_address(test_case=self))
            set_prepairing_data_response = ChannelUtils.send(
                test_case=self, report=set_prepairing_data, response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID++ 2.0 INVALID_ARGUMENT (2) Error Code returned by the device")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=set_prepairing_data_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ERR_1816_0009")
    # end def test_set_pairing_data_rfu_data_type

    @features('Feature1816')
    @level('ErrorHandling')
    def test_get_pairing_data_rfu_data_type(self):
        """
        Check an HID++ error code INVALID_ARGUMENT (2) is raised if the set pairing data data_type parameters is set
        to its RFU values
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send prepairing_data_management with prepairing_slot=0 and "
                                 "prepairing_management_control='Start'")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some interesting {rfu_data_type} value in range [2..0xFF]")
        # ---------------------------------------------------------------------------
        for rfu_data_type in compute_sup_values(self.feature_1816.set_prepairing_data_cls.TYPE.RFU, True):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send get_prepairing_data with data_type={rfu_data_type}")
            # ---------------------------------------------------------------------------
            get_prepairing_data = self.feature_1816.get_prepairing_data_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
                data_type=rfu_data_type)
            get_prepairing_data_response = ChannelUtils.send(
                test_case=self, report=get_prepairing_data, response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID++ 2.0 INVALID_ARGUMENT (2) Error Code returned by the device")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=get_prepairing_data_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ERR_1816_0010")
    # end def test_get_pairing_data_rfu_data_type

    @features('Feature1816')
    @level('ErrorHandling')
    def test_prepairing_data_management_rfu_data_type(self):
        """
        Check an HID++ error code INVALID_ARGUMENT (2) is raised if the prepairing_data_management data_type parameters
        is set to its RFU values
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some interesting {rfu_data_type} value in range [4..0xFF]")
        # ---------------------------------------------------------------------------
        for rfu_data_type in compute_sup_values(self.feature_1816.prepairing_data_management_cls.MODE.RFU, True):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send prepairing_data_management with data_type={rfu_data_type}")
            # ---------------------------------------------------------------------------
            # Send prepairing_data_management with prepairing_slot=0 and prepairing_management_control='Start'
            prepairing_data_management = self.feature_1816.prepairing_data_management_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
                prepairing_slot=self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
                mode=rfu_data_type)
            prepairing_data_management_response = ChannelUtils.send(
                test_case=self, report=prepairing_data_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID++ 2.0 INVALID_ARGUMENT (2) Error Code returned by the device")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=prepairing_data_management_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ERR_1816_0011")
    # end def test_prepairing_data_management_response_rfu_data_type
# end class BleProPrePairingErrorHandlingTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
