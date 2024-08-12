#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.emulatorsmanager
:brief: Emulators Management class
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/10/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.emulatorinterfaces import EmulatorInterface
from pyraspi.raspi import Raspi
from pyraspi.services.basicbuttonemulator import BasicButtonEmulator
from pyraspi.services.daemon import Daemon
from pyraspi.services.gamemodebuttonemulator import GameModeButtonEmulator
from pyraspi.services.gamemodeslideremulator import GameModeSliderEmulator
from pyraspi.services.jlinkconnectioncontrol import FtdiPoweredDeviceJlinkConnectionControl
from pyraspi.services.jlinkconnectioncontrol import KosmosJlinkConnectionControl
from pyraspi.services.jlinkconnectioncontrol import MockJlinkConnectionControl
from pyraspi.services.jlinkconnectioncontrol import PowerSupplyBoardJlinkConnectionControl
from pyraspi.services.keyboardemulator import KeyboardEmulator
from pyraspi.services.kosmos.ambientlightsensoremulator import AmbientLightSensorEmulator
from pyraspi.services.kosmos.buttonemulator import KosmosButtonEmulator
from pyraspi.services.kosmos.config.alsconfiguration import GET_ALS_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.config.buttonlayout import BUTTON_LAYOUT_BY_ID
from pyraspi.services.kosmos.config.keybaordlayout import GET_KEYBOARD_LAYOUT_BY_ID
from pyraspi.services.kosmos.config.ledlayout import GET_LED_LAYOUT_BY_ID
from pyraspi.services.kosmos.config.opticalsensorconfig import SENSOR_ORIENTATION_BY_ID
from pyraspi.services.kosmos.config.sliderlayout import PROXIMITY_SENSOR_LAYOUT_BY_ID
from pyraspi.services.kosmos.config.sliderlayout import SLIDER_LAYOUT_BY_ID
from pyraspi.services.kosmos.dualkeymatrixemulator import KosmosDualKeyMatrixEmulator
from pyraspi.services.kosmos.hybridbuttonemulator import KosmosHybridButtonEmulator
from pyraspi.services.kosmos.hybridkeymatrixemulator import KosmosHybridKeyMatrixEmulator
from pyraspi.services.kosmos.i2c.leddrivericframesparser import GET_I2C_LED_DRIVER_BY_ID
from pyraspi.services.kosmos.keymatrixemulator import KosmosKeyMatrixEmulator
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.kosmosi2cspy import KosmosLedSpyOverI2c
from pyraspi.services.kosmos.kosmosledspy import KosmosLedSpy
from pyraspi.services.kosmos.mockkosmos import MockKosmos
from pyraspi.services.kosmos.motionemulator import KosmosMotionEmulator
from pyraspi.services.kosmos.powerslideremulator import KosmosPowerSliderEmulator
from pyraspi.services.kosmos.proximitysensoremulator import ProximitySensorEmulator
from pyraspi.services.mcp4725 import MCP4725
from pyraspi.services.powersupply import MCP4725PowerSupplyEmulationInterface
from pytestbox.base.configurationmanager import ConfigurationManager
from pytransport.tools.agilent import Agilent
from pyusb.tools.powersupply import AgilentPowerSupplyEmulationInterface


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class EmulatorsManager(EmulatorInterface):
    """
    Manage emulators
    """
    def __init__(self, features):
        """
        :param features: Context features
        :type features: ``context.features``

        :raise ``AssertionError``: If an instance already exists
        """
        if EmulatorInterface.get_instance(features) is not None:
            raise AssertionError('Creating a new instance is not allowed: this class is a singleton. Use get_instance')
        else:
            self.features = features
            self.kosmos = None
            self.power_supply_emulator = None
            self.power_slider_emulator = None
            self.button_stimuli_emulator = None
            self.ambient_light_sensor_emulator = None
            self.proximity_sensor_emulator = None
            self.led_spy = None
            self.led_spy_over_i2c = None
            self.motion_emulator = None
            self.jlink_connection_control = None
            self.game_mode_emulator = None
            EmulatorInterface._EmulatorInterface__instance = self
        # end if
    # end def __init__

    @classmethod
    def get_instance(cls, features):
        """
        Get Emulators Manager instance

        :param features: Context features
        :type features: ``context.features``

        :return: Emulators Manager instance
        :rtype: ``EmulatorsManager``
        """
        if EmulatorInterface.get_instance(features) is None:
            cls(features)
        # end if
        return EmulatorInterface.get_instance(features)
    # end def get_instance

    @classmethod
    def is_jlink_io_switch_present(cls, features):
        """
        Check if the Jlink connection control is present

        :param features: Context features
        :type features: ``context.features``

        :return: Emulators Manager instance
        :rtype: ``EmulatorsManager``
        """
        emulators_manager = EmulatorsManager.get_instance(features=features)
        return not isinstance(emulators_manager.jlink_connection_control, MockJlinkConnectionControl)
    # end def is_jlink_io_switch_present

    def __del__(self):
        """
        Destructor
        """
        if getattr(self, 'kosmos', None) is not None:
            # De-reference Kosmos instance (running SPI threads) to ensure it can be deleted before exiting program
            self.kosmos = None
        # end if
        if getattr(self, 'button_stimuli_emulator', None) is not None:
            self.button_stimuli_emulator = None  # De-reference it to be sure its __del__ method is called
        # end if
        if getattr(self, 'game_mode_emulator', None) is not None:
            self.game_mode_emulator = None  # De-reference it to be sure its __del__ method is called
        # end if
        if getattr(self, 'power_supply_emulator', None) is not None:
            self.power_supply_emulator = None  # De-reference it to be sure its __del__ method is called
        # end if
    # end def __del__

    def init(self, device_type=None):
        """
        Initialize emulators based on external hardware

        :param device_type: Device type - OPTIONAL
        :type device_type: ``pytestbox.base.configurationmanager.ConfigurationManager.DEVICE_TYPE``
        """
        self.init_kosmos()
        self.init_power_supply()
        self.init_power_slider_emulator()
        self.init_button_emulator(device_type)
        self.init_ambient_light_sensor_emulator()
        self.init_proximity_sensor_emulator()
        self.init_led_monitoring_service()
        self.init_led_spy_over_i2c_monitoring_service()
        self.init_motion_emulator()
        self.init_jlink_io_switch()
        self.init_game_mode_emulator()
    # end def init

    def init_kosmos(self):
        """
        Initialize Kosmos emulator instance

        :return: Kosmos object
        :rtype: ``KosmosInterface``
        """
        if self.kosmos is not None:
            # No need to re-init
            return
        # end if

        daemon = Daemon()
        if daemon.is_host_kosmos():
            # Get Kosmos emulator instance singleton
            daemon.log_kosmos_setup_info()
            self.kosmos = Kosmos.get_instance()
            self.kosmos.clear(force=True)
        else:
            daemon.log_standard_setup_info()
            self.kosmos = MockKosmos.get_instance()
        # end if
    # end def init_kosmos

    def init_power_supply(self):
        """
        Initialize power supply emulator
        """
        if self.power_supply_emulator is not None:
            # No need to re-init
            return
        # end if

        # Create power supply emulator class
        if MCP4725.discover():
            self.power_supply_emulator = MCP4725PowerSupplyEmulationInterface.get_instance(
                self.features.PRODUCT.DEVICE.BATTERY.F_NominalVoltage, reset_gpio=False)
        elif Agilent.discover_agilent():
            self.power_supply_emulator = AgilentPowerSupplyEmulationInterface(test_features=self.features)
        # end if
    # end def init_power_supply

    def init_power_slider_emulator(self):
        """
        Initialize power slider emulator
        """
        if self.power_slider_emulator is not None:
            # No need to re-init
            return
        # end if

        # Create power slider emulator class
        if self.kosmos is not None and not self.kosmos.is_fake() and \
                self.features.PRODUCT.F_ProductReference in SLIDER_LAYOUT_BY_ID:
            self.power_slider_emulator = KosmosPowerSliderEmulator(
                kosmos=self.kosmos, fw_id=self.features.PRODUCT.F_ProductReference)
        # end if
    # end def init_power_slider_emulator

    def init_button_emulator(self, device_type=None):
        """
        Initialize button emulator

        :param device_type: Device type - OPTIONAL
        :type device_type: ``pytestbox.base.configurationmanager.ConfigurationManager.DEVICE_TYPE``

        :raise ``AssertionError``: If button stimuli emulator instantiation fails
        """
        if self.button_stimuli_emulator is not None:
            # No need to re-init
            return
        # end if

        if device_type in [ConfigurationManager.DEVICE_TYPE.MOUSE, ConfigurationManager.DEVICE_TYPE.KEYPAD]:
            if self.kosmos.is_fake():
                # Create a Button emulator instance
                self.button_stimuli_emulator = BasicButtonEmulator(verbose=self.features.LOGGING.F_EmulatorVerbose)
            elif self.features.PRODUCT.F_ProductReference in BUTTON_LAYOUT_BY_ID:
                if BUTTON_LAYOUT_BY_ID[self.features.PRODUCT.F_ProductReference].HAS_HYBRID_SWITCH:
                    self.button_stimuli_emulator = KosmosHybridButtonEmulator(
                        kosmos=self.kosmos, fw_id=self.features.PRODUCT.F_ProductReference)
                else:
                    self.button_stimuli_emulator = KosmosButtonEmulator(
                        kosmos=self.kosmos, fw_id=self.features.PRODUCT.F_ProductReference)
                # end if
                # Release all buttons
                self.button_stimuli_emulator.release_all()
            # end if
        elif device_type == ConfigurationManager.DEVICE_TYPE.KEYBOARD and \
                self.features.PRODUCT.F_ProductReference in GET_KEYBOARD_LAYOUT_BY_ID:
            if self.kosmos.is_fake():
                fw_id = self.features.PRODUCT.F_ProductReference \
                    if self.features.PRODUCT.DEVICE.F_KeyboardType != 'optical_switch_array' \
                    else self.features.PRODUCT.F_ProductReference + '_MT8816'
                self.button_stimuli_emulator = KeyboardEmulator(fw_id=fw_id)
                # Release all keys
                self.button_stimuli_emulator.release_all()
            else:
                if GET_KEYBOARD_LAYOUT_BY_ID[self.features.PRODUCT.F_ProductReference][0].IS_HYBRID:
                    self.button_stimuli_emulator = KosmosHybridKeyMatrixEmulator(
                        kosmos=self.kosmos, fw_id=self.features.PRODUCT.F_ProductReference)
                    # Release all keys
                    self.button_stimuli_emulator.release_all()
                elif GET_KEYBOARD_LAYOUT_BY_ID[self.features.PRODUCT.F_ProductReference][0].IS_ANALOG:
                    self.button_stimuli_emulator = KosmosDualKeyMatrixEmulator(
                        kosmos=self.kosmos, fw_id=self.features.PRODUCT.F_ProductReference)
                    # Setup default settings and release all keys
                    self.button_stimuli_emulator.setup_defaults()
                else:
                    self.button_stimuli_emulator = KosmosKeyMatrixEmulator(
                        kosmos=self.kosmos, fw_id=self.features.PRODUCT.F_ProductReference)
                    # Release all keys
                    self.button_stimuli_emulator.release_all()
                # end if
            # end if
        # end if
    # end def init_button_emulator

    def init_ambient_light_sensor_emulator(self):
        """
        Initialize ambient light sensor emulator
        """
        if self.ambient_light_sensor_emulator is not None:
            # No need to re-init
            return
        # end if

        # Create ambient light sensor emulator instance
        if self.kosmos is not None and not self.kosmos.is_fake() and \
                self.features.PRODUCT.F_ProductReference in GET_ALS_CONFIGURATION_BY_ID:
            self.ambient_light_sensor_emulator = \
                AmbientLightSensorEmulator(kosmos=self.kosmos, fw_id=self.features.PRODUCT.F_ProductReference)
        # end if
    # end def init_ambient_light_sensor_emulator

    def init_proximity_sensor_emulator(self):
        """
        Initialize proximity sensor emulator
        """
        if self.proximity_sensor_emulator is not None:
            # No need to re-init
            return
        # end if

        # Create proximity sensor emulator instance
        if self.kosmos is not None and not self.kosmos.is_fake() and \
                self.features.PRODUCT.F_ProductReference in PROXIMITY_SENSOR_LAYOUT_BY_ID:
            self.proximity_sensor_emulator = \
                ProximitySensorEmulator(kosmos=self.kosmos, fw_id=self.features.PRODUCT.F_ProductReference)
        # end if
    # end def init_proximity_sensor_emulator

    def init_led_monitoring_service(self):
        """
        Initialize LED spy module
        """
        if self.led_spy is not None:
            # No need to re-init
            return
        # end if

        # Create a LED spy instance
        if self.kosmos is not None and not self.kosmos.is_fake() and \
                self.features.PRODUCT.F_ProductReference in GET_LED_LAYOUT_BY_ID:
            self.led_spy = KosmosLedSpy(kosmos=self.kosmos,
                                        fw_id=self.features.PRODUCT.F_ProductReference)
        # end if
    # end def init_led_monitoring_service

    def init_led_spy_over_i2c_monitoring_service(self):
        """
        Initialize LED spy over I2C module
        """
        if self.led_spy_over_i2c is not None:
            # No need to re-init
            return
        # end if

        # Create a LED I2C spy instance
        if self.kosmos is not None and not self.kosmos.is_fake() and \
                self.features.PRODUCT.F_ProductReference in GET_I2C_LED_DRIVER_BY_ID:
            self.led_spy_over_i2c = KosmosLedSpyOverI2c(kosmos=self.kosmos,
                                                        fw_id=self.features.PRODUCT.F_ProductReference)
        # end if
    # end def init_led_spy_over_i2c_monitoring_service

    def init_motion_emulator(self):
        """
        Initialize the motion emulator module
        """
        if self.motion_emulator is not None:
            # No need to re-init
            return
        # end if

        # Create a motion emulator instance
        if self.kosmos is not None and not self.kosmos.is_fake() and \
                self.features.PRODUCT.F_ProductReference in SENSOR_ORIENTATION_BY_ID:
            self.motion_emulator = KosmosMotionEmulator(
                kosmos=self.kosmos, fw_id=self.features.PRODUCT.F_ProductReference)
        # end if
    # end def init_motion_emulator

    def init_jlink_io_switch(self):
        """
        Initialize JLink IO Switch module
        """
        if self.jlink_connection_control is not None:
            # No need to re-init
            return
        # end if

        # LibusbDriver is imported locally because of the import ambiguity between this file and LibusbDriver's file
        # This should be fixed with the Device Manager implementation
        from pyusb.libusbdriver import LibusbDriver
        smart_hubs = LibusbDriver.discover_usb_hub()

        if self.kosmos is not None and not self.kosmos.is_fake():
            self.jlink_connection_control = KosmosJlinkConnectionControl(
                verbose=self.features.LOGGING.F_EmulatorVerbose)
        elif (Raspi.PIN.JLINK_IO_SWITCH is not None and
              PowerSupplyBoardJlinkConnectionControl.is_control_pin_connected(Raspi.PIN.JLINK_IO_SWITCH)):
            self.jlink_connection_control = PowerSupplyBoardJlinkConnectionControl(
                control_pin=Raspi.PIN.JLINK_IO_SWITCH, verbose=self.features.LOGGING.F_EmulatorVerbose)
        elif len(smart_hubs) > 0 and hasattr(self.features.PRODUCT, "F_PowerOnFTDI") and \
                self.features.PRODUCT.F_PowerOnFTDI:
            self.jlink_connection_control = FtdiPoweredDeviceJlinkConnectionControl(
                smart_hub=smart_hubs[0], ftdi_hub_port=LibusbDriver.FTDI_CABLE_PORT_NUMBER,
                verbose=self.features.LOGGING.F_EmulatorVerbose)
        else:
            self.jlink_connection_control = MockJlinkConnectionControl(verbose=self.features.LOGGING.F_EmulatorVerbose)
        # end if
    # end def init_jlink_io_switch

    def get_connected_key_ids(self):
        """
        Get connected key IDs

        :return: Connected key IDs
        :rtype: ``list``
        """
        if self.button_stimuli_emulator is None:
            connected_key_ids = []
        else:
            if self.button_stimuli_emulator.connected_key_ids is None:
                if self.power_supply_emulator is not None:
                    # Turn on the device battery with the last known voltage value
                    self.power_supply_emulator.restart_device()
                # end if
                if self.power_slider_emulator is not None:
                    # Turn the power slider on
                    self.power_slider_emulator.power_on()
                # end if
                self.button_stimuli_emulator.setup_connected_key_ids()
                if self.power_slider_emulator is not None:
                    # Turn the power slider off
                    self.power_slider_emulator.power_off()
                # end if
                # Turn off DUT
                if self.power_supply_emulator is not None:
                    self.power_supply_emulator.turn_off()
                # end if
            # end if
            connected_key_ids = self.button_stimuli_emulator.connected_key_ids
        # end if
        return connected_key_ids
    # end def get_connected_key_ids

    def init_game_mode_emulator(self):
        """
        Initialize game mode emulator
        """
        if self.game_mode_emulator is not None:
            # No need to re-init
            return
        # end if

        # Create game mode slider emulator class
        if self.features.PRODUCT.DEVICE.F_GameModeButtonType == 'game_mode_button'\
                and self.button_stimuli_emulator is not None:
            self.game_mode_emulator = GameModeButtonEmulator(self.button_stimuli_emulator)
        elif self.features.PRODUCT.DEVICE.F_GameModeButtonType == 'game_mode_slider':
            if self.kosmos is None or self.kosmos.is_fake():
                self.game_mode_emulator = GameModeSliderEmulator()
            # end if
        # end if

    # end def init_game_mode_emulator
# end class EmulatorsManager

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
