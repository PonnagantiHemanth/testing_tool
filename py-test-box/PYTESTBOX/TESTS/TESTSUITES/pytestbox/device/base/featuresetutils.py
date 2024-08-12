#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.featuresetutils
:brief:  Helpers for Feature Set feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/10/09
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import auto
from enum import IntEnum
from enum import unique

from pyhid.hidpp.features.common.managedeactivatablefeatures import ManageDeactivatableFeatures
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.oobstate import OobState
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.featureset import FeatureSet
from pyhid.hidpp.features.featureset import FeatureSetFactory
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class FeatureSetTestUtils(DeviceBaseTestUtils):
    """
    Test utils for Feature Set feature
    """
    # List of engineering features which are not deactivatable (not tagged as manufacturing nor compliance)
    ENGINEERING_NOT_DEACTIVATABLE = [
        OobState.FEATURE_ID,
        EnableHidden.FEATURE_ID,
        ManageDeactivatableFeatures.FEATURE_ID,
        ManageDeactivatableFeaturesAuth.FEATURE_ID,
        0x1F04,
        0x1F06
    ]

    @unique
    class FeatureTypes(IntEnum):
        """
        Available features tags
        """
        OBSOLETE = auto()
        HIDDEN = auto()
        ENGINEERING = auto()
        MANUFACTURING_DEACTIVATABLE = auto()
        COMPLIANCE_DEACTIVATABLE = auto()
    # end class FeatureTypes

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        """
        HID++ helper class
        """
        @staticmethod
        def feature_set_get_count(test_case, device_index=None, port_index=None):
            """
            HID++ request to send feature set get count

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase`` or inherited
            :param device_index: Device index
            :type device_index: ``int``
            :param port_index: Port index
            :type port_index: ``int``

            :return: FeatureSet GetCount response
            :rtype: ``pyhid.hidpp.features.featureset.GetCountResponse`` or inherited
            """
            device_index = device_index if device_index is not None else test_case.deviceIndex
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(
                test_case=test_case)

            feature_set_idx = FeatureSetTestUtils.HIDppHelper.get_feature_index(
                test_case, FeatureSet.FEATURE_ID, device_index, port_index)
            feature_set = FeatureSetFactory.create(
                test_case.get_feature_version_from_dut_to_int(feature_set_idx, device_index, port_index))
            get_count_req = feature_set.get_count_cls(deviceIndex=device_index, featureId=feature_set_idx)
            get_count_resp = test_case.send_report_wait_response(
                report=get_count_req,
                response_queue=test_case.hidDispatcher.important_message_queue,
                response_class_type=feature_set.get_count_response_cls)
            return get_count_resp
        # end def feature_set_get_count

        @staticmethod
        def feature_set_get_feature_id(test_case, feature_index, device_index=None, port_index=None):
            """
            HID++ request to send feature set feature id

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase`` or inherited
            :param feature_index: Desired feature index
            :type feature_index: ``int``
            :param device_index: Device index
            :type device_index: ``int``
            :param port_index: Port index
            :type port_index: ``int``

            :return: FeatureSet GetFeatureID response
            :rtype: ``pyhid.hidpp.features.featureset.GetFeatureIDResponse`` or inherited
            """
            device_index = device_index if device_index is not None else test_case.deviceIndex
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(
                test_case=test_case)

            feature_set_idx = FeatureSetTestUtils.HIDppHelper.get_feature_index(
                test_case, FeatureSet.FEATURE_ID, device_index, port_index)
            feature_set = FeatureSetFactory.create(
                test_case.get_feature_version_from_dut_to_int(feature_set_idx, device_index, port_index))
            get_feature_id_req = feature_set.get_feature_id_cls(deviceIndex=device_index,
                                                                featureId=feature_set_idx,
                                                                feature_index_to_get=feature_index)
            get_feature_id_resp = test_case.send_report_wait_response(
                report=get_feature_id_req,
                response_queue=test_case.hidDispatcher.important_message_queue,
                response_class_type=feature_set.get_feature_id_response_cls)
            return get_feature_id_resp
        # end def feature_set_get_feature_id

        _device_index_features = {}

        @classmethod
        def get_features(cls, test_case, device_index=None, port_index=None, refresh=False):
            """
            Get the list of all features in device.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase`` or inherited
            :param device_index: Device index
            :type device_index: ``int``
            :param port_index: Port index
            :type port_index: ``int``
            :param refresh: Force refresh. If false, use cached values if available.
            :type refresh: ``bool``

            :return: List of supported features
            :rtype: ``list[pyhid.hidpp.features.featureset.GetFeatureIDResponse]`` or inherited
            """
            device_index = device_index if device_index is not None else test_case.deviceIndex
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(
                test_case=test_case)

            if port_index not in cls._device_index_features:
                cls._device_index_features[port_index] = {}
            # end if

            if device_index not in cls._device_index_features[port_index]:
                cls._device_index_features[port_index][device_index] = {}
            # end if

            if refresh or not cls._device_index_features[port_index][device_index]:
                cls._device_index_features[port_index][device_index] = cls.get_features_from_device(test_case,
                                                                                                    device_index,
                                                                                                    port_index)
            # end if

            return cls._device_index_features[port_index][device_index]
        # end def get_features

        @classmethod
        def get_features_from_device(cls, test_case, device_index=None, port_index=None):
            """
            Get the list of all features directly from device.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase`` or inherited
            :param device_index: Device index
            :type device_index: ``int``
            :param port_index: Port index
            :type port_index: ``int``

            :return: List of supported features
            :rtype: ``list[pyhid.hidpp.features.featureset.GetFeatureIDResponse]`` or inherited
            """
            device_index = device_index if device_index is not None else test_case.deviceIndex
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(
                test_case=test_case)

            features = []
            feature_count = cls.feature_set_get_count(test_case, device_index, port_index).count
            for feature_index in range(1, int(Numeral(feature_count)) + 1):
                get_feature_id_resp = cls.feature_set_get_feature_id(test_case,
                                                                     feature_index,
                                                                     device_index,
                                                                     port_index)
                features.append(get_feature_id_resp)
            # end for
            return features
        # end def get_features_from_device

        @classmethod
        def get_features_by_type(cls, test_case, feature_types, device_index=None, port_index=None, refresh=False):
            """
            Get the list of all features in device matching given types.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase`` or inherited
            :param feature_types: Feature type(s) to get
            :type feature_types: ``list[FeatureSetTestUtils.FeatureTypes]``
            :param device_index: Device index
            :type device_index: ``int``
            :param port_index: Port index
            :type port_index: ``int``
            :param refresh: Force refresh. If false, use cached values if available.
            :type refresh: ``bool``

            :return: List of supported features matching types
            :rtype: ``list[pyhid.hidpp.features.featureset.GetFeatureIDResponse]`` or inherited
            """
            type_to_attr = {
                FeatureSetTestUtils.FeatureTypes.OBSOLETE: "obsolete",
                FeatureSetTestUtils.FeatureTypes.HIDDEN: "hidden",
                FeatureSetTestUtils.FeatureTypes.ENGINEERING: "engineering",
                FeatureSetTestUtils.FeatureTypes.MANUFACTURING_DEACTIVATABLE: "manufacturing_deactivatable",
                FeatureSetTestUtils.FeatureTypes.COMPLIANCE_DEACTIVATABLE: "compliance_deactivatable",
            }
            features = []
            device_index = device_index if device_index is not None else test_case.deviceIndex
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(
                test_case=test_case)

            for feature in cls.get_features(test_case, device_index, port_index, refresh):
                type_match = True
                for feature_type in feature_types:
                    if not feature.__getattr__(type_to_attr[feature_type]):
                        type_match = False
                        break
                    # end if
                # end for
                if type_match:
                    features.append(feature)
                # end if
            # end for
            return features
        # end def get_features_by_type
    # end class HIDppHelper
# end class FeatureSetTestUtils
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
