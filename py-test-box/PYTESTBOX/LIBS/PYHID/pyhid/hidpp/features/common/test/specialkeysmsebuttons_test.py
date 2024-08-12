#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.feature.common.test.specialkeysmsebuttons_test
:brief: HID++ 2.0 ``SpecialKeysMSEButtons`` test module
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/05/10
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.specialkeysmsebuttons import AnalyticsKeyEventsV4toV6
from pyhid.hidpp.features.common.specialkeysmsebuttons import DivertedButtonsEvent
from pyhid.hidpp.features.common.specialkeysmsebuttons import DivertedRawMouseXYEventV2toV6
from pyhid.hidpp.features.common.specialkeysmsebuttons import DivertedRawWheelV5toV6
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCapabilitiesV6
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCapabilitiesV6Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfo
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV0Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV1Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV2Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV3Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV4Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV5toV6Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReporting
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReportingV0Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReportingV1Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReportingV2Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReportingV3Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReportingV4Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReportingV5toV6Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCount
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCountResponse
from pyhid.hidpp.features.common.specialkeysmsebuttons import ResetAllCidReportSettingsV6
from pyhid.hidpp.features.common.specialkeysmsebuttons import ResetAllCidReportSettingsV6Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV0
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV0Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV1
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV1Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV2
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV2Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV3
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV3Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV4
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV4Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV5ToV6Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV5toV6
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtons
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsFactory
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsV0
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsV1
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsV2
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsV3
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsV4
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsV5
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsV6
from pyhid.hidpp.features.test.root_test import RootTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SpecialKeysMSEButtonsInstantiationTestCase(TestCase):
    """
    Test ``SpecialKeysMSEButtons`` testing classes instantiations
    """

    @staticmethod
    def test_special_key_mse_buttons():
        """
        Test ``SpecialKeysMSEButtons`` class instantiation
        """
        my_class = SpecialKeysMSEButtons(device_index=0,
                                         feature_index=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_special_key_mse_buttons

    @staticmethod
    def test_get_count():
        """
        Test ``GetCount`` class instantiation
        """
        my_class = GetCount(device_index=0,
                            feature_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_count

    @staticmethod
    def test_get_cid_info():
        """
        Test ``GetCidInfo`` class instantiation
        """
        my_class = GetCidInfo(device_index=0,
                              feature_index=0,
                              ctrl_id_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_cid_info

    @staticmethod
    def test_get_cid_reporting():
        """
        Test ``GetCidReporting`` class instantiation
        """
        my_class = GetCidReporting(device_index=0,
                                   feature_index=0,
                                   ctrl_id=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_cid_reporting

    @staticmethod
    def test_set_cid_reporting_v0():
        """
        Test ``SetCidReportingV0`` class instantiation
        """
        my_class = SetCidReportingV0(device_index=0,
                                     feature_index=0,
                                     ctrl_id=0,
                                     persist_valid=False,
                                     persist=False,
                                     divert_valid=False,
                                     divert=False)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_cid_reporting_v0

    @staticmethod
    def test_set_cid_reporting_v1():
        """
        Test ``SetCidReportingV1`` class instantiation
        """
        my_class = SetCidReportingV1(device_index=0,
                                     feature_index=0,
                                     ctrl_id=0,
                                     persist_valid=False,
                                     persist=False,
                                     divert_valid=False,
                                     divert=False,
                                     remap=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v1

    @staticmethod
    def test_set_cid_reporting_v2():
        """
        Test ``SetCidReportingV2`` class instantiation
        """
        my_class = SetCidReportingV2(device_index=0,
                                     feature_index=0,
                                     ctrl_id=0,
                                     raw_xy_valid=False,
                                     raw_xy=False,
                                     persist_valid=False,
                                     persist=False,
                                     divert_valid=False,
                                     divert=False,
                                     remap=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v2

    @staticmethod
    def test_set_cid_reporting_v3():
        """
        Test ``SetCidReportingV3`` class instantiation
        """
        my_class = SetCidReportingV3(device_index=0,
                                     feature_index=0,
                                     ctrl_id=0,
                                     force_raw_xy_valid=False,
                                     force_raw_xy=False,
                                     raw_xy_valid=False,
                                     raw_xy=False,
                                     persist_valid=False,
                                     persist=False,
                                     divert_valid=False,
                                     divert=False,
                                     remap=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v3

    @staticmethod
    def test_set_cid_reporting_v4():
        """
        Test ``SetCidReportingV4`` class instantiation
        """
        my_class = SetCidReportingV4(device_index=0,
                                     feature_index=0,
                                     ctrl_id=0,
                                     force_raw_xy_valid=False,
                                     force_raw_xy=False,
                                     raw_xy_valid=False,
                                     raw_xy=False,
                                     persist_valid=False,
                                     persist=False,
                                     divert_valid=False,
                                     divert=False,
                                     remap=0,
                                     analytics_key_event_valid=False,
                                     analytics_key_event=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v4

    @staticmethod
    def test_set_cid_reporting_v5_to_v6():
        """
        Test ``SetCidReportingV5toV6`` class instantiation
        """
        my_class = SetCidReportingV5toV6(device_index=0,
                                         feature_index=0,
                                         ctrl_id=0,
                                         force_raw_xy_valid=False,
                                         force_raw_xy=False,
                                         raw_xy_valid=False,
                                         raw_xy=False,
                                         persist_valid=False,
                                         persist=False,
                                         divert_valid=False,
                                         divert=False,
                                         remap=0,
                                         raw_wheel_valid=False,
                                         raw_wheel=False,
                                         analytics_key_event_valid=False,
                                         analytics_key_event=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCidReportingV5toV6(device_index=0,
                                         feature_index=0,
                                         ctrl_id=0xFFFF,
                                         force_raw_xy_valid=True,
                                         force_raw_xy=True,
                                         raw_xy_valid=True,
                                         raw_xy=True,
                                         persist_valid=True,
                                         persist=True,
                                         divert_valid=True,
                                         divert=True,
                                         remap=0xFFFF,
                                         raw_wheel_valid=True,
                                         raw_wheel=True,
                                         analytics_key_event_valid=True,
                                         analytics_key_event=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v5_to_v6
    
    @staticmethod
    def test_get_capabilities_v6():
        """
        Test ``GetCapabilitiesV6`` class instantiation
        """
        my_class = GetCapabilitiesV6(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities
    
    @staticmethod
    def test_reset_all_cid_report_settings_v6():
        """
        Test ``ResetAllCidReportSettingsV6`` class instantiation
        """
        my_class = ResetAllCidReportSettingsV6(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_reset_all_cid_report_settings_v6

    @staticmethod
    def test_get_count_response():
        """
        Test ``GetCountResponse`` class instantiation
        """
        my_class = GetCountResponse(device_index=0,
                                    feature_index=0,
                                    count=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_count_response

    @staticmethod
    def test_get_cid_info_v0_response():
        """
        Test ``GetCidInfoV0Response`` class instantiation
        """
        my_class = GetCidInfoV0Response(device_index=0,
                                        feature_index=0,
                                        ctrl_id=0,
                                        task_id=0,
                                        persist=False,
                                        divert=False,
                                        reprog=False,
                                        fn_tog=False,
                                        hot_key=False,
                                        fkey=False,
                                        mouse=False,
                                        fkey_pos=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_info_v0_response

    @staticmethod
    def test_get_cid_info_v1_response():
        """
        Test ``GetCidInfoV1Response`` class instantiation
        """
        my_class = GetCidInfoV1Response(device_index=0,
                                        feature_index=0,
                                        ctrl_id=0,
                                        task_id=0,
                                        virtual=False,
                                        persist=False,
                                        divert=False,
                                        reprog=False,
                                        fn_tog=False,
                                        hot_key=False,
                                        fkey=False,
                                        mouse=False,
                                        fkey_pos=0,
                                        group=0,
                                        gmask=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_info_v1_response

    @staticmethod
    def test_get_cid_info_v2_response():
        """
        Test ``GetCidInfoV2Response`` class instantiation
        """
        my_class = GetCidInfoV2Response(device_index=0,
                                        feature_index=0,
                                        ctrl_id=0,
                                        task_id=0,
                                        virtual=False,
                                        persist=False,
                                        divert=False,
                                        reprog=False,
                                        fn_tog=False,
                                        hot_key=False,
                                        fkey=False,
                                        mouse=False,
                                        fkey_pos=0,
                                        group=0,
                                        gmask=0,
                                        raw_xy=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_info_v2_response

    @staticmethod
    def test_get_cid_info_v3_response():
        """
        Test ``GetCidInfoV3Response`` class instantiation
        """
        my_class = GetCidInfoV3Response(device_index=0,
                                        feature_index=0,
                                        ctrl_id=0,
                                        task_id=0,
                                        virtual=False,
                                        persist=False,
                                        divert=False,
                                        reprog=False,
                                        fn_tog=False,
                                        hot_key=False,
                                        fkey=False,
                                        mouse=False,
                                        fkey_pos=0,
                                        group=0,
                                        gmask=0,
                                        force_raw_xy=False,
                                        raw_xy=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_info_v3_response

    @staticmethod
    def test_get_cid_info_v4_response():
        """
        Test ``GetCidInfoV4Response`` class instantiation
        """
        my_class = GetCidInfoV4Response(device_index=0,
                                        feature_index=0,
                                        ctrl_id=0,
                                        task_id=0,
                                        virtual=False,
                                        persist=False,
                                        divert=False,
                                        reprog=False,
                                        fn_tog=False,
                                        hot_key=False,
                                        fkey=False,
                                        mouse=False,
                                        fkey_pos=0,
                                        group=0,
                                        gmask=0,
                                        analytics_key_events=False,
                                        force_raw_xy=False,
                                        raw_xy=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_info_v4_response

    @staticmethod
    def test_get_cid_info_v5_to_v6_response():
        """
        Test ``GetCidInfoV5toV6Response`` class instantiation
        """
        my_class = GetCidInfoV5toV6Response(device_index=0,
                                            feature_index=0,
                                            ctrl_id=0,
                                            task_id=0,
                                            virtual=False,
                                            persist=False,
                                            divert=False,
                                            reprog=False,
                                            fn_tog=False,
                                            hot_key=False,
                                            fkey=False,
                                            mouse=False,
                                            fkey_pos=0,
                                            group=0,
                                            gmask=0,
                                            raw_wheel=False,
                                            analytics_key_events=False,
                                            force_raw_xy=False,
                                            raw_xy=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCidInfoV5toV6Response(device_index=0,
                                            feature_index=0,
                                            ctrl_id=0xFFFF,
                                            task_id=0xFFFF,
                                            virtual=True,
                                            persist=True,
                                            divert=True,
                                            reprog=True,
                                            fn_tog=True,
                                            hot_key=True,
                                            fkey=True,
                                            mouse=True,
                                            fkey_pos=0xFF,
                                            group=0xFF,
                                            gmask=0xFF,
                                            raw_wheel=True,
                                            analytics_key_events=True,
                                            force_raw_xy=True,
                                            raw_xy=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_info_v5_to_v6_response

    @staticmethod
    def test_get_cid_reporting_v0_response():
        """
        Test ``GetCidReportingV0Response`` class instantiation
        """
        my_class = GetCidReportingV0Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             persist=False,
                                             divert=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_reporting_v0_response

    @staticmethod
    def test_get_cid_reporting_v1_response():
        """
        Test ``GetCidReportingV1Response`` class instantiation
        """
        my_class = GetCidReportingV1Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             persist=False,
                                             divert=False,
                                             remap=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_reporting_v1_response

    @staticmethod
    def test_get_cid_reporting_v2_response():
        """
        Test ``GetCidReportingV2Response`` class instantiation
        """
        my_class = GetCidReportingV2Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             raw_xy=False,
                                             persist=False,
                                             divert=False,
                                             remap=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_reporting_v2_response

    @staticmethod
    def test_get_cid_reporting_v3_response():
        """
        Test ``GetCidReportingV3Response`` class instantiation
        """
        my_class = GetCidReportingV3Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             force_raw_xy=False,
                                             raw_xy=False,
                                             persist=False,
                                             divert=False,
                                             remap=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_reporting_v3_response

    @staticmethod
    def test_get_cid_reporting_v4_response():
        """
        Test ``GetCidReportingV4Response`` class instantiation
        """
        my_class = GetCidReportingV4Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             force_raw_xy=False,
                                             raw_xy=False,
                                             persist=False,
                                             divert=False,
                                             remap=0,
                                             analytics_key_evt=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_reporting_v4_response

    @staticmethod
    def test_get_cid_reporting_v5_to_v6_response():
        """
        Test ``GetCidReportingV5toV6Response`` class instantiation
        """
        my_class = GetCidReportingV5toV6Response(device_index=0,
                                                 feature_index=0,
                                                 ctrl_id=0,
                                                 force_raw_xy=False,
                                                 raw_xy=False,
                                                 persist=False,
                                                 divert=False,
                                                 remap=0,
                                                 raw_wheel=False,
                                                 analytics_key_evt=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCidReportingV5toV6Response(device_index=0,
                                                 feature_index=0,
                                                 ctrl_id=0xFFFF,
                                                 force_raw_xy=True,
                                                 raw_xy=True,
                                                 persist=True,
                                                 divert=True,
                                                 remap=0xFFFF,
                                                 raw_wheel=True,
                                                 analytics_key_evt=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_cid_reporting_v5_to_v6_response

    @staticmethod
    def test_set_cid_reporting_v0_response():
        """
        Test ``SetCidReportingV0Response`` class instantiation
        """
        my_class = SetCidReportingV0Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             persist_valid=False,
                                             persist=False,
                                             divert_valid=False,
                                             divert=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v0_response

    @staticmethod
    def test_set_cid_reporting_v1_response():
        """
        Test ``SetCidReportingV1Response`` class instantiation
        """
        my_class = SetCidReportingV1Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             persist_valid=False,
                                             persist=False,
                                             divert_valid=False,
                                             divert=False,
                                             remap=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v1_response

    @staticmethod
    def test_set_cid_reporting_v2_response():
        """
        Test ``SetCidReportingV2Response`` class instantiation
        """
        my_class = SetCidReportingV2Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             raw_xy_valid=False,
                                             raw_xy=False,
                                             persist_valid=False,
                                             persist=False,
                                             divert_valid=False,
                                             divert=False,
                                             remap=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v2_response

    @staticmethod
    def test_set_cid_reporting_v3_response():
        """
        Test ``SetCidReportingV3Response`` class instantiation
        """
        my_class = SetCidReportingV3Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             force_raw_xy_valid=False,
                                             force_raw_xy=False,
                                             raw_xy_valid=False,
                                             raw_xy=False,
                                             persist_valid=False,
                                             persist=False,
                                             divert_valid=False,
                                             divert=False,
                                             remap=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v3_response

    @staticmethod
    def test_set_cid_reporting_v4_response():
        """
        Test ``SetCidReportingV4Response`` class instantiation
        """
        my_class = SetCidReportingV4Response(device_index=0,
                                             feature_index=0,
                                             ctrl_id=0,
                                             force_raw_xy_valid=False,
                                             force_raw_xy=False,
                                             raw_xy_valid=False,
                                             raw_xy=False,
                                             persist_valid=False,
                                             persist=False,
                                             divert_valid=False,
                                             divert=False,
                                             remap=0,
                                             analytics_key_event_valid=False,
                                             analytics_key_event=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v4_response

    @staticmethod
    def test_set_cid_reporting_v5_to_v6_response():
        """
        Test ``SetCidReportingV5ToV6Response`` class instantiation
        """
        my_class = SetCidReportingV5ToV6Response(device_index=0,
                                                 feature_index=0,
                                                 ctrl_id=0,
                                                 force_raw_xy_valid=False,
                                                 force_raw_xy=False,
                                                 raw_xy_valid=False,
                                                 raw_xy=False,
                                                 persist_valid=False,
                                                 persist=False,
                                                 divert_valid=False,
                                                 divert=False,
                                                 remap=0,
                                                 raw_wheel_valid=False,
                                                 raw_wheel=False,
                                                 analytics_key_event_valid=False,
                                                 analytics_key_event=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCidReportingV5ToV6Response(device_index=0,
                                                 feature_index=0,
                                                 ctrl_id=0xFFFF,
                                                 force_raw_xy_valid=True,
                                                 force_raw_xy=True,
                                                 raw_xy_valid=True,
                                                 raw_xy=True,
                                                 persist_valid=True,
                                                 persist=True,
                                                 divert_valid=True,
                                                 divert=True,
                                                 remap=0xFFFF,
                                                 raw_wheel_valid=True,
                                                 raw_wheel=True,
                                                 analytics_key_event_valid=True,
                                                 analytics_key_event=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_cid_reporting_v5_to_v6_response

    @staticmethod
    def test_get_capabilities_v6_response():
        """
        Test ``GetCapabilitiesV6Response`` class instantiation
        """
        my_class = GetCapabilitiesV6Response(device_index=0, feature_index=0, reset_all_cid_report_settings_flag=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesV6Response(device_index=0xFF, feature_index=0xFF,
                                             reset_all_cid_report_settings_flag=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_v6_response

    @staticmethod
    def test_get_capabilities_flags():
        """
        Test ``GetCapabilitiesV6Response.Flags`` class instantiation
        """
        my_class = GetCapabilitiesV6Response.Flags(reset_all_cid_report_settings_flag=False)
    # end def test_get_capabilities_flags

    @staticmethod
    def test_reset_all_cid_report_settings_v6_response():
        """
        Test ``ResetAllCidReportSettingsV6Response`` class instantiation
        """
        my_class = ResetAllCidReportSettingsV6Response(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ResetAllCidReportSettingsV6Response(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_reset_all_cid_report_settings_v6_response

    @staticmethod
    def test_diverted_button_event():
        """
        Test ``DivertButtonEvent`` class instantiation
        """
        my_class = DivertedButtonsEvent(device_index=0,
                                        feature_index=0,
                                        ctrl_id_1=0,
                                        ctrl_id_2=0,
                                        ctrl_id_3=0,
                                        ctrl_id_4=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_diverted_button_event

    @staticmethod
    def test_diverted_raw_mouse_xy_event_v2_to_v6():
        """
        Test ``DivertedRawMouseXYEventV2toV6`` class instantiation
        """
        my_class = DivertedRawMouseXYEventV2toV6(device_index=0,
                                                 feature_index=0,
                                                 dx=0,
                                                 dy=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_diverted_raw_mouse_xy_event_v2_to_v6

    @staticmethod
    def test_analytics_key_event_v4_to_v6():
        """
        Test ``AnalyticsKeyEventsV4toV6`` class instantiation
        """
        my_class = AnalyticsKeyEventsV4toV6(device_index=0,
                                            feature_index=0,
                                            ctrl_id_1=0,
                                            event_1=0,
                                            ctrl_id_2=0,
                                            event_2=0,
                                            ctrl_id_3=0,
                                            event_3=0,
                                            ctrl_id_4=0,
                                            event_4=0,
                                            ctrl_id_5=0,
                                            event_5=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_analytics_key_event_v4_to_v6

    @staticmethod
    def test_diverted_raw_wheel_v5_to_v6():
        """
        Test ``DivertedRawWheelV5toV6`` class instantiation
        """
        my_class = DivertedRawWheelV5toV6(device_index=0, feature_index=0, resolution=0, periods=0, delta_v=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DivertedRawWheelV5toV6(device_index=0xFF, feature_index=0xFF, resolution=1, periods=0xF,
                                          delta_v=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_diverted_raw_wheel_v5_to_v6
# end class SpecialKeysMSEButtonsInstantiationTestCase


class SpecialKeysMSEButtonsTestCase(TestCase):
    """
    Test ``SpecialKeysMSEButtons`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": SpecialKeysMSEButtonsV0,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_cid_info_cls": GetCidInfo,
                    "get_cid_reporting_cls": GetCidReporting,
                    "set_cid_reporting_cls": SetCidReportingV0,
                    "get_count_response_cls": GetCountResponse,
                    "get_cid_info_response_cls": GetCidInfoV0Response,
                    "get_cid_reporting_response_cls": GetCidReportingV0Response,
                    "set_cid_reporting_response_cls": SetCidReportingV0Response,
                },
                "max_function_index": 3
            },
            1: {
                "cls": SpecialKeysMSEButtonsV1,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_cid_info_cls": GetCidInfo,
                    "get_cid_reporting_cls": GetCidReporting,
                    "set_cid_reporting_cls": SetCidReportingV1,
                    "get_count_response_cls": GetCountResponse,
                    "get_cid_info_response_cls": GetCidInfoV1Response,
                    "get_cid_reporting_response_cls": GetCidReportingV1Response,
                    "set_cid_reporting_response_cls": SetCidReportingV1Response,
                },
                "max_function_index": 3
            },
            2: {
                "cls": SpecialKeysMSEButtonsV2,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_cid_info_cls": GetCidInfo,
                    "get_cid_reporting_cls": GetCidReporting,
                    "set_cid_reporting_cls": SetCidReportingV2,
                    "get_count_response_cls": GetCountResponse,
                    "get_cid_info_response_cls": GetCidInfoV2Response,
                    "get_cid_reporting_response_cls": GetCidReportingV2Response,
                    "set_cid_reporting_response_cls": SetCidReportingV2Response,
                },
                "max_function_index": 3
            },
            3: {
                "cls": SpecialKeysMSEButtonsV3,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_cid_info_cls": GetCidInfo,
                    "get_cid_reporting_cls": GetCidReporting,
                    "set_cid_reporting_cls": SetCidReportingV3,
                    "get_count_response_cls": GetCountResponse,
                    "get_cid_info_response_cls": GetCidInfoV3Response,
                    "get_cid_reporting_response_cls": GetCidReportingV3Response,
                    "set_cid_reporting_response_cls": SetCidReportingV3Response,
                },
                "max_function_index": 3
            },
            4: {
                "cls": SpecialKeysMSEButtonsV4,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_cid_info_cls": GetCidInfo,
                    "get_cid_reporting_cls": GetCidReporting,
                    "set_cid_reporting_cls": SetCidReportingV4,
                    "get_count_response_cls": GetCountResponse,
                    "get_cid_info_response_cls": GetCidInfoV4Response,
                    "get_cid_reporting_response_cls": GetCidReportingV4Response,
                    "set_cid_reporting_response_cls": SetCidReportingV4Response,
                },
                "max_function_index": 3
            },
            5: {
                "cls": SpecialKeysMSEButtonsV5,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_cid_info_cls": GetCidInfo,
                    "get_cid_reporting_cls": GetCidReporting,
                    "set_cid_reporting_cls": SetCidReportingV5toV6,
                    "get_count_response_cls": GetCountResponse,
                    "get_cid_info_response_cls": GetCidInfoV5toV6Response,
                    "get_cid_reporting_response_cls": GetCidReportingV5toV6Response,
                    "set_cid_reporting_response_cls": SetCidReportingV5ToV6Response,
                },
                "max_function_index": 3
            },
            6: {
                "cls": SpecialKeysMSEButtonsV6,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_cid_info_cls": GetCidInfo,
                    "get_cid_reporting_cls": GetCidReporting,
                    "set_cid_reporting_cls": SetCidReportingV5toV6,
                    "get_capabilities_cls": GetCapabilitiesV6,
                    "reset_all_cid_report_settings_cls": ResetAllCidReportSettingsV6,
                    "get_count_response_cls": GetCountResponse,
                    "get_cid_info_response_cls": GetCidInfoV5toV6Response,
                    "get_cid_reporting_response_cls": GetCidReportingV5toV6Response,
                    "set_cid_reporting_response_cls": SetCidReportingV5ToV6Response,
                    "get_capabilities_response_cls": GetCapabilitiesV6Response,
                    "reset_all_cid_report_settings_response_cls": ResetAllCidReportSettingsV6Response,
                },
                "max_function_index": 5
            },
        }
    # end def setUpClass

    def test_special_keys_mouse_buttons_factory(self):
        """
        Test Special Keys Mouse Buttons Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(SpecialKeysMSEButtonsFactory.create(version)), expected["cls"])
        # end for loop

    # end def test_special_keys_mouse_buttons_factory

    def test_special_keys_mouse_buttons_factory_version_out_of_range(self):
        """
        Test Special Keys Mouse Buttons Factory with out of range versions
        """
        for version in [7, 8]:
            with self.assertRaises(KeyError):
                SpecialKeysMSEButtonsFactory.create(version)
            # end with
        # end for
    # end def test_special_keys_mouse_buttons_factory_version_out_of_range

    def test_special_keys_mouse_buttons_factory_interfaces(self):
        """
        Check Special Keys Mouse Buttons Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            special_keys_mouse_buttons = SpecialKeysMSEButtonsFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(special_keys_mouse_buttons, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(special_keys_mouse_buttons, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_special_keys_mouse_buttons_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            special_keys_mouse_buttons = SpecialKeysMSEButtonsFactory.create(version)
            self.assertEqual(special_keys_mouse_buttons.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class SpecialKeysMSEButtonsTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
