#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.controllistutils
:brief: Helpers for ``ControlList`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hid.controlidtable import CidTable
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.controllist import ControlList
from pyhid.hidpp.features.common.controllist import ControlListFactory
from pyhid.hidpp.features.common.controllist import GetControlListResponse
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ControlListTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ControlList`` feature
    """
    # Cache the CID list supported by the device
    _cid_list_from_device = None

    class GetCountResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCountResponse``
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
                "count": (
                    cls.check_count,
                    test_case.f.PRODUCT.FEATURES.COMMON.CONTROL_LIST.F_Count)
            }
        # end def get_default_check_map

        @staticmethod
        def check_count(test_case, response, expected):
            """
            Check count field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCountResponse to check
            :type response: ``pyhid.hidpp.features.common.controllist.GetCountResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert count that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Count shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.count),
                msg="The count parameter differs "
                    f"(expected:{expected}, obtained:{response.count})")
        # end def check_count
    # end class GetCountResponseChecker

    class GetControlListResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetControlListResponse``
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
            cid_list = ControlListTestUtils.get_cid_list_from_dut_layouts(test_case=test_case)

            check_map = {}
            for cid_index in range(GetControlListResponse.NUM_OF_CID_PER_PACKET):
                check_map[f'cid_{cid_index}'] = (getattr(cls, f'check_cid_{cid_index}'), cid_list)
            # end for

            return check_map
        # end def get_default_check_map

        @staticmethod
        def check_cid_0(test_case, response, cid_list):
            """
            Check cid_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetControlListResponse to check
            :type response: ``pyhid.hidpp.features.common.controllist.GetControlListResponse``
            :param cid_list: CID list
            :type cid_list: ``HexList | int``

            :raise ``AssertionError``: Assert cid_0 is included in the given cid_list
            """
            test_case.assertIn(
                member=to_int(response.cid_0),
                container=cid_list,
                msg=f"The cid_0 parameter is not in the CID list:{cid_list}, obtained:{response.cid_0})")
        # end def check_cid_0

        @staticmethod
        def check_cid_1(test_case, response, cid_list):
            """
            Check cid_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetControlListResponse to check
            :type response: ``pyhid.hidpp.features.common.controllist.GetControlListResponse``
            :param cid_list: CID list
            :type cid_list: ``HexList | int``

            :raise ``AssertionError``: Assert cid_1 is included in the given cid_list
            """
            test_case.assertIn(
                member=to_int(response.cid_1),
                container=cid_list,
                msg=f"The cid_1 parameter is not in the CID list:{cid_list}, obtained:{response.cid_1})")
        # end def check_cid_1

        @staticmethod
        def check_cid_2(test_case, response, cid_list):
            """
            Check cid_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetControlListResponse to check
            :type response: ``pyhid.hidpp.features.common.controllist.GetControlListResponse``
            :param cid_list: CID list
            :type cid_list: ``HexList | int``

            :raise ``AssertionError``: Assert cid_2 is included in the given cid_list
            """
            test_case.assertIn(
                member=to_int(response.cid_2),
                container=cid_list,
                msg=f"The cid_2 parameter is not in the CID list:{cid_list}, obtained:{response.cid_2})")
        # end def check_cid_2

        @staticmethod
        def check_cid_3(test_case, response, cid_list):
            """
            Check cid_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetControlListResponse to check
            :type response: ``pyhid.hidpp.features.common.controllist.GetControlListResponse``
            :param cid_list: CID list
            :type cid_list: ``HexList | int``

            :raise ``AssertionError``: Assert cid_3 is included in the given cid_list
            """
            test_case.assertIn(
                member=to_int(response.cid_3),
                container=cid_list,
                msg=f"The cid_3 parameter is not in the CID list:{cid_list}, obtained:{response.cid_3})")
        # end def check_cid_3

        @staticmethod
        def check_cid_4(test_case, response, cid_list):
            """
            Check cid_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetControlListResponse to check
            :type response: ``pyhid.hidpp.features.common.controllist.GetControlListResponse``
            :param cid_list: CID list
            :type cid_list: ``HexList | int``

            :raise ``AssertionError``: Assert cid_4 is included in the given cid_list
            """
            test_case.assertIn(
                member=to_int(response.cid_4),
                container=cid_list,
                msg=f"The cid_4 parameter is not in the CID list:{cid_list}, obtained:{response.cid_4})")
        # end def check_cid_4

        @staticmethod
        def check_cid_5(test_case, response, cid_list):
            """
            Check cid_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetControlListResponse to check
            :type response: ``pyhid.hidpp.features.common.controllist.GetControlListResponse``
            :param cid_list: CID list
            :type cid_list: ``HexList | int``

            :raise ``AssertionError``: Assert cid_5 is included in the given cid_list
            """
            test_case.assertIn(
                member=to_int(response.cid_5),
                container=cid_list,
                msg=f"The cid_5 parameter is not in the CID list:{cid_list}, obtained:{response.cid_5})")
        # end def check_cid_5

        @staticmethod
        def check_cid_6(test_case, response, cid_list):
            """
            Check cid_6 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetControlListResponse to check
            :type response: ``pyhid.hidpp.features.common.controllist.GetControlListResponse``
            :param cid_list: CID list
            :type cid_list: ``HexList | int``

            :raise ``AssertionError``: Assert cid_6 is included in the given cid_list
            """
            test_case.assertIn(
                member=to_int(response.cid_6),
                container=cid_list,
                msg=f"The cid_6 parameter is not in the CID list:{cid_list}, obtained:{response.cid_6})")
        # end def check_cid_6

        @staticmethod
        def check_cid_7(test_case, response, cid_list):
            """
            Check cid_7 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetControlListResponse to check
            :type response: ``pyhid.hidpp.features.common.controllist.GetControlListResponse``
            :param cid_list: CID list
            :type cid_list: ``HexList | int``

            :raise ``AssertionError``: Assert cid_7 is included in the given cid_list
            """
            test_case.assertIn(
                member=to_int(response.cid_7),
                container=cid_list,
                msg=f"The cid_7 parameter is not in the CID list:{cid_list}, obtained:{response.cid_7})")
        # end def check_cid_7
    # end class GetControlListResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=ControlList.FEATURE_ID, factory=ControlListFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_count(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetCount``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetCountResponse
            :rtype: ``GetCountResponse``
            """
            feature_1b10_index, feature_1b10, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b10.get_count_cls(
                device_index=device_index,
                feature_index=feature_1b10_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1b10.get_count_response_cls)
            return response
        # end def get_count

        @classmethod
        def get_control_list(cls, test_case, offset, device_index=None, port_index=None,
                             software_id=None, padding=None):
            """
            Process ``GetControlList``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param offset: Offset
            :type offset: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetControlListResponse
            :rtype: ``GetControlListResponse``
            """
            feature_1b10_index, feature_1b10, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b10.get_control_list_cls(
                device_index=device_index,
                feature_index=feature_1b10_index,
                offset=HexList(offset))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1b10.get_control_list_response_cls)
            return response
        # end def get_control_list
    # end class HIDppHelper

    @classmethod
    def refresh_cid_list(cls, test_case):
        """
        Refresh control id list from device

        Note: Shall invoke this method after changed keyboard to another language layout

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        count = to_int(cls.HIDppHelper.get_count(test_case=test_case).count)
        cid_list = []
        for offset in range(0, count, 8):
            resp = cls.HIDppHelper.get_control_list(test_case=test_case, offset=offset)
            cid_list += [CidTable(to_int(resp.cid_0)), CidTable(to_int(resp.cid_1)), CidTable(to_int(resp.cid_2)),
                         CidTable(to_int(resp.cid_3)), CidTable(to_int(resp.cid_4)), CidTable(to_int(resp.cid_5)),
                         CidTable(to_int(resp.cid_6)), CidTable(to_int(resp.cid_7))]
        # end for
        cls._cid_list_from_device = cid_list
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg=f"Supported Control ID List: {cls._cid_list_from_device}")
        # --------------------------------------------------------------------------------------------------------------
    # end def refresh_cid_list

    @classmethod
    def get_cid_list_from_dut_layouts(cls, test_case):
        """
        Get control id list from key matrices

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The cid list retrieved from device
        :rtype: ``list[CidTable]``
        """
        config = test_case.f.PRODUCT.FEATURES.COMMON.CONTROL_LIST
        key_ids_of_all_layouts = set(
            sum([list(layout.KEYS.keys()) for layout in test_case.button_stimuli_emulator._keyboard_layouts], []))
        cid_list_from_key_matrices = \
            [cid for cid, key_id in CID_TO_KEY_ID_MAP.items() if key_id in key_ids_of_all_layouts]
        cid_list_from_roller_layout = \
            [CidTable.ROLLER0_SCROLL_UP, CidTable.ROLLER0_SCROLL_DOWN] * config.F_HasRoller_0 + \
            [CidTable.ROLLER1_SCROLL_UP, CidTable.ROLLER1_SCROLL_DOWN] * config.F_HasRoller_1
        # In the device reported CID list, the unmounted keys are represented by CidTable.NONE.
        cid_list = cid_list_from_key_matrices + cid_list_from_roller_layout + [CidTable.NONE]

        return cid_list
    # end def get_cid_list_from_dut_layouts

    @classmethod
    def get_cids_sharing_key_id(cls):
        """
        Get the list of control ids sharing the KEY_ID with another pair

        :return: The cid list which connecting to the same KEY_ID in the CID_TO_KEY_ID_MAP
        :rtype: ``list[CidTable]``
        """
        return [cid for cid, key_id in CID_TO_KEY_ID_MAP.items() if list(CID_TO_KEY_ID_MAP.values()).count(key_id) > 1]
    # end def get_cids_sharing_key_id

    @classmethod
    def get_cids_sharing_key_id_with_cid(cls, cid):
        """
        Get the list of control ids sharing the KEY_ID with the pair matching the given "cid"

        :param cid: Control ID
        :type cid: ``int | CidTable``

        :return: The cid list which connecting to the same KEY_ID with the input "cid"
        :rtype: ``list[CidTable]``
        """
        return [_cid for _cid in cls.get_cids_sharing_key_id() if CID_TO_KEY_ID_MAP[_cid] == CID_TO_KEY_ID_MAP[cid]]
    # end def get_cids_sharing_key_id_with_cid

    @classmethod
    def get_cid_list_from_device(cls, test_case, force_refresh=False):
        """
        Get control id list from device

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param force_refresh: Flag indicating the CID list from the device shall be reset or not - OPTIONAL
        :type force_refresh: ``bool``

        :return: The cid list retrieved from device
        :rtype: ``list[CidTable]``
        """
        if not cls._cid_list_from_device or force_refresh:
            cls.refresh_cid_list(test_case=test_case)
        # end if
        return cls._cid_list_from_device
    # end def get_cid_list_from_device

    @classmethod
    def get_cid_index(cls, test_case, cid):
        """
        Get the index in the control id list

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param cid: Control ID
        :type cid: ``int | CidTable``

        :return: The index of the control id in the control id list
        :rtype: ``int | None``
        """
        cid_list = cls.get_cid_list_from_device(test_case=test_case)
        return cls.get_cid_index_by_provided_cid_list(cid_list=cid_list, cid=cid)
    # end def get_cid_index

    @classmethod
    def get_cid_index_by_provided_cid_list(cls, cid_list, cid):
        """
        Get the index in the control id list by the provided cid list

        :param cid_list: The cid list retrieved from device
        :type cid_list: ``list[CidTable]``
        :param cid: Control ID
        :type cid: ``int | CidTable``

        :return: The index of the control id in the control id list
        :rtype: ``int | None``
        """
        return cid_list.index(cid) if cid in cid_list else None
    # end def get_cid_index_by_provided_cid_list

    @classmethod
    def cid_to_key_id(cls, test_case, cid):
        """
        Convert the control id to the corresponding key id

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param cid: Control ID
        :type cid: ``int | CidTable``

        :return: The corresponding key id of the control id
        :rtype: ``KEY_ID | None``
        """
        cid_list = cls.get_cid_list_from_device(test_case=test_case)
        return CID_TO_KEY_ID_MAP[cid] if cid in cid_list else None
    # end def cid_to_key_id

    @classmethod
    def cidx_to_key_id(cls, test_case, cid_index):
        """
        Get the key id by cid index

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param cid_index: Index of Control ID in the cid list
        :type cid_index: ``int``

        :return: The corresponding key id of the control id index
        :rtype: ``KEY_ID | None``
        """
        cid_list = cls.get_cid_list_from_device(test_case=test_case)
        return cls.cid_to_key_id(test_case=test_case, cid=cid_list[cid_index])
    # end def cidx_to_key_id

    @classmethod
    def key_id_to_cid(cls, test_case, key_id):
        """
        Get the cid by key id

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_id: The key id
        :type key_id: ``KEY_ID``

        :return: The corresponding control id of the key id
        :rtype: ``int | None``
        """
        cid_list = cls.get_cid_list_from_device(test_case=test_case)
        return cls.key_id_to_cid_by_provided_cid_list(cid_list=cid_list, key_id=key_id)
    # end def key_id_to_cid

    @classmethod
    def key_id_to_cid_by_provided_cid_list(cls, cid_list, key_id):
        """
        Get the cid by key id by the provided cid list

        :param cid_list: The cid list retrieved from device
        :type cid_list: ``list[CidTable]``
        :param key_id: The key id
        :type key_id: ``KEY_ID``

        :return: The corresponding control id of the key id
        :rtype: ``int | None``
        """
        cid = None
        cid_to_keyid_map = iter(CID_TO_KEY_ID_MAP.items())
        while cid is None:
            possible_cid = next((_cid for _cid, _key_id in cid_to_keyid_map if _key_id == key_id), None)
            if possible_cid in cid_list:
                cid = possible_cid
            elif possible_cid is None:
                return None
            # end if
        # end while
        return cid
    # end def key_id_to_cid_by_provided_cid_list

    @classmethod
    def key_id_to_cidx(cls, test_case, key_id):
        """
        Get the cid index by key id

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_id: The key id
        :type key_id: ``KEY_ID``

        :return: The corresponding control id index of the key id
        :rtype: ``int | None``
        """
        return cls.get_cid_index(test_case=test_case, cid=cls.key_id_to_cid(test_case=test_case, key_id=key_id))
    # end def key_id_to_cidx
# end class ControlListTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
