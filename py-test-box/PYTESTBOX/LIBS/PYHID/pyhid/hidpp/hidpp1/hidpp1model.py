#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.hidpp1model
    :brief: HID++ 1.0 Set Register Model
    :author: Christophe Roquebert
    :date: 2020/02/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.bleservicechanged import BleServiceChanged
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.devicerecovery import DeviceRecovery
from pyhid.hidpp.hidpp1.notifications.dfutimeout import DfuTimeout
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.notifications.displaypasskeykey import DisplayPassKeyKey
from pyhid.hidpp.hidpp1.notifications.linkqualityinfo import LinkQualityInfoLong
from pyhid.hidpp.hidpp1.notifications.linkqualityinfo import LinkQualityInfoShort
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.hidpp1.notifications.requestdisplaypasskey import RequestDisplayPassKey
from pyhid.hidpp.hidpp1.registers.connectionstate import ConnectionStateModel
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import EnableHidReportingModel
from pyhid.hidpp.hidpp1.registers.enterupgrademode import EnterUpgradeModeModel
from pyhid.hidpp.hidpp1.registers.getrssi import GetRssiModel
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesEnableModel
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesInfoAndDisableModel
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import NonVolatileMemoryAccessModel
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryoperation import NonVolatileMemoryOperationModel
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformationModel
from pyhid.hidpp.hidpp1.registers.passwd import PasswordModel
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import PerformDeviceConnectionModel
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscoveryModel
from pyhid.hidpp.hidpp1.registers.prepairingdata import PrepairingDataModel
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import PrepairingManagementModel
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnectionModel
from pyhid.hidpp.hidpp1.registers.randomdata import RandomDataModel
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import ReceiverFwInfoModel
from pyhid.hidpp.hidpp1.registers.reset import ResetModel
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import RFRegisterAccessModel
from pyhid.hidpp.hidpp1.registers.securedfucontrol import SecureDfuControlModel
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyCentralModel
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyPeripheralModel
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyCentralModel
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyPeripheralModel
from pyhid.hidpp.hidpp1.registers.setltkkey import SetLTKKeyModel
from pyhid.hidpp.hidpp1.registers.startsession import StartSessionModel
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControlModel
from pyhid.hidpp.hidpp1.registers.uniqueidentifier import UniqueIdentifierModel
from pyhid.hidpp.hidpp1.setgetregister import Hidpp1RegisterModel


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class Hidpp1RegisterMap(object):
    """
    HID++ 1.0 Register Map representation
    """
    @classmethod
    def _get_data_model(cls):
        """
        Register Map data model. Map register address to class

        :return: Register data model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterAddress.ENABLE_HIDPP_REPORTING: EnableHidReportingModel,
            Hidpp1Data.Hidpp1RegisterAddress.CONNECTION_STATE: ConnectionStateModel,
            Hidpp1Data.Hidpp1RegisterAddress.QUAD_DEVICE_CONNECTION: QuadDeviceConnectionModel,
            Hidpp1Data.Hidpp1RegisterAddress.GET_RSSI: GetRssiModel,
            Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION: NonVolatilePairingInformationModel,
            Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_DISCOVERY: PerformDeviceDiscoveryModel,
            Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_CONNECTION_DISCONNECTION: PerformDeviceConnectionModel,
            Hidpp1Data.Hidpp1RegisterAddress.TEST_MODE_CONTROL: TestModeControlModel,
            Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS: RFRegisterAccessModel,
            Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS: NonVolatileMemoryAccessModel,
            Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_OPERATION: NonVolatileMemoryOperationModel,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT: PrepairingManagementModel,
            Hidpp1Data.Hidpp1RegisterAddress.SET_LTK_KEY: SetLTKKeyModel,
            Hidpp1Data.Hidpp1RegisterAddress.SET_IRK_KEY_CENTRAL: SetIRKKeyCentralModel,
            Hidpp1Data.Hidpp1RegisterAddress.SET_IRK_KEY_PERIPHERAL: SetIRKKeyPeripheralModel,
            Hidpp1Data.Hidpp1RegisterAddress.SET_CSRK_KEY_CENTRAL: SetCSRKKeyCentralModel,
            Hidpp1Data.Hidpp1RegisterAddress.SET_CSRK_KEY_PERIPHERAL: SetCSRKKeyPeripheralModel,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA: PrepairingDataModel,
            Hidpp1Data.Hidpp1RegisterAddress.ENTER_FIRMWARE_UPGRADE_MODE: EnterUpgradeModeModel,
            Hidpp1Data.Hidpp1RegisterAddress.RESET: ResetModel,
            Hidpp1Data.Hidpp1RegisterAddress.RECEIVER_FW_INFO: ReceiverFwInfoModel,
            Hidpp1Data.Hidpp1RegisterAddress.DFU_CONTROL: SecureDfuControlModel,
            Hidpp1Data.Hidpp1RegisterAddress.RANDOM_DATA: RandomDataModel,
            Hidpp1Data.Hidpp1RegisterAddress.START_SESSION: StartSessionModel,
            Hidpp1Data.Hidpp1RegisterAddress.PASSWORD: PasswordModel,
            Hidpp1Data.Hidpp1RegisterAddress.MANAGE_DEACTIVATABLE_FEATURES_GET_INFO_AND_DISABLE_FEATURES:
                ManageDeactivatableFeaturesInfoAndDisableModel,
            Hidpp1Data.Hidpp1RegisterAddress.MANAGE_DEACTIVATABLE_FEATURES_ENABLE_FEATURES:
                ManageDeactivatableFeaturesEnableModel,
            Hidpp1Data.Hidpp1RegisterAddress.UNIQUE_IDENTIFIER: UniqueIdentifierModel,
        }
    # end def _get_data_model

    @classmethod
    def has_r0(cls, address):
        """
        Check if a register address has a R0 field

        :return: True if r0
        :rtype: ``bool``
        """
        return cls._get_data_model()[address].has_r0() if address in cls._get_data_model().keys() else False
    # end def has_r0

    @classmethod
    def get_message_cls(cls, sub_id, message_type, address, r0=None):
        """
        Get matching message class

        :param sub_id: Register Sub Id
        :type sub_id: ``int``
        :param message_type: Message type (request or response)
        :type message_type: ``string``
        :param address: Register address
        :type address: ``int``
        :param r0: Register R0
        :type r0: ``int``
        :return: Message class
        :rtype: ``class``
        """
        data_model = cls._get_data_model()
        return data_model[address].get_message_cls(sub_id, message_type, r0) if address in data_model else None
    # end def get_message_cls

    @classmethod
    def get_available_responses_classes(cls):
        """
        Get all available response classes in model

        :return: Response classes
        :rtype: ``tuple``
        """
        responses = []
        for reg_cls in cls._get_data_model().values():
            responses += reg_cls.get_available_responses_classes()
        # end for
        return tuple(responses)
    # end def get_available_responses_classes

    @classmethod
    def get_available_requests_classes(cls):
        """
        Get all available requests classes in model

        :return: Requests classes
        :rtype: ``tuple``
        """
        requests = []
        for reg_cls in cls._get_data_model().values():
            requests += reg_cls.get_available_requests_classes()
        # end for
        return tuple(requests)
    # end def get_available_requests_classes

    @classmethod
    def get_available_classes(cls):
        """
        Get all available classes in the model

        :return: All classes
        :rtype: ``tuple``
        """
        return cls.get_available_requests_classes() + cls.get_available_responses_classes()
    # end def get_available_classes

    @classmethod
    def get_available_responses_map(cls):
        """
        Get available response classes mapped with their sub id, address and r0

        :return: Response classes map
        :rtype: ``dict``
        """
        responses_map = {}
        for reg_addr, reg_cls in cls._get_data_model().items():
            for sub_id in reg_cls.get_sub_ids():
                responses_map[(sub_id, reg_addr)] = reg_cls.get_message_cls(sub_id, "response")
            # end for
            for r0 in reg_cls.get_r0s():
                for sub_id in reg_cls.get_sub_ids():
                    responses_map[(sub_id, reg_addr, r0)] = reg_cls.get_message_cls(sub_id, "response", r0)
                # end for
            # end for
        # end for
        return responses_map
    # end def get_available_responses_map
# end class Hidpp1RegisterMap


class Hidpp1NotificationMap(object):
    """
    HID++ 1.0 Notifications map
    """
    @classmethod
    def get_available_events_map(cls):
        """
        Get available event classes mapped with their sub id

        :return: Response classes map
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1NotificationSubId.DEVICE_DISCONNECTION: DeviceDisconnection,
            Hidpp1Data.Hidpp1NotificationSubId.DEVICE_CONNECTION: DeviceConnection,
            Hidpp1Data.Hidpp1NotificationSubId.LINK_QUALITY_INFO_LONG: LinkQualityInfoLong,
            Hidpp1Data.Hidpp1NotificationSubId.LINK_QUALITY_INFO_SHORT: LinkQualityInfoShort,
            Hidpp1Data.Hidpp1NotificationSubId.REQUEST_DISPLAY_PASSKEY: RequestDisplayPassKey,
            Hidpp1Data.Hidpp1NotificationSubId.DISPLAY_PASSKEY_KEY: DisplayPassKeyKey,
            Hidpp1Data.Hidpp1NotificationSubId.DEVICE_DISCOVERY: DeviceDiscovery,
            Hidpp1Data.Hidpp1NotificationSubId.DEVICE_RECOVERY: DeviceRecovery,
            Hidpp1Data.Hidpp1NotificationSubId.DISCOVERY_STATUS: DiscoveryStatus,
            Hidpp1Data.Hidpp1NotificationSubId.PAIRING_STATUS: PairingStatus,
            Hidpp1Data.Hidpp1NotificationSubId.BLE_SERVICE_CHANGED: BleServiceChanged,
            Hidpp1Data.Hidpp1NotificationSubId.DFU_TIMEOUT: DfuTimeout,
        }
    # end def get_available_events_map

    @classmethod
    def get_connection_events_classes(cls):
        """
        Get connection event classes

        :return: Connection event classes
        :rtype: ``tuple``
        """
        events = [
            DeviceDisconnection,
            DeviceConnection,
        ]
        return tuple(events)
    # end def get_connection_events_classes

    @classmethod
    def get_available_events_classes(cls):
        """
        Get all available response classes in model

        :return: Event classes
        :rtype: ``tuple``
        """
        events = list(cls.get_available_events_map().values())
        events.remove(DeviceConnection)
        events.remove(DeviceDisconnection)
        return tuple(events)
    # end def get_available_events_classes
# end class Hidpp1NotificationMap


class Hidpp1Model(object):
    """
    HID++ 1.0 model
    """
    @classmethod
    def _get_data_model(cls):
        """
        HID++ 1.0 global model

        :return: Model
        :rtype: ``dict``
        """
        return {
            "register_notification": Hidpp1NotificationMap,
            "register_types": Hidpp1RegisterModel,
            "register_map": Hidpp1RegisterMap
        }
    # end def _get_data_model

    @classmethod
    def get_register_sub_ids(cls):
        """
        Get register Sub Ids

        :return: Sub Ids
        :rtype: ``list``
        """
        return cls._get_data_model()["register_types"].get_sub_ids()
    # end def get_register_sub_ids

    @classmethod
    def get_reg_sub_id_base_cls(cls, sub_id, message_type):
        """
        Get register class

        :param sub_id: Register Sub Id
        :type sub_id: ``int``
        :param message_type: Message type (request or response)
        :type message_type: ``string``
        :return: Register class
        :rtype: ``class``
        """
        return cls._get_data_model()["register_types"].get_message_cls(sub_id, message_type)
    # end def get_sub_id_base_cls

    @classmethod
    def has_r0(cls, address):
        """
        Check if register model has r0

        :param address: address of the register
        :type address: ``int``
        :return: True if register model has r0
        :rtype: ``bool``
        """
        return cls._get_data_model()["register_map"].has_r0(address)
    # end def has_r0

    @classmethod
    def get_message_cls(cls, sub_id, message_type, address=None, r0=None):
        """
        Get message class

        :param sub_id: Register sub id
        :type sub_id: ``int``
        :param message_type: Message type (request or response)
        :type message_type: ``string``
        :param address: Register address
        :type address: ``int``
        :param r0: Register R0
        :type r0: ``int``
        :return: Message class
        :rtype: ``class``
        """
        data_model = cls._get_data_model()
        msg_cls = data_model["register_map"].get_message_cls(sub_id, message_type, address, r0)
        if msg_cls is None:
            msg_cls = data_model["register_types"].get_message_cls(sub_id, message_type)
        return msg_cls
    # end def get_message_cls

    @classmethod
    def get_available_responses_classes(cls):
        """
        List of responses listed in the model

        :return: list of response classes
        :rtype: ``tuple``
        """
        data_model = cls._get_data_model()
        responses = data_model["register_types"].get_available_responses_classes()
        responses += data_model["register_map"].get_available_responses_classes()
        return tuple(responses)
    # end def get_available_responses_classes

    @classmethod
    def get_available_responses_map(cls):
        """
        Get available responses map with their sub id, address and r0

        :return: Available responses map
        :rtype: ``dict``
        """
        data_model = cls._get_data_model()
        return {
            **data_model["register_types"].get_available_responses_map(),
            **data_model["register_map"].get_available_responses_map(),
        }
    # end def get_available_responses_map

    @classmethod
    def get_available_events_map(cls):
        """
        Get available events map with their sub id

        :return: Available responses map
        :rtype: ``dict``
        """
        data_model = cls._get_data_model()
        return {
            **data_model["register_notification"].get_available_events_map(),
        }
    # end def get_available_events_map

    @classmethod
    def get_available_events_classes(cls):
        """
        List of events listed in the model

        :return: list of response classes
        :rtype: ``tuple``
        """
        data_model = cls._get_data_model()
        responses = data_model["register_notification"].get_available_events_classes()
        return tuple(responses)
    # end def get_available_events_classes

    @classmethod
    def get_connection_events_classes(cls):
        """
        List of connection notifications listed in the model

        :return: list of response classes
        :rtype: ``tuple``
        """
        data_model = cls._get_data_model()
        responses = data_model["register_notification"].get_connection_events_classes()
        return tuple(responses)
    # end def get_connection_events_classes
# end def Hidpp1Model

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
