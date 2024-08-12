#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.lightspeedprepairingutils
:brief: Helpers for ``LightspeedPrepairing`` feature
:author: Zane Lu <zlu@logitech.com>
:date: 2022/06/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.lightspeedprepairing import GetPrepairingData
from pyhid.hidpp.features.common.lightspeedprepairing import LightspeedPrepairing
from pyhid.hidpp.features.common.lightspeedprepairing import LightspeedPrepairingFactory
from pyhid.hidpp.features.common.lightspeedprepairing import PrepairingManagement
from pyhid.hidpp.features.common.lightspeedprepairing import SetLTK
from pyhid.hidpp.features.common.lightspeedprepairing import SetPrepairingData
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.receiver.base.receiverinfoutils import ReceiverInfoUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LightspeedPrepairingTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``LightspeedPrepairing`` feature
    """

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetCapabilities`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetCapabilitiesResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.LIGHTSPEED_PREPAIRING
            return {
                "reserved_flags": (
                    cls.check_reserved_flags, 0),
                "reserved_slots": (
                    cls.check_reserved_slots, 0),
                "use_attr": (
                    cls.check_use_attr, config.F_UseAttr),
                "ls2": (
                    cls.check_ls2, config.F_Ls2Slot),
                "crush": (
                    cls.check_crush, config.F_CrushSlot),
                "ls": (
                    cls.check_ls, config.F_LsSlot)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved_flags(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved_flags),
                msg=f"The reserved_flags parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved_flags})")
        # end def check_reserved_flags

        @staticmethod
        def check_reserved_slots(test_case, response, expected):
            """
            Check reserved_slots field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved_slots),
                msg=f"The reserved_slots parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved_slots})")
        # end def check_reserved_slots

        @staticmethod
        def check_use_attr(test_case, response, expected):
            """
            Check use_attr field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.use_attr)),
                msg=f"The use_attr parameter differs "
                    f"(expected:{expected}, obtained:{response.use_attr})")
        # end def check_use_attr

        @staticmethod
        def check_ls2(test_case, response, expected):
            """
            Check ls2 field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.ls2),
                msg=f"The ls2 parameter differs "
                    f"(expected:{expected}, obtained:{response.ls2})")
        # end def check_ls2

        @staticmethod
        def check_crush(test_case, response, expected):
            """
            Check crush field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.crush),
                msg=f"The crush parameter differs "
                    f"(expected:{expected}, obtained:{response.crush})")
        # end def check_crush

        @staticmethod
        def check_ls(test_case, response, expected):
            """
            Check ls field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.ls),
                msg=f"The ls parameter differs "
                    f"(expected:{expected}, obtained:{response.ls})")
        # end def check_ls
    # end class GetCapabilitiesResponseChecker

    class GetPrepairingDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetPrepairingData`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetPrepairingDataResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "information_type": (
                    cls.check_information_type, None),
                "data_type": (
                    cls.check_data_type, None),
                "data": (
                    cls.check_data, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_information_type(test_case, response, expected):
            """
            Check information_type field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPrepairingDataResponse to check
            :type response: ``GetPrepairingDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.information_type)),
                msg=f"The information_type parameter differs "
                    f"(expected:{expected}, obtained:{response.information_type})")
        # end def check_information_type

        @staticmethod
        def check_data_type(test_case, response, expected):
            """
            Check data_type field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPrepairingDataResponse to check
            :type response: ``GetPrepairingDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.data_type)),
                msg=f"The data_type parameter differs "
                    f"(expected:{expected}, obtained:{response.data_type})")
        # end def check_data_type

        @staticmethod
        def check_data(test_case, response, expected):
            """
            Check data field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPrepairingDataResponse to check
            :type response: ``GetPrepairingDataResponse``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.data)),
                msg=f"The data parameter differs "
                    f"(expected:{expected}, obtained:{response.data})")
        # end def check_data
    # end class GetPrepairingDataResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=LightspeedPrepairing.FEATURE_ID,
                           factory=LightspeedPrepairingFactory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetCapabilitiesResponse
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_1817_index, feature_1817, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1817.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_1817_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1817.get_capabilities_response_cls)
            return response
        # end def get_capabilities

        @classmethod
        def prepairing_management(cls, test_case, ls2, crush, ls, prepairing_management_control, device_index=None, port_index=None):
            """
            Process ``PrepairingManagement``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param ls2: LS2
            :type ls2: ``bool`` or ``HexList``
            :param crush: Crush
            :type crush: ``bool`` or ``HexList``
            :param ls: LS
            :type ls: ``bool`` or ``HexList``
            :param prepairing_management_control: prepairing_management_control
            :type prepairing_management_control: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: PrepairingManagementResponse
            :rtype: ``PrepairingManagementResponse``
            """
            feature_1817_index, feature_1817, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1817.prepairing_management_cls(
                device_index=device_index,
                feature_index=feature_1817_index,
                ls2=ls2,
                crush=crush,
                ls=ls,
                prepairing_management_control=HexList(prepairing_management_control))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1817.prepairing_management_response_cls)
            return response
        # end def prepairing_management

        @classmethod
        def set_ltk(cls, test_case, ltk, device_index=None, port_index=None):
            """
            Process ``SetLTK``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param ltk: ltk
            :type ltk: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetLTKResponse
            :rtype: ``SetLTKResponse``
            """
            feature_1817_index, feature_1817, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1817.set_ltk_cls(
                device_index=device_index,
                feature_index=feature_1817_index,
                ltk=ltk)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1817.set_ltk_response_cls)
            return response
        # end def set_ltk

        @classmethod
        def set_prepairing_data(cls, test_case, data_type,
                                pairing_address_base=None, address_dest=None,
                                equad_attributes=None,
                                device_index=None, port_index=None):
            """
            Process ``SetPrepairingData``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param data_type: Data Type
            :type data_type: ``int`` or ``HexList``
            :param pairing_address_base: pairing address base - OPTIONAL
            :type pairing_address_base: ``HexList``
            :param address_dest: address dest - OPTIONAL
            :type address_dest: `int`` or ``HexList``
            :param equad_attributes: equad attributes - OPTIONAL
            :type equad_attributes: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetPrepairingDataResponse
            :rtype: ``SetPrepairingDataResponse``
            """
            feature_1817_index, feature_1817, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            if HexList(data_type) == HexList(SetPrepairingData.DataType.PAIRING_ADDRESS):
                report = feature_1817.set_prepairing_data_cls(
                    device_index=device_index,
                    feature_index=feature_1817_index,
                    data_type=HexList(data_type),
                    pairing_address_base=pairing_address_base,
                    address_dest=address_dest)
            else:
                report = feature_1817.set_prepairing_data_cls(
                    device_index=device_index,
                    feature_index=feature_1817_index,
                    data_type=HexList(data_type),
                    equad_attributes=equad_attributes)
            # end if
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1817.set_prepairing_data_response_cls)
            return response
        # end def set_prepairing_data

        @classmethod
        def get_prepairing_data(cls, test_case, information_type, data_type,
                                device_index=None, port_index=None):
            """
            Process ``GetPrepairingData``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param information_type: information_type
            :type information_type: ``int`` or ``HexList``
            :param data_type: data_type
            :type data_type: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetPrepairingDataResponse
            :rtype: ``GetPrepairingDataResponse``
            """
            feature_1817_index, feature_1817, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1817.get_prepairing_data_cls(
                device_index=device_index,
                feature_index=feature_1817_index,
                information_type=HexList(information_type),
                data_type=HexList(data_type),
                reserved=HexList("00" * (GetPrepairingData.LEN.RESERVED // 8)))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1817.get_prepairing_data_response_cls)
            return response
        # end def get_prepairing_data
    # end class HIDppHelper

    @classmethod
    def get_the_pairing_information_from_the_receiver(cls, test_case, port_index=None):
        """
        Get the receiver base address, last dest id and the pairing info equad attributes

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param port_index: Port index - OPTIONAL
        :type port_index: ``int``

        :return: (receiver base address, receiver last dest id, pairing info equad attributes)
        :rtype: (``HexList``, ``int``, ``HexList``)
        """
        port_index = port_index if port_index is not None else ChannelUtils.get_port_index(
            test_case=test_case)

        # switch to the receiver channel
        initial_device_index = ChannelUtils.get_device_index(test_case=test_case)
        ChannelUtils.close_channel(test_case=test_case)
        new_channel = DeviceManagerUtils.get_channel(
            test_case=test_case,
            channel_id=ChannelIdentifier(port_index=port_index, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER))
        DeviceManagerUtils.set_channel(test_case=test_case, new_channel=new_channel)

        equad_info_response = ReceiverInfoUtils.get_receiver_equad_info(test_case=test_case)
        pairing_info_response = ReceiverInfoUtils.get_receiver_pairing_info(test_case=test_case)

        # switch to the device channel
        ChannelUtils.close_channel(test_case=test_case)
        new_channel = DeviceManagerUtils.get_channel(
            test_case=test_case,
            channel_id=ChannelIdentifier(port_index=port_index, device_index=initial_device_index))
        DeviceManagerUtils.set_channel(test_case=test_case, new_channel=new_channel)

        return equad_info_response.base_address,\
               equad_info_response.last_dest_id,\
               pairing_info_response.equad_attributes
    # end def get_the_pairing_information_from_the_receiver

    @classmethod
    def pre_pairing_sequence(cls, test_case, slot_index, base_address=None, last_dest_id=None,
                             equad_attributes=None, long_term_key=None, port_index=None):
        """
        Set the base address with the last dest id
        Set the equad attributes

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param slot_index: index for LS(0x01), Crush(0x02), LS2(0x04)
        :type slot_index: ``int | PrepairingManagement.PairingSlot``
        :param base_address: Receiver base address - OPTIONAL
        :type base_address: ``HexList``
        :param last_dest_id: Receiver last dest id - OPTIONAL
        :type last_dest_id: ``int``
        :param equad_attributes: Receiver equad attributes - OPTIONAL
        :type equad_attributes: ``HexList``
        :param long_term_key: Long Term Key - OPTIONAL
        :type long_term_key: ``HexList``
        :param port_index: Port index - OPTIONAL
        :type port_index: ``int``

        :return: Long term key
        :rtype: ``HexList``
        """
        test_case.post_requisite_reload_nvs = True

        equad_info, pairing_info, extended_pairing_info, equad_name, fw_information = \
            ReceiverTestUtils.get_receiver_nv_pairing_info(test_case=test_case)

        base_address = base_address if base_address is not None else equad_info.base_address
        last_dest_id = last_dest_id if last_dest_id is not None else equad_info.last_dest_id
        equad_attributes = equad_attributes if equad_attributes is not None else pairing_info.equad_attributes

        cls.HIDppHelper.prepairing_management(
            test_case=test_case,
            ls2=(slot_index == PrepairingManagement.PairingSlot.LS2),
            crush=(slot_index == PrepairingManagement.PairingSlot.CRUSH),
            ls=(slot_index == PrepairingManagement.PairingSlot.LS),
            prepairing_management_control=PrepairingManagement.Control.START
        )

        cls.HIDppHelper.set_prepairing_data(test_case, SetPrepairingData.DataType.PAIRING_ADDRESS,
                                            pairing_address_base=base_address,
                                            address_dest=last_dest_id)
        cls.HIDppHelper.set_prepairing_data(test_case, SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
                                            equad_attributes=equad_attributes)

        if long_term_key is None:
            long_term_key = RandHexList(SetLTK.LEN.LTK//8)
            long_term_key[6] = to_int(fw_information.equad_id) >> 8,
            long_term_key[7] = to_int(fw_information.equad_id) & 0xFF,
        # end if

        cls.HIDppHelper.set_ltk(test_case, long_term_key)

        cls.HIDppHelper.prepairing_management(
            test_case=test_case,
            ls2=(slot_index == PrepairingManagement.PairingSlot.LS2),
            crush=(slot_index == PrepairingManagement.PairingSlot.CRUSH),
            ls=(slot_index == PrepairingManagement.PairingSlot.LS),
            prepairing_management_control=PrepairingManagement.Control.STORE
        )
        return long_term_key
    # end def pre_pairing_sequence

    @classmethod
    def get_pairing_information(cls, test_case, slot_index, information_type=GetPrepairingData.InfoType.PAIRING):
        """
        Get the base address with the last dest id
        Get the equad attributes

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param slot_index: index for LS(0x01), Crush(0x02), LS2(0x04)
        :type slot_index: ``int | PrepairingManagement.PairingSlot``
        :param information_type: Pairing information Type - OPTIONAL
        :type information_type: ``int``

        :return: (base address, last dest id, equad attributes)
        :rtype: ``tuple[HexList, int, HexList]``
        """
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=test_case,
            ls2=(slot_index == PrepairingManagement.PairingSlot.LS2),
            crush=(slot_index == PrepairingManagement.PairingSlot.CRUSH),
            ls=(slot_index == PrepairingManagement.PairingSlot.LS),
            prepairing_management_control=PrepairingManagement.Control.START
        )

        address_data = LightspeedPrepairingTestUtils.HIDppHelper.get_prepairing_data(
            test_case=test_case,
            information_type=information_type,
            data_type=GetPrepairingData.DataType.PAIRING_ADDRESS
        )

        attributes_data = LightspeedPrepairingTestUtils.HIDppHelper.get_prepairing_data(
            test_case=test_case,
            information_type=information_type,
            data_type=GetPrepairingData.DataType.EQUAD_ATTRIBUTES
        )

        return address_data.data.pairing_address_base,\
               address_data.data.address_dest,\
               attributes_data.data.equad_attributes
    # end def get_pairing_information
# end class LightspeedPrepairingTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
