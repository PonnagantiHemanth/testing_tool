#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.podsconfiguration
:brief: PODS configuration per Kosmos ID
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/11/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Union

from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.ambientlightsensoremulator import AmbientLightSensorEmulator
from pyraspi.services.kosmos.config.alsconfiguration import IngaAlsConfiguration
from pyraspi.services.kosmos.config.alsconfiguration import NormanAlsConfiguration
from pyraspi.services.kosmos.config.opticalsensorconfig import CanovaSquareLayout
from pyraspi.services.kosmos.config.opticalsensorconfig import Hero2Layout
from pyraspi.services.kosmos.config.opticalsensorconfig import HeroLayout
from pyraspi.services.kosmos.config.opticalsensorconfig import NormalMouseLayout
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_A
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_B
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_C
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_D
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_E
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_F
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_G
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_H
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_0
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_1
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_2

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
# Input voltage threshold : voltage threshold is selected by measuring the maximum voltage (Vmax) and the minimum
# voltage (Vmin) of the signal and set Vthreshold = (Vmax - Vmin) / 2
NORMAN_LED_SPY_INPUT_VOLTAGE_THRESHOLD = 1.05
# Special case for Topaz: Normally threshold = (Vmax - Vmin) / 2 = 1.45 but the threshold has been increased because the
# transitions between high and low level are better detected with a greater value (voltage chose empirically)
TOPAZ_I2C_SPY_INPUT_VOLTAGE_THRESHOLD = 1.8
CINDERELLA_WIRELESS_I2C_SPY_INPUT_VOLTAGE_THRESHOLD = 1.8
INGA_I2C_SPY_INPUT_VOLTAGE_THRESHOLD = 1.45
INGA_LED_SPY_INPUT_VOLTAGE_THRESHOLD = 3.2 / 2  # Half of VCC
SLIMPLUS_LED_SPY_INPUT_VOLTAGE_THRESHOLD = 1.05
BEAGLE_USB_480_ANALYSER_DIGITAL_OUTPUT_THRESHOLD = 3.3 / 2  # Half of Beagle digital output voltage

MAXIMUM_DAC_VOLTAGE = 3.3

ENABLE_DEBUG_PIO = False  # Set to True if the FPGA bitstream is configured with debug PIO


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@dataclass
class ChannelConfiguration:
    """
    Dataclass representing the configuration of a DAC Channel

    Dataclass constructor arguments:
    ``voltage``: Voltage value of the channel (``float``)
    ``associated_device``: Type of emulator associated to the channel (``DeviceName | DeviceFamilyName | None``)
    ``reset_at_power_off``: Flag indicating if the voltage is set to zero when device is powered off (``bool``)
    """
    voltage: float = 0.0
    associated_device: Union[DeviceName, DeviceFamilyName, None] = None
    reset_at_power_off: bool = False

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        assert 0 <= self.voltage <= MAXIMUM_DAC_VOLTAGE, f'DAC channel voltage is out-of-range: {self.voltage} Volt.'
        assert self.associated_device is None or isinstance(self.associated_device, (DeviceName, DeviceFamilyName)), (
            'Unknown associated device')
        assert isinstance(self.reset_at_power_off, bool), type(self.reset_at_power_off)
    # end def __post_init__
# end class ChannelConfiguration


@dataclass
class DacConfiguration:
    """
    Dataclass representing the configuration of a DAC
    """
    channel_a: ChannelConfiguration = field(default_factory=lambda: ChannelConfiguration())
    channel_b: ChannelConfiguration = field(default_factory=lambda: ChannelConfiguration())
    channel_c: ChannelConfiguration = field(default_factory=lambda: ChannelConfiguration())
    channel_d: ChannelConfiguration = field(default_factory=lambda: ChannelConfiguration())
    channel_e: ChannelConfiguration = field(default_factory=lambda: ChannelConfiguration())
    channel_f: ChannelConfiguration = field(default_factory=lambda: ChannelConfiguration())
    channel_g: ChannelConfiguration = field(default_factory=lambda: ChannelConfiguration())
    channel_h: ChannelConfiguration = field(default_factory=lambda: ChannelConfiguration())
    _dac_id: Union[int, None] = None

    def __post_init__(self):
        """
        Dataclass initialization sanity checks and channels ids lookup map initialization

        :raise ``AssertionError``: Invalid DAC Channel instance type
        """
        assert isinstance(self.channel_a, ChannelConfiguration), type(self.channel_a)
        assert isinstance(self.channel_b, ChannelConfiguration), type(self.channel_b)
        assert isinstance(self.channel_c, ChannelConfiguration), type(self.channel_c)
        assert isinstance(self.channel_d, ChannelConfiguration), type(self.channel_d)
        assert isinstance(self.channel_e, ChannelConfiguration), type(self.channel_e)
        assert isinstance(self.channel_f, ChannelConfiguration), type(self.channel_f)
        assert isinstance(self.channel_g, ChannelConfiguration), type(self.channel_g)
        assert isinstance(self.channel_h, ChannelConfiguration), type(self.channel_h)
    # end def __post_init__

    @property
    def channels(self):
        """
        Return the DAC Channel mapping <DAC Channel number, ChannelConfiguration instance>

        :return: DAC Channel mapping <DAC Channel number, ChannelConfiguration instance>
        :rtype: ``dict[int, ChannelConfiguration]``
        """
        return {
            ADDA_DAC_CH_A: self.channel_a,
            ADDA_DAC_CH_B: self.channel_b,
            ADDA_DAC_CH_C: self.channel_c,
            ADDA_DAC_CH_D: self.channel_d,
            ADDA_DAC_CH_E: self.channel_e,
            ADDA_DAC_CH_F: self.channel_f,
            ADDA_DAC_CH_G: self.channel_g,
            ADDA_DAC_CH_H: self.channel_h
        }
    # end def channels

    @property
    def dac_id(self):
        """
        Get the DAC ID

        :return: DAC ID
        :rtype: ``int``
        """
        return self._dac_id
    # end def property getter dac_id

    @dac_id.setter
    def dac_id(self, dac_id):
        """
        Set the id to the DAC

        :param dac_id: DAC ID
        :type dac_id: ``int``
        """
        self._dac_id = dac_id
    # end def property setter dac_id

    def apply_config(self, device_tree):
        """
        Apply voltages DACs configuration

        :param device_tree: Kosmos Module Device Tree
        :type device_tree: ``DeviceTree``
        """
        voltages = [channel.voltage for channel in self.channels.values()]
        channels = sum(channel for channel in self.channels.keys())
        device_tree.adda.write_dac(volts=voltages,
                                   dac_sel=self.dac_id,
                                   channels=channels)
    # end def apply_config
# end class DacConfiguration


@dataclass
class PodsConfiguration(metaclass=ABCMeta):
    """
    Default and Common implementation class for PODS configuration.
    """
    dac_0: DacConfiguration = field(default_factory=lambda: DacConfiguration())
    dac_1: DacConfiguration = field(default_factory=lambda: DacConfiguration())
    dac_2: DacConfiguration = field(default_factory=lambda: DacConfiguration())

    def __post_init__(self):
        """
        Dataclass initialization sanity checks and DACs ids lookup map initialization

        :raise ``AssertionError``: Invalid DAC instance type
        """
        self.setup()

        assert isinstance(self.dac_0, DacConfiguration), type(self.dac_0)
        assert isinstance(self.dac_1, DacConfiguration), type(self.dac_1)
        assert isinstance(self.dac_2, DacConfiguration), type(self.dac_2)

        self.set_dac_ids()
    # end def __post_init__

    @abstractmethod
    def setup(self):
        """
        Configure PODS DACs of a device
        """
        raise NotImplementedAbstractMethodError()
    # end def setup

    @property
    def dacs(self):
        """
        Return the DAC mapping <DAC number, DacConfiguration instance>

        :return: DAC mapping <DAC number, DacConfiguration instance>
        :rtype: ``dict[int, DacConfiguration]``
        """
        return {ADDA_SEL_DAC_0: self.dac_0,
                ADDA_SEL_DAC_1: self.dac_1,
                ADDA_SEL_DAC_2: self.dac_2}
    # end def property getter dacs

    def set_dac_ids(self):
        """
        Set selection id for each DAC
        """
        for dac_id, dac in self.dacs.items():
            dac.dac_id = dac_id
        # end for
    # end def set_dac_ids

    def init_pods(self, device_tree):
        """
        Initialize PODS DACs channels and voltages

        :param device_tree: Kosmos Module Device Tree
        :type device_tree: ``DeviceTree``
        """
        for dac in self.dacs.values():
            dac.apply_config(device_tree=device_tree)
        # end for
    # end def init_pods
# end class PodsConfiguration


class BaseFpgaPodsConfiguration(PodsConfiguration):
    """
    PodsConfiguration class with no hardware attached.
    This class is meant to be used with the 'base' FPGA config.
    """
    def setup(self):
        """
        Configure PODS: nothing to do
        """
        pass
    # end def setup
# end class BaseFpgaPodsConfiguration


class NormanPodsConfiguration(PodsConfiguration):
    """
    Configure PODS DACs of Norman keyboard according to :
    https://docs.google.com/document/d/1tNtyeDco_j5j2R-DYRUqWiqcbflzQfRUofXLr7JjFDo
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        # Kosmos PIO output voltage levels configuration of ALS emulator
        self.dac_1 = DacConfiguration(
            channel_a=ChannelConfiguration(
                voltage=AmbientLightSensorEmulator.get_voltage_from_lux_and_config(
                    illuminance=NormanAlsConfiguration.LUMINANCE_DEFAULT_VALUE,
                    als_configuration=NormanAlsConfiguration()),
                associated_device=DeviceFamilyName.AMBIENT_LIGHT_SENSOR,
                reset_at_power_off=True))
        # Kosmos LED-spy input voltage thresholds configuration of LED spy emulator
        self.dac_2 = DacConfiguration(channel_a=ChannelConfiguration(voltage=NORMAN_LED_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.LED_SPY),
                                      channel_b=ChannelConfiguration(voltage=NORMAN_LED_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.LED_SPY),
                                      channel_c=ChannelConfiguration(voltage=NORMAN_LED_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.LED_SPY))
    # end def setup
# end class NormanPodsConfiguration


class TopazPodsConfiguration(PodsConfiguration):
    """
    Configure PODS DACs of Topaz keyboard according to :
    https://docs.google.com/document/d/1GfBsXLtHGT8U-VIFOBM2CwRF5ooMxy4Id_3afBCzrBQ
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        # Kosmos PIO input voltage thresholds of I2C-spy
        self.dac_0 = DacConfiguration(channel_a=ChannelConfiguration(voltage=TOPAZ_I2C_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.I2C_SPY),
                                      channel_b=ChannelConfiguration(voltage=TOPAZ_I2C_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.I2C_SPY))
    # end def setup
# end class TopazPodsConfiguration


class CinderellaWirelessPodsConfiguration(PodsConfiguration):
    """
    Configure PODS DACs of Cinderella Wireless keyboard according to :
    https://docs.google.com/document/d/12k6ulAIjZQaFsxFKzY74pCFboheE6mRsNHnyoB0HbWI/edit
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        # Kosmos PIO input voltage thresholds of I2C-spy
        self.dac_0 = DacConfiguration(channel_a=ChannelConfiguration(
            voltage=CINDERELLA_WIRELESS_I2C_SPY_INPUT_VOLTAGE_THRESHOLD,
            associated_device=DeviceName.I2C_SPY))
    # end def setup
# end class CinderellaWirelessPodsConfiguration


class IngaPodsConfiguration(PodsConfiguration):
    """
    Configure PODS DACs of Inga keyboard.
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        # Kosmos PIO input voltage thresholds of I2C-spy
        self.dac_0 = DacConfiguration(channel_a=ChannelConfiguration(voltage=INGA_I2C_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.I2C_SPY))
        # Kosmos PIO output voltage levels configuration of ALS emulator
        self.dac_1 = DacConfiguration(
            channel_a=ChannelConfiguration(
                voltage=AmbientLightSensorEmulator.get_voltage_from_lux_and_config(
                    illuminance=IngaAlsConfiguration.LUMINANCE_DEFAULT_VALUE,
                    als_configuration=IngaAlsConfiguration()),
                associated_device=DeviceFamilyName.AMBIENT_LIGHT_SENSOR))
        # Kosmos LED_SPY input voltage threshold
        self.dac_2 = DacConfiguration(channel_a=ChannelConfiguration(voltage=INGA_LED_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.LED_SPY))
    # end def setup
# end class IngaPodsConfiguration


class SlimplusPodsConfiguration(PodsConfiguration):
    """
    Configure PODS DACs of Slimplus keyboard according to :
    https://docs.google.com/document/d/1eFq0ES1e-RENb9qHGnurHWIAuOFX0AdTGhfTDJ2E_7A
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        # Kosmos LED-spy input voltage thresholds configuration of LED spy emulator
        self.dac_2 = DacConfiguration(channel_a=ChannelConfiguration(voltage=SLIMPLUS_LED_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.LED_SPY),
                                      channel_b=ChannelConfiguration(voltage=SLIMPLUS_LED_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.LED_SPY))
    # end def setup
# end class SlimplusPodsConfiguration


class CortadoPodsConfiguration(PodsConfiguration):
    """
    Configure PODS DACs of Cortado keyboard according to :
    https://docs.google.com/document/d/1NtMmYW_gx_5MQYagqZDfe0hxweWAgFsBkcBeTEvRobI
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        # Kosmos LED-spy input voltage thresholds configuration of LED spy emulator
        self.dac_2 = DacConfiguration(channel_a=ChannelConfiguration(voltage=SLIMPLUS_LED_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.LED_SPY),
                                      channel_b=ChannelConfiguration(voltage=SLIMPLUS_LED_SPY_INPUT_VOLTAGE_THRESHOLD,
                                                                     associated_device=DeviceName.LED_SPY))
    # end def setup
# end class CortadoPodsConfiguration


class SanakPodsConfiguration(PodsConfiguration):
    """
    Configure PODS DACs of normal mouse.
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        # Kosmos PIO input voltage thresholds configuration of optical sensor emulator
        self.dac_0 = DacConfiguration(channel_a=ChannelConfiguration(voltage=NormalMouseLayout.DUT_VCC_SENSOR_VOLTAGE/2,
                                                                     associated_device=DeviceName.SPI_E7792),
                                      channel_b=ChannelConfiguration(voltage=NormalMouseLayout.DUT_VCC_SENSOR_VOLTAGE/2,
                                                                     associated_device=DeviceName.SPI_E7792))
        # Kosmos PIO output voltage levels configuration of optical sensor emulator
        self.dac_1 = DacConfiguration(channel_a=ChannelConfiguration(voltage=NormalMouseLayout.DUT_VCC_SENSOR_VOLTAGE,
                                                                     associated_device=DeviceName.SPI_E7792),
                                      channel_b=ChannelConfiguration(voltage=NormalMouseLayout.DUT_VCC_SENSOR_VOLTAGE,
                                                                     associated_device=DeviceName.SPI_E7792))
    # end def setup
# end class SanakPodsConfiguration


class BazookaPodsConfiguration(PodsConfiguration):
    """
    Configure PODS DACs of Bazooka mouse according to :
    https://docs.google.com/document/d/1rPzeDEjGH5toFf6DhRO_Mk-s1xDd3Mn5PP6H9BvdqII
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        # Kosmos PIO input voltage thresholds configuration of optical sensor emulator
        self.dac_0 = DacConfiguration(channel_a=ChannelConfiguration(voltage=HeroLayout.DUT_VCC_SENSOR_VOLTAGE / 2,
                                                                     associated_device=DeviceName.SPI_E7788),
                                      channel_b=ChannelConfiguration(voltage=HeroLayout.DUT_VCC_SENSOR_VOLTAGE / 2,
                                                                     associated_device=DeviceName.SPI_E7788))
        # Kosmos PIO output voltage levels configuration of optical sensor emulator
        self.dac_1 = DacConfiguration(channel_a=ChannelConfiguration(voltage=HeroLayout.DUT_VCC_SENSOR_VOLTAGE,
                                                                     associated_device=DeviceName.SPI_E7788),
                                      channel_b=ChannelConfiguration(voltage=HeroLayout.DUT_VCC_SENSOR_VOLTAGE,
                                                                     associated_device=DeviceName.SPI_E7788))
    # end def setup
# end class BazookaPodsConfiguration


class Bazooka2PodsConfiguration(PodsConfiguration):
    """
    Configure PODS DACs of Bazooka2 mouse according to :
    https://docs.google.com/document/d/1Cim9xQLUo9_sRZM2XoQ5acE41vwSAcA7tBmPhPrX4xU
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        voltage = Hero2Layout.DUT_VCC_SENSOR_VOLTAGE
        fname = DeviceName.SPI_E7790
        # Kosmos PIO input voltage thresholds configuration of optical sensor emulator
        if ENABLE_DEBUG_PIO:  # configure inputs threshold, so the comparator does not oscillate around zero volt
            self.dac_0 = DacConfiguration(channel_a=ChannelConfiguration(voltage=voltage/2, associated_device=fname),
                                          channel_b=ChannelConfiguration(voltage=voltage/2, associated_device=fname),
                                          channel_d=ChannelConfiguration(voltage=voltage/2, associated_device=fname),
                                          channel_e=ChannelConfiguration(voltage=voltage/2, associated_device=fname),
                                          channel_f=ChannelConfiguration(voltage=voltage/2, associated_device=fname),
                                          channel_g=ChannelConfiguration(voltage=voltage/2, associated_device=fname),
                                          channel_h=ChannelConfiguration(voltage=voltage/2, associated_device=fname))
        else:
            self.dac_0 = DacConfiguration(channel_a=ChannelConfiguration(voltage=voltage/2, associated_device=fname),
                                          channel_b=ChannelConfiguration(voltage=voltage/2, associated_device=fname))
        # end if
        # Kosmos PIO output voltage levels configuration of optical sensor emulator
        if ENABLE_DEBUG_PIO:
            self.dac_1 = DacConfiguration(channel_a=ChannelConfiguration(voltage=voltage, associated_device=fname),
                                          channel_b=ChannelConfiguration(voltage=voltage, associated_device=fname),
                                          channel_d=ChannelConfiguration(voltage=voltage, associated_device=fname),
                                          channel_e=ChannelConfiguration(voltage=voltage, associated_device=fname),
                                          channel_f=ChannelConfiguration(voltage=voltage, associated_device=fname),
                                          channel_g=ChannelConfiguration(voltage=voltage, associated_device=fname),
                                          channel_h=ChannelConfiguration(voltage=voltage, associated_device=fname))
        else:
            self.dac_1 = DacConfiguration(channel_a=ChannelConfiguration(voltage=voltage, associated_device=fname),
                                          channel_b=ChannelConfiguration(voltage=voltage, associated_device=fname))
        # end if
        # Kosmos LED-spy input voltage thresholds configuration of LED spy emulator
        self.dac_2 = DacConfiguration(
            channel_h=ChannelConfiguration(voltage=BEAGLE_USB_480_ANALYSER_DIGITAL_OUTPUT_THRESHOLD,
                                           associated_device=DeviceName.LED_SPY))
    # end def setup
# end class Bazooka2PodsConfiguration


class Footloose2PodsConfiguration(Bazooka2PodsConfiguration):
    """
    Configure PODS DACs of Footloose2 mouse according to :
    https://docs.google.com/document/d/1T0hMfR9j05gqOmdCLwgIsiPznQXCC-dhAAp5IbZr5sI/view
    """
# end class Footloose2PodsConfiguration

class TurbotBleProPodsConfiguration(PodsConfiguration):
    """
    PodsConfiguration class for the Turbot_ble_pro device with a PAW3266 optical sensor.
    This class is meant to be used with the 'turbot_ble_pro' FPGA config.
    """
    def setup(self):
        """
        Configure PODS: nothing to do
        """
        SPI_BUS_VOLTAGE = 2.2  # Volts
        INPUT_THRESHOLD = SPI_BUS_VOLTAGE / 2  # Volts

        ENABLE_DEBUG_PIO = False  # Set to True if the FPGA bitstream is configured with debug PIO

        # Kosmos PIO input voltage thresholds configuration of KBD GTECH Emulator
        self.dac_0 = DacConfiguration(
            # PIO[0]: INPUT: SCLK
            # PIO[1]: INPUT: NCS
            channel_a=ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.SPI_PAW3266),
            # PIO[2]: INPUT/OUTPUT: SDIO
            # PIO[3]: OUTPUT: MOTION
            channel_b=ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.SPI_PAW3266),
        )

        if ENABLE_DEBUG_PIO:  # configure inputs threshold, so the comparator does not oscillate around zero volt
            # PIO[4] to PIO[15]: OUTPUT: DEBUG
            self.dac_0.channel_c = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.SPI_PAW3266)
            self.dac_0.channel_d = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.SPI_PAW3266)
            self.dac_0.channel_e = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.SPI_PAW3266)
            self.dac_0.channel_f = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.SPI_PAW3266)
            self.dac_0.channel_g = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.SPI_PAW3266)
            self.dac_0.channel_h = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.SPI_PAW3266)
        # end if

        # Kosmos PIO output voltage levels configuration of KBD GTECH Emulator
        self.dac_1 = DacConfiguration(
            # PIO[0]: INPUT: SCLK
            # PIO[1]: INPUT: NCS
            channel_a=ChannelConfiguration(voltage=0, associated_device=DeviceName.SPI_PAW3266),
            # PIO[2]: INPUT/OUTPUT: SDIO
            # PIO[3]: OUTPUT: MOTION
            channel_b=ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.SPI_PAW3266),
        )
        if ENABLE_DEBUG_PIO:
            # PIO[4] to PIO[15]: OUTPUT: DEBUG
            self.dac_1.channel_c = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.SPI_PAW3266)
            self.dac_1.channel_d = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.SPI_PAW3266)
            self.dac_1.channel_e = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.SPI_PAW3266)
            self.dac_1.channel_f = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.SPI_PAW3266)
            self.dac_1.channel_g = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.SPI_PAW3266)
            self.dac_1.channel_h = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.SPI_PAW3266)
        # end if
    # end def setup
# end class TurbotBleProPodsConfiguration


class GalvatronPodsConfiguration(PodsConfiguration):
    """
    PodsConfiguration class for the Galvatron Analog Keyboard.
    This class is meant to be used with the 'galvatron' FPGA config.
    """
    def setup(self):
        """
        Configure PODS: nothing to do
        """
        SPI_BUS_VOLTAGE = 3.3  # Volts
        INPUT_THRESHOLD = SPI_BUS_VOLTAGE / 2  # Volts

        ENABLE_DEBUG_PIO = False  # Set to True if the FPGA bitstream is configured with debug PIO

        # Kosmos PIO input voltage thresholds configuration of KBD GTECH Emulator
        self.dac_0 = DacConfiguration(
            # PIO[0]: INPUT: SCLK
            # PIO[1]: INPUT: NCS
            channel_a=ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.KBD_GTECH),
            # PIO[2]: INPUT: MOSI
            # PIO[3]: INPUT: MISO_IN: from GTECH MCU
            channel_b=ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.KBD_GTECH),
            # PIO[4]: OUTPUT: MISO_OUT: to LOGI MCU
            # PIO[5]: INPUT: INT
            channel_c=ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.KBD_GTECH),
        )
        if ENABLE_DEBUG_PIO:  # configure inputs threshold, so the comparator does not oscillate around zero volt
            # PIO[6] to PIO[15]: OUTPUT: DEBUG
            self.dac_0.channel_d = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.KBD_GTECH)
            self.dac_0.channel_e = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.KBD_GTECH)
            self.dac_0.channel_f = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.KBD_GTECH)
            self.dac_0.channel_g = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.KBD_GTECH)
            self.dac_0.channel_h = ChannelConfiguration(voltage=INPUT_THRESHOLD, associated_device=DeviceName.KBD_GTECH)
        # end if

        # Kosmos PIO output voltage levels configuration of KBD GTECH Emulator
        self.dac_1 = DacConfiguration(
            # PIO[0]: INPUT: SCLK
            # PIO[1]: INPUT: NCS
            channel_a=ChannelConfiguration(voltage=0., associated_device=DeviceName.KBD_GTECH),
            # PIO[2]: INPUT: MOSI
            # PIO[3]: INPUT: MISO_IN: from GTECH MCU
            channel_b=ChannelConfiguration(voltage=0., associated_device=DeviceName.KBD_GTECH),
            # PIO[4]: OUTPUT: MISO_OUT: to LOGI MCU
            # PIO[5]: INPUT: INT
            channel_c=ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.KBD_GTECH)
        )
        if ENABLE_DEBUG_PIO:
            # PIO[6] to PIO[15]: OUTPUT: DEBUG
            self.dac_1.channel_d = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.KBD_GTECH)
            self.dac_1.channel_e = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.KBD_GTECH)
            self.dac_1.channel_f = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.KBD_GTECH)
            self.dac_1.channel_g = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.KBD_GTECH)
            self.dac_1.channel_h = ChannelConfiguration(voltage=SPI_BUS_VOLTAGE, associated_device=DeviceName.KBD_GTECH)
        # end if
    # end def setup
# end class GalvatronPodsConfiguration


class CanovaPodsConfiguration(PodsConfiguration):
    """
    PodsConfiguration class for the Canova square board.
    This class is meant to be used with the 'liza' FPGA config.
    """
    def setup(self):
        """
        Configure PODS DACs used by DUT
        """
        # Kosmos PIO input voltage thresholds of I2C-spy
        # Kosmos PIO input voltage thresholds configuration of optical sensor emulator
        self.dac_0 = DacConfiguration(
            # PIO[0]: INPUT: SCL & PIO[1]: INPUT: SDA
            channel_a=ChannelConfiguration(
                voltage=INGA_I2C_SPY_INPUT_VOLTAGE_THRESHOLD, associated_device=DeviceName.I2C_SPY),
            # PIO[2]: INPUT: SCLK & PIO[3]: INPUT: NCS
            channel_b=ChannelConfiguration(
                voltage=CanovaSquareLayout.DUT_VCC_SENSOR_VOLTAGE/2, associated_device=DeviceName.SPI_PMW3816),
            # PIO[4]: INPUT: MOSI & PIO[5]: OUTPUT: MISO
            channel_c=ChannelConfiguration(
                voltage=CanovaSquareLayout.DUT_VCC_SENSOR_VOLTAGE/2, associated_device=DeviceName.SPI_PMW3816),
            # PIO[6]: OUTPUT: MOTION
            channel_d=ChannelConfiguration(
                voltage=CanovaSquareLayout.DUT_VCC_SENSOR_VOLTAGE/2, associated_device=DeviceName.SPI_PMW3816))
        # Kosmos PIO output voltage levels configuration of optical sensor emulator
        self.dac_1 = DacConfiguration(
            # PIO[0]: INPUT: SCL & PIO[1]: INPUT: SDA
            channel_a=ChannelConfiguration(voltage=0, associated_device=DeviceName.I2C_SPY),
            # PIO[2]: INPUT: SCLK & PIO[3]: INPUT: NCS
            channel_b=ChannelConfiguration(voltage=0, associated_device=DeviceName.SPI_PMW3816),
            # PIO[4]: INPUT: MOSI & PIO[5]: OUTPUT: MISO
            channel_c=ChannelConfiguration(
                voltage=CanovaSquareLayout.DUT_VCC_SENSOR_VOLTAGE, associated_device=DeviceName.SPI_PMW3816),
            # PIO[6]: OUTPUT: MOTION
            channel_d=ChannelConfiguration(
                voltage=CanovaSquareLayout.DUT_VCC_SENSOR_VOLTAGE, associated_device=DeviceName.SPI_PMW3816)
        )
    # end def setup
# end class CanovaPodsConfiguration

GET_PODS_CONFIGURATION_BY_KOSMOS_ID = {
    2: CinderellaWirelessPodsConfiguration(),
    4: TopazPodsConfiguration(),
    5: IngaPodsConfiguration(),  # Pollux
    6: IngaPodsConfiguration(),  # Pollux
    8: CortadoPodsConfiguration(),  # Cortado
    7: GalvatronPodsConfiguration(),
    10: GalvatronPodsConfiguration(),
    18: Bazooka2PodsConfiguration(),  # BAZ2 8kHz
    19: Bazooka2PodsConfiguration(),  # Tiger Board
    20: SlimplusPodsConfiguration(),
    22: SlimplusPodsConfiguration(),
    25: CortadoPodsConfiguration(),  # Cortado for Apple
    26: IngaPodsConfiguration(),  # Pollux
    27: IngaPodsConfiguration(),  # Boston
    28: Bazooka2PodsConfiguration(),
    29: SanakPodsConfiguration(),  # Hadron Platform
    35: Bazooka2PodsConfiguration(),
    38: SanakPodsConfiguration(),  # Graviton Platform
    39: Bazooka2PodsConfiguration(),  # Tiger Board
    40: SlimplusPodsConfiguration(),  # Chengdu (Kavalon Platform)
    41: TurbotBleProPodsConfiguration(),   # Avalon2 Platform
    42: IngaPodsConfiguration(),  # Fujian98
    43: Footloose2PodsConfiguration(),
    47: CanovaPodsConfiguration(),  # Canova
    48: NormanPodsConfiguration(),
}


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
