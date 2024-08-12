#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.hid.common.feature_1E00
:brief: Validates HID common feature 0x1E00
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/05/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pyharness.selector import features
from pyharness.selector import services
from pyharness.extensions import level
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_wrong_range
from pylibrary.tools.util import compute_sup_values
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import GetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import GetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.featureset import FeatureSetFactory
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.configchange import ConfigChange
from pyhid.hidpp.features.configchange import SetConfigurationComplete
from pyhid.hidpp.features.configchange import SetConfigurationCompleteResponse
from pyhid.hidpp.features.configchange import GetConfigurationCookie
from pyhid.hidpp.features.configchange import GetConfigurationCookieResponse
from pyhid.hiddispatcher import HIDDispatcher


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ApplicationEnableHiddenTestCase(BaseTestCase):
    """
    Validates Enable Hidden Features TestCases
    """

    WARNING_VERBOSE = False

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(ApplicationEnableHiddenTestCase, self).setUp()
        
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0x1E00)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_id = ChannelUtils.update_feature_mapping(test_case=self, feature_id=EnableHidden.FEATURE_ID)
    # end def setUp
    
    @features('Feature1E00')
    @level('Interface')
    def test_GetEnableHiddenFeaturesAPI(self):
        """
        Validates GetEnableHiddenFeatures API (Feature 0x1E00)
        
        EnableByte  [0]GetEnableHiddenFeatures()
        """

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetEnableHiddenFeatures')
        # --------------------------------------------------------------------------------------------------------------
        get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id)
        get_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                report=get_enable_hidden_features,
                                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                response_class_type=GetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetEnableHiddenFeatures response format')
        # --------------------------------------------------------------------------------------------------------------
        # The type of response is already checked in self.getMessage
        self.assertEqual(expected=get_enable_hidden_features.deviceIndex,
                         obtained=get_enable_hidden_features_response.deviceIndex,
                         msg='The deviceIndex parameter differs from the one expected')
        self.assertEqual(expected=get_enable_hidden_features.featureIndex,
                         obtained=get_enable_hidden_features_response.featureIndex,
                         msg='The featureIndex parameter differs from the one expected')
        self.assertFalse(expr=(get_enable_hidden_features_response.enableByte == '0') or
                              (get_enable_hidden_features_response.enableByte == '1'),
                         msg='The enableByte parameter is not in its valid range')
        
        self.testCaseChecked("FNT_1E00_0001")
    # end def test_GetEnableHiddenFeaturesAPI

    @features('Feature1E00')
    @level('Interface')
    def test_SetEnableHiddenFeaturesAPI(self):
        """
        Validates SetEnableHiddenFeatures API (Feature 0x1E00)

        null    [1]SetEnableHiddenFeatures(enable byte)
        """

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetEnableHiddenFeatures')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.DISABLED)
        set_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                report=set_enable_hidden_features,
                                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate SetEnableHiddenFeatures response format')
        # --------------------------------------------------------------------------------------------------------------
        # The type of response is already checked in self.getMessage
        self.assertEqual(expected=set_enable_hidden_features.deviceIndex,
                         obtained=set_enable_hidden_features_response.deviceIndex,
                         msg='The deviceIndex parameter differs from the one expected')
        self.assertEqual(expected=set_enable_hidden_features.featureIndex,
                         obtained=set_enable_hidden_features_response.featureIndex,
                         msg='The featureIndex parameter differs from the one expected')

        self.testCaseChecked("FNT_1E00_0002")
    # end def test_SetEnableHiddenFeaturesAPI

    @features('Feature1E00')
    @level('Business')
    def test_SetGetEnableHiddenFeatures(self):
        """
        Validates EnableHiddenFeatures Business case (enabling/disabling the device's engineering features)
        """

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetEnableHiddenFeatures (enable byte = 1)')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.ENABLED)
        ChannelUtils.send(test_case=self,
                          report=set_enable_hidden_features,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send GetEnableHiddenFeatures')
        # --------------------------------------------------------------------------------------------------------------
        get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id)
        get_enable_hidden_features_response = ChannelUtils.send(
            test_case=self,
            report=get_enable_hidden_features,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=GetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetEnableHiddenFeatures.enableByte = 1')
        # --------------------------------------------------------------------------------------------------------------
        # The type is already checked in self.getMessage
        self.assertEqual(expected=HexList(EnableHidden.ENABLED),
                         obtained=get_enable_hidden_features_response.enableByte,
                         msg='The enableByte parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send SetEnableHiddenFeatures (enable byte = 0)')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.DISABLED)
        ChannelUtils.send(test_case=self,
                          report=set_enable_hidden_features,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Send GetEnableHiddenFeatures')
        # --------------------------------------------------------------------------------------------------------------
        get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id)
        get_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                report=get_enable_hidden_features,
                                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                response_class_type=GetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate GetEnableHiddenFeatures.enableByte = 0')
        # --------------------------------------------------------------------------------------------------------------
        # The type is already checked in self.getMessage
        self.assertEqual(expected=HexList(EnableHidden.DISABLED),
                         obtained=get_enable_hidden_features_response.enableByte,
                         msg='The enableByte parameter differs from the one expected')

        self.testCaseChecked("FNT_1E00_0003")
    # end def test_SetGetEnableHiddenFeatures

    @features('Feature1E00')
    @features('Feature0001v1+')
    @level('Functionality')
    def test_VerifyHiddenFeaturesEnabled(self):
        """
        Validates this feature enables the access to all the Engineering features (meaning the features having bit5 of
        featureType field set to 1).
        """

        # Get the 0x0001 FeatureSet feature object
        feature_set_feature = FeatureSetFactory.create(self.config_manager.get_feature_version(
            self.f.PRODUCT.FEATURES.IMPORTANT.FEATURE_SET))

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetEnableHiddenFeatures (enable byte = 1)')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.ENABLED)
        ChannelUtils.send(test_case=self,
                          report=set_enable_hidden_features,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send FeatureSet.getCount to retrieve \'count\' value')
        # --------------------------------------------------------------------------------------------------------------
        feature_set_feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=feature_set_feature.get_count_cls.FEATURE_ID)
        get_count = feature_set_feature.get_count_cls(deviceIndex=ChannelUtils.get_device_index(self),
                                                      featureId=feature_set_feature_id)
        get_count_response = ChannelUtils.send(test_case=self,
                                               report=get_count,
                                               response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                                               response_class_type=feature_set_feature.get_count_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop over the range [1..count]')
        # --------------------------------------------------------------------------------------------------------------
        feature_count = get_count_response.count.toLong()

        for f_index in range(1, feature_count+1):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send FeatureSet.getFeatureID to retrieve featureType.eng')
            # ----------------------------------------------------------------------------------------------------------
            get_feature_id = feature_set_feature.get_feature_id_cls(
                deviceIndex=ChannelUtils.get_device_index(self),
                featureId=feature_set_feature_id, feature_index_to_get=f_index)
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=feature_set_feature.get_feature_id_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 4: Send FeatureX request if FeatureX.featureType.eng = 1')
            # ----------------------------------------------------------------------------------------------------------
            if get_feature_id_response.engineering_hidden == 1:
                hidden_feature_request_class = self.current_channel.hid_dispatcher.\
                    get_first_request_class_from_feature_id_and_version(feature_id=get_feature_id_response.feature_id,
                                                                        version=get_feature_id_response.feature_version)

                if hidden_feature_request_class is not None:
                    self.logTrace("Hidden feature " + format(get_feature_id_response.feature_id.toLong(), '#06x') +
                                  " recognised as " + hidden_feature_request_class.__name__ + "\n")
                    """
                    Since we don't know which hidden feature we are using, 
                    we have to use default values for the parameters.
                    This could create some unwanted behaviour, so we decided to change the function index
                    to the highest value (0x0F) to trigger the error HIDPP_ERR_INVALID_FUNCTION_ID (0x07).
                    However this still create the risk (very unlikely) of this function index being valid.
                    Therefore, a better solution has to be thought in the future to cover all risks.
                    """
                    hidden_feature_feature_id = ChannelUtils.update_feature_mapping(
                        test_case=self, feature_id=get_feature_id_response.feature_id)
                    hidden_feature_request = hidden_feature_request_class(ChannelUtils.get_device_index(self),
                                                                          hidden_feature_feature_id)
                    hidden_feature_request.functionIndex = 0x0F
                    hidden_feature_response = ChannelUtils.send(test_case=self,
                                                                report=hidden_feature_request,
                                                                response_queue_name=HIDDispatcher.QueueName.ERROR,
                                                                response_class_type=ErrorCodes)

                    # --------------------------------------------------------------------------------------------------
                    self.logTitle2('Test Check 1: Validate FeatureX response received')
                    # --------------------------------------------------------------------------------------------------

                    self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                                     obtained=hidden_feature_response.errorCode,
                                     msg='The errorCode parameter differs from the one expected')
                elif ApplicationEnableHiddenTestCase.WARNING_VERBOSE:
                    self.log_warning(f"Hidden feature {format(get_feature_id_response.feature_id.toLong(), '#06x')} "
                                     f"class not implemented yet\n")
                # end if
            # end if
        # end for

        self.testCaseChecked("FNT_1E00_0004")
    # end def test_VerifyHiddenFeaturesEnabled

    @features('Feature1E00')
    @features('Feature0001v1+')
    @level('Functionality')
    def test_VerifyHiddenFeaturesDisabled(self):
        """
        Validates this feature disables the access to all the Engineering features (meaning the feature having bit5 of
        featureType field set to 1).
        """

        # Get the 0x0001 FeatureSet feature object
        feature_set_feature = FeatureSetFactory.create(self.config_manager.get_feature_version(
            self.f.PRODUCT.FEATURES.IMPORTANT.FEATURE_SET))

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetEnableHiddenFeatures (enable byte = 0)')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.DISABLED)
        ChannelUtils.send(test_case=self,
                          report=set_enable_hidden_features,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send FeatureSet.getCount to retrieve \'count\' value')
        # --------------------------------------------------------------------------------------------------------------
        feature_set_feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=feature_set_feature.get_count_cls.FEATURE_ID)
        get_count = feature_set_feature.get_count_cls(deviceIndex=ChannelUtils.get_device_index(self),
                                                      featureId=feature_set_feature_id)
        get_count_response = ChannelUtils.send(test_case=self,
                                               report=get_count,
                                               response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                                               response_class_type=feature_set_feature.get_count_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop over the range [1..count]')
        # --------------------------------------------------------------------------------------------------------------
        feature_count = get_count_response.count.toLong()

        for f_index in range(1, feature_count+1):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send FeatureSet.getFeatureID to retrieve featureType.eng')
            # ----------------------------------------------------------------------------------------------------------
            get_feature_id = feature_set_feature.get_feature_id_cls(
                deviceIndex=ChannelUtils.get_device_index(self),
                featureId=feature_set_feature_id, feature_index_to_get=f_index)
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=feature_set_feature.get_feature_id_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 4: Send FeatureX request if FeatureX.featureType.eng = 1')
            # ----------------------------------------------------------------------------------------------------------
            if get_feature_id_response.engineering_hidden == 1:
                hidden_feature_request_class = self.current_channel.hid_dispatcher.\
                    get_first_request_class_from_feature_id_and_version(feature_id=get_feature_id_response.feature_id,
                                                                        version=get_feature_id_response.feature_version)

                if hidden_feature_request_class is not None:
                    self.logTrace("Hidden feature " + format(get_feature_id_response.feature_id.toLong(), '#06x') +
                                  " recognised as " + hidden_feature_request_class.__name__ + "\n")
                    """
                    Since we don't know which hidden feature we are using, 
                    we have to use default values for the parameters. 
                    If the hidden features are not well disabled, this could create some unwanted behaviour.
                    Therefore, a better solution has to be thought in the future to cover all risks.
                    The solution in test_VerifyHiddenFeaturesEnabled of changing the function index to the highest 
                    value (0x0F) to trigger the error HIDPP_ERR_INVALID_FUNCTION_ID (0x07) is not possible to use 
                    because this error is triggered before HIDPP_ERR_NOT_ALLOWED (0x05), which is the one we want.
                    """
                    hidden_feature_feature_id = ChannelUtils.update_feature_mapping(
                        test_case=self, feature_id=get_feature_id_response.feature_id)
                    hidden_feature_request = hidden_feature_request_class(ChannelUtils.get_device_index(self),
                                                                          hidden_feature_feature_id)
                    hidden_feature_response = ChannelUtils.send(test_case=self,
                                                                report=hidden_feature_request,
                                                                response_queue_name=HIDDispatcher.QueueName.ERROR,
                                                                response_class_type=ErrorCodes)

                    # --------------------------------------------------------------------------------------------------
                    self.logTitle2('Test Check 1: Check HIDPP_ERR_NOT_ALLOWED (0x05) Error Code returned by the device')
                    # --------------------------------------------------------------------------------------------------

                    self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                                     obtained=hidden_feature_response.errorCode,
                                     msg='The errorCode parameter differs from the one expected')
                elif ApplicationEnableHiddenTestCase.WARNING_VERBOSE:
                    self.log_warning(f"Hidden feature {format(get_feature_id_response.feature_id.toLong(), '#06x')} "
                                     f"class not implemented yet\n")
                # end if
            # end if
        # end for

        self.testCaseChecked("FNT_1E00_0005")
    # end def test_VerifyHiddenFeaturesDisabled

    @features('Feature1E00')
    @features('Feature1802')
    @features('Feature0001v1+')
    @level('Functionality')
    @services('PowerSupply')
    def test_VerifyHiddenFeatureDisabledAfterReset(self):
        """
        Validates GetEnableHiddenFeatures enable byte default value after a reset.
        """

        # Get the 0x0001 FeatureSet feature object
        feature_set_feature = FeatureSetFactory.create(self.config_manager.get_feature_version(
            self.f.PRODUCT.FEATURES.IMPORTANT.FEATURE_SET))

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetEnableHiddenFeatures (enable byte = 1)')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.ENABLED)
        ChannelUtils.send(test_case=self,
                          report=set_enable_hidden_features,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Reset the device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(LinkEnablerInfo.HID_PP_MASK, hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send FeatureSet.getFeatureID to ' +
                       'retrieve the first feature with featureType.eng = 1')
        # --------------------------------------------------------------------------------------------------------------
        feature_set_feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=feature_set_feature.get_count_cls.FEATURE_ID)
        get_count = feature_set_feature.get_count_cls(deviceIndex=ChannelUtils.get_device_index(self),
                                                      featureId=feature_set_feature_id)
        get_count_response = ChannelUtils.send(test_case=self,
                                               report=get_count,
                                               response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                                               response_class_type=feature_set_feature.get_count_response_cls)

        feature_count = get_count_response.count.toLong()
        break_loop = False

        for f_index in range(1, feature_count+1):
            get_feature_id = feature_set_feature.get_feature_id_cls(
                deviceIndex=ChannelUtils.get_device_index(self),
                featureId=feature_set_feature_id, feature_index_to_get=f_index)
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=feature_set_feature.get_feature_id_response_cls)

            if get_feature_id_response.engineering_hidden == 1:
                hidden_feature_request_class = self.current_channel.hid_dispatcher.\
                    get_first_request_class_from_feature_id_and_version(feature_id=get_feature_id_response.feature_id,
                                                                        version=get_feature_id_response.feature_version)

                if hidden_feature_request_class is not None:
                    # --------------------------------------------------------------------------------------------------
                    self.logTitle2('Test Step 4: Send FeatureX request')
                    # --------------------------------------------------------------------------------------------------

                    self.logTrace("Hidden feature " + format(get_feature_id_response.feature_id.toLong(), '#06x') +
                                  " recognised as " + hidden_feature_request_class.__name__ + "\n")
                    """
                    Since we don't know which hidden feature we are using, 
                    we have to use default values for the parameters. 
                    If the hidden features are not well disabled, this could create some unwanted behaviour.
                    Therefore, a better solution has to be thought in the future to cover all risks.
                    The solution in test_VerifyHiddenFeaturesEnabled of changing the function index to the highest 
                    value (0x0F) to trigger the error HIDPP_ERR_INVALID_FUNCTION_ID (0x07) is not possible to use 
                    because this error is triggered before HIDPP_ERR_NOT_ALLOWED (0x05), which is the one we want.
                    """
                    hidden_feature_feature_id = ChannelUtils.update_feature_mapping(
                        test_case=self, feature_id=get_feature_id_response.feature_id)
                    hidden_feature_request = hidden_feature_request_class(ChannelUtils.get_device_index(self),
                                                                          hidden_feature_feature_id)
                    hidden_feature_response = ChannelUtils.send(test_case=self,
                                                                report=hidden_feature_request,
                                                                response_queue_name=HIDDispatcher.QueueName.ERROR,
                                                                response_class_type=ErrorCodes)

                    # --------------------------------------------------------------------------------------------------
                    self.logTitle2('Test Check 1: Check HIDPP_ERR_NOT_ALLOWED (0x05) Error Code returned by the device')
                    # --------------------------------------------------------------------------------------------------

                    self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                                     obtained=hidden_feature_response.errorCode,
                                     msg='The errorCode parameter differs from the one expected')

                    break_loop = True
                elif ApplicationEnableHiddenTestCase.WARNING_VERBOSE:
                    self.log_warning(f"Hidden feature {format(get_feature_id_response.feature_id.toLong(), '#06x')} "
                                     f"class not implemented yet\n")
                # end if
            # end if

            if break_loop:
                break
            # end if
        # end for

        self.testCaseChecked("FNT_1E00_0006")
    # end def test_VerifyHiddenFeatureDisabledAfterReset

    @features('Feature1E00')
    @level('Functionality')
    def test_VerifySoftwareIdIgnored(self):
        """
        Validates GetEnableHiddenFeatures softwareId validity range

        SwID n boundary values 0 to F
        """

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop over softwareId validity range')
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GetEnableHiddenFeatures.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send GetEnableHiddenFeatures with softwareId in its validity range')
            # ----------------------------------------------------------------------------------------------------------
            get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                                 feature_index=self.feature_id)
            get_enable_hidden_features.softwareId = software_id
            get_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                    report=get_enable_hidden_features,
                                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                    response_class_type=GetEnableHiddenFeaturesResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check softwareId in its validity range')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=get_enable_hidden_features.softwareId,
                             obtained=get_enable_hidden_features_response.softwareId,
                             msg='The softwareId parameter differs from the one expected')
        # end for

        self.testCaseChecked("FNT_1E00_0007")
    # end def test_VerifySoftwareIdIgnored

    @features('Feature1E00')
    @level('Functionality')
    def test_VerifyInvalidEnableByteIgnored(self):
        """
        Validates SetEnableHiddenFeatures with a enable byte greater than 1
        """

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop over enable byte error range')
        # --------------------------------------------------------------------------------------------------------------
        """
        Be sure to test:
            - boundary values: 0x02 and 0xFF
            - nibble switch: 0x10 and 0x11
        """
        range_to_test = [0x02, 0xFF, 0x10, 0x11]

        for invalid_enable_byte in range_to_test:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send SetEnableHiddenFeatures with enable byte > 1')
            # ----------------------------------------------------------------------------------------------------------
            set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                                 feature_index=self.feature_id,
                                                                 enable_byte=invalid_enable_byte)
            ChannelUtils.send(test_case=self,
                              report=set_enable_hidden_features,
                              response_queue_name=HIDDispatcher.QueueName.COMMON,
                              response_class_type=SetEnableHiddenFeaturesResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate GetEnableHiddenFeatures.enable Byte value = 0')
            # ----------------------------------------------------------------------------------------------------------
            get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                                 feature_index=self.feature_id)
            get_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                    report=get_enable_hidden_features,
                                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                    response_class_type=GetEnableHiddenFeaturesResponse)

            self.assertEqual(expected=HexList(EnableHidden.DISABLED),
                             obtained=get_enable_hidden_features_response.enableByte,
                             msg='The enableByte parameter differs from the one expected')
        # end for

        self.testCaseChecked("FNT_1E00_0008")
    # end def test_VerifyInvalidEnableByteIgnored

    @features('Feature1E00')
    @level('ErrorHandling')
    def test_VerifyInvalidFunctionIndexError(self):
        """
        Validates EnableHiddenFeatures robustness processing (Feature 0x1E00)

        Tests function index error range [2..0xF]
        """

        for invalid_function_index in compute_wrong_range(
                [x for x in range(GetEnableHiddenFeatures.MAX_FUNCTION_INDEX + 1)], max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send EnableHiddenFeatures with a wrong function index value')
            # ----------------------------------------------------------------------------------------------------------
            get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                                 feature_index=self.feature_id)
            get_enable_hidden_features.functionIndex = invalid_function_index
            get_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                    report=get_enable_hidden_features,
                                                                    response_queue_name=HIDDispatcher.QueueName.ERROR,
                                                                    response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check InvalidFunctionId (0x07) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_enable_hidden_features_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for

        self.testCaseChecked("ROT_1E00_0001")
    # end def test_VerifyInvalidFunctionIndexError

    @features('Feature1E00')
    @level('Robustness')
    def test_Padding(self):
        """
        Validates SetEnableHiddenFeatures and GetEnableHiddenFeatures padding bytes are ignored

        Request: 0x10.DeviceIndex.0x00.0x1F.0xbb.0xPP.0xPP
        """

        enable_byte_to_alternate = EnableHidden.DISABLED

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop over SetEnableHiddenFeatures padding range')
        # --------------------------------------------------------------------------------------------------------------
        for paddingByte in compute_sup_values(HexList(Numeral(SetEnableHiddenFeatures.DEFAULT.PADDING,
                                                              SetEnableHiddenFeatures.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send SetEnableHiddenFeatures with several value for padding ' +
                           '(alternate enable byte to 0 and 1)')
            # ----------------------------------------------------------------------------------------------------------
            if enable_byte_to_alternate == EnableHidden.ENABLED:
                enable_byte_to_alternate = EnableHidden.DISABLED
            else:
                enable_byte_to_alternate = EnableHidden.ENABLED
            # end if

            set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                                 feature_index=self.feature_id,
                                                                 enable_byte=enable_byte_to_alternate)
            set_enable_hidden_features.padding = paddingByte
            ChannelUtils.send(test_case=self,
                              report=set_enable_hidden_features,
                              response_queue_name=HIDDispatcher.QueueName.COMMON,
                              response_class_type=SetEnableHiddenFeaturesResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate GetEnableHiddenFeatures.enable Byte value')
            # ----------------------------------------------------------------------------------------------------------
            get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                                 feature_index=self.feature_id)
            get_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                    report=get_enable_hidden_features,
                                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                    response_class_type=GetEnableHiddenFeaturesResponse)

            self.assertEqual(expected=HexList(enable_byte_to_alternate),
                             obtained=get_enable_hidden_features_response.enableByte,
                             msg='The enableByte parameter differs from the one expected')
        # end for

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop over GetEnableHiddenFeatures padding range')
        # --------------------------------------------------------------------------------------------------------------
        for paddingByte in compute_sup_values(HexList(Numeral(GetEnableHiddenFeatures.DEFAULT.PADDING,
                                                              GetEnableHiddenFeatures.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send GetEnableHiddenFeatures with several value for padding')
            # ----------------------------------------------------------------------------------------------------------
            get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                                 feature_index=self.feature_id)
            get_enable_hidden_features.padding = paddingByte
            get_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                    report=get_enable_hidden_features,
                                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                    response_class_type=GetEnableHiddenFeaturesResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Validate GetEnableHiddenFeatures response')
            # ----------------------------------------------------------------------------------------------------------
            # We can still use enable_byte_to_alternate as it is the last value we used with SetEnableHiddenFeatures
            self.assertEqual(expected=HexList(enable_byte_to_alternate),
                             obtained=get_enable_hidden_features_response.enableByte,
                             msg='The enableByte parameter differs from the one expected')
        # end for

        self.testCaseChecked("ROT_1E00_0002")
    # end def test_Padding

    @features('Feature1E00')
    @features('Feature0020')
    @level('Robustness')
    def test_ValidateBss(self):
        """
        Validates bss variables integrity
        """

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetEnableHiddenFeatures (enable byte = 0)')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.DISABLED)
        ChannelUtils.send(test_case=self,
                          report=set_enable_hidden_features,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send SetConfigurationComplete with cookie = 0xFFFF')
        # --------------------------------------------------------------------------------------------------------------
        config_change_feature_id = ChannelUtils.update_feature_mapping(test_case=self,
                                                                       feature_id=ConfigChange.FEATURE_ID)
        set_configuration_complete = SetConfigurationComplete(deviceIndex=ChannelUtils.get_device_index(self),
                                                              featureId=config_change_feature_id,
                                                              configurationCookie=0xFFFF)
        ChannelUtils.send(test_case=self,
                          report=set_configuration_complete,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetConfigurationCompleteResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate SetConfigurationComplete processing don\'t corrupt enable Byte value ' +
                       'in memory')
        # --------------------------------------------------------------------------------------------------------------
        get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id)
        get_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                report=get_enable_hidden_features,
                                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                response_class_type=GetEnableHiddenFeaturesResponse)

        self.assertEqual(expected=HexList(EnableHidden.DISABLED),
                         obtained=get_enable_hidden_features_response.enableByte,
                         msg='The enableByte parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send SetEnableHiddenFeatures (enable byte = 0)')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.DISABLED)
        ChannelUtils.send(test_case=self,
                          report=set_enable_hidden_features,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate SetEnableHiddenFeatures processing don\'t corrupt cookie value ' +
                       'in memory')
        # --------------------------------------------------------------------------------------------------------------
        get_configuration_cookie = GetConfigurationCookie(deviceIndex=ChannelUtils.get_device_index(self),
                                                          featureId=config_change_feature_id)
        get_configuration_cookie_response = ChannelUtils.send(test_case=self,
                                                              report=get_configuration_cookie,
                                                              response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                              response_class_type=GetConfigurationCookieResponse)

        self.assertEqual(expected=0xFFFF,
                         obtained=get_configuration_cookie_response.configurationCookie,
                         msg='The configurationCookie parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Send SetEnableHiddenFeatures (enable byte = 1)')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.ENABLED)
        ChannelUtils.send(test_case=self,
                          report=set_enable_hidden_features,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Send SetConfigurationComplete with cookie = 0x0000')
        # --------------------------------------------------------------------------------------------------------------
        set_configuration_complete = SetConfigurationComplete(deviceIndex=ChannelUtils.get_device_index(self),
                                                              featureId=config_change_feature_id,
                                                              configurationCookie=0x0000)
        ChannelUtils.send(test_case=self,
                          report=set_configuration_complete,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetConfigurationCompleteResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate SetConfigurationComplete processing don\'t corrupt enable Byte value ' +
                       'in memory')
        # --------------------------------------------------------------------------------------------------------------
        get_enable_hidden_features = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id)
        get_enable_hidden_features_response = ChannelUtils.send(test_case=self,
                                                                report=get_enable_hidden_features,
                                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                response_class_type=GetEnableHiddenFeaturesResponse)

        self.assertEqual(expected=HexList(EnableHidden.ENABLED),
                         obtained=get_enable_hidden_features_response.enableByte,
                         msg='The enableByte parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 6: Send SetEnableHiddenFeatures (enable byte = 1)')
        # --------------------------------------------------------------------------------------------------------------
        set_enable_hidden_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                             feature_index=self.feature_id,
                                                             enable_byte=EnableHidden.ENABLED)
        ChannelUtils.send(test_case=self,
                          report=set_enable_hidden_features,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Validate SetEnableHiddenFeatures processing don\'t corrupt cookie value ' +
                       'in memory')
        # --------------------------------------------------------------------------------------------------------------
        get_configuration_cookie = GetConfigurationCookie(deviceIndex=ChannelUtils.get_device_index(self),
                                                          featureId=config_change_feature_id)
        get_configuration_cookie_response = ChannelUtils.send(test_case=self,
                                                              report=get_configuration_cookie,
                                                              response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                              response_class_type=GetConfigurationCookieResponse)

        self.assertEqual(expected=0x0000,
                         obtained=get_configuration_cookie_response.configurationCookie,
                         msg='The configurationCookie parameter differs from the one expected')

        self.testCaseChecked("ROT_1E00_0003")
    # end def test_ValidateBss
# end class ApplicationEnableHiddenTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
