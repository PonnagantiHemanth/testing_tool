#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.deviceinformationutils
:brief:  Helpers for device information feature
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/11/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from json import load
from os.path import exists
from os.path import join
from sys import stdout

from PYTHON import pysetup
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationFactory
from pyhid.hidpp.features.common.deviceinformation import GetDeviceInfoResponseV1 # noqa
from pyhid.hidpp.features.common.deviceinformation import GetDeviceInfoResponseV2ToV3 # noqa
from pyhid.hidpp.features.common.deviceinformation import GetDeviceInfoResponseV4ToV5 # noqa
from pyhid.hidpp.features.common.deviceinformation import GetDeviceInfoResponseV6ToV8 # noqa
from pyhid.hidpp.features.common.deviceinformation import GetFwInfoResponseV1ToV7
from pyhid.hidpp.features.common.deviceinformation import GetFwInfoResponseV8
from pyhid.hidpp.features.common.deviceinformation import GetDeviceSerialNumberResponseV4ToV8
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceInformationTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on device information feature
    """
    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=DeviceInformation.FEATURE_ID, factory=DeviceInformationFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_device_info(cls, test_case, device_index=None, port_index=None):
            """
            Get device information (i.e. information that characterises the whole device)

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: The response to ``GetDeviceInfoV1ToV8`` request
            :rtype: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|GetDeviceInfoResponseV4ToV5|
            GetDeviceInfoResponseV6ToV8``
            """
            feature_0003_index, feature_0003, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0003.get_device_info_cls(test_case.deviceIndex, feature_0003_index)

            response = ChannelUtils.send(
                test_case=test_case, report=report, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_0003.get_device_info_response_cls)
            return response
        # end def get_device_info

        @classmethod
        def get_extended_model_id(cls, test_case):
            """
            Get extended model id

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Extended model id
            :rtype: ``int`` or ``HexList``
            """
            return cls.get_device_info(test_case=test_case).extended_model_id
        # end def get_extended_model_id

        @classmethod
        def get_fw_info(cls, test_case, entity_index, device_index=None, port_index=None):
            """
            Get device information (i.e. information that characterises the whole device)

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param entity_index: Index of the firmware or hardware entity
            :type entity_index: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: The response to ``GetFwInfoV1ToV8`` request
            :rtype: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            """
            feature_0003_index, feature_0003, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0003.get_fw_info_cls(test_case.deviceIndex, feature_0003_index, entity_index=entity_index)

            response = ChannelUtils.send(
                test_case=test_case, report=report, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_0003.get_fw_info_response_cls)
            return response
        # end def get_fw_info

        @classmethod
        def get_device_serial_number(cls, test_case, device_index=None, port_index=None):
            """
            Get device serial number

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: serial number
            :rtype: ``int`` or ``HexList``
            """
            feature_0003_index, feature_0003, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0003.get_device_serial_number_cls(device_index, feature_0003_index)

            response = ChannelUtils.send(
                test_case=test_case, report=report, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_0003.get_device_serial_number_response_cls)
            return response.serial_number
        # end def get_device_serial_number
    # end class HIDppHelper

    class GetDeviceInfoResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        TODO
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the getDeviceInfo API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "entity_count": (cls.check_entity_count,
                                 test_case.config_manager.get_feature(ConfigurationManager.ID.ENTITY_COUNT)),
                "unit_id": (cls.check_unit_id, test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_UnitId),
                "transport_reserved": (cls.check_transport_reserved, 0),
                "serial": (cls.check_serial, 0),
                "usb": (cls.check_usb,
                        test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb or
                        bool(test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_BootLoaderTransportUsb)),
                "e_quad": (cls.check_e_quad,
                           test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportEQuad or
                           bool(test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_BootLoaderTransportEQuad)),
                "btle": (cls.check_btle,
                         test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportBTLE or
                         bool(test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_BootLoaderTransportBTLE)),
                "bt": (cls.check_bt,
                       test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportBT or
                       bool(test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_BootLoaderTransportBT)),
                "model_id": (cls.check_model_id,
                             test_case.config_manager.get_feature(ConfigurationManager.ID.MODEL_ID)),
                "extended_model_id": (cls.check_extended_model_id,
                                      test_case.config_manager.get_feature(ConfigurationManager.ID.EXTENDED_MODEL_ID)),
                "capabilities_reserved": (cls.check_capabilities_reserved, 0),
                "serial_number": (cls.check_serial_number,
                                  test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_CapabilitiesSerialNumber)
            }
        # end def get_default_check_map

        @staticmethod
        def check_entity_count(test_case, get_device_info_response, expected):
            """
            Check entity count field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(get_device_info_response.entity_count)),
                                  expected=int(expected),
                                  msg="The entity_count parameter differs from the one expected")
        # end def check_entity_count

        @staticmethod
        def check_unit_id(test_case, get_device_info_response, expected):
            """
            Check unit id field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Set of valid expected values
            :type expected: ``list``
            """
            test_case.assertIn(member=str(HexList(get_device_info_response.unit_id)),
                               container=expected,
                               msg="The unit_id parameter differs from the one expected")
        # end def check_unit_id

        @staticmethod
        def check_transport_reserved(test_case, get_device_info_response, expected):
            """
            Check transport reserved field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=get_device_info_response.transport_reserved,
                                  expected=expected,
                                  msg="All transport reserved bits should be 0 (Reserved for future "
                                      "use")
        # end def check_transport_reserved

        @staticmethod
        def check_serial(test_case, get_device_info_response, expected):
            """
            Check serial field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(get_device_info_response.serial)),
                                  expected=int(expected),
                                  msg="The serial parameter differs from the one expected")
        # end def check_serial

        @staticmethod
        def check_usb(test_case, get_device_info_response, expected):
            """
            Check usb field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(get_device_info_response.usb)),
                                  expected=int(expected),
                                  msg="The usb parameter differs from the one expected")
        # end def check_usb

        @staticmethod
        def check_e_quad(test_case, get_device_info_response, expected):
            """
            Check eQuad field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(get_device_info_response.e_quad)),
                                  expected=int(expected),
                                  msg="The e_quad parameter differs from the one expected")
        # end def check_e_quad

        @staticmethod
        def check_btle(test_case, get_device_info_response, expected):
            """
            Check BTLE field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(get_device_info_response.btle)),
                                  expected=int(expected),
                                  msg="The btle parameter differs from the one expected")
        # end def check_btle

        @staticmethod
        def check_bt(test_case, get_device_info_response, expected):
            """
            Check BT field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(get_device_info_response.bt)),
                                  expected=int(expected),
                                  msg="The bt parameter differs from the one expected")
        # end def check_bt

        @staticmethod
        def check_model_id(test_case, get_device_info_response, expected):
            """
            Check modelID field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=HexList(get_device_info_response.model_id),
                                  expected=HexList(expected),
                                  msg="The model_id parameter differs from the one expected")
        # end def check_model_id

        @staticmethod
        def check_extended_model_id(test_case, get_device_info_response, expected):
            """
            Check extended model id field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                obtained=int(Numeral(get_device_info_response.extended_model_id)),
                expected=int(expected),
                msg="The extended_model_id parameter differs from the one expected")
        # end def check_extended_model_id

        @staticmethod
        def check_capabilities_reserved(test_case, get_device_info_response, expected):
            """
            Check capabilities field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=get_device_info_response.capabilities_reserved,
                                  expected=expected,
                                  msg="All reserved bits should be 0 (Reserved for future use")
        # end def check_capabilities_reserved

        @staticmethod
        def check_serial_number(test_case, get_device_info_response, expected):
            """
            Check serial number field in getDeviceInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_info_response: getDeviceInfo response to check
            :type get_device_info_response: ``GetDeviceInfoResponseV1|GetDeviceInfoResponseV2ToV3|
            GetDeviceInfoResponseV4ToV5|GetDeviceInfoResponseV6ToV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(
                obtained=int(Numeral(get_device_info_response.serial_number)),
                expected=int(expected),
                msg="The serial number parameter differs from the one expected")
        # end def check_serial_number
    # end class GetDeviceInfoResponseChecker

    class GetFwInfoResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        TODO
        """
        ERASED_VALUE = 0
        TWO_BYTES_ERASED_VALUE = HexList("0000")

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the getFwInfo API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :return: Default check map
            :rtype: ``dict``
            """
            return DeviceInformationTestUtils.GetFwInfoResponseChecker.get_check_map_for_entity(test_case,
                                                                                                entity_index=0)
        # end def get_default_check_map

        @classmethod
        def get_check_map_for_entity(cls, test_case, entity_index):
            """
            Get the default check methods and expected values for the getFwInfo API for a given entity index

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param entity_index: Index of the entity to check
            :type entity_index: ``int``
            :return: Default check map
            :rtype: ``dict``
            """
            # Fetch the json file in the DFU_FILES folder
            extra_ver_data_json = join(pysetup.TESTS_PATH, 'DFU_FILES', 'extraVer.json')

            extra_version_information = None
            if exists(extra_ver_data_json):
                with open(extra_ver_data_json, "r") as f:
                    json_data = load(f)
                # end with

                fw_type = str(int(test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_FwType[entity_index]))
                if fw_type in json_data:
                    extra_version_information = json_data[fw_type]
                # end if
            elif test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_ExtraVersionInformation:
                LogHelper.log_info(test_case, f"{extra_ver_data_json} does not existed. "
                                              f"Use F_ExtraVersionInformation[{entity_index}] from settings.ini")
                extra_version_information = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.\
                    F_ExtraVersionInformation[entity_index]
            else:
                test_case.log_warning(message="Skip extra version data check due to missing extraVer.json or specified "
                                              "values for F_ExtraVersionInformation in ini")
            # end if

            check_map = {
               "fw_type": (cls.check_fw_type, test_case.config_manager.get_feature(
                   ConfigurationManager.ID.FW_TYPE)[entity_index]),
               "fw_prefix": (cls.check_fw_prefix, test_case.config_manager.get_feature(
                   ConfigurationManager.ID.FW_PREFIX)[entity_index]),
               "fw_number": (cls.check_fw_number, test_case.config_manager.get_feature(
                   ConfigurationManager.ID.FW_NUMBER)[entity_index]),
               "fw_revision": (cls.check_fw_revision, test_case.config_manager.get_feature(
                   ConfigurationManager.ID.REVISION)[entity_index]),
               "fw_build": (cls.check_fw_build, test_case.config_manager.get_feature(
                   ConfigurationManager.ID.BUILD)[entity_index]),
               "reserved": (cls.check_reserved, test_case.config_manager.get_feature(
                   ConfigurationManager.ID.FW_RESERVED)[entity_index]),
               "slot_id": (cls.check_slot_id, 0),
               "invalid": (cls.check_invalid, 0),
               "active": None,
               "transport_id": (cls.check_transport_id, test_case.config_manager.get_feature(
                   ConfigurationManager.ID.TRANSPORT_ID)[entity_index]),
            }

            if extra_version_information:
                check_map["extra_version_information"] = \
                    (cls.check_extra_version_information, extra_version_information)
            else:
                check_map["extra_version_information"] = None
            # end if

            return check_map
        # end def get_check_map_for_entity

        @staticmethod
        def check_fw_type(test_case, get_fw_info_response, expected):
            """
            Check type field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            test_case.assertEqual(
                obtained=HexList(get_fw_info_response.fw_type),
                expected=HexList(expected),
                msg="The fw_type parameter differs from the one expected")
        # end def check_fw_type

        @staticmethod
        def check_fw_prefix(test_case, get_fw_info_response, expected):
            """
            Check fw prefix field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            test_case.assertEqual(
                obtained=HexList([i for i in get_fw_info_response.fw_prefix if i not in [0x00, 0x20]]),
                expected=HexList([ord(i) for i in expected if i != ' ']),
                msg="The fw_prefix parameter differs from the one expected")
        # end def check_fw_prefix

        @staticmethod
        def check_fw_number(test_case, get_fw_info_response, expected):
            """
            Check fw number field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            test_case.assertEqual(
                obtained=HexList(get_fw_info_response.fw_number),
                expected=HexList(expected),
                msg="The fw_number parameter differs from the one expected")
        # end def check_fw_number

        @staticmethod
        def check_fw_revision(test_case, get_fw_info_response, expected):
            """
            Check revision field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            test_case.assertEqual(
                obtained=HexList(get_fw_info_response.fw_revision),
                expected=HexList(expected),
                msg="The fw_revision parameter differs from the one expected")
        # end def check_fw_revision

        @staticmethod
        def check_fw_build(test_case, get_fw_info_response, expected):
            """
            Check build field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            if expected == 'None':
                stdout.write("The fw_build parameter shall be defined in settings for all entities to be compared "
                             f"with the received value = 0x{HexList(get_fw_info_response.fw_build)}\n")
            else:
                test_case.assertEqual(
                    obtained=HexList(get_fw_info_response.fw_build),
                    expected=HexList(expected),
                    msg="The fw_build parameter differs from the one expected")
            # end if
        # end def check_fw_build

        @staticmethod
        def check_reserved(test_case, get_fw_info_response, expected):
            """
            Check reserved field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=get_fw_info_response.reserved,
                                  expected=int(expected),
                                  msg="All reserved bits should be 0 (Reserved for future use")
        # end def check_reserved

        @staticmethod
        def check_slot_id(test_case, get_fw_info_response, expected):
            """
            Check slot_id field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=get_fw_info_response.slot_id,
                                  expected=expected,
                                  msg="The slot_id parameter differs from the one expected")
        # end def check_slot_id

        @staticmethod
        def check_invalid(test_case, get_fw_info_response, expected):
            """
            Check invalid field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=get_fw_info_response.invalid,
                                  expected=expected,
                                  msg="The invalid parameter differs from the one expected")
        # end def check_invalid

        @staticmethod
        def check_active(test_case, get_fw_info_response, expected):
            """
            Check active field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=get_fw_info_response.active,
                                  expected=expected,
                                  msg="The active parameter differs from the one expected")
        # end def check_active

        @staticmethod
        def check_transport_id(test_case, get_fw_info_response, expected):
            """
            Check transport id field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            test_case.assertEqual(
                obtained=HexList(get_fw_info_response.transport_id),
                expected=HexList(expected),
                msg="The transport_id parameter differs from the one expected")
        # end def check_transport_id

        @staticmethod
        def check_extra_version_information(test_case, get_fw_info_response, expected):
            """
            Check extra version information field in getFwInfo response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_fw_info_response: getFwInfo response to check
            :type get_fw_info_response: ``GetFwInfoResponseV1ToV7|GetFwInfoResponseV8``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            test_case.assertEqual(
                obtained=HexList(get_fw_info_response.extra_version_information),
                expected=HexList(expected),
                msg="The extra_version_information parameter differs from the one expected")
        # end def check_extra_version_information

        @classmethod
        def get_check_erased_entity(cls, test_case, entity_index=0):
            """
            Get the default check methods and expected values for the getFwInfo API for a given entity index

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param entity_index: Index of the entity to check
            :type entity_index: ``int``
            :return: check map
            :rtype: ``dict``
            """
            return {
                "fw_type": (cls.check_fw_type, cls.ERASED_VALUE),
                "fw_prefix": (cls.check_fw_prefix, ''),
                "fw_number": (cls.check_fw_number, cls.ERASED_VALUE),
                "fw_revision": (cls.check_fw_revision, cls.ERASED_VALUE),
                "fw_build": (cls.check_fw_build, cls.TWO_BYTES_ERASED_VALUE),
                "reserved": (cls.check_reserved, cls.ERASED_VALUE),
                "active": None,
                "transport_id": (cls.check_transport_id, cls.TWO_BYTES_ERASED_VALUE),
                "extra_version_information": None
            }
        # end def get_check_erased_entity
    # end class GetFwInfoResponseChecker

    class GetDeviceSerialNumberResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        TODO
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the getDeviceSerialNumber API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "serial_number": (cls.check_device_serial_number,
                                  test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_SerialNumber),
            }
        # end def get_default_check_map

        @staticmethod
        def check_device_serial_number(test_case, get_device_serial_number_response, expected):
            """
            Check serial number field in getDeviceSerialNumber response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param get_device_serial_number_response: getDeviceSerialNumber response to check
            :type get_device_serial_number_response: ``GetDeviceSerialNumberResponseV4ToV8``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            test_case.assertEqual(
                obtained=HexList(get_device_serial_number_response.serial_number),
                expected=HexList(expected),
                msg="The serial_number parameter differs from the one expected")
        # end def check_device_serial_number
    # end class GetDeviceSerialNumberResponseChecker

    @classmethod
    def get_active_entity_type(cls, test_case, device_index):
        """
        Get type of the active entity

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param device_index: Index of the device
        :type device_index: ``int``

        :return: Expected entity type
        :rtype: ``int``
        """
        fw_type_active = None
        for entity_index in range(test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount):
            get_fw_info_response = cls.HIDppHelper.get_fw_info(test_case=test_case, entity_index=entity_index,
                                                               device_index=device_index)

            if get_fw_info_response.active:
                fw_type_active = get_fw_info_response.fw_type
                break
            # end if
        # end for
        return int(Numeral(fw_type_active))
    # end def get_active_entity_type

    @classmethod
    def check_active_entity_type(cls, test_case, device_index, entity_type):
        """
        Check type of the active entity

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param device_index: Index of the device
        :type device_index: ``int``
        :param entity_type: Expected entity type
        :type entity_type: ``int``
        """
        fw_type_active = cls.get_active_entity_type(test_case, device_index)

        test_case.assertEquals(expected=int(entity_type),
                               obtained=fw_type_active,
                               msg='Device is not in expected mode')
    # end def check_active_entity_type

    @classmethod
    def check_active_entity_type_is_main_app(cls, test_case, device_index):
        """
        Check type of the active entity is "Main application"

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param device_index: Index of the device
        :type device_index: ``int``
        """
        cls.check_active_entity_type(test_case, device_index, DeviceInformation.EntityTypeV1.MAIN_APP)
    # end def check_active_entity_type_is_main_app

    @staticmethod
    def get_upgradable_entities(test_case,
                                device_index):
        """
        Get the list of entities with their upgradable capability : index of the entity is set to
        true in the list if the entity is upgradable

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param device_index: Index of the device
        :type device_index: ``int``
        :return: List of upgradable capability for each entity
        :rtype: ``list``
        """
        int_upgradable_entity_types = [int(x) for x in
                                       test_case.f.PRODUCT.FEATURES.COMMON.DFU.F_UpgradableEntityTypes]
        upgradable_entities = [False] * test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount
        for entity_index in range(test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount):
            get_fw_info_response = DeviceInformationTestUtils.HIDppHelper.get_fw_info(
                test_case=test_case, entity_index=entity_index, device_index=device_index)

            if int(Numeral(get_fw_info_response.fw_type)) in int_upgradable_entity_types:
                upgradable_entities[entity_index] = True
            # end if
        # end for
        return upgradable_entities
    # end def get_upgradable_entities
# end class DeviceInformationTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
