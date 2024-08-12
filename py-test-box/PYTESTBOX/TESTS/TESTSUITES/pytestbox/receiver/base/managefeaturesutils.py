#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.base.managefeaturesutils
:brief:  Helpers for receiver manage deactivatable features command set
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/11/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesEnableFeaturesRequest
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesEnableFeaturesResponse
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesGetInfoRequest
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesGetInfoResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.receiver.base.receiverbasetestutils import ReceiverBaseTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
MANUF_HIDPP_MASK = 0x01
COMPL_HIDPP_MASK = 0x02
GOTHARD = 0x04


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ManageFeaturesUtils(ReceiverBaseTestUtils):
    """
    This class provides helpers for receiver manage deactivatable features command set
    """
    class HIDppHelper(ReceiverBaseTestUtils.HIDppHelper):
        """
        HID++ 1.0 helper class
        """
        @classmethod
        def enable_features(cls, test_case, manufacturing=False, compliance=False, gothard=False, log_step=0,
                            log_check=0):
            """
            Re-activate the features locked in the field

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param manufacturing: Enable Manufacturing features - OPTIONAL
            :type manufacturing: ``bool``
            :param compliance: Enable Compliance features - OPTIONAL
            :type compliance: ``bool``
            :param gothard: Enable Gothard - OPTIONAL
            :type gothard: ``bool``
            :param log_step: Log step number, if <= 0 no log printed
            :type log_step: ``int``
            :param log_check: Log check number, if <= 0 no log printed
            :type log_check: ``int``
            """
            if log_step > 0:
                # ---------------------------------------------------------------------------
                test_case.logTitle2(f'Test Step {log_step}: Enable the manufacturing features')
                # ---------------------------------------------------------------------------
            # end if
            enable_features_resp = test_case.send_report_wait_response(
                report=ManageDeactivatableFeaturesEnableFeaturesRequest(enable_gothard=gothard,
                                                                        enable_compliance=compliance,
                                                                        enable_manufacturing=manufacturing),
                response_queue=test_case.hidDispatcher.receiver_response_queue,
                response_class_type=ManageDeactivatableFeaturesEnableFeaturesResponse)
            if log_check > 0:
                # ---------------------------------------------------------------------------
                test_case.logTitle2(f'Test Check {log_check}: Check the Enable Features response')
                # ---------------------------------------------------------------------------
            # end if
            ManageFeaturesUtils.MessageChecker.check_fields(
                test_case, enable_features_resp, ManageDeactivatableFeaturesEnableFeaturesResponse, {})
            if log_check > 0:
                # ---------------------------------------------------------------------------
                test_case.logTitle2(f'Test Check {log_check}: Check the Get Info response')
                # ---------------------------------------------------------------------------
            # end if
            get_info_resp = test_case.send_report_wait_response(
                report=ManageDeactivatableFeaturesGetInfoRequest(),
                response_queue=test_case.hidDispatcher.receiver_response_queue,
                response_class_type=ManageDeactivatableFeaturesGetInfoResponse)
            ManageFeaturesUtils.ManageDeactivatableFeaturesGetInfoResponseChecker.check_fields(
                test_case, get_info_resp, ManageDeactivatableFeaturesGetInfoResponse)
            test_case.assertEqual(expected=1, obtained=get_info_resp.state_bit_map.manufacturing,
                                  msg='manufacturing bit shall be set')
        # end def enable_features
    # end class HIDppHelper

    class ManageDeactivatableFeaturesGetInfoResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        Test utils to check Manage Deactivatable Features 'Get Info' response
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
                "support_bit_map": (cls.check_support_bit_map, MANUF_HIDPP_MASK),
                "persist_bit_map": (cls.check_persist_bit_map, 0),
                "state_bit_map": (cls.check_state_bit_map_in_range, (0, MANUF_HIDPP_MASK)),
            }
        # end def get_default_check_map

        @staticmethod
        def check_support_bit_map(test_case, message, expected):
            """
            Check Support Bit Map value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``ManageDeactivatableFeaturesGetInfoResponse``
            :param expected: expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(HexList(message.support_bit_map))), expected=expected,
                                  msg="Support Bit Map bits are not as expected")
        # end def check_support_bit_map

        @staticmethod
        def check_persist_bit_map(test_case, message, expected):
            """
            Check Persist Bit Map value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``ManageDeactivatableFeaturesGetInfoResponse``
            :param expected: expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(HexList(message.persist_bit_map))), expected=expected,
                                  msg="Persist Bit Map bits are not as expected")
        # end def check_persist_bit_map

        @staticmethod
        def check_state_bit_map_in_range(test_case, message, expected):
            """
            Check state bitmap value is within a range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``ManageDeactivatableFeaturesGetInfoResponse``
            :param expected: State BitMap expected range value
            :type expected: ``tuple``
            """
            assert len(expected) == 2
            obt = int(Numeral(HexList(message.state_bit_map)))
            test_case.assertTrue(expr=(expected[0] <= obt <= expected[1]),
                                 msg=f'State BitMap {obt} should be in valid range [{expected[0]}, '
                                     f'{expected[1]}]')
        # end def check_state_bit_map_in_range

    # end class ManageDeactivatableFeaturesEnableFeaturesResponseChecker

# end class ManageFeaturesUtils

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
