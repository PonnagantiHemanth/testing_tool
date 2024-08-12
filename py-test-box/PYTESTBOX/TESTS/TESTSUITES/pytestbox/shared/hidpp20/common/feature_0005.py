#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp20.common.feature_0005
:brief: Validate HID++ 2.0 common feature 0x0005
https://docs.google.com/spreadsheets/d/1rYgsHRRwjKoZ7uPTFVPJ3tHp9n3QUvifbXEWTxGu7sw/edit?usp=sharing
:author: Christophe Roquebert
:date: 2018/12/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceTypeAndNameTestCaseMixin(CommonBaseTestCase, ABC):
    """
    Validate Device Type and Name TestCases
    """
    def setUpClass(self):
        """
        Define variables
        """
        super().setUpClass()

        self.feature_0005_index = None
        self.feature_0005 = None
    # end def setUpClass

    def generic_get_full_device_name(self):
        """
        Validate GetDeviceName Business case sequence
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceNameCount')
        # ---------------------------------------------------------------------------
        get_device_name_count_response = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name_count(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceName with index = 0')
        # ---------------------------------------------------------------------------
        full_name = HexList()
        current_char_index = 0
        get_device_name_response = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name(
            test_case=self, char_index=current_char_index)

        while (current_char_index + (self.feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME // 8)) < \
                to_int(get_device_name_count_response.device_name_count):
            full_name += get_device_name_response.device_name
            current_char_index += self.feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME // 8

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetDeviceName with an incremented index until end of name')
            # ---------------------------------------------------------------------------
            get_device_name_response = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name(
                test_case=self, char_index=current_char_index)
        # end while

        if (to_int(get_device_name_count_response.device_name_count) % (
                self.feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME // 8)) != 0:
            full_name += get_device_name_response.device_name[:to_int(
                get_device_name_count_response.device_name_count) % (
                    self.feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME // 8)]
        else:
            full_name += get_device_name_response.device_name
        # end if

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetDeviceName.deviceName value')
        # ---------------------------------------------------------------------------
        marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        self.assertEqual(expected=marketing_name,
                         obtained=ascii_converter(full_name),
                         msg='The deviceName parameter differs from the one expected')
        # end for
    # end def generic_get_full_device_name
# end class DeviceTypeAndNameTestCaseMixin


class SharedDeviceTypeAndNameTestCase(DeviceTypeAndNameTestCaseMixin, ABC):
    """
    Validate Get Device info TestCases
    """

    @features('Feature0005')
    @level('Interface')
    def test_get_device_name_count(self):
        """
        Validate GetDeviceNameCount normal processing (Feature 0x0005)
        
        Device type and name
         deviceNameCount    [0]GetDeviceNameCount()
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceNameCount')
        # ---------------------------------------------------------------------------
        get_device_name_count_response = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name_count(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetDeviceNameCount.deviceNameCount value')
        # ---------------------------------------------------------------------------
        marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        self.assertEqual(expected=len(marketing_name),
                         obtained=to_int(get_device_name_count_response.device_name_count),
                         msg='The deviceNameCount parameter differs from the one expected')
        
        self.testCaseChecked("INT_0005_0001")
    # end def test_get_device_name_count
    
    @features('Feature0005')
    @level('Interface')
    def test_get_device_name(self):
        """
        Validate GetDeviceName normal processing (Feature 0x0005)
        
        Device type and name
         deviceName         [1] getDeviceName(charIndex)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceName with index = 0')
        # ---------------------------------------------------------------------------
        get_device_name_response = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name(
                test_case=self, char_index=0)
                
        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetDeviceName.deviceName first part')
        # ---------------------------------------------------------------------------
        marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        self.assertEqual(
            expected=marketing_name[:+(self.feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME // 8)],
            obtained=ascii_converter(get_device_name_response.device_name),
            msg='The deviceName parameter differs from the one expected')
        
        self.testCaseChecked("INT_0005_0002")
    # end def test_get_device_name
    
    @features('Feature0005')
    @level('Business', 'SmokeTests')
    def test_get_full_device_name(self):
        """
        Validate GetDeviceName Business case sequence
        
        Retrieve the whole device name string
        """
        self.generic_get_full_device_name()
        
        self.testCaseChecked("BUS_0005_0003")
    # end def test_get_full_device_name
    
    @features('Feature0005')
    @level('Functionality')
    def test_get_device_name_by_index(self):
        """
        Validate GetDeviceName index validity range
        
        Check all possible values from 0 to the marketing name string length
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceName with all valid char indexes')
        # ---------------------------------------------------------------------------
        for char_index in range(len(self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME))):
            get_device_name_response = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name(
                test_case=self, char_index=char_index)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetDeviceName.deviceName trailing characters')
            # ---------------------------------------------------------------------------
            marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
            if len(marketing_name) < char_index + self.feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME // 8:
                # Check trailing characters
                self.assertEqual(expected=0,
                                 obtained=get_device_name_response.device_name[len(marketing_name) - char_index],
                                 msg='The trailing character(s) differ(s) from the one expected')
                name = get_device_name_response.device_name[: len(marketing_name) - char_index]
            else:
                name = get_device_name_response.device_name
            # end if
                
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetDeviceName.deviceName value')
            # ---------------------------------------------------------------------------
            self.assertEqual(
                expected=marketing_name[char_index:(
                        char_index + self.feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME // 8)],
                obtained=ascii_converter(name),
                msg='The deviceName parameter differs from the one expected')
        # end for
        
        self.testCaseChecked("FUN_0005_0004")
    # end def test_get_device_name_by_index
    
    @features('Feature0005')
    @level('ErrorHandling')
    def test_wrong_index(self):
        """
        Validate GetDeviceName robustness processing (Feature 0x0005)
        
        Device type and name with charIndex greater than the marketing name length
         deviceName         [1] getDeviceName(charIndex)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceName with wrong index value')
        # ---------------------------------------------------------------------------
        for char_index in compute_sup_values(
                                len(self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME))):
            get_device_name = self.feature_0005.get_device_name_cls(
                ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_0005_index, char_index=char_index)
            get_device_name_response = ChannelUtils.send(
                test_case=self,
                report=get_device_name,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes
            )

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=get_device_name.featureIndex,
                             obtained=get_device_name_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=get_device_name.functionIndex,
                             obtained=get_device_name_response.functionIndex,
                             msg='The request and response function indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=get_device_name_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for
        
        self.testCaseChecked("ERR_0005_0001")
    # end def test_wrong_index
    
    @features('Feature0005')
    @level('Interface')
    def test_get_device_type(self):
        """
        Validate GetDeviceType normal processing (Feature 0x0005)
        
        Device type and name
         deviceType    [0]GetDeviceType()
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceType')
        # ---------------------------------------------------------------------------
        get_device_type_response = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_type(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetDeviceType.deviceType value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=self.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType,
                         obtained=to_int(get_device_type_response.device_type),
                         msg='The deviceType parameter differs from the expected one')
        
        self.testCaseChecked("INT_0005_0005")
    # end def test_get_device_type
    
    @features('Feature0005')
    @level('ErrorHandling')
    def test_wrong_function_id(self):
        """
        Validate GetDevice robustness processing (Feature 0x0005)
        
        Function indexes valid range [0..2]
          Tests wrong indexes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceName with wrong index value')
        # ---------------------------------------------------------------------------
        for function_index in compute_wrong_range([x for x in range(
                self.feature_0005.get_device_type_response_cls.FUNCTION_INDEX+1)], max_value=0xF):
            get_device_type = self.feature_0005.get_device_type_cls(
                ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0005_index)
            get_device_type.function_index = int(function_index)
            get_device_type_response = ChannelUtils.send(
                test_case=self,
                report=get_device_type,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes
            )

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=get_device_type.featureIndex,
                             obtained=get_device_type_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=get_device_type.functionIndex,
                             obtained=get_device_type_response.functionIndex,
                             msg='The request and response function indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_device_type_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for
        
        self.testCaseChecked("ERR_0005_0002")
    # end def test_wrong_function_id
    
    @features('Feature0005')
    @level('Robustness')
    def test_software_id(self):
        """
        Validate GetDeviceName softwareId validity range

        deviceName = [1]GetDeviceName(charIndex)
        Request: 0x10.DeviceIndex.0x00.0x1n.0xii.0x00.0x00
          SwID n boundary values 0 to F
        """ 
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceName with softwareId in its validity range')
        # ---------------------------------------------------------------------------
        for software_id in compute_inf_values(self.feature_0005.get_device_name_cls.DEFAULT.SOFTWARE_ID):
            get_device_name = self.feature_0005.get_device_name_cls(
                ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0005_index, char_index=0)
            get_device_name.software_id = software_id
            get_device_name_response = ChannelUtils.send(
                test_case=self,
                report=get_device_name,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0005.get_device_name_response_cls
            )
            
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetDeviceName.softwareId matches the one from the request')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=software_id,
                             obtained=get_device_name_response.softwareId,
                             msg='The softwareId parameter differs from the one expected')

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetDeviceName.deviceName first part')
            # ---------------------------------------------------------------------------
            marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
            self.assertEqual(
                expected=marketing_name[:+(self.feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME//8)],
                obtained=ascii_converter(get_device_name_response.device_name),
                msg='The deviceName parameter differs from the one expected')
        
        self.testCaseChecked("ROB_0005_0006")
    # end def test_software_id
    
    @features('Feature0005')
    @level('Robustness')
    def test_padding(self):
        """
        Validate GetDeviceName padding bytes are ignored
        
        deviceName = [1]GetDeviceName(charIndex)
        Request: 0x10.DeviceIndex.0x00.0x1F.0xii.0xPP.0xPP
        """ 
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceName with several value for padding')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(self.feature_0005.get_device_name_cls.DEFAULT.PADDING,
                                                               self.feature_0005.get_device_name_cls.LEN.PADDING//8))):
            get_device_name = self.feature_0005.get_device_name_cls(
                ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0005_index, char_index=0)
            get_device_name.padding = padding_byte
            get_device_name_response = ChannelUtils.send(
                test_case=self,
                report=get_device_name,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0005.get_device_name_response_cls
            )

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetDeviceName response received')
            # ---------------------------------------------------------------------------
            marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
            self.assertEqual(
                expected=marketing_name[:+(self.feature_0005.get_device_name_response_cls.LEN.DEVICE_NAME//8)],
                obtained=ascii_converter(get_device_name_response.device_name),
                msg='The deviceName parameter differs from the one expected')
        
        self.testCaseChecked("ROB_0005_0003")
    # end def test_padding
# end class SharedDeviceTypeAndNameTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
