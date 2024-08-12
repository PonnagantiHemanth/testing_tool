#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.managedeactivatablefeaturesutils
:brief:  Helpers for Manage Deactivatable Features feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/10/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import time

from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ManageDeactivatableFeaturesTestUtils(DeviceBaseTestUtils):
    """
    Test utils for Manage Deactivatable Features feature
    """
    class NvsHelper(DeviceBaseTestUtils.NvsHelper):
        """
        Test utils to manage NVS
        """
        @staticmethod
        def set_counters(test_case, manuf_hidpp_counter=None, compl_hidpp_counter=None, gothard_counter=None):
            """
            Set counters in NVS

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param manuf_hidpp_counter: Manufacturing counter value. The memory value is preserved if set to None.
            :type manuf_hidpp_counter: ``int``
            :param compl_hidpp_counter: Compliance counter value. The memory value is preserved if set to None.
            :type compl_hidpp_counter: ``int``
            :param gothard_counter: Gothard counter value. The memory value is preserved if set to None.
            :type gothard_counter: ``int``
            """
            if test_case.memory_manager is not None:
                if None in [manuf_hidpp_counter, compl_hidpp_counter, gothard_counter]:
                    test_case.memory_manager.read_nvs()
                    last_conn_cntr_chunk = test_case.memory_manager.get_active_chunk_by_name('NVS_X1E01_CONN_CNTR_ID')
                    nvs_manuf_counter = last_conn_cntr_chunk.disable_manufacturing_registers_counter
                    nvs_compl_counter = last_conn_cntr_chunk.disable_compliance_registers_counter
                    nvs_gothard_counter = last_conn_cntr_chunk.disable_gothard_counter
                    manuf_hidpp_counter = manuf_hidpp_counter if manuf_hidpp_counter is not None else nvs_manuf_counter
                    compl_hidpp_counter = compl_hidpp_counter if compl_hidpp_counter is not None else nvs_compl_counter
                    gothard_counter = gothard_counter if gothard_counter is not None else nvs_gothard_counter
                # end if
                new_data = HexList([manuf_hidpp_counter, compl_hidpp_counter, gothard_counter])
                test_case.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_X1E01_CONN_CNTR_ID', data=new_data)
                test_case.memory_manager.load_nvs()
                # Let time for reset to complete. It will decrement counters by 1
                time.sleep(1.0)
            # end if
        # end def set_counters

        @staticmethod
        def check_counters(test_case, expected_manuf_counter=None, expected_compl_counter=None,
                           expected_gothard_counter=None):
            """
            Check counters values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param expected_manuf_counter: Expected value for manufacturing counter
            :type expected_manuf_counter: ``int``
            :param expected_compl_counter: Expected value for manufacturing counter
            :type expected_compl_counter: ``int``
            :param expected_gothard_counter: Expected value for manufacturing counter
            :type expected_gothard_counter: ``int``
            """
            test_case.memory_manager.read_nvs()
            conn_counters_chunk_list = test_case.memory_manager.get_active_chunk_by_name('NVS_X1E01_CONN_CNTR_ID')

            if expected_manuf_counter is not None:
                obt = int(Numeral(conn_counters_chunk_list.disable_manufacturing_registers_counter))
                exp = int(Numeral(expected_manuf_counter))
                test_case.assertEqual(
                    obtained=obt,
                    expected=exp,
                    msg=f"Manufacturing counter value in NVS {obt} differs from the expected value {exp}")
            # end if
            if expected_compl_counter is not None:
                obt = int(Numeral(conn_counters_chunk_list.disable_compliance_registers_counter))
                exp = int(Numeral(expected_compl_counter))
                test_case.assertEqual(
                    obtained=obt,
                    expected=exp,
                    msg=f"Compliance counter value in NVS {obt} differs from the expected value {exp}")
            # end if
            if expected_gothard_counter is not None:
                obt = int(Numeral(conn_counters_chunk_list.disable_gothard_counter))
                exp = int(Numeral(expected_gothard_counter))
                test_case.assertEqual(
                    obtained=obt,
                    expected=exp,
                    msg = f"Gothard counter value in NVS {obt} differs from the expected value {exp}")
            # end if
        # end def check_counters
    # end class NvsHelper

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        """
        HID++ helper class
        """
        @staticmethod
        def set_counters(test_case, device_index, feature, feature_index, manuf_hidpp_counter=None,
                         compl_hidpp_counter=None, gothard_counter=None):
            """
            Helper to set counters

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index
            :type device_index: ``int``
            :param feature: Manage Deactivatable Features feature
            :type feature: ``ManageDeactivatableFeaturesInterface``
            :param feature_index: Manage Deactivatable Features feature index
            :type feature_index: ``int``
            :param manuf_hidpp_counter: Manufacturing counter value. Do not set if None.
            :type manuf_hidpp_counter: ``int``
            :param compl_hidpp_counter: Compliance counter value. Do not set if None.
            :type compl_hidpp_counter: ``int``
            :param gothard_counter: Gothard counter value. Do not set if None.
            :type gothard_counter: ``int``
            """
            set_counters_req = feature.set_counters_cls(
                device_index,
                feature_index,
                gothard=True if gothard_counter is not None else False,
                compl_hidpp=True if compl_hidpp_counter is not None else False,
                manuf_hidpp=True if manuf_hidpp_counter is not None else False,
                manuf_hidpp_counter=manuf_hidpp_counter if manuf_hidpp_counter is not None else 0xFF,
                compl_hidpp_counter=compl_hidpp_counter if compl_hidpp_counter is not None else 0xFF,
                gothard_counter=gothard_counter if gothard_counter is not None else 0xFF
            )

            return test_case.send_report_wait_response(
                report=set_counters_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature.set_counters_response_cls)
        # end def set_counters
    # end class HIDppHelper

    class GetCountersResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check Get Counter response
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
                "all_bit": (cls.check_support_bit_map_all, 0),
                "gothard": None,
                "compl_hidpp": None,
                "manuf_hidpp": None,
                "support_bitmap_reserved": (cls.check_support_bit_map_reserved, 0),
                "manuf_hidpp_counter": (
                    cls.check_manuf_hidpp_counter_in_range,
                    (0, test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter)
                ),
                "compl_hidpp_counter": (
                    cls.check_compl_hidpp_counter_in_range,
                    (0, test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter)
                ),
                "gothard_counter": (
                    cls.check_gotthard_counter_in_range,
                    (0, test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter)
                ),
            }
        # end def get_default_check_map

        @staticmethod
        def check_support_bit_map_all(test_case, message, expected):
            """
            Check Support Bit Map All bit value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            :param expected: All bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.all_bit)), expected=expected,
                                  msg="Support Bit Map All bit is not as expected")
        # end def check_support_bit_map_all

        @staticmethod
        def check_support_bit_map_reserved(test_case, message, expected):
            """
            Check Support Bit Map reserved value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            :param expected: Reserved field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.support_bitmap_reserved)), expected=expected,
                                  msg="Support Bit Map reserved is not as expected")
        # end def check_support_bit_map_reserved

        @staticmethod
        def check_manuf_hidpp_counter(test_case, message, expected):
            """
            Check field manufHidppCounter

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            :param expected: Manufacturing counter field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.manuf_hidpp_counter)), expected=expected,
                                  msg="Manufacturing counter is not as expected")
        # end def check_manuf_hidpp_counter

        @staticmethod
        def check_manuf_hidpp_counter_in_range(test_case, message, expected):
            """
            Check field manufHidppCounter is within a range

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            :param expected: Manufacturing counter field expected range value
            :type expected: ``tuple``
            """
            assert len(expected) == 2
            obt = int(Numeral(message.manuf_hidpp_counter))
            exp_min = expected[0]
            exp_max = expected[1]
            test_case.assertTrue(expr=(exp_min <= obt <= exp_max),
                                 msg=f'Manufacturing counter {obt} should be in valid range [{exp_min}, {exp_max}]')
        # end def check_manuf_hidpp_counter_in_range

        @staticmethod
        def check_compl_hidpp_counter(test_case, message, expected):
            """
            Check field complHidppCounter

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            :param expected: Compliance counter field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.compl_hidpp_counter)), expected=expected,
                                  msg='Compliance counter is not as expected')
        # end def check_compl_hidpp_counter

        @staticmethod
        def check_compl_hidpp_counter_in_range(test_case, message, expected):
            """
            Check field complHidppCounter is within a range

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            :param expected: Compliance counter field expected range value
            :type expected: ``tuple``
            """
            assert len(expected) == 2
            obt = int(Numeral(message.compl_hidpp_counter))
            exp_min = expected[0]
            exp_max = expected[1]
            test_case.assertTrue(expr=(exp_min <= obt <= exp_max),
                                 msg=f'Compliance counter {obt} should be in valid range [{exp_min}, {exp_max}]')
        # end def check_compl_hidpp_counter_in_range

        @staticmethod
        def check_gotthard_counter(test_case, message, expected):
            """
            Check field gothardCounter

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            :param expected: Gothard counter field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.gothard_counter)), expected=expected,
                                  msg='Gotthard counter is not as expected')
        # end def check_compl_hidpp_counter

        @staticmethod
        def check_gotthard_counter_in_range(test_case, message, expected):
            """
            Check field gothardCounter is within a range

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            :param expected: Gothard counter field expected range value
            :type expected: ``tuple``
            """

            assert len(expected) == 2
            obt = int(Numeral(message.gothard_counter))
            exp_min = expected[0]
            exp_max = expected[1]
            test_case.assertTrue(expr=(exp_min <= obt <= exp_max),
                                 msg=f'Gotthard counter {obt} should be in valid range [{exp_min}, {exp_max}]')
        # end def check_gotthard_counter_in_range

        @classmethod
        def check_counters(cls, test_case, message, message_cls, expected_manuf_counter=None,
                           expected_compl_counter=None, expected_gothard_counter=None):
            """
            Check counters values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Get counters response messsage
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            :param expected_manuf_counter: Expected value for manufacturing counter
            :type expected_manuf_counter: ``int``
            :param expected_compl_counter: Expected value for manufacturing counter
            :type expected_compl_counter: ``int``
            :param expected_gothard_counter: Expected value for manufacturing counter
            :type expected_gothard_counter: ``int``
            :param message_cls: Message class
            :type message_cls: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetCountersResponse``
            """
            check_map = cls.get_default_check_map(test_case)
            if expected_manuf_counter is None:
                check_map["manuf_hidpp_counter"] = None
            else:
                check_map["manuf_hidpp_counter"] = (cls.check_manuf_hidpp_counter, expected_manuf_counter)
            # end if

            if expected_compl_counter is None:
                check_map["compl_hidpp_counter"] = None
            else:
                check_map["compl_hidpp_counter"] = (cls.check_compl_hidpp_counter, expected_compl_counter)
            # end if

            if expected_gothard_counter is None:
                check_map["gothard_counter"] = None
            else:
                check_map["gothard_counter"] = (cls.check_gotthard_counter, expected_gothard_counter)
            # end if

            cls.check_fields(test_case, message, message_cls, check_map)
        # end def check_counters
    # end class GetCountersResponseChecker

    class GetReactInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check Get React Info response
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
                "auth_feature": (cls.check_auth_feature,
                                 test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_AuthFeature),
            }
        # end def get_default_check_map

        @staticmethod
        def check_auth_feature(test_case, message, expected):
            """
            Check Support Bit Map reserved value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.managedeactivatablefeatures.GetReactInfoResponse``
            :param expected: Authentication feature field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.auth_feature)), expected=expected,
                                  msg="Authentication feature is not as expected")
        # end def check_auth_feature
    # end class GetReactInfoResponseChecker
# end class ManageDeactivatableFeaturesTestUtils
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
