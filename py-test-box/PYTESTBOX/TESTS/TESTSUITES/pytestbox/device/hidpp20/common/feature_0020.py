#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
""" @package pytestbox.hid.common.feature_0020

@brief  Validates HID common feature 0x0020

@author Christophe Roquebert

@date   2019/01/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import BaseTestCase
from pyharness.selector import features
from pyharness.extensions import level
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pyhid.hidpp.features.configchange import ConfigChange
from pyhid.hidpp.features.configchange import GetConfigurationCookie
from pyhid.hidpp.features.configchange import GetConfigurationCookieResponse
from pyhid.hidpp.features.configchange import SetConfigurationComplete
from pyhid.hidpp.features.configchange import SetConfigurationCompleteResponse
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pylibrary.tools.util import compute_inf_values


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ApplicationConfigChangeTestCase(BaseTestCase):
    """
    Validates Configuration Change TestCases
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(ApplicationConfigChangeTestCase, self).setUp()
        
        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0x0020)')
        # ---------------------------------------------------------------------------
        self.feature_id = self.updateFeatureMapping(feature_id=ConfigChange.FEATURE_ID)
    # end def setUp
    
    @features('Feature0020')
    @level('Interface')
    def test_GetConfigurationCookie(self):
        """
        @tc_synopsis Validates GetConfigurationCookie normal processing (Feature 0x0020)
        
         ConfigurationCookie     [0]GetConfigurationCookie()
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetConfigurationCookie')
        # ---------------------------------------------------------------------------
        get_configuration_cookie = GetConfigurationCookie(deviceIndex=self.deviceIndex,
                                                          featureId=self.feature_id)
        get_configuration_cookie_response = self.send_report_wait_response(
            report=get_configuration_cookie,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=GetConfigurationCookieResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetConfigurationCookie.featureIndex value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=get_configuration_cookie.featureIndex,
                         obtained=get_configuration_cookie_response.featureIndex,
                         msg='The featureIndex parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate GetConfigurationCookie.functionIndex value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=get_configuration_cookie.functionIndex,
                         obtained=get_configuration_cookie_response.functionIndex,
                         msg='The functionIndex parameter differs from the one expected')
        
        self.testCaseChecked("FNT_0020_0001")
    # end def test_GetConfigurationCookie
      
    @features('Feature0020')
    @level('Interface')
    def test_SetConfigurationComplete_Reset(self):
        """
        @tc_synopsis Validates SetConfigurationComplete normal processing (Feature 0x0020)
         
         configurationCookie [1] SetConfigurationComplete(configurationCookie=0x0000)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetConfigurationComplete with cookie=0x0000')
        # ---------------------------------------------------------------------------
        set_config_complete = SetConfigurationComplete(deviceIndex=self.deviceIndex,
                                                       featureId=self.feature_id,
                                                       configurationCookie=0)
        set_config_complete_response = self.send_report_wait_response(
            report=set_config_complete,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=SetConfigurationCompleteResponse)
                 
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate SetConfigurationComplete.configurationCookie set to 0x0000')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList('0000'),
                         obtained=set_config_complete_response.configurationCookie,
                         msg='The deviceName parameter differs from the one expected')
        
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send GetConfigurationCookie')
        # ---------------------------------------------------------------------------
        get_configuration_cookie = GetConfigurationCookie(deviceIndex=self.deviceIndex,
                                                          featureId=self.feature_id)
        get_configuration_cookie_response = self.send_report_wait_response(
            report=get_configuration_cookie,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=GetConfigurationCookieResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate GetConfigurationCookie.configurationCookie value is 0x0000')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList('0000'),
                         obtained=get_configuration_cookie_response.configurationCookie,
                         msg='The configurationCookie parameter differs from the one expected')
         
        self.testCaseChecked("FNT_0020_0002")
    # end def test_SetConfigurationComplete_Reset
    
    @features('Feature0020')
    @level('Functionality')
    def test_SetConfigurationComplete(self):
        """
        @tc_synopsis Validates SetConfigurationComplete with different cookie values
         
         configurationCookie [1] SetConfigurationComplete(configurationCookie)
         test design technique: raise each bit of the 16 bits cookie one at a time.
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetConfigurationComplete with some specific cookie values')
        # ---------------------------------------------------------------------------
        for cookie in compute_sup_values(HexList(Numeral(0, SetConfigurationComplete.LEN.CONFIGURATION_COOKIE//8))):
            set_config_complete = SetConfigurationComplete(deviceIndex=self.deviceIndex,
                                                           featureId=self.feature_id,
                                                           configurationCookie=cookie)
            set_config_complete_response = self.send_report_wait_response(
                report=set_config_complete,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=SetConfigurationCompleteResponse)
                     
            # ---------------------------------------------------------------------------
            self.logTitle2("""Test Check 1: Validate SetConfigurationComplete.configurationCookie value 
                                            matches the one from the request""")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=set_config_complete.configurationCookie,
                             obtained=set_config_complete_response.configurationCookie,
                             msg='The configurationCookie parameter differs from the one expected')
         
        self.testCaseChecked("FNT_0020_0003")
    # end def test_SetConfigurationComplete

    @features('Feature0020')
    @level('Business', 'SmokeTests')
    def test_SetGetConfig(self):
        """
        @tc_synopsis Interleave SetConfigurationComplete and GetConfigurationCookie requests
        
         Check the coherence between the cookie values returned by both commands
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetConfigurationComplete with some specific cookie values')
        # ---------------------------------------------------------------------------
        for _ in range(5):
            set_config_complete = SetConfigurationComplete(deviceIndex=self.deviceIndex,
                                                           featureId=self.feature_id,
                                                           configurationCookie=RandHexList(2))
            set_config_complete_response = self.send_report_wait_response(
                report=set_config_complete,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=SetConfigurationCompleteResponse)
                     
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send GetConfigurationCookie')
            # ---------------------------------------------------------------------------
            get_configuration_cookie = GetConfigurationCookie(deviceIndex=self.deviceIndex,
                                                              featureId=self.feature_id)
            get_configuration_cookie_response = self.send_report_wait_response(
                report=get_configuration_cookie,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=GetConfigurationCookieResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2("""Test Check 1: Validate GetConfigurationCookie.configurationCookie 
                                            matches SetConfigurationComplete.configurationCookie""")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=set_config_complete_response.configurationCookie,
                             obtained=get_configuration_cookie_response.configurationCookie,
                             msg='The configurationCookie value differs between the 2 responses')
        
        self.testCaseChecked("FNT_0020_0004")
    # end def test_SetGetConfig

    @features('Feature0020')
    @level('ErrorHandling')
    def test_WrongFunctionId(self):
        """
        @tc_synopsis Validates ConfigChange robustness processing (Feature 0x0020)
         
        Function indexes valid range [0..1]
          Tests wrong indexes
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetDeviceName with wrong index value')
        # ---------------------------------------------------------------------------
        for function_index in compute_wrong_range([x for x in range(
                SetConfigurationCompleteResponse.FUNCTION_INDEX+1)], max_value=0xF):
            set_config_complete = SetConfigurationComplete(deviceIndex=self.deviceIndex,
                                                           featureId=self.feature_id,
                                                           configurationCookie=RandHexList(2))
            set_config_complete.functionIndex = int(function_index)
            set_config_complete_response = self.send_report_wait_response(
                report=set_config_complete,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check Error Codes returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=set_config_complete.featureIndex,
                             obtained=set_config_complete_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=set_config_complete.functionIndex,
                             obtained=set_config_complete_response.functionIndex,
                             msg='The request and response function indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=set_config_complete_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for
         
        self.testCaseChecked("ROT_0020_0001")
    # end def test_WrongFunctionId
     
    @features('Feature0020')
    @level('Functionality')
    def test_SoftwareId(self):
        """
        Validates SetConfigurationComplete softwareId validity range
 
          SwID n boundary values 0 to F
        """ 
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetConfigurationComplete with softwareId in its validity range')
        # ---------------------------------------------------------------------------
        for software_id in compute_inf_values(SetConfigurationComplete.DEFAULT.SOFTWARE_ID):
            set_config_complete = SetConfigurationComplete(deviceIndex=self.deviceIndex,
                                                           featureId=self.feature_id,
                                                           configurationCookie=RandHexList(2))
            set_config_complete.softwareId = software_id
            set_config_complete_response = self.send_report_wait_response(
                report=set_config_complete,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=SetConfigurationCompleteResponse)
             
            # ---------------------------------------------------------------------------
            self.logTitle2("""Test Check 1: Validate SetConfigurationComplete.softwareId matches 
                                            the one from the request""")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=software_id,
                             obtained=set_config_complete_response.softwareId,
                             msg='The softwareId parameter differs from the one expected')

            # ---------------------------------------------------------------------------
            self.logTitle2("""Test Check 2: Validate SetConfigurationComplete.configurationCookie value 
                                            matches the one from the request""")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=set_config_complete.configurationCookie,
                             obtained=set_config_complete_response.configurationCookie,
                             msg='The configurationCookie parameter differs from the one expected')
         
        self.testCaseChecked("FNT_0020_0005")
    # end def test_SoftwareId
     
    @features('Feature0020')
    @level('Robustness')
    def test_Padding(self):
        """
        Validates SetConfigurationComplete padding bytes are ignored
         
        Request: 0x10.DeviceIndex.0x00.0x1F.0xCC.0xCC.0xPP
        """ 
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetConfigurationComplete with several value for padding')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(SetConfigurationComplete.DEFAULT.PADDING,
                                                               SetConfigurationComplete.LEN.PADDING//8))):
            set_config_complete = SetConfigurationComplete(deviceIndex=self.deviceIndex,
                                                           featureId=self.feature_id,
                                                           configurationCookie=RandHexList(2))
            set_config_complete.padding = padding_byte
            set_config_complete_response = self.send_report_wait_response(
                report=set_config_complete,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=SetConfigurationCompleteResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2("""Test Check 1: Validate SetConfigurationComplete.configurationCookie value 
                                            matches the one from the request""")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=set_config_complete.configurationCookie,
                             obtained=set_config_complete_response.configurationCookie,
                             msg='The configurationCookie parameter differs from the one expected')
         
        self.testCaseChecked("ROT_0020_0002")
    # end def test_Padding
# end class ApplicationConfigChangeTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
