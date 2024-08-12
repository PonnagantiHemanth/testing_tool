#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.managedeactivatablefeaturesauthutils
:brief:  Helpers for Manage Deactivatable Features (based on authentication mechanism) feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pytestbox.base.basetestutils import CommonBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedManageDeactivatableFeaturesAuthTestUtils(CommonBaseTestUtils):
    """
    Test utils for Manage Deactivatable Features with authentication feature
    """
    class BitMapChecker(CommonBaseTestUtils.MessageChecker):
        """
        Helper to check BitMaps
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "all_bit": (cls.check_all_bit, 0),
                "manufacturing": (cls.check_manufacturing, 0),
                "compliance": (cls.check_compliance, 0),
                "gothard": (cls.check_gotthard, 0),
                "reserved": (cls.check_reserved, 0),
            }
        # end def get_default_check_map

        @classmethod
        def check_all_bit(cls, test_case, bitmap, expected):
            """
            Check AllBit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``ManageDeactivatableFeaturesAuth.BitMap``
            :param expected: AllBit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.all_bit)), expected=int(Numeral(expected)),
                                  msg="All bit in bit map is not as expected")
        # end def check_all_bit

        @classmethod
        def check_manufacturing(cls, test_case, bitmap, expected):
            """
            Check manufacturing bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``ManageDeactivatableFeaturesAuth.BitMap``
            :param expected: Manufacturing bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.manufacturing)), expected=int(Numeral(expected)),
                                  msg="Manufacturing bit in bit map is not as expected")
        # end def check_manufacturing

        @classmethod
        def check_compliance(cls, test_case, bitmap, expected):
            """
            Check compliance bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``ManageDeactivatableFeaturesAuth.BitMap``
            :param expected: Compliance bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.compliance)), expected=int(Numeral(expected)),
                                  msg="Compliance bit in bit map is not as expected")
        # end def check_compliance

        @classmethod
        def check_gotthard(cls, test_case, bitmap, expected):
            """
            Check Gotthard bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``ManageDeactivatableFeaturesAuth.BitMap``
            :param expected: Gotthard bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.gothard)), expected=int(Numeral(expected)),
                                  msg="Gotthard bit in bit map is not as expected")
        # end def check_gotthard

        @classmethod
        def check_reserved(cls, test_case, bitmap, expected):
            """
            Check reserved bits in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``ManageDeactivatableFeaturesAuth.BitMap``
            :param expected: Reserved field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.reserved)), expected=int(Numeral(expected)),
                                  msg="Reserved field in bit map is not as expected")
        # end def check_reserved
    # end class BitMapChecker

    class GetInfoResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        Test utils to check getInfo response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            bit_map_checker = SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker
            config = test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH
            return {
                "support_bit_map": (cls.check_support_bit_map, {
                    "all_bit": (bit_map_checker.check_all_bit, 0),
                    "manufacturing": (bit_map_checker.check_manufacturing, config.F_SupportManufacturing),
                    "compliance": (bit_map_checker.check_compliance, config.F_SupportCompliance),
                    "gothard": (bit_map_checker.check_gotthard, config.F_SupportGotthard),
                    "reserved": (bit_map_checker.check_reserved, 0),
                }),
                "persist_bit_map": (cls.check_persist_bit_map, {
                    "all_bit": (bit_map_checker.check_all_bit, 0),
                    "manufacturing": (bit_map_checker.check_manufacturing, config.F_PersistentActivationManufacturing),
                    "compliance": (bit_map_checker.check_compliance, config.F_PersistentActivationCompliance),
                    "gothard": (bit_map_checker.check_gotthard, config.F_PersistentActivationGotthard),
                    "reserved": (bit_map_checker.check_reserved, 0),
                }),
                "state_bit_map": (cls.check_state_bit_map, {
                    "all_bit": (bit_map_checker.check_all_bit, 0),
                    "manufacturing": (bit_map_checker.check_manufacturing, 0),
                    "compliance": (bit_map_checker.check_compliance, 0),
                    "gothard": (bit_map_checker.check_gotthard, 0),
                    "reserved": (bit_map_checker.check_reserved, 0),
                }),
            }
        # end def get_default_check_map

        @classmethod
        def check_support_bit_map(cls, test_case, message, expected):
            """
            Check support bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``ManageDeactivatableFeaturesAuth``
            :param expected: Expected bit map check map
            :type expected: ``dict``
            """
            SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_fields(
                test_case, message.support_bit_map, ManageDeactivatableFeaturesAuth.BitMap, expected)
        # end def check_support_bit_map

        @classmethod
        def check_persist_bit_map(cls, test_case, message, expected):
            """
            Check persist bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``ManageDeactivatableFeaturesAuth``
            :param expected: Expected bit map check map
            :type expected: ``dict``
            """
            SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_fields(
                test_case, message.persist_bit_map, ManageDeactivatableFeaturesAuth.BitMap, expected)
        # end def check_persist_bit_map

        @classmethod
        def check_state_bit_map(cls, test_case, message, expected):
            """
            Check state bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``ManageDeactivatableFeaturesAuth``
            :param expected: Expected bit map check map
            :type expected: ``dict``
            """
            SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_fields(
                test_case, message.state_bit_map, ManageDeactivatableFeaturesAuth.BitMap, expected)
        # end def check_state_persist_bit_map
    # end class GetInfoResponseChecker

    class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
        # See ``CommonBaseTestUtils.HIDppHelper``
        @classmethod
        def get_feature_interface(cls, test_case):
            """
            Get the feature interface

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Manage Deactivatable Features interface
            :rtype: ``FeatureInterface`` or ``ManageDeactivatableFeaturesAuthV0``
            """
            raise NotImplementedAbstractMethodError
        # end def get_feature_interface

        @classmethod
        def get_feature_response_queue(cls, test_case):
            """
            Get feature's response message queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Message queue for the feature's response
            :rtype: ``HidMessageQueue``
            """
            raise NotImplementedAbstractMethodError
        # end def feature_response_queue

        @classmethod
        def get_info(cls, test_case, device_index=None, port_index=None):
            """
            Send getInfo request

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: getInfo response
            :rtype: ``GetInfoResponse`` or ``ManageDeactivatableFeaturesGetInfoResponse``
            """
            raise NotImplementedAbstractMethodError
        # end def get_info

        @classmethod
        def get_disable_features_req(cls, test_case, disable_all=False, manufacturing=False, compliance=False,
                                     gotthard=False, device_index=None, port_index=None):
            """
            Get disable features with manage deactivatable features (based on authentication mechanism) feature request.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param disable_all: Disable all features - OPTIONAL
            :type disable_all: ``bool``
            :param manufacturing: Disable Manufacturing features - OPTIONAL
            :type manufacturing: ``bool``
            :param compliance: Disable Compliance features - OPTIONAL
            :type compliance: ``bool``
            :param gotthard: Disable Gotthard - OPTIONAL
            :type gotthard: ``bool``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: disableFeatures request
            :rtype: ``DisableFeaturesRequest`` or ``ManageDeactivatableFeaturesDisableFeaturesRequest``
            """
            raise NotImplementedAbstractMethodError
        # end def get_disable_features_req

        @classmethod
        def disable_features(cls, test_case, disable_all=False, manufacturing=False, compliance=False, gotthard=False,
                             device_index=None, port_index=None):
            """
            Disable features with manage deactivatable features (based on authentication mechanism) feature.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param disable_all: Disable all features - OPTIONAL
            :type disable_all: ``bool``
            :param manufacturing: Disable Manufacturing features - OPTIONAL
            :type manufacturing: ``bool``
            :param compliance: Disable Compliance features - OPTIONAL
            :type compliance: ``bool``
            :param gotthard: Disable Gotthard - OPTIONAL
            :type gotthard: ``bool``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: disableFeatures response
            :rtype: ``DisableFeaturesResponse`` or ``ManageDeactivatableFeaturesDisableFeaturesResponse``
            """
            raise NotImplementedAbstractMethodError
        # end def disable_features

        @classmethod
        def get_enable_features_req(cls, test_case, enable_all=False, manufacturing=False, compliance=False,
                                    gotthard=False, device_index=None, port_index=None):
            """
            Get enable features with manage deactivatable features (based on authentication mechanism) feature request.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param enable_all: Enable all features - OPTIONAL
            :type enable_all: ``bool``
            :param manufacturing: Enable Manufacturing features - OPTIONAL
            :type manufacturing: ``bool``
            :param compliance: Enable Compliance features - OPTIONAL
            :type compliance: ``bool``
            :param gotthard: Enable Gotthard - OPTIONAL
            :type gotthard: ``bool``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: enableFeatures request
            :rtype: ``EnableFeaturesRequest`` or ``ManageDeactivatableFeaturesEnableFeaturesRequest``
            """
            raise NotImplementedAbstractMethodError
        # end def get_enable_features_req

        @classmethod
        def enable_features(cls, test_case, enable_all=False, manufacturing=False, compliance=False, gotthard=False,
                            start_session=True, device_index=None, port_index=None):
            """
            Enable a group of features with the manage deactivatable features (based on authentication mechanism)
            feature.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param enable_all: Enable all features - OPTIONAL
            :type enable_all: ``bool``
            :param manufacturing: Enable Manufacturing features - OPTIONAL
            :type manufacturing: ``bool``
            :param compliance: Enable Compliance features - OPTIONAL
            :type compliance: ``bool``
            :param gotthard: Enable Gotthard - OPTIONAL
            :type gotthard: ``bool``
            :param start_session: Start required session(s) - OPTIONAL
            :type start_session: ``bool``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: enableFeatures response
            :rtype: ``EnableFeaturesResponse`` or ``ManageDeactivatableFeaturesEnableFeaturesResponse``
            """
            raise NotImplementedAbstractMethodError
        # end def enable_features

        class GetFeaturesReturnIndex:
            """
            Define return order of ``get_features`` method
            """
            MANUFACTURING = 0
            COMPLIANCE = 1
            GOTTHARD = 2
        # end class GetFeaturesReturnIndex

        @classmethod
        def get_features(cls, test_case, manufacturing=False, compliance=False, gotthard=False):
            """
            Get available features

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param manufacturing: Get manufacturing features
            :type manufacturing: ``bool``
            :param compliance: Get compliance features
            :type compliance: ``bool``
            :param gotthard: Get Gotthard features
            :type gotthard: ``bool``

            :return: Available features for each type
            :rtype: ``list``
            """
            raise NotImplementedAbstractMethodError
        # end def get_features

        @classmethod
        def check_enabled_features(cls, test_case, features, device_index=None, port_index=None):
            """
            Check features are enabled

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param features: List of features to check
            :type features: ``list``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            """
            raise NotImplementedAbstractMethodError
        # end def check_enabled_features

        @classmethod
        def check_disabled_features(cls, test_case, features, device_index=None, port_index=None):
            """
            Check features are disabled

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param features: List of features to check
            :type features: ``list``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            """
            raise NotImplementedAbstractMethodError
        # end def check_disabled_features

        @classmethod
        def check_state(cls, test_case, expected_state=None, device_index=None, port_index=None):
            """
            Check deactivatable features state

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param expected_state: Expected state
            :type expected_state: ``ManageDeactivatableFeaturesAuth.BitMap``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            """
            get_info_resp = cls.get_info(test_case, device_index, port_index)

            check_map = SharedManageDeactivatableFeaturesAuthTestUtils.GetInfoResponseChecker.get_default_check_map(
                test_case)
            if expected_state is not None:
                check_map["state_bit_map"] = (
                    SharedManageDeactivatableFeaturesAuthTestUtils.GetInfoResponseChecker.check_state_bit_map,
                    {
                        "all_bit": (SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_all_bit,
                                    expected_state.all_bit),
                        "manufacturing": (
                            SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_manufacturing,
                            expected_state.manufacturing),
                        "compliance": (SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_compliance,
                                       expected_state.compliance),
                        "gothard": (SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_gotthard,
                                    expected_state.gothard),
                        "reserved": (SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_reserved,
                                     expected_state.reserved),
                    }
                )
            # end if

            SharedManageDeactivatableFeaturesAuthTestUtils.GetInfoResponseChecker.check_fields(
                test_case, get_info_resp, cls.get_feature_interface(test_case).get_info_response_cls, check_map)
        # end def check_state

        @classmethod
        def check_manufacturing_enabled(cls, test_case):
            """
            Check manufacturing features are enabled

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            manufacturing_features = cls.get_features(test_case, manufacturing=True)[
                cls.GetFeaturesReturnIndex.MANUFACTURING]
            cls.check_enabled_features(test_case, manufacturing_features)
        # end def check_manufacturing_enabled

        @classmethod
        def check_manufacturing_disabled(cls, test_case):
            """
            Check manufacturing features are disabled

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            manufacturing_features = cls.get_features(test_case, manufacturing=True)[
                cls.GetFeaturesReturnIndex.MANUFACTURING]
            cls.check_disabled_features(test_case, manufacturing_features)
        # end def check_manufacturing_disabled

        @classmethod
        def check_compliance_enabled(cls, test_case):
            """
            Check compliance features are enabled

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            compliance_features = cls.get_features(test_case, compliance=True)[cls.GetFeaturesReturnIndex.COMPLIANCE]
            cls.check_enabled_features(test_case, compliance_features)
        # end def check_compliance_enabled

        @classmethod
        def check_compliance_disabled(cls, test_case):
            """
            Check compliance features are disabled

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            compliance_features = cls.get_features(test_case, compliance=True)[cls.GetFeaturesReturnIndex.COMPLIANCE]
            cls.check_disabled_features(test_case, compliance_features)
        # end def check_compliance_disabled
    # end class HIDppHelper

    class NvsHelper(CommonBaseTestUtils.NvsHelper):
        """
        See ``CommonBaseTestUtils.NvsHelper``
        """
        @classmethod
        def check_state(cls, test_case, expected_state=None):
            """
            Check deactivatable features state

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param expected_state: Expected state
            :type expected_state: ``ManageDeactivatableFeaturesAuth.BitMap``
            """
            if expected_state is None:
                expected_state = ManageDeactivatableFeaturesAuth.BitMap()
            # end if

            test_case.memory_manager.read_nvs()
            nvs_states = test_case.memory_manager.get_chunks_by_name('NVS_X1E02_STATE_ID')
            if len(nvs_states) > 0:
                current_state = HexList(nvs_states[-1])
            else:
                # NVS chunk not found: default value is Gotthard disabled
                current_state = HexList('00')
            # end if
            SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_fields(
                test_case,
                ManageDeactivatableFeaturesAuth.BitMap.fromHexList(HexList(current_state)),
                ManageDeactivatableFeaturesAuth.BitMap,
                {
                    "all_bit": (SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_all_bit,
                                expected_state.all_bit),
                    "manufacturing": (SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_manufacturing,
                                      expected_state.manufacturing),
                    "compliance": (SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_compliance,
                                   expected_state.compliance),
                    "gothard": (SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_gotthard,
                                expected_state.gothard),
                    "reserved": (SharedManageDeactivatableFeaturesAuthTestUtils.BitMapChecker.check_reserved,
                                 expected_state.reserved),
                }
            )
        # end def check_state

        @classmethod
        def force_state(cls, test_case, state=None):
            """
            Force deactivatable features state

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param state: State to force. Default: Persistent features will be forced. - OPTIONAL
            :type state: ``ManageDeactivatableFeaturesAuth.BitMap``
            """
            if state is None:
                config = test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH
                state = ManageDeactivatableFeaturesAuth.BitMap(
                    manufacturing=config.F_PersistentActivationManufacturing,
                    compliance=config.F_PersistentActivationCompliance,
                    gothard=config.F_PersistentActivationGotthard)
            # end if
            if test_case.memory_manager is not None:
                test_case.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_X1E02_STATE_ID', data=HexList(state))
                test_case.memory_manager.load_nvs()
            # end if
        # end def force_state
    # end class NvsHelper
# end class SharedManageDeactivatableFeaturesAuthTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
