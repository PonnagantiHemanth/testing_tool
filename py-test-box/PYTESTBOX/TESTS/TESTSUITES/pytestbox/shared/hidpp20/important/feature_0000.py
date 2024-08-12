#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp20.important.feature_0000
:brief: Shared HID++ 2.0 IRoot Important Package
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import importlib
from random import choice
from sys import stdout

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.systems import AbstractSubSystem
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.featureset import FeatureSetFactory
from pyhid.hidpp.features.root import FeatureIniConfigInfo
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.features.root import RootFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper

# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------
DEBUG = False
DEPRECATED_HIDPP20_FEATURES = [0x1C00, 0x4100]


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class IRootTestCaseMixin(CommonBaseTestCase):
    """
    Validate Root feature Test Case
    """

    GET_PROTOCOL_PING_DATA = HexList('00')
    PROTOCOL_NUMBER = HexList("04")

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # Get the 0x0000 root feature object
        self.feature_0000 = RootFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT))
        # Get the 0x0001 FeatureSet feature object
        self.feature_0001 = FeatureSetFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.FEATURE_SET))
    # end def setUp

    def reset(self, *args, **kwargs):
        # This implementation is done only to remove the abstract implementation warning
        super().reset(*args, **kwargs)
    # end def reset

    @features('Feature0000')
    @level('Business', 'SmokeTests')
    def test_ping_data(self):
        """
        Validate Ping Data Business case sequence

        IRoot
        version = [1]GetProtocolVersion()
        Request: 0x10.DeviceIndex.0x00.0x1n.0x00.0x00.0xUU
          0xUU boundary values are 0x00 and 0xFF
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_title_2(self, 'Test Loop over pingData in range [1..0xFF]')
        # --------------------------------------------------------------------------------------------------------------
        ping_data_list = compute_sup_values(self.GET_PROTOCOL_PING_DATA)
        ping_data_list_length = len(ping_data_list)
        for _ in range(ping_data_list_length):
            ping_data = choice(ping_data_list)
            ping_data_list.remove(ping_data)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Root.GetProtocolVersion with a random pinData')
            # ----------------------------------------------------------------------------------------------------------
            get_protocol_version = self.feature_0000.get_protocol_version_cls(
                deviceIndex=ChannelUtils.get_device_index(test_case=self), pingData=ping_data)
            get_protocol_version_response = ChannelUtils.send(
                test_case=self,
                report=get_protocol_version,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0000.get_protocol_version_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate Root.GetProtocolVersion.pinData returned by the DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=ping_data,
                             obtained=get_protocol_version_response.pingData,
                             msg='The ping parameter differs from the one sent in the request')
        # end for

        self.testCaseChecked("FUN_0000_0004")
    # end def test_ping_data

    @features('Feature0000')
    @level('Time-consuming')
    def test_all_feature_id(self):
        """
        Validate GetFeature with all possible featId value
        """
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.IMPORTANT,
            class_type=self.feature_0000.get_feature_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_title_2(self, 'Test Loop over feature index range')
        # --------------------------------------------------------------------------------------------------------------
        feature_id_list = []
        # Important & Common range
        feature_id_test_list = list(range(1, 0xF0))
        # Common range
        feature_id_test_list.extend(list(range(0x1000, 0x1010)) +
                                    list(range(0x1300, 0x1310)) +
                                    list(range(0x1500, 0x1510)) +
                                    list(range(0x1600, 0x1610)) +
                                    list(range(0x1700, 0x1710)) +
                                    list(range(0x1800, 0x18F0)) +
                                    list(range(0x1980, 0x1990)) +
                                    list(range(0x1A10, 0x1A30)) +
                                    list(range(0x1B00, 0x1C00)) +
                                    list(range(0x1D40, 0x1F30)))
        # Mouse range
        feature_id_test_list.extend(list(range(0x2000, 0x2010)) +
                                    list(range(0x2110, 0x2160)) +
                                    list(range(0x2200, 0x2260)) +
                                    [0x2300, 0x2400])
        # Keyboard range
        feature_id_test_list.extend(list(range(0x40A0, 0x4230)) +
                                    list(range(0x4300, 0x4310)) +
                                    list(range(0x4520, 0x4620)))
        # Touchpad range
        feature_id_test_list.extend(list(range(0x6100, 0x6120)) +
                                    list(range(0x6500, 0x6510)))
        # Gaming range
        feature_id_test_list.extend(list(range(0x8000, 0x8140)) +
                                    list(range(0x8300, 0x8400)))
        # Peripheral range
        feature_id_test_list.extend(list(range(0x9000, 0x9010)) +
                                    list(range(0x9200, 0x92F0)) +
                                    list(range(0x9300, 0x9330)) +
                                    list(range(0x9400, 0x9410)))
        # Prototypes range
        feature_id_test_list.extend(list(range(0xF000, 0xF0D0)))

        for feature_id in feature_id_test_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Root.GetFeature with featureId in all known ranges')
            # ----------------------------------------------------------------------------------------------------------
            get_feature = self.feature_0000.get_feature_cls(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                            featureId=feature_id)
            get_feature_response = ChannelUtils.send(
                test_case=self,
                report=get_feature,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0000.get_feature_response_cls)

            feature_index = int(get_feature_response.featIndex)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate Root.GetFeature.featIndex is not DEPRECATED_HIDPP20_FEATURES')
            # ----------------------------------------------------------------------------------------------------------
            if feature_index in DEPRECATED_HIDPP20_FEATURES:
                # These features should not be in products.
                self.assertEqual(expected=0, obtained=int(Numeral(feature_index)),
                                 msg="These features should not be in products.")
            # end if
            if feature_index != 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate Root.GetFeature.featIndex is unique')
                # ------------------------------------------------------------------------------------------------------
                self.assertFalse(expr=get_feature_response.featIndex in feature_id_list,
                                 msg=(f"The index in the feature table shall be unique (\n"
                                      f"{get_feature_response.featIndex} already in {str(feature_id_list)})."))
                feature_id_list.append(int(get_feature_response.featIndex))
                # This print should stay in the console because it has been considered useful
                print('feature index=0x%s version=%d on position %d' % (str(Numeral(feature_id, 2)),
                                                                        int(Numeral(get_feature_response.featVer)),
                                                                        int(get_feature_response.featIndex)))
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check Root.GetFeature.featVer is 0 if feature not found')
                # ------------------------------------------------------------------------------------------------------
                # The value 0 indicates the feature was not found
                self.assertEqual(expected=0,
                                 obtained=int(Numeral(get_feature_response.featVer)),
                                 msg="The featVer shall be 0 if feature not supported.")
            # end if
        # end for
        if self.config_manager.get_feature(ConfigurationManager.ID.FEATURE_COUNT) is not None:
            self.assertEqual(
                expected=int(Numeral(self.config_manager.get_feature(ConfigurationManager.ID.FEATURE_COUNT))),
                obtained=len(feature_id_list),
                msg=f'Found {len(feature_id_list)} features, expected '
                    f'{int(Numeral(self.config_manager.get_feature(ConfigurationManager.ID.FEATURE_COUNT)))}')
        else:
            stdout.write("The feature count parameter shall be defined in settings for all protocol to be compared "
                         f"with the actual list length = {len(feature_id_list)}\n")
        # end if
        self.testCaseChecked("FUN_0000_0005")
    # end def test_all_feature_id
# end class IRootTestCaseMixin


class SharedIRootTestCase(IRootTestCaseMixin):
    """
    Validate Root feature

    [0] getFeature(featId) -> featIndex, featType, featVer

    [1] getProtocolVersion(0, 0, pingData) -> protocolNum, targetSw, pingData
    """

    @features('Feature0000')
    @features('Feature0001')
    @level('Interface')
    def test_get_feature_0001_common_part(self):
        """
        Validate GetFeature common part API (Feature 0x0000) when calling FeatureSet

        IRoot getFeature v0
         featIndex, featType = [0]getFeature(featId)
        IRoot getFeature v1
         featIndex, featType, featVer = [0]getFeature(featId)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature with featureId = 0x0001')
        # --------------------------------------------------------------------------------------------------------------
        feature_id = self.feature_0001.get_count_cls.FEATURE_ID
        get_feature = self.feature_0000.get_feature_cls(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                        featureId=feature_id)
        get_feature_response = ChannelUtils.send(
            test_case=self,
            report=get_feature,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0000.get_feature_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.featIndex returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=feature_id,
                         obtained=get_feature_response.featIndex,
                         msg="The index in the feature table used to access the feature differs from the expected one")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.obsolete returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_cls.NOT_OBSOLETE,
                         obtained=get_feature_response.obsl,
                         msg="The obsolete parameter does not match the expected one")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.hidden returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_cls.NOT_HIDDEN,
                         obtained=get_feature_response.hidden,
                         msg="The hidden parameter does not match the expected one")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.engineering returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_cls.NOT_ENGINEERING_ONLY,
                         obtained=get_feature_response.eng,
                         msg="The engineering parameter does not match the expected one")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.reserved bits returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_response_cls.DEFAULT.RESERVED,
                         obtained=get_feature_response.reserved,
                         msg="The reserved bits shall be equal to 0!")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.feature version returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_cls.DEFAULT.PADDING,
                         obtained=int(Numeral(get_feature_response.padding)),
                         msg="The feature version parameter does not match the expected one !")

        self.testCaseChecked("INT_0000_0001")
    # end def test_get_feature_0001_common_part

    @features('Feature0000')
    @features('Feature0001')
    @level('Functionality')
    def test_get_feature_0001_version(self):
        """
        Validate GetFeature 0x0001 version parameter
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature with featureId = 0x0001')
        # --------------------------------------------------------------------------------------------------------------
        feature_id = self.feature_0001.get_count_cls.FEATURE_ID
        get_feature = self.feature_0000.get_feature_cls(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                        featureId=feature_id)
        get_feature_response = ChannelUtils.send(
            test_case=self,
            report=get_feature,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0000.get_feature_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.feature version returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HexList(self.feature_0001.VERSION),
                         obtained=get_feature_response.featVer,
                         msg="The feature 0x0001 version parameter does not match the expected one !")

        self.testCaseChecked("INT_0000_0002")
    # end def test_get_feature_0001_version

    @features('Feature0000')
    @level('Interface')
    def test_protocol_version(self):
        """
        Validate Root.getProtocolVersion normal processing (Feature 0x0000)

        protocolNum, targetSw, pingData [0]getProtocolVersion(0, 0, pingData)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetProtocolVersion with pingData = 0')
        # --------------------------------------------------------------------------------------------------------------
        ping_data = self.GET_PROTOCOL_PING_DATA
        get_protocol_version = self.feature_0000.get_protocol_version_cls(
            deviceIndex=ChannelUtils.get_device_index(test_case=self), pingData=ping_data)
        get_protocol_version_response = ChannelUtils.send(
            test_case=self,
            report=get_protocol_version,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0000.get_protocol_version_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate Root.GetProtocolVersion.protocol number returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.f.PRODUCT.FEATURES.IMPORTANT.ROOT.F_ProtocolNum,
                         obtained=get_protocol_version_response.protocolNum,
                         msg='The protocolNum parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate Root.GetProtocolVersion.target Software returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.config_manager.get_feature(ConfigurationManager.ID.TARGET_SW),
                         obtained=get_protocol_version_response.targetSw,
                         msg='The targetSw parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate Root.GetProtocolVersion.pinData returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ping_data,
                         obtained=get_protocol_version_response.pingData,
                         msg='The ping data shall be equal to 0!')

        self.testCaseChecked("INT_0000_0003")
    # end def test_protocol_version

    @features('Feature0000')
    @level('Functionality')
    def test_software_id(self):
        """
        Validate ForceDeviceReset softwareId validity range

          SwID n boundary values 0 to F
        """
        for software_id in compute_inf_values(self.feature_0000.get_feature_cls.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Root.GetFeature(0x0001) with softwareId in its validity range')
            # ----------------------------------------------------------------------------------------------------------
            get_protocol_version = self.feature_0000.get_protocol_version_cls(
                deviceIndex=ChannelUtils.get_device_index(test_case=self), pingData=RandHexList(1))
            get_protocol_version.softwareId = software_id
            get_protocol_version_response = ChannelUtils.send(
                test_case=self,
                report=get_protocol_version,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0000.get_protocol_version_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check softwareId in its validity range')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=software_id,
                             obtained=get_protocol_version_response.softwareId,
                             msg='The softwareId parameter differs from the one sent in the request')
        # end for

        self.testCaseChecked("FNT_0000_0006")
    # end def test_software_id

    @features('Feature0000')
    @level('Functionality')
    def get_feature_0000(self):
        """
        Validate GetFeature robustness processing (Feature 0x0000)

        IRoot
        featIndex, featType, featVer = [0]getFeature(featId = 0x0000)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature with featureId = 0x0000')
        # --------------------------------------------------------------------------------------------------------------
        feature_id = self.feature_0000.get_feature_cls.FEATURE_ID
        get_feature = self.feature_0000.get_feature_cls(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                        featureId=feature_id)
        get_feature_response = ChannelUtils.send(
            test_case=self,
            report=get_feature,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0000.get_feature_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate Root.GetFeature.featIndex returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
                expected=0,
                obtained=get_feature_response.featIndex,
                msg="The index in the feature table used to access the feature differs from the expected one.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.obsolete returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_feature_response.obsl,
                         msg="The obsolete parameter does not match the expected one !")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.hidden returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_feature_response.hidden,
                         msg="The hidden parameter does not match the expected one !")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.engineering returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_feature_response.eng,
                         msg="The engineering parameter does not match the expected one !")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.reserved bits returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=get_feature_response.reserved,
                         msg="The reserved bits shall be equal to 0!")

        self.testCaseChecked("FUN_0000_0007")
    # end def get_feature_0000

    @features('Feature0000v1+')
    @level('Functionality')
    def get_feature_0000_version(self):
        """
        Validate GetFeature version parameter (v1 API specific) when calling Root
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature with featureId = 0x0000')
        # --------------------------------------------------------------------------------------------------------------
        feature_id = self.feature_0000.get_feature_cls.FEATURE_ID
        get_feature = self.feature_0000.get_feature_cls(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                        featureId=feature_id)
        get_feature_response = ChannelUtils.send(
            test_case=self,
            report=get_feature,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0000.get_feature_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.feature version returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HexList(self.feature_0000.get_feature_response_cls.VERSION),
                         obtained=get_feature_response.featVer,
                         msg="The feature version parameter does not match the expected one !")

        self.testCaseChecked("FUN_0000_0008")
    # end def get_feature_0000_version

    @features('Feature0000v1+')
    @features('Feature0003')
    @level('Functionality')
    def test_get_feature_0003(self):
        """
        Validate GetFeature 0x0003 parameters
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature with featureId = 0x0003')
        # --------------------------------------------------------------------------------------------------------------
        feature_id = DeviceInformation.FEATURE_ID
        get_feature = self.feature_0000.get_feature_cls(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                        featureId=feature_id)
        get_feature_response = ChannelUtils.send(
            test_case=self,
            report=get_feature,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0000.get_feature_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.obsolete bit returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_cls.NOT_OBSOLETE,
                         obtained=get_feature_response.obsl,
                         msg="The obsolete bit does not match the expected one !")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.hidden bit returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_cls.NOT_HIDDEN,
                         obtained=get_feature_response.hidden,
                         msg="The hidden bit does not match the expected one !")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.engineering bit returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_cls.NOT_ENGINEERING_ONLY,
                         obtained=get_feature_response.eng,
                         msg="The engineering bit does not match the expected one !")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.reserved bits returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_response_cls.DEFAULT.RESERVED,
                         obtained=get_feature_response.reserved,
                         msg="The reserved bits shall be equal to 0!")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.padding returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_0000.get_feature_cls.DEFAULT.PADDING,
                         obtained=int(Numeral(get_feature_response.padding)),
                         msg="The feature version parameter does not match the expected one !")

        self.testCaseChecked("FUN_0000_0009")
    # end def test_get_feature_0003

    @features('Feature0000v1+')
    @features('Feature0003v2')
    @level('Functionality')
    def test_get_feature_0003_version(self):
        """
        Validate GetFeature version parameter (v1 API specific) when calling GetFwInfo
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature with featureId = 0x0003')
        # --------------------------------------------------------------------------------------------------------------
        feature_id = DeviceInformation.FEATURE_ID
        get_feature = self.feature_0000.get_feature_cls(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                        featureId=feature_id)
        get_feature_response = ChannelUtils.send(
            test_case=self,
            report=get_feature,
            response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
            response_class_type=self.feature_0000.get_feature_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Root.GetFeature.feature version returned by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HexList('02'),
                         obtained=get_feature_response.featVer,
                         msg="The feature 0x0003 version parameter does not match the expected one !")

        self.testCaseChecked("FUN_0000_0010")
    # end def test_get_feature_0003_version

    @features('Feature0000')
    @level('ErrorHandling')
    def test_not_zero(self):
        """
        Validate get protocol version zero error range

        Check boundary values (1 and 0xFF) plus all bits in the byte
        [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_title_2(self, 'Test Loop over feature "zero" error range')
        # --------------------------------------------------------------------------------------------------------------
        for not_zero in compute_wrong_range(HexList(Numeral(self.feature_0000.get_protocol_version_cls.DEFAULT.ZERO,
                                                            self.feature_0000.get_protocol_version_cls.LEN.ZERO // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Root.GetProtocolVersion with a modified "zero" value')
            # ----------------------------------------------------------------------------------------------------------
            ping_data = self.GET_PROTOCOL_PING_DATA
            get_protocol_version = self.feature_0000.get_protocol_version_cls(
                deviceIndex=ChannelUtils.get_device_index(test_case=self), pingData=ping_data)
            get_protocol_version.zero = not_zero
            get_protocol_version_response = ChannelUtils.send(
                test_case=self,
                report=get_protocol_version,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0000.get_protocol_version_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate Root.GetProtocolVersion.protocol number returned by the DUT')
            # ----------------------------------------------------------------------------------------------------------
            f = self.getFeatures()
            self.assertEqual(expected=f.PRODUCT.FEATURES.IMPORTANT.ROOT.F_ProtocolNum,
                             obtained=get_protocol_version_response.protocolNum,
                             msg='The protocolNum parameter differs from the one expected')
        # end for
        self.testCaseChecked("ERR_0000_0001")
    # end def test_not_zero

    @features('Feature0000')
    @level('ErrorHandling')
    def test_wrong_function_index(self):
        """
        Validate GetFeature robustness processing (Feature 0x0000)

        Function indexes valid range [0..1]
        Tests wrong indexes
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetFeature with wrong function index value')
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(list(range(Root.MAX_FUNCTION_INDEX + 1)), max_value=0xF):
            first_feature_id = 0x0001
            wrong_get_feature = self.feature_0000.get_feature_cls(
                deviceIndex=ChannelUtils.get_device_index(test_case=self), featureId=first_feature_id)
            wrong_get_feature.functionIndex = int(function_index)
            wrong_get_feature_response = ChannelUtils.send(
                test_case=self,
                report=wrong_get_feature,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check InvalidFunctionId (7) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=wrong_get_feature.featureIndex,
                             obtained=wrong_get_feature_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=wrong_get_feature.functionIndex,
                             obtained=wrong_get_feature_response.functionIndex,
                             msg='The request and response function indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=wrong_get_feature_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for
        self.testCaseChecked("ERR_0000_0002")
    # end def test_wrong_function_index

    @features('Feature0000')
    @level('Robustness')
    def test_padding(self):
        """
        Validate GetFeature padding bytes are ignored

        Request: 0x10.DeviceIndex.0x00.0x1F.0xPP.0xPP.0xPP
        """
        for padding_byte in compute_sup_values(HexList(Numeral(self.feature_0000.get_feature_cls.DEFAULT.PADDING,
                                                               self.feature_0000.get_feature_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetFeature with several value for padding')
            # ----------------------------------------------------------------------------------------------------------
            first_feature_id = 0x0001
            get_feature = self.feature_0000.get_feature_cls(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                            featureId=first_feature_id)
            get_feature.padding = padding_byte
            get_feature_response = ChannelUtils.send(
                test_case=self,
                report=get_feature,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0000.get_feature_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Root.GetFeature.featIndex returned by the DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(
                    expected=first_feature_id,
                    obtained=get_feature_response.featIndex,
                    msg="The index in the feature table used to access the feature differs from the expected one.")
        # end for
        self.testCaseChecked("ROT_0000_0003")
    # end def test_padding
# end class SharedIRootTestCase


class ApplicationOnlyIRootTestCase(SharedIRootTestCase, IRootTestCaseMixin):

    @features('Feature0000')
    @level('Functionality')
    @bugtracker('Wrong_8081_Feature_Version')
    @bugtracker('Wrong1807VersionReturned')
    def test_check_all_features_version(self):
        """
        Validate if all feature versions defined in ini settings file are equal to the values returned by the DUT
        through the 0x0000 getFeature(featId) → featureIndex, featureType, featureVersion
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Retrieve all enabled HID++2.0 features version from ini config')
        # --------------------------------------------------------------------------------------------------------------
        raw_feature_info_list = self._retrieve_features_info()
        revised_feature_info_list = self._revise_feature_info(raw_feature_info_list)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over range {enabled_feature_setting_list}")
        # --------------------------------------------------------------------------------------------------------------
        for feature in revised_feature_info_list:
            feature_module = getattr(importlib.import_module(feature.class_import_path), feature.class_name)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getFeature request with featId=0x{feature_module.FEATURE_ID:04x}')
            # ----------------------------------------------------------------------------------------------------------
            get_feature_request = self.feature_0000.get_feature_cls(
                deviceIndex=ChannelUtils.get_device_index(test_case=self),
                featureId=feature_module.FEATURE_ID)
            get_feature_response = ChannelUtils.send(
                test_case=self,
                report=get_feature_request,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0000.get_feature_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check getFeature response with featureVersion={feature.version} for feature '
                                      f'0x{feature_module.FEATURE_ID:04x}')
            # ----------------------------------------------------------------------------------------------------------
            if get_feature_response.featIndex == 0:
                if feature_module.FEATURE_ID == 0x0000:
                    pass
                elif feature_module.FEATURE_ID == 0x00c2 or feature_module.FEATURE_ID == 0x00c3 or \
                        feature_module.FEATURE_ID == 0x00d0:
                    # 0x00c2 and 0x00c3 might be supported in USB mode only for some gaming devices
                    # 0x00d0 only exists in bootloader mode except some gaming devices
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(self, f"Skip 0x{feature_module.FEATURE_ID:04x}")
                    # --------------------------------------------------------------------------------------------------
                    continue
                # end if
            else:
                self.assertNotEquals(unexpected=0,
                                     obtained=int(Numeral(get_feature_response.featIndex)),
                                     msg=f"The feature index is 0 for feature 0x{feature_module.FEATURE_ID:04x}")
            # end if

            self.assertEqual(expected=feature.version,
                             obtained=int(Numeral(get_feature_response.featVer)),
                             msg=f"The feature 0x{feature_module.FEATURE_ID:04x} version parameter does not match the "
                                 f"expected one!\nExpected: {feature.version}\nObtained: "
                                 f"{int(Numeral(get_feature_response.featVer))}"
                             )
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_0000_0011")
    # end def test_check_all_features_version

    def _retrieve_features_info(self):
        """
        Retrieve all HID++2.0 information [feature_category, feature_name, feature_version] to a list

        :return: raw hidpp features list
        :rtype: ``list[FeatureIniConfigInfo]``
        """
        raw_feature_info_list = []
        for f_category in self.f.PRODUCT.FEATURES:
            if isinstance(getattr(self.f.PRODUCT.FEATURES, f_category), AbstractSubSystem) is False:
                continue
            # end if
            for f_name in getattr(self.f.PRODUCT.FEATURES, f_category):
                # Version is 0 by default if the feature is enabled, otherwise version is None
                if isinstance(eval(f'self.f.PRODUCT.FEATURES.{f_category}.{f_name}'), AbstractSubSystem) is False:
                    continue
                elif eval(f'self.f.PRODUCT.FEATURES.{f_category}.{f_name}.F_Enabled'):
                    f_version = self.config_manager.get_feature_version(
                        eval(f'self.f.PRODUCT.FEATURES.{f_category}.{f_name}'))
                    f_version = f_version if f_version else 0
                else:
                    f_version = None
                # end if
                raw_feature_info_list.append(FeatureIniConfigInfo(category=f_category, name=f_name, version=f_version))
            # end for
        # end for

        LogHelper.log_info(self, "raw_feature_info_list:")
        for raw_feature_info in raw_feature_info_list:
            LogHelper.log_info(self, f"{raw_feature_info}")
        # end for
        return raw_feature_info_list
    # end def _retrieve_features_info

    def _revise_feature_info(self, raw_feature_info_list):
        """
        Revise raw_feature_info_list which includes
        - Filter disabled features
        - Initialize class name and class import path

        :param raw_feature_info_list: raw hidpp features list
        :type raw_feature_info_list: ``list[FeatureIniConfigInfo]``

        :return: revised hidpp features list
        :rtype: ``list[FeatureIniConfigInfo]``
        """
        revised_feature_info_list = []
        for raw_feature_info in raw_feature_info_list:
            if raw_feature_info.version is not None:
                raw_feature_info.get_class_name()
                raw_feature_info.get_class_import_path()
                revised_feature_info_list.append(raw_feature_info)
            # end if
        # end for

        LogHelper.log_info(self, "revised_feature_info_list:")
        for feature_info in revised_feature_info_list:
            LogHelper.log_info(self, f"{feature_info}")
        # end for

        return revised_feature_info_list
    # end def _revise_feature_info
# end class ApplicationOnlyIRootTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
