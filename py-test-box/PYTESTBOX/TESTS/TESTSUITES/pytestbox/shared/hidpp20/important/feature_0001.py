#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp20.important.feature_0001
:brief: Shared HID++ 2.0 FeatureSet Important Package
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from random import choice
from random import sample
from sys import stdout

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.featureset import FeatureSet
from pyhid.hidpp.features.featureset import FeatureSetFactory
from pyhid.hidpp.features.featureset import GetCount
from pyhid.hidpp.features.featureset import GetFeatureID
from pyhid.hidpp.features.root import RootFactory
from pyhid.hidpp.features.root import RootGetFeature
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.featuresetutils import FeatureSetTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class IFeatureSetTestCaseMixin(CommonBaseTestCase, ABC):
    """
    Validate Feature Set Test Cases
    """
    # Extract k elements from the feature list to test parameter coherence
    SAMPLE_COUNT = 5

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x0001)")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0001_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=FeatureSet.FEATURE_ID)
        self.feature_0001 = FeatureSetFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.FEATURE_SET))
    # end def setUp

    @features('Feature0001')
    @level('Interface')
    def test_get_count(self):
        """
        Validate FeatureSet.GetCount normal processing (Feature 0x0001)

        [0x0001]IFeatureSet
         count              =  [0]GetCount()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send FeatureSet.GetCount')
        # --------------------------------------------------------------------------------------------------------------
        get_count = GetCount(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                             featureId=self.feature_0001_index)
        get_count_response = ChannelUtils.send(
            test_case=self,
            report=get_count,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0001.get_count_response_cls)

        if self.config_manager.get_feature(ConfigurationManager.ID.FEATURE_COUNT) is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate FeatureSet.GetCount.count value')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(self.config_manager.get_feature(ConfigurationManager.ID.FEATURE_COUNT)),
                             obtained=get_count_response.count,
                             msg='The count parameter differs from the one expected')
        else:
            stdout.write("The feature count parameter shall be defined in settings for all protocol to be compared "
                         f"with the received value = 0x{get_count_response.count}\n")
            self.assertEqual(expected=get_count.software_id,
                             obtained=get_count_response.software_id,
                             msg='The software_id parameter differs from the one expected')
        # end if

        self.testCaseChecked("INT_0001_0001")
    # end def test_get_count

    @features('Feature0001')
    @level('Business', 'SmokeTests')
    def test_business_case(self):
        """
        Validate GetFeatureID Business case
        """
        feature_id_list = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send FeatureSet.GetCount')
        # --------------------------------------------------------------------------------------------------------------
        get_count = GetCount(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                             featureId=self.feature_0001_index)
        get_count_response = ChannelUtils.send(
            test_case=self,
            report=get_count,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0001.get_count_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over feature index in range [1 .. Count]')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(int(Numeral(get_count_response.count)+1)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send FeatureSet.GetFeatureID')
            # ----------------------------------------------------------------------------------------------------------
            get_feature_id = GetFeatureID(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                          featureId=self.feature_0001_index,
                                          feature_index_to_get=index)
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0001.get_feature_id_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetFeatureID.feature id is unique')
            # ----------------------------------------------------------------------------------------------------------
            self.assertFalse(get_feature_id_response.feature_id in feature_id_list,
                             msg="The index in the feature table shall be unique. ")
            feature_id_list.append(int(Numeral(get_feature_id_response.feature_id)))
        # end for

        self.testCaseChecked("BUS_0001_0009")
    # end def test_business_case
# end class IFeatureSetTestCaseMixin


class SharedIFeatureSetTestCase(IFeatureSetTestCaseMixin, ABC):
    """
    Validate TestCases
    """

    @features('Feature0001')
    @level('Interface')
    def test_get_feature_id(self):
        """
        Validate FeatureSet.GetFeatureID normal processing (Feature 0x0001)

        [0x0001]IFeatureSet
         featureID, featureType     =  [1]GetFeatureID(featureIndex)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send FeatureSet.GetFeatureID')
        # --------------------------------------------------------------------------------------------------------------
        get_feature_id = GetFeatureID(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                      featureId=self.feature_0001_index,
                                      feature_index_to_get=self.feature_0001_index)
        get_feature_id_response = ChannelUtils.send(
            test_case=self,
            report=get_feature_id,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0001.get_feature_id_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.featureID value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HexList(Numeral(FeatureSet.FEATURE_ID, 2)),
                         obtained=get_feature_id_response.feature_id,
                         msg='The featureID parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.obsolete bit')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_feature_id_response.obsolete,
                         msg='The obsolete parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.hidden bit')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_feature_id_response.sw_hidden,
                         msg='The hidden parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.engineering bit')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_feature_id_response.engineering_hidden,
                         msg='The engineering parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.reserved bits')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_feature_id_response.reserved,
                         msg='The reserved bits shall be equal to 0!')

        self.testCaseChecked("INT_0001_0002")
    # end def test_get_feature_id

    @features('Feature0001v1+')
    @level('Interface')
    def test_get_feature0001_version(self):
        """
        Validate FeatureSet.GetFeatureID.feature 0x0001 version parameter

        [0x0001]IFeatureSet
         featureID, featureType, featureVersion     =  [1]GetFeatureID(featureIndex)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send FeatureSet.GetFeatureID(0x0001)')
        # --------------------------------------------------------------------------------------------------------------
        get_feature_id = self.feature_0001.get_feature_id_cls(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                              featureId=self.feature_0001_index,
                                                              feature_index_to_get=self.feature_0001_index)
        get_feature_id_response = ChannelUtils.send(
            test_case=self,
            report=get_feature_id,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0001.get_feature_id_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.feature_version value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=HexList(self.config_manager.get_feature_version(
                self.f.PRODUCT.FEATURES.IMPORTANT.FEATURE_SET)),
            obtained=get_feature_id_response.feature_version,
            msg='The 0x0001 feature version parameter differs from the one expected')

        self.testCaseChecked("INT_0001_0003")
    # end def test_get_feature0001_version

    @features('Feature0001')
    @level('Functionality')
    def test_get_all_feature_id(self):
        """
        Validate GetFeatureID Business case retrieving all available feature
        using an incremented index

        """
        feature_id_list = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over feature index in range [1 .. Count]')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(self._get_hidpp_feature_count()+1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send FeatureSet.GetFeatureID')
            # ----------------------------------------------------------------------------------------------------------
            get_feature_id = GetFeatureID(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                          featureId=self.feature_0001_index,
                                          feature_index_to_get=index)
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0001.get_feature_id_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetFeatureID.feature id is unique')
            # ----------------------------------------------------------------------------------------------------------
            self.assertFalse(get_feature_id_response.feature_id in feature_id_list,
                             msg="The index in the feature table shall be unique. ")
            feature_id_list.append(int(Numeral(get_feature_id_response.feature_id)))
            # test_case.logTrace('Feature Id=%s, Version=%s, Obsolete=%d, Hidden=%d, Engineering=%d' %
            #                    (get_feature_id_response.feature_id, get_feature_id_response.feature_version,
            #                     get_feature_id_response.obsolete, get_feature_id_response.sw_hidden,
            #                     get_feature_id_response.engineering_hidden))
        # end for

        self.testCaseChecked("FUN_0001_0004")
    # end def test_get_all_feature_id

    @features('Feature0001')
    @level('Functionality')
    def test_random_index(self):
        """
        Validate GetFeatureID request retrieving all available feature
        using a randomly chosen index

        """
        feature_id_list = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over feature index in a random order')
        # --------------------------------------------------------------------------------------------------------------
        index_list = list(range(self._get_hidpp_feature_count()+1))
        index_list_length = len(index_list)
        for _ in range(index_list_length):
            index = choice(index_list)
            index_list.remove(index)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send FeatureSet.GetFeatureID with a randomly chosen index')
            # ----------------------------------------------------------------------------------------------------------
            get_feature_id = GetFeatureID(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                          featureId=self.feature_0001_index,
                                          feature_index_to_get=index)
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0001.get_feature_id_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetFeatureID.feature id is unique')
            # ----------------------------------------------------------------------------------------------------------
            self.assertFalse(get_feature_id_response.feature_id in feature_id_list,
                             msg="The index in the feature table shall be unique. ")
            feature_id_list.append(int(Numeral(get_feature_id_response.feature_id)))
        # end for

        self.testCaseChecked("FUN_0001_0005")
    # end def test_random_index

    @features('Feature0001v1+')
    @level('Functionality')
    def test_parameter_coherence(self):
        """
        Validate GetFeatureID parameters do not change from one call to another.

        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over feature index in a random order')
        # ---------------------------------------------------------------------------
        feature_count = self._get_hidpp_feature_count()
        sample_count = self.SAMPLE_COUNT if feature_count >= self.SAMPLE_COUNT else feature_count
        for index in sample(range(feature_count + 1), sample_count):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send FeatureSet.GetFeatureID(index)')
            # ---------------------------------------------------------------------------
            get_feature_id = GetFeatureID(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                          featureId=self.feature_0001_index,
                                          feature_index_to_get=index)
            first_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0001.get_feature_id_response_cls)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send FeatureSet.GetCount to insert another command between the 2 GetFeatureID '
                                     'requests')
            # ---------------------------------------------------------------------------
            get_count = GetCount(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                 featureId=self.feature_0001_index)
            ChannelUtils.send(
                test_case=self,
                report=get_count,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0001.get_count_response_cls)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send FeatureSet.getFeatureID(index) again')
            # ---------------------------------------------------------------------------
            second_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0001.get_feature_id_response_cls)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.featureID value coherence')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=first_response.feature_id,
                             obtained=second_response.feature_id,
                             msg='The featureID parameter differs from the one call to another')

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.obsolete bit coherence')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=first_response.obsolete,
                             obtained=second_response.obsolete,
                             msg='The obsolete parameter differs from the one call to another')

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.hidden bit coherence')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=first_response.sw_hidden,
                             obtained=second_response.sw_hidden,
                             msg='The hidden parameter differs from the one call to another')

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.engineering bit coherence')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=first_response.engineering_hidden,
                             obtained=second_response.engineering_hidden,
                             msg='The engineering parameter differs from the one call to another')

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.feature_version coherence')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=first_response.feature_version,
                             obtained=second_response.feature_version,
                             msg='The feature version parameter differs from the one call to another')
        # end for

        self.testCaseChecked("FUN_0001_0007")
    # end def test_parameter_coherence

    @features('Feature0001')
    @level('Functionality')
    def test_SoftwareId(self):
        """
        Validate GetFeature softwareId validity range

          SwID n boundary values 0 to F
        """
        for software_id in compute_inf_values(GetFeatureID.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Root.GetFeature(0x0001) with softwareId in its validity range')
            # ----------------------------------------------------------------------------------------------------------
            get_feature_id = GetFeatureID(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                          featureId=self.feature_0001_index,
                                          feature_index_to_get=1)
            get_feature_id.softwareId = software_id
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0001.get_feature_id_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check softwareId in its validity range')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=software_id,
                             obtained=get_feature_id_response.softwareId,
                             msg='The softwareId parameter differs from the one sent in the request')
        # end for

        self.testCaseChecked("FUN_0001_0006")
    # end def test_SoftwareId

    @features('Feature0001')
    @features('Feature0000v1+')
    @level('Interface')
    def test_get_feature0000_version(self):
        """
        Validate FeatureSet.GetFeatureID.feature 0x0000 version parameter

        [0x0001]IFeatureSet
         featureID, featureType, featureVersion     =  [1]GetFeatureID(featureIndex)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send FeatureSet.GetFeatureID(0x0000)')
        # --------------------------------------------------------------------------------------------------------------
        get_feature_id = GetFeatureID(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                      featureId=self.feature_0001_index,
                                      feature_index_to_get=RootGetFeature.FEATURE_ID)
        get_feature_id_response = ChannelUtils.send(
            test_case=self,
            report=get_feature_id,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0001.get_feature_id_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.feature_version value')
        # --------------------------------------------------------------------------------------------------------------
        # Get the 0x0000 root feature object
        self.feature_0000 = RootFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT))
        self.assertEqual(expected=HexList(self.feature_0000.get_feature_response_cls.VERSION),
                         obtained=get_feature_id_response.feature_version,
                         msg='The 0x0000 feature version parameter differs from the one expected')

        self.testCaseChecked("FNT_0001_0008")
    # end def test_get_feature0000_version

    @features('Feature0001v2+')
    @level('Functionality')
    def test_tags_engineering_deactivatable(self):
        """
        A feature tagged as engineering shall also be tagged as manufacturing or compliance deactivatable,
        unless it belongs to a list of exceptions.
        Currently, the list is: 0x1E00, 0x1805, 0x1E01, 0x1F04, 0x1f06.  It could be modified in the future.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get list of features with engineering tags')
        # --------------------------------------------------------------------------------------------------------------
        engineering_features = FeatureSetTestUtils.HIDppHelper.get_features_by_type(
            self, [FeatureSetTestUtils.FeatureTypes.ENGINEERING])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check features in the engineering list are also tagged as manufacturing or '
                                  'compliance deactivatable (except exception)')
        # --------------------------------------------------------------------------------------------------------------
        not_deactivatable_engineering_features = []
        for feature in engineering_features:
            rule = feature.manufacturing_deactivatable or feature.compliance_deactivatable
            exception = int(Numeral(feature.feature_id)) in FeatureSetTestUtils.ENGINEERING_NOT_DEACTIVATABLE
            if not rule and not exception:
                not_deactivatable_engineering_features.append(feature)
            # end if
        # end for
        self.assertListEqual(not_deactivatable_engineering_features, [],
                             "A feature tagged as engineering shall also be tagged as manufacturing or compliance "
                             "deactivatable, unless it belongs to a list of exceptions")

        self.testCaseChecked("FUN_0001_0010")
    # end def test_tags_engineering_deactivatable

    @features('Feature0001v2+')
    @level('Functionality')
    def test_tags_manufacturing_xor_compliance(self):
        """
        A feature shall not be tagged both as manufacturing and compliance deactivatable.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get list of features with manufacturing and compliance deactivatable tags')
        # --------------------------------------------------------------------------------------------------------------
        both_tags_features = FeatureSetTestUtils.HIDppHelper.get_features_by_type(
            self,
            [FeatureSetTestUtils.FeatureTypes.MANUFACTURING_DEACTIVATABLE,
             FeatureSetTestUtils.FeatureTypes.COMPLIANCE_DEACTIVATABLE]
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check list is empty')
        # --------------------------------------------------------------------------------------------------------------
        self.assertListEqual(both_tags_features, [], "No feature should be tagged both as manufacturing and "
                                                     "compliance deactivatable")
        self.testCaseChecked("FUN_0001_0011")
    # end def test_tags_manufacturing_xor_compliance

    @features('Feature0001')
    @level('ErrorHandling')
    def test_wrong_feature_id(self):
        """
        Validate GetFeatureID with a feature index greater than count
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over feature index error range')
        # --------------------------------------------------------------------------------------------------------------
        for wrong_index in compute_sup_values(self._get_hidpp_feature_count()):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetFeatureID with a wrong featureIndex')
            # ----------------------------------------------------------------------------------------------------------
            get_feature_id = GetFeatureID(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                          featureId=self.feature_0001_index,
                                          feature_index_to_get=wrong_index)
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check INVALID_ARGUMENT (2) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=get_feature_id_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for
        self.testCaseChecked("ERR_0001_0001")
    # end def test_wrong_feature_id

    @features('Feature0001')
    @level('ErrorHandling')
    def test_wrong_function_index(self):
        """
        Validate FeatureSet robustness processing (Feature 0x0001)

        Function indexes valid range [0..1]
          Tests wrong indexes
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send FeatureSet with wrong function index value')
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range([x for x in range(
                GetFeatureID.MAX_FUNCTION_INDEX + 1)], max_value=0xF):
            first_feature_id = 0x0001
            wrong_get_feature = GetFeatureID(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                             featureId=self.feature_0001_index,
                                             feature_index_to_get=first_feature_id)
            wrong_get_feature.functionIndex = int(function_index)
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=wrong_get_feature,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check InvalidFunctionId (7) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=wrong_get_feature.featureIndex,
                             obtained=get_feature_id_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_feature_id_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for
        self.testCaseChecked("ERR_0001_0002")
    # end def test_wrong_function_index

    @features('Feature0001v1+')
    @level('Robustness')
    def test_padding(self):
        """
        Validate GetFeatureID padding bytes are ignored

        Request: 0x10.DeviceIndex.0x00.0x1F.0xPP.0xPP.0xPP
        """
        for paddingByte in compute_sup_values(
                HexList(Numeral(GetFeatureID.DEFAULT.PADDING, GetFeatureID.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetFeatureID with several value for padding')
            # ----------------------------------------------------------------------------------------------------------
            first_feature_id = 0x0001
            get_feature_id = self.feature_0001.get_feature_id_cls(
                deviceIndex=ChannelUtils.get_device_index(test_case=self), featureId=self.feature_0001_index,
                feature_index_to_get=first_feature_id)
            get_feature_id.padding = paddingByte
            get_feature_id_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_id,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0001.get_feature_id_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate FeatureSet.GetFeatureID.feature_version value')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(
                expected=HexList(self.config_manager.get_feature_version(
                    self.f.PRODUCT.FEATURES.IMPORTANT.FEATURE_SET)),
                obtained=get_feature_id_response.feature_version,
                msg='The feature version parameter differs from the one expected')
        # end for
        self.testCaseChecked("ROB_0001_0003")
    # end def test_padding

    def _get_hidpp_feature_count(self):
        """
        Retrieve the feature count from the settings if available else request it from the firmware

        :return: HID++ feature count supported by the current protocol (i.e. BLE, LSx or USB) and
                 mode (Application or Bootloader)
        :rtype: ``int``
        """
        hidpp_feature_count = self.config_manager.get_feature(ConfigurationManager.ID.FEATURE_COUNT)
        if hidpp_feature_count is None:
            get_count = GetCount(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                 featureId=self.feature_0001_index)
            get_count_response = ChannelUtils.send(
                test_case=self,
                report=get_count,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0001.get_count_response_cls)
            stdout.write("The feature count parameter shall be defined in settings for all protocol to be compared "
                         f"with the value = 0x{get_count_response.count} provided by the firmware\n")
            hidpp_feature_count = get_count_response.count
        # end if
        return int(Numeral(hidpp_feature_count))
    # end def _get_hidpp_feature_count
# end class SharedIFeatureSetTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
