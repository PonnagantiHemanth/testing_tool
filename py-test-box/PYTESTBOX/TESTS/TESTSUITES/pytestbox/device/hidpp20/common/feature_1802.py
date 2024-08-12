#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.hid.common.feature_1802
:brief:  Validates HID common feature 0x1802
:author: Christophe Roquebert <croquebert@logitech.com>
:date:   2019/03/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.devicereset import DeviceReset
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import GetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import GetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pylibrary.tools.util import compute_inf_values
from pytransport.transportcontext import TransportContextException
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------
DEBUG = False


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ApplicationDeviceResetTestCase(BaseTestCase):
    """
    Validates Device reset TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(ApplicationDeviceResetTestCase, self).setUp()

        # Restart the executor with specific task list
        self.reset(task_bitmap=LinkEnablerInfo.HID_PP_MASK, verify_connection_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0x1802)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1802_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=DeviceReset.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Send Root.GetFeature(0x1E00)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1e00_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=GetEnableHiddenFeatures.FEATURE_ID)
    # end def setUp

    def tearDown(self):
        """
        Destructor of the test
        """
        super(ApplicationDeviceResetTestCase, self).tearDown()
    # end def tearDown

    @features('Feature1802')
    @level('Interface')
    def test_ForceDeviceReset(self):
        """
        Validates ForceDeviceReset normal processing (Feature 0x1802)

          void [0]ForceDeviceReset ()
        """
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        get_hidden = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(test_case=self),
                                             feature_index=self.feature_1e00_index)
        ChannelUtils.send(test_case=self,
                          report=get_hidden,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=GetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send ForceDeviceReset')
        # --------------------------------------------------------------------------------------------------------------
        force_device_reset = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                              featureId=self.feature_1802_index)
        try:
            ChannelUtils.send_only(test_case=self, report=force_device_reset, timeout=.6)
        except TransportContextException as e:
            if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                pass
            else:
                raise
            # end if
        # end try

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check no response or error message are returned')
        # --------------------------------------------------------------------------------------------------------------
        # It seems that in Unifying it is not happening.
        # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
        #  interesting to investigate a better solution
        if not isinstance(self.current_channel, ThroughEQuadReceiverChannel):
            CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                test_case=self, link_enabler=LinkEnablerInfo.HID_PP_MASK)
        # end if
        # Check Common message queue is empty
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON, timeout=.1)
        # Check Error code message queue is empty
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR, timeout=.1)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate the Enable byte has been reset')
        # --------------------------------------------------------------------------------------------------------------
        get_hidden_response = ChannelUtils.send(test_case=self,
                                                report=get_hidden,
                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                response_class_type=GetEnableHiddenFeaturesResponse)
        self.assertEqual(expected=EnableHidden.DISABLED,
                         obtained=int(Numeral(get_hidden_response.enableByte)),
                         msg='The enableByte parameter has not been reset')

        self.testCaseChecked("FNT_1802_0001")
    # end def test_ForceDeviceReset

    @features('Feature1802')
    @level('Time-consuming')
    def test_DeviceReset(self):
        """
        Validates ForceDeviceReset in run, walk and sleep power mode
        """
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop over the power mode [run, walk, sleep] but not deepSleep')
        # --------------------------------------------------------------------------------------------------------------
        f = self.getFeatures()
        for delay in f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay[:-1 or None]:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Enable Hidden Feature')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Wait until the device enter the targeted power mode')
            # ----------------------------------------------------------------------------------------------------------
            sleep(int(delay))
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check the current consumption using the ina226.')
            # ----------------------------------------------------------------------------------------------------------
            # TODO: connect ina226 current consumption board as soon as available

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send ForceDeviceReset')
            # ----------------------------------------------------------------------------------------------------------
            force_device_reset = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(self),
                                                  featureId=self.feature_1802_index)
            try:
                ChannelUtils.send_only(test_case=self, report=force_device_reset, timeout=.6)
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                else:
                    raise
                # end if
            # end try

            # Wait DUT to complete reset procedure
            # It seems that in Unifying it is not happening.
            # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
            #  interesting to investigate a better solution
            if not isinstance(self.current_channel, ThroughEQuadReceiverChannel):
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Validate the Enable byte has been reset')
            # ----------------------------------------------------------------------------------------------------------
            get_hidden = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                 feature_index=self.feature_1e00_index)
            get_hidden_response = ChannelUtils.send(test_case=self,
                                                    report=get_hidden,
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=GetEnableHiddenFeaturesResponse)
            self.assertEqual(expected=EnableHidden.DISABLED,
                             obtained=int(Numeral(get_hidden_response.enableByte)),
                             msg='The enableByte parameter has not been reset')
        # end for

        self.testCaseChecked("FNT_1802_0002")
    # end def test_DeviceReset

    @features('Feature1802')
    @level('Functionality')
    def test_SoftwareId(self):
        """
        Validates ForceDeviceReset softwareId validity range

          SwID n boundary values 0 to F
        """
        for software_id in compute_inf_values(DeviceReset.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Enable Hidden Feature')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send ForceDeviceReset with softwareId in its validity range')
            # ----------------------------------------------------------------------------------------------------------
            force_device_reset = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(self),
                                                  featureId=self.feature_1802_index)
            force_device_reset.softwareId = software_id
            try:
                ChannelUtils.send_only(test_case=self, report=force_device_reset, timeout=.6)
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                else:
                    raise
                # end if
            # end try

            # Reset device connection
            # It seems that in Unifying it is not happening.
            # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
            #  interesting to investigate a better solution
            if not isinstance(self.current_channel, ThroughEQuadReceiverChannel):
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                    test_case=self, link_enabler=LinkEnablerInfo.HID_PP_MASK)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate the Enable byte has been reset')
            # ----------------------------------------------------------------------------------------------------------
            get_hidden = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                 feature_index=self.feature_1e00_index)
            get_hidden_response = ChannelUtils.send(test_case=self,
                                                    report=get_hidden,
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=GetEnableHiddenFeaturesResponse)
            self.assertEqual(expected=EnableHidden.DISABLED,
                             obtained=int(Numeral(get_hidden_response.enableByte)),
                             msg='The enableByte parameter has not been reset')
        # end for
        self.testCaseChecked("FNT_1802_0003")
    # end def test_SoftwareId

    @features('Feature1802')
    @level('Functionality')
    def test_NotEnabled(self):
        """
        Validates ForceDeviceReset is blocked by default or after disabling it by HID++.
        """
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#3: The engineering features shall be disabled')
        # --------------------------------------------------------------------------------------------------------------
        get_hidden = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                             feature_index=self.feature_1e00_index)
        get_hidden_response = ChannelUtils.send(test_case=self,
                                                report=get_hidden,
                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                response_class_type=GetEnableHiddenFeaturesResponse)
        self.assertEqual(expected=EnableHidden.DISABLED,
                         obtained=int(Numeral(get_hidden_response.enableByte)),
                         msg='The enableByte parameter has not been reset')

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send ForceDeviceReset without enabling the feature')
        # --------------------------------------------------------------------------------------------------------------
        force_device_reset = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(self),
                                              featureId=self.feature_1802_index)
        force_device_reset_response = ChannelUtils.send(test_case=self,
                                                        report=force_device_reset,
                                                        response_queue_name=HIDDispatcher.QueueName.ERROR,
                                                        response_class_type=ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check NotAllowed (5) Error Code returned by the device')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=force_device_reset.featureIndex,
                         obtained=force_device_reset_response.featureIndex,
                         msg='The request and response feature indexes differ !')
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=force_device_reset_response.errorCode,
                         msg='The received error code do not match the expected one !')

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Enable Hidden Feature')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 2: The engineering features is enabled')
        # --------------------------------------------------------------------------------------------------------------
        get_hidden_response = ChannelUtils.send(test_case=self,
                                                report=get_hidden,
                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                response_class_type=GetEnableHiddenFeaturesResponse)
        self.assertEqual(expected=EnableHidden.ENABLED,
                         obtained=int(Numeral(get_hidden_response.enableByte)),
                         msg='The enableByte parameter has not been reset')

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Disable Hidden Feature')
        # --------------------------------------------------------------------------------------------------------------
        # create a Set Enable Hidden Feature instance
        set_hidden = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                             feature_index=self.feature_1e00_index,
                                             enable_byte=EnableHidden.DISABLED)
        ChannelUtils.send(test_case=self,
                          report=set_hidden,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 2: The engineering features shall be disabled')
        # --------------------------------------------------------------------------------------------------------------
        get_hidden_response = ChannelUtils.send(test_case=self,
                                                report=get_hidden,
                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                response_class_type=GetEnableHiddenFeaturesResponse)
        self.assertEqual(expected=EnableHidden.DISABLED,
                         obtained=int(Numeral(get_hidden_response.enableByte)),
                         msg='The enableByte parameter has not been reset')

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Send ForceDeviceReset without enabling the feature')
        # --------------------------------------------------------------------------------------------------------------
        force_device_reset = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(self),
                                              featureId=self.feature_1802_index)
        force_device_reset_response = ChannelUtils.send(test_case=self,
                                                        report=force_device_reset,
                                                        response_queue_name=HIDDispatcher.QueueName.ERROR,
                                                        response_class_type=ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Check NotAllowed (5) Error Code returned by the device')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=force_device_reset.featureIndex,
                         obtained=force_device_reset_response.featureIndex,
                         msg='The request and response feature indexes differ !')
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=force_device_reset_response.errorCode,
                         msg='The received error code do not match the expected one !')

        self.testCaseChecked("ROT_1802_0004")
    # end def test_NotEnabled

    @features('Feature1802')
    @level('ErrorHandling')
    def test_WrongFunctionIndex(self):
        """
        Validates ForceDeviceReset robustness processing (Feature 0x0020)

        Function indexes valid range [0]
          Tests wrong indexes
        """
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Hidden Feature')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        for function_index in compute_wrong_range([x for x in range(DeviceReset.MAX_FUNCTION_INDEX+1)], max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send ForceDeviceReset with wrong function index value')
            # ----------------------------------------------------------------------------------------------------------
            wrong_force_device_reset_function = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(self),
                                                                 featureId=self.feature_1802_index)
            wrong_force_device_reset_function.functionIndex = int(function_index)
            wrong_force_device_reset_function_response = ChannelUtils.send(
                test_case=self,
                report=wrong_force_device_reset_function,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check InvalidFunctionId (7) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=wrong_force_device_reset_function.featureIndex,
                             obtained=wrong_force_device_reset_function_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=wrong_force_device_reset_function_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for
        self.testCaseChecked("ROT_1802_0001")
    # end def test_WrongIndex

    @features('Feature1802')
    @level('Robustness')
    def test_Padding(self):
        """
        Validates ForceDeviceReset padding bytes are ignored

        Request: 0x10.DeviceIndex.0x00.0x1F.0xPP.0xPP.0xPP
        """
        # To limit the number of reset on our device, we apply the same test value to all 3 padding bytes
        #
        for padding_byte in [HexList('010101'), HexList('A5A5A5'), HexList('FFFFFF')]:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Enable Hidden Feature')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send ForceDeviceReset with several value for padding')
            # ----------------------------------------------------------------------------------------------------------
            force_device_reset = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(self),
                                                  featureId=self.feature_1802_index)
            force_device_reset.padding = padding_byte
            try:
                ChannelUtils.send_only(test_case=self, report=force_device_reset, timeout=.6)
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                else:
                    raise
                # end if
            # end try

            # Reset device connection
            # It seems that in Unifying it is not happening.
            # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
            #  interesting to investigate a better solution
            if not isinstance(self.current_channel, ThroughEQuadReceiverChannel):
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                    test_case=self, link_enabler=LinkEnablerInfo.HID_PP_MASK)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate the Enable byte has been reset')
            # ----------------------------------------------------------------------------------------------------------
            get_hidden = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                 feature_index=self.feature_1e00_index)
            get_hidden_response = ChannelUtils.send(test_case=self,
                                                    report=get_hidden,
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=GetEnableHiddenFeaturesResponse)
            self.assertEqual(expected=EnableHidden.DISABLED,
                             obtained=int(Numeral(get_hidden_response.enableByte)),
                             msg='The enableByte parameter has not been reset')
        # end for
        self.testCaseChecked("ROT_2250_0002")
    # end def test_Padding
# end class ApplicationDeviceResetTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
