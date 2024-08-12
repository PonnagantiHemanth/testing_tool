#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.hostsinfoutils
:brief:  Helpers for Hosts Info feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pyhid.hidpp.features.common.hostsinfo import BLEDescriptorPage0
from pyhid.hidpp.features.common.hostsinfo import BLEDescriptorPage1DualUuid
from pyhid.hidpp.features.common.hostsinfo import BLEDescriptorPage1Header
from pyhid.hidpp.features.common.hostsinfo import BLEDescriptorPage1SingleUuid
from pyhid.hidpp.features.common.hostsinfo import BLEDescriptorPage1TripleUuid
from pyhid.hidpp.features.common.hostsinfo import GetHostFriendlyNameResponseV1ToV2
from pyhid.hidpp.features.common.hostsinfo import HostsInfo
from pyhid.hidpp.features.common.hostsinfo import HostsInfoFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HostsInfoTestUtils(DeviceBaseTestUtils):
    """
    Test utils for Hosts Info feature
    """
    class CapabilityMaskBitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Helper to check CapabilityMask BitMap
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
                "reserved_byte_0": (cls.check_reserved_byte_0, 0),
                "set_os_version": (cls.check_set_os_version, 0),
                "delete_host": (cls.check_delete_host, 0),
                "move_host": (cls.check_move_host, 0),
                "set_name": (cls.check_set_name, 0),
                "get_name": (cls.check_get_name, 0),
                "reserved_byte_1": (cls.check_reserved_byte_1, 0),
                "ble_hd": (cls.check_ble_hd, 0),
                "bt_hd": (cls.check_bt_hd, 0),
                "usb_hd": (cls.check_usb_hd, 0),
                "equad_hd": (cls.check_equad_hd, 0),
            }
        # end def get_default_check_map

        @classmethod
        def check_reserved_byte_0(cls, test_case, bitmap, expected):
            """
            Check reserved bits in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained CapabilityMask bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: Reserved field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.reserved_byte_0)), expected=int(Numeral(expected)),
                                  msg="Reserved field in bit map Byte 0 is not as expected")
        # end def check_reserved_byte_0

        @classmethod
        def check_set_os_version(cls, test_case, bitmap, expected):
            """
            Check set_os_version in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: set_os_version expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.set_os_version)), expected=int(Numeral(expected)),
                                  msg="set_os_version in bit map is not as expected")
        # end def check_all_bit

        @classmethod
        def check_delete_host(cls, test_case, bitmap, expected):
            """
            Check delete_host bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: delete_host bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.delete_host)), expected=int(Numeral(expected)),
                                  msg="delete_host bit in bit map is not as expected")
        # end def check_delete_host

        @classmethod
        def check_move_host(cls, test_case, bitmap, expected):
            """
            Check move_host bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: move_host bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.move_host)), expected=int(Numeral(expected)),
                                  msg="move_host bit in bit map is not as expected")
        # end def check_move_host

        @classmethod
        def check_set_name(cls, test_case, bitmap, expected):
            """
            Check set_name bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: set_name bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.set_name)), expected=int(Numeral(expected)),
                                  msg="set_name bit in bit map is not as expected")
        # end def check_set_name

        @classmethod
        def check_get_name(cls, test_case, bitmap, expected):
            """
            Check get_name bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: get_name bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.get_name)), expected=int(Numeral(expected)),
                                  msg="get_name bit in bit map is not as expected")
        # end def check_get_name

        @classmethod
        def check_reserved_byte_1(cls, test_case, bitmap, expected):
            """
            Check reserved bits in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained CapabilityMask bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: Reserved field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.reserved_byte_1)), expected=int(Numeral(expected)),
                                  msg="Reserved field in bit map Byte 1 is not as expected")
        # end def check_reserved_byte_1

        @classmethod
        def check_ble_hd(cls, test_case, bitmap, expected):
            """
            Check ble_hd bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: ble_hd bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.ble_hd)), expected=int(Numeral(expected)),
                                  msg="ble_hd bit in bit map is not as expected")
        # end def check_ble_hd

        @classmethod
        def check_bt_hd(cls, test_case, bitmap, expected):
            """
            Check bt_hd bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: bt_hd bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.bt_hd)), expected=int(Numeral(expected)),
                                  msg="bt_hd bit in bit map is not as expected")
        # end def check_bt_hd

        @classmethod
        def check_usb_hd(cls, test_case, bitmap, expected):
            """
            Check usb_hd bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: usb_hd bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.usb_hd)), expected=int(Numeral(expected)),
                                  msg="usb_hd bit in bit map is not as expected")
        # end def check_usb_hd

        @classmethod
        def check_equad_hd(cls, test_case, bitmap, expected):
            """
            Check equad_hd bit in bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Obtained bitmap
            :type bitmap: ``HostsInfo.CapabilityMaskBitMap``
            :param expected: equad_hd bit expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(bitmap.equad_hd)), expected=int(Numeral(expected)),
                                  msg="equad_hd bit in bit map is not as expected")
        # end def check_equad_hd
    # end class BitMapChecker

    class GetFeatureInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check getFeatureInfo response
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
            bit_map_checker = HostsInfoTestUtils.CapabilityMaskBitMapChecker
            config = test_case.f.PRODUCT.FEATURES.COMMON.HOSTS_INFO
            change_host_config = test_case.f.PRODUCT.FEATURES.COMMON.CHANGE_HOST
            return {
                "capability_mask": (cls.check_capability_mask_bit_map, {
                    "reserved_byte_0": (bit_map_checker.check_reserved_byte_0, 0),
                    "set_os_version": (bit_map_checker.check_set_os_version, config.F_SupportSetOSVersion),
                    "delete_host": (bit_map_checker.check_delete_host, 0),
                    "move_host": (bit_map_checker.check_move_host, 0),
                    "set_name": (bit_map_checker.check_set_name, config.F_SupportSetName),
                    "get_name": (bit_map_checker.check_get_name, config.F_SupportGetName),
                    "reserved_byte_1": (bit_map_checker.check_reserved_byte_1, 0),
                    "ble_hd": (bit_map_checker.check_ble_hd, config.F_SupportBLEDescriptor),
                    "bt_hd": (bit_map_checker.check_bt_hd, config.F_SupportBTDescriptor),
                    "usb_hd": (bit_map_checker.check_usb_hd, config.F_SupportUSBDescriptor),
                    "equad_hd": (bit_map_checker.check_equad_hd, 0),
                }),
                "num_hosts": (cls.check_num_hosts, test_case.f.PRODUCT.DEVICE.F_NbHosts),
                "current_host": (cls.check_current_host_in_range, test_case.f.PRODUCT.DEVICE.F_NbHosts),
            }
        # end def get_default_check_map

        @classmethod
        def check_capability_mask_bit_map(cls, test_case, message, expected):
            """
            Check capability mask bit map

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``HostsInfo``
            :param expected: Expected bit map check map
            :type expected: ``dict``
            """
            HostsInfoTestUtils.CapabilityMaskBitMapChecker.check_fields(
                test_case, message.capability_mask, HostsInfo.CapabilityMaskBitMap, expected)
        # end def check_capability_mask_bit_map

        @classmethod
        def check_num_hosts(cls, test_case, message, expected):
            """
            Check num hosts

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetFeatureInfoResponseV1ToV2``
            :param expected: Num Hosts field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.num_hosts)), expected=int(Numeral(expected)),
                                  msg="num_hosts value is not as expected")
        # end def check_num_hosts

        @classmethod
        def check_current_host_in_range(cls, test_case, message, expected):
            """
            Check current host value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetFeatureInfoResponseV1ToV2``
            :param expected: current_host field expected value
            :type expected: ``int``
            """
            obt = int(Numeral(message.current_host))
            test_case.assertTrue(expr=(0 <= obt <= expected-1),
                                 msg=f'current_host value {obt} should be in range [{0}, {expected-1}]')
        # end def check_current_host_in_range
    # end class GetFeatureInfoResponseChecker

    class GetHostInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check getHostInfo response
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.HOSTS_INFO
            return {
                "host_index": (cls.check_host_index, 0),
                "status": (cls.check_status, HostsInfo.STATUS.PAIRED),
                "bus_type": (cls.check_bus_type, config.F_HostBusType),
                "num_pages": (cls.check_num_pages_in_range, 5),
                "name_len": (cls.check_name_len_in_range, config.F_HostNameMaxLength),
                "name_max_len": (cls.check_name_max_len, config.F_HostNameMaxLength),
            }
        # end def get_default_check_map

        @classmethod
        def check_host_index(cls, test_case, message, expected):
            """
            Check host index

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostInfoResponseV1``
            :param expected: hostIndex field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.host_index)), expected=int(Numeral(expected)),
                                  msg="host_index value is not as expected")
        # end def check_host_index

        @classmethod
        def check_status(cls, test_case, message, expected):
            """
            Check status

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostInfoResponseV1``
            :param expected: status field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.status)), expected=int(Numeral(expected)),
                                  msg="status value is not as expected")
        # end def check_status

        @classmethod
        def check_bus_type(cls, test_case, message, expected):
            """
            Check bus_type

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostInfoResponseV1``
            :param expected: bus_type field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.bus_type)), expected=int(Numeral(expected)),
                                  msg="bus_type value is not as expected")
        # end def check_bus_type

        @classmethod
        def check_num_pages_in_range(cls, test_case, message, expected):
            """
            Check current host value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostInfoResponseV1``
            :param expected: num_pages field expected value
            :type expected: ``int``
            """
            min_num_pages = 0
            max_num_pages = 0
            if int(Numeral(message.bus_type)) == HostsInfo.BUSTYPE.BT:
                min_num_pages = 2
                max_num_pages = 2
            elif int(Numeral(message.bus_type)) in [HostsInfo.BUSTYPE.BLE, HostsInfo.BUSTYPE.BOLT]:
                max_num_pages = expected
            # end if
            obt = int(Numeral(message.num_pages))
            test_case.assertTrue(expr=(min_num_pages <= obt <= max_num_pages),
                                 msg=f'num_pages value {obt} should be in range [{min_num_pages}, {max_num_pages}]')
        # end def check_current_host_in_range

        @staticmethod
        def check_name_len_in_range(test_case, message, expected):
            """
            Check name_len field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            value = int(Numeral(message.name_len))
            max_value = int(Numeral(expected))
            LogHelper.log_check(
                    test_case, f"Validate GetHostInfoResponse.name_len:{value} in range[0, {max_value}]")
            test_case.assertTrue(expr=(0 <= value <= max_value),
                                 msg=f'The name_len {message.name_len} is not in range[0, {expected}]')
        # end def check_name_len_in_range

        @staticmethod
        def check_name_max_len(test_case, message, expected):
            """
            Check name_len field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostInfoResponseV1``
            :param expected: name_max_len expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(obtained=int(Numeral(message.name_max_len)), expected=int(Numeral(expected)),
                                  msg="name_max_len value is not as expected")
        # end def check_name_max_len
    # end class GetHostInfoResponseChecker

    class GetHostDescriptorResponseChecker(GetHostInfoResponseChecker):
        """
        Test utils to check getHostDescriptor response
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.HOSTS_INFO
            return {
                "host_index": (cls.check_host_index, 0),
                "bus_type": (cls.check_bus_type, config.F_HostBusType),
                "page_index": (cls.check_page_index, 0),
                "host_descriptor": None,
            }
        # end def get_default_check_map

        @classmethod
        def check_page_index(cls, test_case, message, expected):
            """
            Check page index value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostDescriptorResponseV1``
            :param expected: page_index field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.page_index)), expected=int(Numeral(expected)),
                                  msg="page_index value is not as expected")
        # end def check_page_index
    # end class GetHostDescriptorResponseChecker

    class GetHostFriendlyNameResponseChecker(GetHostInfoResponseChecker):
        """
        Test utils to check getHostFriendlyName response
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
                "host_index": (cls.check_host_index, 0),
                "byte_index": (cls.check_byte_index, 0),
                "name_chunk": (cls.check_name_chunk, (HostsInfoTestUtils.NAME.BLE_FRIENDLY_NAME, 0)),
            }
        # end def get_default_check_map

        @classmethod
        def check_byte_index(cls, test_case, message, expected):
            """
            Check byte index value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostFriendlyNameResponseV1ToV2``
            :param expected: byte_index field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.byte_index)), expected=int(Numeral(expected)),
                                  msg="byte_index value is not as expected")
        # end def check_byte_index

        @classmethod
        def check_name_chunk(cls, test_case, message, data):
            """
            Check name chunk value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostFriendlyNameResponseV1ToV2``
            :param data: (name_chunk , offset)
            :type data: ``tuple``
            """
            (expected, offset) = data
            friendly_name_chunk = HexList.fromString(expected)[offset:offset+14]
            friendly_name_chunk.addPadding(GetHostFriendlyNameResponseV1ToV2.LEN.NAME_CHUNK // 8, fromLeft=False)
            test_case.assertEqual(obtained=message.name_chunk, expected=friendly_name_chunk,
                                  msg=f'name_chunk value is not as expected: {HexList.toString(message.name_chunk)} '
                                      f'!= {HexList.toString(friendly_name_chunk)}')
        # end def check_name_chunk
    # end class GetHostFriendlyNameResponseChecker

    class SetHostFriendlyNameResponseChecker(GetHostInfoResponseChecker):
        """
        Test utils to check setHostFriendlyName response
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
                "host_index": (cls.check_host_index, 0),
                "name_len": (cls.check_name_len, len(HostsInfoTestUtils.NAME.BLE_FRIENDLY_NAME)),
            }
        # end def get_default_check_map

        @classmethod
        def check_name_len(cls, test_case, message, expected):
            """
            Check name len value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.SetHostFriendlyNameResponseV1ToV2``
            :param expected: name_len field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.name_len)), expected=int(Numeral(expected)),
                                  msg="name_len value is not as expected")
        # end def check_name_len
    # end class SetHostFriendlyNameResponseChecker

    class GetHostOsVersionResponseChecker(GetHostInfoResponseChecker):
        """
        Test utils to check getHostOsVersion response
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
                "host_index": (cls.check_host_index, 0),
                "os_type": (cls.check_os_type, 0),
                "os_version": (cls.check_os_version, 0),
                "os_revision": (cls.check_os_revision, 0),
                "os_build": (cls.check_os_build, 0),
            }
        # end def get_default_check_map

        @classmethod
        def check_os_type(cls, test_case, message, expected):
            """
            Check os_type

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostOsVersionResponseV1ToV2``
            :param expected: os_type field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.os_type)), expected=int(Numeral(expected)),
                                  msg="os_type value is not as expected")
        # end def check_os_type

        @classmethod
        def check_os_version(cls, test_case, message, expected):
            """
            Check OS version

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostOsVersionResponseV1ToV2``
            :param expected: os_version field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.os_version)), expected=int(Numeral(expected)),
                                  msg="os_version value is not as expected")
        # end def check_os_version

        @classmethod
        def check_os_revision(cls, test_case, message, expected):
            """
            Check OS Revision

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostOsVersionResponseV1ToV2``
            :param expected: os_revision field expected value
            :type expected: ``HexList`` or ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.os_revision)), expected=int(Numeral(expected)),
                                  msg="os_revision value is not as expected")
        # end def check_os_revision

        @classmethod
        def check_os_build(cls, test_case, message, expected):
            """
            Check OS Build

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``pyhid.hidpp.features.common.hostsinfo.GetHostOsVersionResponseV1ToV2``
            :param expected: os_build field expected value
            :type expected: ``HexList`` or ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.os_build)), expected=int(Numeral(expected)),
                                  msg="os_build value is not as expected")
        # end def check_os_build
    # end class GetHostOsVersionResponseChecker

    class SetHostOsVersionResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check setHostOsVersion response
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
            return {}
        # end def get_default_check_map
    # end class SetHostOsVersionResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case, feature_id=HostsInfo.FEATURE_ID, factory=HostsInfoFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_feature_info(cls, test_case, device_index=None, port_index=None):
            """
            Get the number of hosts in the registry and the currently active host index (logically the caller).
            Also returns a capability_mask for the device.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: host basic information response
            :rtype: ``GetHostInfoResponseV1``
            """
            feature_1815_index, feature_1815, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            get_feature_info_req = feature_1815.get_feature_info_cls(device_index, feature_1815_index)
            get_feature_info_resp = test_case.send_report_wait_response(
                report=get_feature_info_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1815.get_feature_info_response_cls)
            return get_feature_info_resp
        # end def get_feature_info

        @classmethod
        def get_host_info(cls, test_case, host_index, device_index=None, port_index=None):
            """
            Get a particular host basic information..

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param host_index: Channel / host index. 0xFF = Current Host.
            :type host_index: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: host basic information response
            :rtype: ``GetHostInfoResponseV1``
            """
            feature_1815_index, feature_1815, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            get_host_info_req = feature_1815.get_host_info_cls(device_index, feature_1815_index, host_index=host_index)
            get_host_info_resp = test_case.send_report_wait_response(
                report=get_host_info_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1815.get_host_info_response_cls)
            return get_host_info_resp
        # end def get_host_info

        @classmethod
        def get_host_descriptor(cls, test_case, host_index, page_index, device_index=None, port_index=None):
            """
            Get a particular host basic information..

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param host_index: Channel / host index. 0xFF = Current Host.
            :type host_index: ``int``
            :param page_index: Channel / host index. 0xFF = Current Host.
            :type page_index: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: host basic information response
            :rtype: ``GetHostInfoResponseV1``
            """
            feature_1815_index, feature_1815, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            get_host_descriptor_req = feature_1815.get_host_descriptor_cls(
                device_index, feature_1815_index, host_index=host_index, page_index=page_index)
            get_host_descriptor_resp = test_case.send_report_wait_response(
                report=get_host_descriptor_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1815.get_host_descriptor_response_cls)
            return get_host_descriptor_resp
        # end def get_host_descriptor

        @classmethod
        def get_host_friendly_name(cls, test_case, host_index, byte_index, device_index=None, port_index=None):
            """
            Get a Host Friendly Name chunk. Can be null if the host channel is not paired.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param host_index: Channel / host index. 0xFF = Current Host.
            :type host_index: ``int``
            :param byte_index: Index of the first host name byte to copy (0..nameLen-1 returned by getHostInfo()).
            :type byte_index: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: host basic information response
            :rtype: ``GetHostFriendlyNameResponseV1ToV2``
            """
            feature_1815_index, feature_1815, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            get_host_friendly_name_req = feature_1815.get_host_friendly_name_cls(
                device_index, feature_1815_index, host_index=host_index, byte_index=byte_index)
            get_host_friendly_name_resp = test_case.send_report_wait_response(
                report=get_host_friendly_name_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1815.get_host_friendly_name_response_cls)
            return get_host_friendly_name_resp
        # end def get_host_friendly_name

        @classmethod
        def set_host_friendly_name_chunk(cls, test_case, host_index, byte_index, name_chunk, device_index=None,
                                         port_index=None):
            """
            Write a host name chunk, starting at byteIndex.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param host_index: Channel / host index. 0xFF = Current Host.
            :type host_index: ``int``
            :param byte_index: Index of the first host name byte to copy (0..nameLen-1 returned by getHostInfo()).
            :type byte_index: ``int``
            :param name_chunk: The host name chunk to write, padded with null bytes '\0' if
                                it is shorter than the payload size (HPPLong: 16 bytes).
            :type name_chunk: ``HexList`` or ``str``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: host basic information response
            :rtype: ``SetHostFriendlyNameResponseV1ToV2``
            """
            feature_1815_index, feature_1815, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            set_host_friendly_name_req = feature_1815.set_host_friendly_name_cls(
                device_index, feature_1815_index, host_index=host_index, byte_index=byte_index,
                name_chunk=name_chunk)
            set_host_friendly_name_resp = test_case.send_report_wait_response(
                report=set_host_friendly_name_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1815.set_host_friendly_name_response_cls)
            return set_host_friendly_name_resp
        # end def set_host_friendly_name_chunk

        @classmethod
        def set_host_friendly_name(cls, test_case, host_index, name, device_index=None, port_index=None):
            """
            Write a whole host name chunk

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param host_index: Channel / host index. 0xFF = Current Host.
            :type host_index: ``int``
            :param name: The host name to write.
            :type name: ``HexList`` or ``str``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: host basic information response
            :rtype: ``list[SetHostFriendlyNameResponseV1ToV2]``
            """
            _, feature_1815, _, _ = cls.get_parameters(test_case, device_index=device_index, port_index=port_index)

            name = HexList.fromString(name) if isinstance(name, str) else name
            name_len = len(name)
            set_host_friendly_name_resp_list = []
            for chunk_index in range(1 + name_len * 8 // feature_1815.set_host_friendly_name_cls.LEN.NAME_CHUNK):
                min_offset = chunk_index * feature_1815.set_host_friendly_name_cls.LEN.NAME_CHUNK // 8
                max_offset = min(name_len,
                                 (chunk_index+1) * feature_1815.set_host_friendly_name_cls.LEN.NAME_CHUNK // 8)
                set_host_friendly_name_resp_list.append(cls.set_host_friendly_name_chunk(
                    test_case, host_index=host_index, byte_index=min_offset, name_chunk=name[min_offset:max_offset]))
            # end for
            return set_host_friendly_name_resp_list
        # end def set_host_friendly_name

        @classmethod
        def get_host_os_version(cls, test_case, host_index, device_index=None, port_index=None):
            """
            Read Host OS Type and Version, saved previously by SW. Can be null.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param host_index: Channel / host index. 0xFF = Current Host.
            :type host_index: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: host basic information response
            :rtype: ``GetHostOsVersionResponseV1ToV2``
            """
            feature_1815_index, feature_1815, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            get_host_os_version_req = feature_1815.get_host_os_version_cls(
                device_index, feature_1815_index, host_index=host_index)
            get_host_os_version_resp = test_case.send_report_wait_response(
                report=get_host_os_version_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1815.get_host_os_version_response_cls)
            return get_host_os_version_resp
        # end def get_host_os_version

        @classmethod
        def set_host_os_version(cls, test_case, host_index, os_type, os_version, os_revision, os_build,
                                device_index=None, port_index=None):
            """
            Read Host OS Type and Version, saved previously by SW. Can be null.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param host_index: Channel / host index. 0xFF = Current Host.
            :type host_index: ``int``
            :param os_type: Enumerated values (defined in the same order as x4531 Platform Descriptor OS bit field):
                            0: Unknown
                            1: Windows
                            2: WinEmb
                            3: Linux
                            4: Chrome
                            5: Android
                            6: MacOS
                            7: IOS
            :type os_type: ``int``
            :param os_version: Os 1st Version number.
            :type os_version: ``int``
            :param os_revision: Os 2nd Version number [Big Endian].
            :type os_revision: ``HexList`` or ``int``
            :param os_build: Os 3rd Version number [Big Endian].
            :type os_build: ``HexList`` or ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: host basic information response
            :rtype: ``SetHostOsVersionResponseV1ToV2``
            """
            feature_1815_index, feature_1815, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            set_host_os_version_req = feature_1815.set_host_os_version_cls(
                device_index, feature_1815_index, host_index=host_index, os_type=os_type,
                os_version=os_version, os_revision=os_revision, os_build=os_build)
            set_host_os_version_resp = test_case.send_report_wait_response(
                report=set_host_os_version_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1815.set_host_os_version_response_cls)
            return set_host_os_version_resp
        # end def set_host_os_version
    # end class HIDppHelper

    class UUID:
        """
        BLE UUID used in BLE Host descriptors
        """
        BLE_MEASUREMENT_INTERVAL = 0x2A21
        BLE_MODEL_NUMBER = 0x2A24
        BLE_SERIAL_NUMBER = 0x2A25
        BLE_MANUFACTURER_NAME = 0x2A29
    # end class UUID

    class NAME:
        """
        NAME used in BLE Host descriptors
        """
        BLE_MODEL_NUMBER = 'Bolt receiver'
        BLE_MANUFACTURER_NAME = 'Logitech'
        BLE_FRIENDLY_NAME = BLE_MANUFACTURER_NAME + ' ' + BLE_MODEL_NUMBER
    # end class NAME

    @classmethod
    def get_ble_descriptor(cls, test_case, host_index):
        """
        Retrieve a BLE descriptor which may have been split into several messages

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param host_index: Channel / host index. 0xFF = Current Host.
        :type host_index: ``int``

        :return:
        """
        ble_address = None
        host_descriptor_data = HexList()
        ble_descriptor = None
        # Get the number of pages to parse
        get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(test_case, host_index)

        for page_id in range(int(Numeral(get_host_info_resp.num_pages))):
            get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_descriptor(test_case, host_index, page_id)
            if get_host_info_resp.page_index == 0:
                host_descriptor_header = BLEDescriptorPage0.fromHexList(get_host_info_resp.host_descriptor)
                if host_descriptor_header.valid_address:
                    ble_address = host_descriptor_header.bluetooth_address
                # end if
            else:
                host_descriptor_data += get_host_info_resp.host_descriptor
            # end if
        # end for

        if len(host_descriptor_data) > 0:
            ble_descriptor_class = None
            ble_descriptor = BLEDescriptorPage1Header.fromHexList(host_descriptor_data)
            if int(Numeral(ble_descriptor.number_of_uuids)) == 1:
                ble_descriptor_class = BLEDescriptorPage1SingleUuid
            elif int(Numeral(ble_descriptor.number_of_uuids)) == 2:
                ble_descriptor_class = BLEDescriptorPage1DualUuid
            elif int(Numeral(ble_descriptor.number_of_uuids)) == 3:
                ble_descriptor_class = BLEDescriptorPage1TripleUuid
            # end if
            for uuid_index in range(int(Numeral(ble_descriptor.number_of_uuids))):
                for field in [x for x in ble_descriptor_class.FIELDS if x.name.startswith(f'data_{uuid_index}')]:
                    field.length = int(Numeral(getattr(ble_descriptor, f'size_{uuid_index}')))*8
                # end for
                ble_descriptor = ble_descriptor_class.fromHexList(host_descriptor_data)
            # end for
        # end if
        return ble_address, ble_descriptor
    # end def get_ble_descriptor

    @classmethod
    def check_ble_descriptor(cls, test_case, ble_descriptor, receiver_serial_number):
        """
        Retrieve a BLE descriptor which may have been split into several messages

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_descriptor: BLE Host descriptor.
        :type ble_descriptor: ``BLEDescriptorPage1Header``
        :param receiver_serial_number: Serial number
        :type receiver_serial_number: ``HexList``
        """
        for uuid_index in range(int(Numeral(ble_descriptor.number_of_uuids))):
            test_case.assertTrue(hasattr(ble_descriptor, f'uuid_{uuid_index}'))
            uuid_value = getattr(ble_descriptor, f'uuid_{uuid_index}')
            # ---------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Validate uuid size and data length are matching')
            # ---------------------------------------------------------------------------
            test_case.assertEqual(expected=int(Numeral(getattr(ble_descriptor, f'size_{uuid_index}'))),
                                  obtained=len(HexList(getattr(ble_descriptor, f'data_{uuid_index}'))),
                                  msg='UUID size and data length do not match')

            if int(Numeral(uuid_value)) == HostsInfoTestUtils.UUID.BLE_MANUFACTURER_NAME:
                # ---------------------------------------------------------------------------
                LogHelper.log_check(test_case, 'Validate BLE UUID Manufacturing Name')
                # ---------------------------------------------------------------------------
                test_case.assertEqual(expected=HostsInfoTestUtils.NAME.BLE_MANUFACTURER_NAME,
                                      obtained=ascii_converter(HexList(getattr(ble_descriptor, f'data_{uuid_index}'))),
                                      msg='The BLE UUID Manufacturing Name differs from the expected one')

            elif int(Numeral(uuid_value)) == HostsInfoTestUtils.UUID.BLE_MODEL_NUMBER:
                # ---------------------------------------------------------------------------
                LogHelper.log_check(test_case, 'Validate BLE UUID Model Number')
                # ---------------------------------------------------------------------------
                test_case.assertEqual(expected=HostsInfoTestUtils.NAME.BLE_MODEL_NUMBER,
                                      obtained=ascii_converter(HexList(getattr(ble_descriptor, f'data_{uuid_index}'))),
                                      msg='The BLE UUID Model Number differs from the expected one')

            elif (int(Numeral(uuid_value)) == HostsInfoTestUtils.UUID.BLE_SERIAL_NUMBER and
                  receiver_serial_number is not None):
                # ---------------------------------------------------------------------------
                LogHelper.log_check(test_case, 'Validate BLE UUID Serial Number')
                # ---------------------------------------------------------------------------
                test_case.assertEqual(expected=receiver_serial_number,
                                      obtained=HexList(getattr(ble_descriptor, f'data_{uuid_index}')),
                                      msg='The BLE UUID Serial Number differs from the expected one')
            else:
                test_case.fail(f'Unknown UUID received = 0x{uuid_value}')
            # end if
        # end for
    # end def check_ble_descriptor

# end class HostsInfoTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
