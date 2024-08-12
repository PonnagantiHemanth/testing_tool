#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.i2c.leddrivericframesparser
:brief: LED driver IC I2C frames parser Class
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/08/03
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from enum import IntEnum
from enum import auto
from enum import unique

from numpy import full
from numpy import nan
from numpy import uint16
from numpy import uint8

from pyraspi.services.kosmos.i2c.rgbalgorithms.rgbalgoc import RgbComponents
from pyraspi.services.kosmos.i2cspyparser import I2cSpyFrameRun


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@dataclass
class LedAddress:
    """
    Register addresses of I2C Led Driver
    """
    # LED driver IC number
    led_address_ic: uint8 = 0
    # LED address page number in driver IC
    led_address_page: uint8 = 0
    # BLUE Led address
    blue_led_address: uint8 = 0
    # GREEN Led address
    green_led_address: uint8 = 0
    # RED Led address
    red_led_address: uint8 = 0
# end class LedAddress


class IssiLedDriverI2cFrame:
    """
    Define the i2c message format compatible with the following Led Driver ICs from Lumissil microsystems:
    - IS31FL3742A:  cf https://www.mouser.ch/datasheet/2/198/IS31FL3742A_DS-1839511.pdf
    - IS31FL3741A: cf https://www.lumissil.com/assets/pdf/core/IS31FL3741A_DS.pdf
    -IS31FL3746A: cf https://lumissil.com/assets/pdf/core/IS31FL3746A_DS.pdf
    """
    UNLOCK_MESSAGE = [0xFE, 0xC5]
    PAGE0_REGISTER_MESSAGE = [0xFD, 0x00]
    PAGE1_REGISTER_MESSAGE = [0xFD, 0x01]
    PAGE2_REGISTER_MESSAGE = [0xFD, 0x02]
    PAGE3_REGISTER_MESSAGE = [0xFD, 0x03]
    PAGE4_REGISTER_MESSAGE = [0xFD, 0x04]

    @unique
    class I2cLedDriverFrameType(IntEnum):
        """
        I2C Led Driver Frame types
        """
        UNDETERMINED = auto()
        UNLOCK = auto()
        ACCESS_PAGE0_REGISTER = auto()
        ACCESS_PAGE1_REGISTER = auto()
        ACCESS_PAGE2_REGISTER = auto()
        ACCESS_PAGE3_REGISTER = auto()
        ACCESS_PAGE4_REGISTER = auto()
        SET_PWM_PAGE0_VALUE = auto()
        SET_PWM_PAGE1_VALUE = auto()
        SET_PWM_PAGE2_VALUE = auto()
        SET_PWM_PAGE3_VALUE = auto()
        SET_PWM_PAGE4_VALUE = auto()
    # end class I2cLedDriverFrameType

    def __init__(self, slave_address, page0_led_number, page1_led_number=0, page2_led_number=0, page3_led_number=0,
                 page4_led_number=0):
        """
        :param slave_address: address of the IC LED driver
        :type slave_address: ``int``
        :param page0_led_number: number of LED on the page0 of the IC LED driver
        :type page0_led_number: ``int``
        :param page1_led_number: number of LED on the page1 of the IC LED driver - OPTIONAL
        :type page1_led_number: ``int``
        :param page2_led_number: number of LED on the page2 of the IC LED driver - OPTIONAL
        :type page2_led_number: ``int``
        :param page3_led_number: number of LED on the page3 of the IC LED driver - OPTIONAL
        :type page3_led_number: ``int``
        :param page4_led_number: number of LED on the page4 of the IC LED driver - OPTIONAL
        :type page4_led_number: ``int``
        """
        self.slave_address = slave_address
        self.page0_led_number = page0_led_number
        self.page1_led_number = page1_led_number
        self.page2_led_number = page2_led_number
        self.page3_led_number = page3_led_number
        self.page4_led_number = page4_led_number
        self.state = self.I2cLedDriverFrameType.UNDETERMINED
    # end def __init__

    def is_unlock_message(self, frame):
        """
        Check if i2c frame is an unlock message

        :param frame: I2C frame
        :type frame: ``I2cSpyFrame``

        :return: Flag indicating if the frame matches the unlock command
        :rtype: ``bool``
        """
        return True if frame[0] == self.slave_address and list(frame[1::]) == self.UNLOCK_MESSAGE else False
    # end def is_unlock_message

    def is_access_page_register_message(self, frame, page_num):
        """
        Check if i2c frame is an access page register message

        :param frame: I2C frame
        :type frame: ``frame``
        :param page_num: the page number to access
        :type page_num: ``int``

        :return: Flag indicating if the frame matches the access page command
        :rtype: ``bool``
        """
        status = False
        address = frame[0]
        data = list(frame[1::])
        access_page_message = self.PAGE0_REGISTER_MESSAGE
        if page_num == 1:
            access_page_message = self.PAGE1_REGISTER_MESSAGE
        elif page_num == 2:
            access_page_message = self.PAGE2_REGISTER_MESSAGE
        elif page_num == 3:
            access_page_message = self.PAGE3_REGISTER_MESSAGE
        elif page_num == 4:
            access_page_message = self.PAGE4_REGISTER_MESSAGE
        # end if

        if self.state == self.I2cLedDriverFrameType.UNLOCK and address == self.slave_address and \
                data == access_page_message:
            status = True
        # end if
        return status
    # end def is_access_page_register_message

    def is_set_pwm_value_message(self, frame, page_num):
        """
        Check if i2c frame is a set pwm value message

        :param frame: I2C frame
        :type frame: ``I2cSpyFrame``
        :param page_num: the page number to set pwm value
        :type page_num: ``int``

        :return: status
        :rtype: ``bool``
        """
        status = False
        address = frame[0]
        data = list(frame[2::])
        frame_type = self.I2cLedDriverFrameType.ACCESS_PAGE0_REGISTER
        data_len = self.page0_led_number
        if page_num == 1:
            frame_type = self.I2cLedDriverFrameType.ACCESS_PAGE1_REGISTER
            data_len = self.page1_led_number
        elif page_num == 2:
            frame_type = self.I2cLedDriverFrameType.ACCESS_PAGE2_REGISTER
            data_len = self.page2_led_number
        elif page_num == 3:
            frame_type = self.I2cLedDriverFrameType.ACCESS_PAGE3_REGISTER
            data_len = self.page3_led_number
        elif page_num == 4:
            frame_type = self.I2cLedDriverFrameType.ACCESS_PAGE4_REGISTER
            data_len = self.page4_led_number
        # end if
        if self.state == frame_type and address == self.slave_address and len(data) == data_len:
            status = True
        # end if
        return status
    # end def is_set_pwm_value_message

    def update_state(self, frame):
        """
        Update ``IssiLedDriverI2cFrame`` with a new ``I2cSpyFrame``

        :param frame: new I2C frame
        :type frame: ``I2cSpyFrame``
        """
        if self.is_unlock_message(frame):
            self.state = self.I2cLedDriverFrameType.UNLOCK
        elif self.is_access_page_register_message(frame, page_num=0):
            self.state = self.I2cLedDriverFrameType.ACCESS_PAGE0_REGISTER
        elif self.is_access_page_register_message(frame, page_num=1):
            self.state = self.I2cLedDriverFrameType.ACCESS_PAGE1_REGISTER
        elif self.is_access_page_register_message(frame, page_num=2):
            self.state = self.I2cLedDriverFrameType.ACCESS_PAGE2_REGISTER
        elif self.is_access_page_register_message(frame, page_num=3):
            self.state = self.I2cLedDriverFrameType.ACCESS_PAGE3_REGISTER
        elif self.is_access_page_register_message(frame, page_num=4):
            self.state = self.I2cLedDriverFrameType.ACCESS_PAGE4_REGISTER
        elif self.is_set_pwm_value_message(frame, page_num=0):
            self.state = self.I2cLedDriverFrameType.SET_PWM_PAGE0_VALUE
        elif self.is_set_pwm_value_message(frame, page_num=1):
            self.state = self.I2cLedDriverFrameType.SET_PWM_PAGE1_VALUE
        elif self.is_set_pwm_value_message(frame, page_num=2):
            self.state = self.I2cLedDriverFrameType.SET_PWM_PAGE2_VALUE
        elif self.is_set_pwm_value_message(frame, page_num=3):
            self.state = self.I2cLedDriverFrameType.SET_PWM_PAGE3_VALUE
        elif self.is_set_pwm_value_message(frame, page_num=4):
            self.state = self.I2cLedDriverFrameType.SET_PWM_PAGE4_VALUE
        else:
            self.state = self.I2cLedDriverFrameType.UNDETERMINED
        # end if
    # end def update_state
# end class IssiLedDriverI2cFrame


class GenericDriverIcParser:
    """
    Generic Class for LED driver IC parser
    """
    # I2C spy module ID available
    i2c_spy_module_available_ids = None
    MAXIMUM_TIMESTAMP_DIFFERENCE_BETWEEN_DATA_ON_A_SAME_FRAME = 0.025  # in seconds

    @unique
    class BufferStatus(IntEnum):
        """
        Buffer Status
        """
        BUFFER_EMPTY = auto()
        BUFFER_IN_PROGRESS = auto()
        BUFFER_FULL = auto()
    # end class BufferStatus

    def __init__(self):
        self.led_ic_buffer_spy_timestamp = 0
        self.led_ic_buffer_state = self.BufferStatus.BUFFER_EMPTY
    # end def __init__

    def reset(self):
        """
        Reset the LED driver IC parser
        """
        self.led_ic_buffer_spy_timestamp = 0
        self.led_ic_buffer_state = self.BufferStatus.BUFFER_EMPTY
    # end def reset

    def update(self, frame, i2c_id=0):
        """
        Update the driver IC state machine and fill the ``led_ic_buffer_by_led_id`` if necessary

        :param frame: A I2C frame from ``I2cSpyFrameRun``
        :type frame: ``I2cSpyFrameRun``
        :param i2c_id: I2C SPY module instance identifier, defaults to 0 - OPTIONAL
        :type i2c_id: ``int``
        """
        raise NotImplementedError('update method not implemented')
    # end def update

    def get_led_spy_buffer(self):
        """
        Get the LED driver IC frames buffer from the I2C spy module. Set led_ic_buffer_state variable to BUFFER_EMPTY

        return: led_ic_buffer_by_led_id
        :rtype: ``list``
        """
        raise NotImplementedError('get_led_spy_buffer method not implemented')
    # end def get_led_spy_buffer
# end class GenericDriverIcParser


class IngaLedDriverIcFramesParser(GenericDriverIcParser):
    """
    Define the IS31FL3742 (https://www.mouser.ch/datasheet/2/198/IS31FL3742A_DS-1839511.pdf) LED driver IC frames parser
     used on an Inga keyboard.
    """
    # I2C spy module ID available
    i2c_spy_module_available_ids = [0]

    # DriverIC IS3742A part
    IS3742_ADDR = 0x60
    # For LED layout in driver IC 3742A
    IS3742A_LED_NB_PG0 = 180
    IS3742A_LED_NB_TOTAL = IS3742A_LED_NB_PG0
    MAXIMUM_LED_ID = 180

    def __init__(self):
        super().__init__()
        self.is3742_driver_ic = IssiLedDriverI2cFrame(self.IS3742_ADDR, self.IS3742A_LED_NB_PG0)
        self.is3742_buff = [nan for _ in range(0, self.IS3742A_LED_NB_PG0 + 1)]
    # end def __init__

    def reset(self):
        # See ``GenericDriverIcParser.reset``
        super().reset()
        self.is3742_driver_ic = IssiLedDriverI2cFrame(self.IS3742_ADDR, self.IS3742A_LED_NB_PG0)
        self.is3742_buff = [nan for _ in range(0, self.IS3742A_LED_NB_PG0 + 1)]
    # end def reset

    def get_led_spy_buffer(self):
        # See ``GenericDriverIcParser.get_led_spy_buffer``

        led_ic_buffer_by_led_id = [nan for _ in range(0, self.MAXIMUM_LED_ID + 1)]
        # led_id = 0 is reserved
        for led_id in range(1, self.MAXIMUM_LED_ID + 1):
            led_ic_buffer_by_led_id[led_id] = self.is3742_buff[led_id]
        # end for

        self.led_ic_buffer_state = self.BufferStatus.BUFFER_EMPTY
        return led_ic_buffer_by_led_id
    # end def get_led_spy_buffer

    def update(self, frame, i2c_id=0):
        # See ``GenericDriverIcParser.update``

        self.is3742_driver_ic.update_state(frame)
        if self.is3742_driver_ic.state == self.is3742_driver_ic.I2cLedDriverFrameType.SET_PWM_PAGE0_VALUE:
            self.is3742_buff[0:self.IS3742A_LED_NB_PG0 + 1] = frame[1:self.IS3742A_LED_NB_PG0 + 2]
            if self.led_ic_buffer_state == self.BufferStatus.BUFFER_EMPTY:
                self.led_ic_buffer_state = self.BufferStatus.BUFFER_FULL
                self.led_ic_buffer_spy_timestamp = frame.time
            # end if
        # end if
    # end def update
# end class IngaLedDriverIcFramesParser


class TopazDriverIcParser(GenericDriverIcParser):
    """
    LED driver IC parser for Topaz keyboard.

    Note : For now only ONE driver IC can be parsed either DriverIC IS31FL3741A
    (https://www.lumissil.com/assets/pdf/core/IS31FL3741A_DS.pdf) or DriverIC IS31FL3746A
    (https://lumissil.com/assets/pdf/core/IS31FL3746A_DS.pdf)
    """

    # I2C spy module ID available
    i2c_spy_module_available_ids = [0, 1]

    # DriverIC IS3741A part
    IS3741_ADDR = 0x66
    # For LED layout in driver IC 3741A
    IS3741A_PAGE0_LED_NUM = 0xB3 + 1
    IS3741A_PAGE1_LED_NUM = 0xAA + 1
    IS3741A_LEDRGB_NB_PG0 = 60
    IS3741A_LEDRGB_NB_PG1 = 57
    IS3741A_LEDRGB_NB_TOTAL = IS3741A_LEDRGB_NB_PG0 + IS3741A_LEDRGB_NB_PG1
    IS3741A_IC_NB = 1

    # DriverIC IS3746A part
    IS3746_ADDR = 0xC0
    IS3746_ADDR_EDGE = 0XDE
    IS3746A_PAGE0_LED_NUM = 0X48
    IS3746A_LEDRGB_NB_PG0 = 24
    IS3746A_IC_NB = 1

    MAXIMUM_LED_ID = 165

    def __init__(self):
        super().__init__()
        self.is3741_buff = full([self.IS3741A_IC_NB, self.IS3741A_LEDRGB_NB_TOTAL * 3], nan)
        self.is3746_buff = full([self.IS3746A_IC_NB, self.IS3746A_LEDRGB_NB_PG0 * 3], nan)
        self.is3741_buff_state = self.BufferStatus.BUFFER_EMPTY
        self.is3746_buff_state = self.BufferStatus.BUFFER_EMPTY

        self.is3741_driver_ic = IssiLedDriverI2cFrame(self.IS3741_ADDR, self.IS3741A_PAGE0_LED_NUM,
                                                      self.IS3741A_PAGE1_LED_NUM)

        self.is3746_driver_ic = IssiLedDriverI2cFrame(self.IS3746_ADDR_EDGE, self.IS3746A_PAGE0_LED_NUM)
        self.led_ic_buffer_by_led_id = [RgbComponents(nan, nan, nan) for _ in range(0, self.MAXIMUM_LED_ID + 1)]
    # end def __init__

    def reset(self):
        # See ``GenericDriverIcParser.reset``
        super().reset()
        self.is3741_buff = full([self.IS3741A_IC_NB, self.IS3741A_LEDRGB_NB_TOTAL * 3], nan)
        self.is3746_buff = full([self.IS3746A_IC_NB, self.IS3746A_LEDRGB_NB_PG0 * 3], nan)
        self.is3741_buff_state = self.BufferStatus.BUFFER_EMPTY
        self.is3746_buff_state = self.BufferStatus.BUFFER_EMPTY

        self.is3741_driver_ic = IssiLedDriverI2cFrame(self.IS3741_ADDR, self.IS3741A_PAGE0_LED_NUM,
                                                      self.IS3741A_PAGE1_LED_NUM)

        self.is3746_driver_ic = IssiLedDriverI2cFrame(self.IS3746_ADDR_EDGE, self.IS3746A_PAGE0_LED_NUM)
        self.led_ic_buffer_by_led_id = [RgbComponents(nan, nan, nan) for _ in range(0, self.MAXIMUM_LED_ID + 1)]
    # end def reset

    def get_led_address(self, led_id):
        """
        Return the LED address corresponding to the LED id.

        :param led_id: The led id.
        :type led_id: ``int``

        :return: The LED Address corresponding to the LED id.
        :rtype: ``LedAddress``
        """
        led_address = LedAddress()
        if led_id > (self.IS3741A_LEDRGB_NB_TOTAL + self.IS3746A_LEDRGB_NB_PG0):
            # edge lighting
            led_address.led_address_ic = 2
            n = led_id - (self.IS3741A_LEDRGB_NB_TOTAL + self.IS3746A_LEDRGB_NB_PG0)
            led_address.led_address_page = 0
            led_address.green_led_address = (n - 1) * 3
            led_address.red_led_address = led_address.green_led_address + 1
            led_address.blue_led_address = led_address.green_led_address + 2

        elif led_id > self.IS3741A_LEDRGB_NB_TOTAL:
            # keypad
            led_address.led_address_ic = 1
            n = led_id - self.IS3741A_LEDRGB_NB_TOTAL
            led_address.led_address_page = 0
            led_address.blue_led_address = (n - 1) * 3
            led_address.green_led_address = led_address.blue_led_address + 1
            led_address.red_led_address = led_address.blue_led_address + 2

        else:
            # main key
            led_address.led_address_ic = 0
            # decide led is at which page of driver IC
            if led_id > self.IS3741A_LEDRGB_NB_PG0:
                led_address.led_address_page = 1
                n = led_id - self.IS3741A_LEDRGB_NB_PG0
            else:
                led_address.led_address_page = 0
                n = led_id
            # end if
            led_address.blue_led_address = (n - 1) * 3
            led_address.green_led_address = led_address.blue_led_address + 1
            led_address.red_led_address = led_address.blue_led_address + 2
        # end if
        return led_address
    # end def get_led_address

    def driver_ic_to_rgb_led_id(self, led_id):
        """
        Return the rgb values of a LED id from the driver IC buffer.

        :param led_id: The led id.
        :type led_id: ``uint8``

        :return: The rgb values from driver IC buffer
        :rtype: ``RgbComponents``

        :raise ``AssertionError``: Led ID is out of bound
        """
        rgb_values = RgbComponents(nan, nan, nan)
        assert led_id <= self.MAXIMUM_LED_ID

        rgb_address = self.get_led_address(led_id)
        if rgb_address.led_address_ic == 0:
            # main key is2741A
            if rgb_address.led_address_page in [0, 1]:
                rgb_values.r = self.is3741_buff[0][rgb_address.led_address_page * self.IS3741A_PAGE0_LED_NUM +
                                                   rgb_address.red_led_address]
                rgb_values.g = self.is3741_buff[0][rgb_address.led_address_page * self.IS3741A_PAGE0_LED_NUM +
                                                   rgb_address.green_led_address]
                rgb_values.b = self.is3741_buff[0][rgb_address.led_address_page * self.IS3741A_PAGE0_LED_NUM +
                                                   rgb_address.blue_led_address]
            # end if
        elif rgb_address.led_address_ic == 2:
            # edge lighting
            rgb_values.r = self.is3746_buff[0][rgb_address.red_led_address]
            rgb_values.g = self.is3746_buff[0][rgb_address.green_led_address]
            rgb_values.b = self.is3746_buff[0][rgb_address.blue_led_address]
        # end if
        return rgb_values
    # end def driver_ic_to_rgb_led_id

    def get_led_spy_buffer(self):
        # See ``GenericDriverIcParser.get_led_spy_buffer``

        led_ic_buffer_by_led_id = [RgbComponents(nan, nan, nan) for _ in range(0, self.MAXIMUM_LED_ID + 1)]
        # led_id = 0 is reserved
        for led_id in range(1, self.MAXIMUM_LED_ID + 1):
            led_ic_buffer_by_led_id[led_id] = self.driver_ic_to_rgb_led_id(uint8(led_id))
        # end for

        self.led_ic_buffer_state = self.BufferStatus.BUFFER_EMPTY
        self.is3741_buff_state = self.BufferStatus.BUFFER_EMPTY
        self.is3746_buff_state = self.BufferStatus.BUFFER_EMPTY

        return led_ic_buffer_by_led_id
    # end def get_led_spy_buffer

    def update(self, frame, i2c_id=0):
        # See ``GenericDriverIcParser.update``
        if (frame.time - self.led_ic_buffer_spy_timestamp) > \
                self.MAXIMUM_TIMESTAMP_DIFFERENCE_BETWEEN_DATA_ON_A_SAME_FRAME:
            self.is3741_buff_state = self.BufferStatus.BUFFER_EMPTY
        # end if

        # is3741 driver IC is connected to I2C SPY module 0
        if i2c_id == 0:
            self.is3741_driver_ic.update_state(frame)
            if self.is3741_driver_ic.state == self.is3741_driver_ic.I2cLedDriverFrameType.SET_PWM_PAGE1_VALUE:
                self.is3741_buff[0][self.IS3741A_PAGE0_LED_NUM::] = frame[2:self.IS3741A_PAGE1_LED_NUM + 2]
                if self.is3741_buff_state == self.BufferStatus.BUFFER_EMPTY:
                    self.is3741_buff_state = self.BufferStatus.BUFFER_IN_PROGRESS
                    self.led_ic_buffer_spy_timestamp = frame.time
                elif self.is3741_buff_state == self.BufferStatus.BUFFER_IN_PROGRESS:
                    self.is3741_buff_state = self.BufferStatus.BUFFER_FULL
                # end if
            elif self.is3741_driver_ic.state == self.is3741_driver_ic.I2cLedDriverFrameType.SET_PWM_PAGE0_VALUE:
                self.is3741_buff[0][0:self.IS3741A_PAGE0_LED_NUM] = frame[2:self.IS3741A_PAGE0_LED_NUM + 2]
                if self.is3741_buff_state == self.BufferStatus.BUFFER_EMPTY:
                    self.is3741_buff_state = self.BufferStatus.BUFFER_IN_PROGRESS
                    self.led_ic_buffer_spy_timestamp = frame.time
                elif self.is3741_buff_state == self.BufferStatus.BUFFER_IN_PROGRESS:
                    self.is3741_buff_state = self.BufferStatus.BUFFER_FULL
                # end if
            # end if

        # is3746 driver IC is connected to I2C SPY module 1
        elif i2c_id == 1:
            self.is3746_driver_ic.update_state(frame)
            if self.is3746_driver_ic.state == self.is3746_driver_ic.I2cLedDriverFrameType.SET_PWM_PAGE0_VALUE:
                self.is3746_buff[0][0:self.IS3746A_PAGE0_LED_NUM] = frame[2:self.IS3746A_PAGE0_LED_NUM + 2]
                if self.is3746_buff_state == self.BufferStatus.BUFFER_EMPTY:
                    self.is3746_buff_state = self.BufferStatus.BUFFER_FULL
                    self.led_ic_buffer_spy_timestamp = frame.time
                # end if
            # end if
        # end if

        # Note : update function works only for one I2C spy module at the same time
        if (self.is3741_buff_state == self.BufferStatus.BUFFER_FULL) or \
                (self.is3746_buff_state == self.BufferStatus.BUFFER_FULL):
            self.led_ic_buffer_state = self.BufferStatus.BUFFER_FULL
        # end if
        # Note : update function works only for one I2C spy module at the same time
        if (self.is3741_buff_state == self.BufferStatus.BUFFER_IN_PROGRESS) or \
                (self.is3746_buff_state == self.BufferStatus.BUFFER_IN_PROGRESS):
            self.led_ic_buffer_state = self.BufferStatus.BUFFER_IN_PROGRESS
        # end if
    # end def update
# end class TopazDriverIcParser


class CinderellaWirelessDriverIcParser(GenericDriverIcParser):
    """
    LED driver IC parser for Cinderella wireless keyboard.
    """

    # I2C spy module ID available
    i2c_spy_module_available_ids = [0]

    # DriverIC IS3741A part
    IS3741_ADDR = 0x66
    # For LED layout in driver IC 3741A
    IS3741A_PAGE0_LED_NUM = 0xB3 + 1
    IS3741A_PAGE1_LED_NUM = 0xAA + 1
    IS3741A_LEDRGB_NB_PG0 = 60
    IS3741A_LEDRGB_NB_PG1 = 57
    IS3741A_LEDRGB_NB_TOTAL = IS3741A_LEDRGB_NB_PG0 + IS3741A_LEDRGB_NB_PG1
    IS3741A_IC_NB = 1

    MAXIMUM_LED_ID = IS3741A_LEDRGB_NB_TOTAL

    def __init__(self):
        super().__init__()
        self.is3741_buff = full([self.IS3741A_IC_NB, self.IS3741A_LEDRGB_NB_TOTAL * 3], nan)
        self.is3741_buff_state = self.BufferStatus.BUFFER_EMPTY

        self.is3741_driver_ic = IssiLedDriverI2cFrame(self.IS3741_ADDR, self.IS3741A_PAGE0_LED_NUM,
                                                      self.IS3741A_PAGE1_LED_NUM)

        self.led_ic_buffer_by_led_id = [RgbComponents(nan, nan, nan) for _ in range(0, self.MAXIMUM_LED_ID + 1)]
    # end def __init__

    def reset(self):
        # See ``GenericDriverIcParser.reset``
        super().reset()
        self.is3741_buff = full([self.IS3741A_IC_NB, self.IS3741A_LEDRGB_NB_TOTAL * 3], nan)
        self.is3741_buff_state = self.BufferStatus.BUFFER_EMPTY

        self.is3741_driver_ic = IssiLedDriverI2cFrame(self.IS3741_ADDR, self.IS3741A_PAGE0_LED_NUM,
                                                      self.IS3741A_PAGE1_LED_NUM)

        self.led_ic_buffer_by_led_id = [RgbComponents(nan, nan, nan) for _ in range(0, self.MAXIMUM_LED_ID + 1)]
    # end def reset

    def get_led_address(self, led_id):
        """
        Return the LED address corresponding to the LED id.

        :param led_id: The led id.
        :type led_id: ``int``

        :return: The LED Address corresponding to the LED id.
        :rtype: ``LedAddress``
        """
        led_address = LedAddress()

        # main key
        led_address.led_address_ic = 0
        # decide led is at which page of driver IC
        if led_id > self.IS3741A_LEDRGB_NB_PG0:
            led_address.led_address_page = 1
            n = led_id - self.IS3741A_LEDRGB_NB_PG0
        else:
            led_address.led_address_page = 0
            n = led_id
        # end if
        led_address.blue_led_address = (n - 1) * 3
        led_address.green_led_address = led_address.blue_led_address + 1
        led_address.red_led_address = led_address.blue_led_address + 2

        return led_address
    # end def get_led_address

    def driver_ic_to_rgb_led_id(self, led_id):
        """
        Return the rgb values of a LED id from the driver IC buffer.

        :param led_id: The led id.
        :type led_id: ``uint8``

        :return: The rgb values from driver IC buffer
        :rtype: ``RgbComponents``

        :raise ``AssertionError``: Led ID is out of bound
        """
        rgb_values = RgbComponents(nan, nan, nan)
        assert led_id <= self.MAXIMUM_LED_ID

        rgb_address = self.get_led_address(led_id)

        if rgb_address.led_address_page in [0, 1]:
            rgb_values.r = self.is3741_buff[0][rgb_address.led_address_page * self.IS3741A_PAGE0_LED_NUM +
                                               rgb_address.red_led_address]
            rgb_values.g = self.is3741_buff[0][rgb_address.led_address_page * self.IS3741A_PAGE0_LED_NUM +
                                               rgb_address.green_led_address]
            rgb_values.b = self.is3741_buff[0][rgb_address.led_address_page * self.IS3741A_PAGE0_LED_NUM +
                                               rgb_address.blue_led_address]
        # end if

        return rgb_values
    # end def driver_ic_to_rgb_led_id

    def get_led_spy_buffer(self):
        # See ``GenericDriverIcParser.get_led_spy_buffer``

        led_ic_buffer_by_led_id = [RgbComponents(nan, nan, nan) for _ in range(0, self.MAXIMUM_LED_ID + 1)]
        # led_id = 0 is reserved
        for led_id in range(1, self.MAXIMUM_LED_ID + 1):
            led_ic_buffer_by_led_id[led_id] = self.driver_ic_to_rgb_led_id(uint8(led_id))
        # end for

        self.led_ic_buffer_state = self.BufferStatus.BUFFER_EMPTY
        self.is3741_buff_state = self.BufferStatus.BUFFER_EMPTY

        return led_ic_buffer_by_led_id
    # end def get_led_spy_buffer

    def update(self, frame, i2c_id=0):
        # See ``GenericDriverIcParser.update``
        if (frame.time - self.led_ic_buffer_spy_timestamp) > \
                self.MAXIMUM_TIMESTAMP_DIFFERENCE_BETWEEN_DATA_ON_A_SAME_FRAME:
            self.is3741_buff_state = self.BufferStatus.BUFFER_EMPTY
        # end if

        # is3741 driver IC is connected to I2C SPY module 0
        self.is3741_driver_ic.update_state(frame)
        if self.is3741_driver_ic.state == self.is3741_driver_ic.I2cLedDriverFrameType.SET_PWM_PAGE1_VALUE:
            self.is3741_buff[0][self.IS3741A_PAGE0_LED_NUM::] = frame[2:self.IS3741A_PAGE1_LED_NUM + 2]
            if self.is3741_buff_state == self.BufferStatus.BUFFER_EMPTY:
                self.is3741_buff_state = self.BufferStatus.BUFFER_IN_PROGRESS
                self.led_ic_buffer_spy_timestamp = frame.time
            elif self.is3741_buff_state == self.BufferStatus.BUFFER_IN_PROGRESS:
                self.is3741_buff_state = self.BufferStatus.BUFFER_FULL
            # end if
        elif self.is3741_driver_ic.state == self.is3741_driver_ic.I2cLedDriverFrameType.SET_PWM_PAGE0_VALUE:
            self.is3741_buff[0][0:self.IS3741A_PAGE0_LED_NUM] = frame[2:self.IS3741A_PAGE0_LED_NUM + 2]
            if self.is3741_buff_state == self.BufferStatus.BUFFER_EMPTY:
                self.is3741_buff_state = self.BufferStatus.BUFFER_IN_PROGRESS
                self.led_ic_buffer_spy_timestamp = frame.time
            elif self.is3741_buff_state == self.BufferStatus.BUFFER_IN_PROGRESS:
                self.is3741_buff_state = self.BufferStatus.BUFFER_FULL
            # end if
        # end if

        # Note : update function works only for one I2C spy module at the same time
        if self.is3741_buff_state == self.BufferStatus.BUFFER_FULL:
            self.led_ic_buffer_state = self.BufferStatus.BUFFER_FULL
        # end if
        # Note : update function works only for one I2C spy module at the same time
        if self.is3741_buff_state == self.BufferStatus.BUFFER_IN_PROGRESS:
            self.led_ic_buffer_state = self.BufferStatus.BUFFER_IN_PROGRESS
        # end if
    # end def update
# end class CinderellaWirelessDriverIcParser


class GarnetDriverIcParser(GenericDriverIcParser):
    """
    LED driver IC parser for Garnet Mouse.

    https://www.lumissil.com/assets/pdf/core/IS31FL3242_DS.pdf
    """

    # I2C spy module ID available
    i2c_spy_module_available_ids = [0]

    # DriverIC IS3242
    IS3242_ADDR = 0x88
    IS3242_START_PWM_REGISTERS_ADDRESS = 0x0E
    IS3242_PWM_REGISTER_NUMBER = 24
    MAXIMUM_LED_ID = 4

    def __init__(self):
        super().__init__()
        self.is3242_buff = [nan for _ in range(0, self.IS3242_PWM_REGISTER_NUMBER + 1)]
        self.led_ic_buffer_by_led_id = [RgbComponents(nan, nan, nan) for _ in range(0, self.MAXIMUM_LED_ID + 1)]
    # end def __init__

    def reset(self):
        # See ``GenericDriverIcParser.reset``
        super().reset()
        self.is3242_buff = [nan for _ in range(0, self.IS3242_PWM_REGISTER_NUMBER + 1)]
        self.led_ic_buffer_by_led_id = [RgbComponents(nan, nan, nan) for _ in range(0, self.MAXIMUM_LED_ID + 1)]
    # end def reset

    def update(self, frame, i2c_id=0):
        # See ``GenericDriverIcParser.update``
        address_i2c = frame[0]
        address_register = frame[1]
        if address_i2c == self.IS3242_ADDR and address_register == self.IS3242_START_PWM_REGISTERS_ADDRESS:
            self.is3242_buff[0:self.IS3242_PWM_REGISTER_NUMBER] = frame[2:self.IS3242_PWM_REGISTER_NUMBER + 2]
            self.led_ic_buffer_state = self.BufferStatus.BUFFER_FULL
            self.led_ic_buffer_spy_timestamp = frame.time
        # end if
    # end def update

    def get_led_spy_buffer(self):
        # See ``GenericDriverIcParser.get_led_spy_buffer``
        led_ic_buffer_by_led_id = [nan for _ in range(0, self.MAXIMUM_LED_ID + 1)]
        # led_id = 0 is reserved
        for led_id in range(1, self.MAXIMUM_LED_ID + 1):
            rgb_values = RgbComponents(nan, nan, nan)
            index = (led_id - 1) * 3 * 2  # 3 for red, green, blue and 2 for High bits and Low bits of PWM Register
            rgb_values.r = uint16(self.is3242_buff[index] + (self.is3242_buff[index + 1] << 8))
            rgb_values.g = uint16(self.is3242_buff[index + 2] + (self.is3242_buff[index + 3] << 8))
            rgb_values.b = uint16(self.is3242_buff[index + 4] + (self.is3242_buff[index + 5] << 8))

            led_ic_buffer_by_led_id[led_id] = rgb_values
        # end for

        self.led_ic_buffer_state = self.BufferStatus.BUFFER_EMPTY
        return led_ic_buffer_by_led_id
    # end def get_led_spy_buffer
# end class GarnetDriverIcParser


GET_I2C_LED_DRIVER_BY_ID = {
    # Pollux firmware on Inga hardware
    'RBO03': IngaLedDriverIcFramesParser(),
    'RBK71': IngaLedDriverIcFramesParser(),
    'RBK75': IngaLedDriverIcFramesParser(),
    'MPK17': TopazDriverIcParser(),
    'MPK25': CinderellaWirelessDriverIcParser(),
    'MPM28': GarnetDriverIcParser(),
}

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
