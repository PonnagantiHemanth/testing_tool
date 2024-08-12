#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.vlp.features.common.contextualdisplay
:brief: VLP 1.0 ``ContextualDisplay`` command interface definition
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/11/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import TYPE
from pyhid.vlp.vlpmessage import VlpMessage
from pyhid.vlp.vlpmessage import VlpMessageRawPayload
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ImageFormat:
    """
    Define Image format Constants
    """
    JPEG = 0x00
    RGB_565 = 0x01
    RGB_888 = 0x02
# end class ImageFormat


class ButtonShape:
    """
    Define Button shape Constants
    """
    RECTANGULAR = 0x01
    CIRCULAR = 0x02
# end class ButtonShape


class DisplayInfoPayload(BitFieldContainerMixin):
    """
    Define the format of a Display Info payload
    """
    class FID:
        """
        Field Identifiers
        """
        DISPLAY_SHAPE = 0xFF
        DISPLAY_DIMENSION = DISPLAY_SHAPE - 1
        HORIZONTAL_RESOLUTION = DISPLAY_DIMENSION - 1
        VERTICAL_RESOLUTION = HORIZONTAL_RESOLUTION - 1
        BUTTON_COUNT = VERTICAL_RESOLUTION - 1
        VISIBLE_AREA_COUNT = BUTTON_COUNT - 1
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        DISPLAY_SHAPE = 0x8
        DISPLAY_DIMENSION = 0x10
        HORIZONTAL_RESOLUTION = 0x10
        VERTICAL_RESOLUTION = 0x10
        BUTTON_COUNT = 0x8
        VISIBLE_AREA_COUNT = 0x8
    # end class LEN

    FIELDS = (
        BitField(fid=FID.DISPLAY_SHAPE, length=LEN.DISPLAY_SHAPE,
                 title="DisplayShape", name="display_shape",
                 checks=(CheckHexList(LEN.DISPLAY_SHAPE // 8), CheckByte(),)),
        BitField(fid=FID.DISPLAY_DIMENSION, length=LEN.DISPLAY_DIMENSION,
                 title="DisplayDimension", name="display_dimension",
                 checks=(CheckHexList(LEN.DISPLAY_DIMENSION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DISPLAY_DIMENSION) - 1),)),
        BitField(fid=FID.HORIZONTAL_RESOLUTION, length=LEN.HORIZONTAL_RESOLUTION,
                 title="HorizontalResolution", name="horizontal_resolution",
                 checks=(CheckHexList(LEN.HORIZONTAL_RESOLUTION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HORIZONTAL_RESOLUTION) - 1),)),
        BitField(fid=FID.VERTICAL_RESOLUTION, length=LEN.VERTICAL_RESOLUTION,
                 title="VerticalResolution", name="vertical_resolution",
                 checks=(CheckHexList(LEN.VERTICAL_RESOLUTION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.VERTICAL_RESOLUTION) - 1),)),
        BitField(fid=FID.BUTTON_COUNT, length=LEN.BUTTON_COUNT,
                 title="ButtonCount", name="button_count",
                 checks=(CheckHexList(LEN.BUTTON_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.VISIBLE_AREA_COUNT, length=LEN.VISIBLE_AREA_COUNT,
                 title="VisibleAreaCount", name="visible_area_count",
                 checks=(CheckHexList(LEN.VISIBLE_AREA_COUNT // 8), CheckByte(),)),
    )

    def __init__(self, display_shape, display_dimension, horizontal_resolution, vertical_resolution, button_count,
                 visible_area_count):
        """
        :param display_shape: Display Shape in the Display info table
        :type display_shape: ``int|HexList``
        :param display_dimension: Display Dimension in the Display info table
        :type display_dimension: ``int|HexList``
        :param horizontal_resolution: Display Horizontal Resolution in the Display info table
        :type horizontal_resolution: ``int|HexList``
        :param vertical_resolution: Display Vertical Resolution in the Display info table
        :type vertical_resolution: ``int|HexList``
        :param button_count: Display Button Count in the Display info table
        :type button_count: ``int|HexList``
        :param visible_area_count: Display Visible Area Count in the Display info table
        :type visible_area_count: ``int|HexList``
        """
        super().__init__(display_shape=display_shape, display_dimension=display_dimension,
                         horizontal_resolution=horizontal_resolution, vertical_resolution=vertical_resolution,
                         button_count=button_count, visible_area_count=visible_area_count)
    # end def __init__
# end class DisplayInfoPayload


class ButtonInfoPayload(BitFieldContainerMixin):
    """
    Define the format of a Display Button Info payload
    """

    class FID(object):
        """
        Field identifiers
        """
        BUTTON_SHAPE = 0xFF
        BUTTON_LOCATION_X = BUTTON_SHAPE - 1
        BUTTON_LOCATION_Y = BUTTON_LOCATION_X - 1
        BUTTON_LOCATION_WIDTH = BUTTON_LOCATION_Y - 1
        BUTTON_LOCATION_HEIGHT = BUTTON_LOCATION_WIDTH - 1
    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        BUTTON_SHAPE = 0x8
        BUTTON_LOCATION_X = 0x10
        BUTTON_LOCATION_Y = 0x10
        BUTTON_LOCATION_WIDTH = 0x10
        BUTTON_LOCATION_HEIGHT = 0x10
    # end class LEN

    FIELDS = (
        BitField(fid=FID.BUTTON_SHAPE, length=LEN.BUTTON_SHAPE,
                 title="ButtonShape", name="button_shape",
                 checks=(CheckHexList(LEN.BUTTON_SHAPE // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_LOCATION_X, length=LEN.BUTTON_LOCATION_X,
                 title="ButtonLocationX", name="button_location_x",
                 checks=(CheckHexList(LEN.BUTTON_LOCATION_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BUTTON_LOCATION_X) - 1),)),
        BitField(fid=FID.BUTTON_LOCATION_Y, length=LEN.BUTTON_LOCATION_Y,
                 title="ButtonLocationY", name="button_location_y",
                 checks=(CheckHexList(LEN.BUTTON_LOCATION_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BUTTON_LOCATION_Y) - 1),)),
        BitField(fid=FID.BUTTON_LOCATION_WIDTH, length=LEN.BUTTON_LOCATION_WIDTH,
                 title="ButtonLocationWidth", name="button_location_width",
                 checks=(CheckHexList(LEN.BUTTON_LOCATION_WIDTH // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BUTTON_LOCATION_WIDTH) - 1),)),
        BitField(fid=FID.BUTTON_LOCATION_HEIGHT, length=LEN.BUTTON_LOCATION_HEIGHT,
                 title="ButtonLocationHeight", name="button_location_height",
                 checks=(CheckHexList(LEN.BUTTON_LOCATION_HEIGHT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BUTTON_LOCATION_HEIGHT) - 1),)),
    )

    def __init__(self, button_shape, button_location_x, button_location_y, button_location_width,
                 button_location_height):
        """
        :param button_shape: Button Shape in the Button info table
        :type button_shape: ``int|HexList``
        :param button_location_x: Button Location X in the Button info table
        :type button_location_x: ``int|HexList``
        :param button_location_y: Button Location Y in the Button info table
        :type button_location_y: ``int|HexList``
        :param button_location_width: Button Location Width in the Button info table
        :type button_location_width: ``int|HexList``
        :param button_location_height: Button Location Height in the Button info table
        :type button_location_height: ``int|HexList``
        """
        super().__init__(button_shape=button_shape, button_location_x=button_location_x,
                         button_location_y=button_location_y, button_location_width=button_location_width,
                         button_location_height=button_location_height)
    # end def __init__
# end class ButtonInfoPayload


class VisibleAreaInfoPayload(BitFieldContainerMixin):
    """
    Define the format of a Display Visible Area Info payload
    """

    class FID(object):
        """
        Field identifiers
        """
        VISIBLE_AREA_SHAPE = 0xFF
        VISIBLE_AREA_LOCATION_X = VISIBLE_AREA_SHAPE - 1
        VISIBLE_AREA_LOCATION_Y = VISIBLE_AREA_LOCATION_X - 1
        VISIBLE_AREA_WIDTH = VISIBLE_AREA_LOCATION_Y - 1
        VISIBLE_AREA_HEIGHT = VISIBLE_AREA_WIDTH - 1
    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        VISIBLE_AREA_SHAPE = 0x8
        VISIBLE_AREA_LOCATION_X = 0x10
        VISIBLE_AREA_LOCATION_Y = 0x10
        VISIBLE_AREA_WIDTH = 0x10
        VISIBLE_AREA_HEIGHT = 0x10
    # end class LEN

    FIELDS = (
        BitField(fid=FID.VISIBLE_AREA_SHAPE, length=LEN.VISIBLE_AREA_SHAPE,
                 title="VisibleAreaShape", name="visible_area_shape",
                 checks=(CheckHexList(LEN.VISIBLE_AREA_SHAPE // 8), CheckByte(),)),
        BitField(fid=FID.VISIBLE_AREA_LOCATION_X, length=LEN.VISIBLE_AREA_LOCATION_X,
                 title="VisibleAreaLocationX", name="visible_area_location_x",
                 checks=(CheckHexList(LEN.VISIBLE_AREA_LOCATION_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.VISIBLE_AREA_LOCATION_X) - 1),)),
        BitField(fid=FID.VISIBLE_AREA_LOCATION_Y, length=LEN.VISIBLE_AREA_LOCATION_Y,
                 title="VisibleAreaLocationY", name="visible_area_location_y",
                 checks=(CheckHexList(LEN.VISIBLE_AREA_LOCATION_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.VISIBLE_AREA_LOCATION_Y) - 1),)),
        BitField(fid=FID.VISIBLE_AREA_WIDTH, length=LEN.VISIBLE_AREA_WIDTH,
                 title="VisibleAreaWidth", name="visible_area_width",
                 checks=(CheckHexList(LEN.VISIBLE_AREA_WIDTH // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.VISIBLE_AREA_WIDTH) - 1),)),
        BitField(fid=FID.VISIBLE_AREA_HEIGHT, length=LEN.VISIBLE_AREA_HEIGHT,
                 title="VisibleAreaHeight", name="visible_area_height",
                 checks=(CheckHexList(LEN.VISIBLE_AREA_HEIGHT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.VISIBLE_AREA_HEIGHT) - 1),)),
    )

    def __init__(self, visible_area_shape, visible_area_location_x, visible_area_location_y, visible_area_width,
                 visible_area_height):
        """
        :param visible_area_shape: Visible Area Shape in the Visible Area info table
        :type visible_area_shape: ``int|HexList``
        :param visible_area_location_x: Visible Area Location X in the Visible Area info table
        :type visible_area_location_x: ``int|HexList``
        :param visible_area_location_y: Visible Area Location Y in the Visible Area info table
        :type visible_area_location_y: ``int|HexList``
        :param visible_area_width: Visible Area Location Width in the Visible Area info table
        :type visible_area_width: ``int|HexList``
        :param visible_area_height: Visible Area Location Height in the Visible Area info table
        :type visible_area_height: ``int|HexList``
        """
        super().__init__(visible_area_shape=visible_area_shape, visible_area_location_x=visible_area_location_x,
                         visible_area_location_y=visible_area_location_y, visible_area_width=visible_area_width,
                         visible_area_height=visible_area_height)
    # end def __init__
# end class VisibleAreaInfoPayload


class ContextualDisplay(VlpMessage):
    """
    This feature is for contextual devices with a display under either physical transparent keys like creative consoles
    or virtual icons like a touch bar or a touch screen.
    """
    FEATURE_ID = 0x19A1
    MAX_FUNCTION_INDEX_V0 = 7

    class DeviceState:
        """
        Define ``DeviceState`` information
        """
        STREAMING_A0 = HexList('A0')
        STANDBY_ANIM_A1 = HexList('A1')
        STANDBY_ANIM_A2 = HexList('A2')
        SPLASH_ANIM_A3 = HexList('A3')
        SPLASH_ANIM_A4 = HexList('A4')
        ONBOARDING_ANIM_A5 = HexList('A5')
        DFU_SCREEN_A6 = HexList('A6')
        INTERNAL_EVENT_LIST = list(range(0xD0, 0xFF))
    # end class DeviceState

    class Capabilities:
        """
        Device Capability values for Contextual Display
        """
        DEFERRABLE = 0
        RGB_565 = 1
        RGB_888 = 2
        JPEG = 3
        CALIBRATED = 4
        ORIGIN = 5
    # end class Capabilities

    DEVICE_STATES = HexList(Numeral(DeviceState.STREAMING_A0), Numeral(DeviceState.STANDBY_ANIM_A1),
                            Numeral(DeviceState.STANDBY_ANIM_A2), Numeral(DeviceState.SPLASH_ANIM_A4),
                            Numeral(DeviceState.ONBOARDING_ANIM_A5), Numeral(DeviceState.DFU_SCREEN_A6))

    # noinspection DuplicatedCode
    class DeviceCapabilities(BitFieldContainerMixin):
        """
        Define ``DeviceCapabilities`` information

        Format:
        ====================================  ==========
        Name                                  Bit count
        ====================================  ==========
        Deferrable Display Update Capability  1
        RGB 565                               1
        RGB 888                               1
        JPEG                                  1
        calibrated                            1
        origin                                2
        Reserved                              25
        ====================================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            ORIGIN = RESERVED - 1
            CALIBRATED = ORIGIN - 1
            JPEG = CALIBRATED - 1
            RGB_888 = JPEG - 1
            RGB_565 = RGB_888 - 1
            DEFERRABLE_DISPLAY_UPDATE_CAPABILITY = RGB_565 - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x19
            ORIGIN = 0x2
            CALIBRATED = 0x1
            JPEG = 0x1
            RGB_888 = 0x1
            RGB_565 = 0x1
            DEFERRABLE_DISPLAY_UPDATE_CAPABILITY = 0x1
        # end class LEN

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=VlpMessage.DEFAULT.RESERVED),
            BitField(fid=FID.ORIGIN, length=LEN.ORIGIN,
                     title="Origin", name="origin",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.ORIGIN) - 1),)),
            BitField(fid=FID.CALIBRATED, length=LEN.CALIBRATED,
                     title="Calibrated", name="calibrated",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.CALIBRATED) - 1),)),
            BitField(fid=FID.JPEG, length=LEN.JPEG,
                     title="Jpeg", name="jpeg",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.JPEG) - 1),)),
            BitField(fid=FID.RGB_888, length=LEN.RGB_888,
                     title="Rgb888", name="rgb_888",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RGB_888) - 1),)),
            BitField(fid=FID.RGB_565, length=LEN.RGB_565,
                     title="Rgb565", name="rgb_565",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RGB_565) - 1),)),
            BitField(fid=FID.DEFERRABLE_DISPLAY_UPDATE_CAPABILITY, length=LEN.DEFERRABLE_DISPLAY_UPDATE_CAPABILITY,
                     title="DeferrableDisplayUpdateCapability", name="deferrable_display_update_capability",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.DEFERRABLE_DISPLAY_UPDATE_CAPABILITY) - 1),)),
        )
    # end class DeviceCapabilities

    class DeviceStateInfo(BitFieldContainerMixin):
        """
        Define ``DeviceStateInfo`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Device State                  8
        """
        class FID(object):
            """
            Field identifiers
            """
            DEVICE_STATE = 0xFF
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            DEVICE_STATE = 0x8
        # end class LEN

        FIELDS = (
            BitField(fid=FID.DEVICE_STATE, length=LEN.DEVICE_STATE,
                     title="Device State", name="device_state",
                     checks=(CheckHexList(LEN.DEVICE_STATE // 8),)),
        )
    # end class DeviceStateInfo

    class ButtonEventInfo(BitFieldContainerMixin):
        """
        Define ``ButtonEventInfo`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Button Event                  8
        """

        class FID(object):
            """
            Field identifiers
            """
            DISPLAY_INDEX = 0xFF
            BUTTON_EVENT = 0xFE
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            DISPLAY_INDEX = 0x8
            BUTTON_INDEX = 0x8
        # end class LEN

        FIELDS = (
            BitField(fid=FID.BUTTON_EVENT, length=LEN.BUTTON_INDEX,
                     title="ButtonIndex", name="button_index",
                     checks=(CheckHexList(LEN.BUTTON_INDEX // 8),)),
        )
    # end class ButtonEventInfo

    # noinspection DuplicatedCode
    class ButtonInfo(BitFieldContainerMixin):
        """
        Define ``ButtonInfo`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Button Shape                  8
        Button Location X             16
        Button Location Y             16
        Button Location Width         16
        Button Location Height        16
        ============================  ==========
        """
        class FID(object):
            """
            Field identifiers
            """
            BUTTON_SHAPE = 0xFF
            BUTTON_LOCATION_X = BUTTON_SHAPE - 1
            BUTTON_LOCATION_Y = BUTTON_LOCATION_X - 1
            BUTTON_LOCATION_WIDTH = BUTTON_LOCATION_Y - 1
            BUTTON_LOCATION_HEIGHT = BUTTON_LOCATION_WIDTH - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            BUTTON_SHAPE = 0x8
            BUTTON_LOCATION_X = 0x10
            BUTTON_LOCATION_Y = 0x10
            BUTTON_LOCATION_WIDTH = 0x10
            BUTTON_LOCATION_HEIGHT = 0x10
        # end class LEN

        FIELDS = (
            BitField(fid=FID.BUTTON_SHAPE, length=LEN.BUTTON_SHAPE,
                     title="ButtonShape", name="button_shape",
                     checks=(CheckHexList(LEN.BUTTON_SHAPE // 8), CheckByte(),)),
            BitField(fid=FID.BUTTON_LOCATION_X, length=LEN.BUTTON_LOCATION_X,
                     title="ButtonLocationX", name="button_location_x",
                     checks=(CheckHexList(LEN.BUTTON_LOCATION_X // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.BUTTON_LOCATION_X) - 1),)),
            BitField(fid=FID.BUTTON_LOCATION_Y, length=LEN.BUTTON_LOCATION_Y,
                     title="ButtonLocationY", name="button_location_y",
                     checks=(CheckHexList(LEN.BUTTON_LOCATION_Y // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.BUTTON_LOCATION_Y) - 1),)),
            BitField(fid=FID.BUTTON_LOCATION_WIDTH, length=LEN.BUTTON_LOCATION_WIDTH,
                     title="ButtonLocationWidth", name="button_location_width",
                     checks=(CheckHexList(LEN.BUTTON_LOCATION_WIDTH // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.BUTTON_LOCATION_WIDTH) - 1),)),
            BitField(fid=FID.BUTTON_LOCATION_HEIGHT, length=LEN.BUTTON_LOCATION_HEIGHT,
                     title="ButtonLocationHeight", name="button_location_height",
                     checks=(CheckHexList(LEN.BUTTON_LOCATION_HEIGHT // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.BUTTON_LOCATION_HEIGHT) - 1),)),
        )

        BUTTON_INFO_LENGTH = sum([field.length for field in FIELDS])
    # end class ButtonInfo

    # noinspection DuplicatedCode
    class VisibleAreaInfo(BitFieldContainerMixin):
        """
        Define ``VisibleAreaInfo`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Visible Area Shape            8
        Visible Area Location X       16
        Visible Area Location Y       16
        Visible Area Width            16
        Visible Area Height           16
        ============================  ==========
        """
        class FID(object):
            """
            Field identifiers
            """
            VISIBLE_AREA_SHAPE = 0xFF
            VISIBLE_AREA_LOCATION_X = VISIBLE_AREA_SHAPE - 1
            VISIBLE_AREA_LOCATION_Y = VISIBLE_AREA_LOCATION_X - 1
            VISIBLE_AREA_WIDTH = VISIBLE_AREA_LOCATION_Y - 1
            VISIBLE_AREA_HEIGHT = VISIBLE_AREA_WIDTH - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            VISIBLE_AREA_SHAPE = 0x8
            VISIBLE_AREA_LOCATION_X = 0x10
            VISIBLE_AREA_LOCATION_Y = 0x10
            VISIBLE_AREA_WIDTH = 0x10
            VISIBLE_AREA_HEIGHT = 0x10
        # end class LEN

        FIELDS = (
            BitField(fid=FID.VISIBLE_AREA_SHAPE, length=LEN.VISIBLE_AREA_SHAPE,
                     title="VisibleAreaShape", name="visible_area_shape",
                     checks=(CheckHexList(LEN.VISIBLE_AREA_SHAPE // 8), CheckByte(),)),
            BitField(fid=FID.VISIBLE_AREA_LOCATION_X, length=LEN.VISIBLE_AREA_LOCATION_X,
                     title="VisibleAreaLocationX", name="visible_area_location_x",
                     checks=(CheckHexList(LEN.VISIBLE_AREA_LOCATION_X // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.VISIBLE_AREA_LOCATION_X) - 1),)),
            BitField(fid=FID.VISIBLE_AREA_LOCATION_Y, length=LEN.VISIBLE_AREA_LOCATION_Y,
                     title="VisibleAreaLocationY", name="visible_area_location_y",
                     checks=(CheckHexList(LEN.VISIBLE_AREA_LOCATION_Y // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.VISIBLE_AREA_LOCATION_Y) - 1),)),
            BitField(fid=FID.VISIBLE_AREA_WIDTH, length=LEN.VISIBLE_AREA_WIDTH,
                     title="VisibleAreaWidth", name="visible_area_width",
                     checks=(CheckHexList(LEN.VISIBLE_AREA_WIDTH // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.VISIBLE_AREA_WIDTH) - 1),)),
            BitField(fid=FID.VISIBLE_AREA_HEIGHT, length=LEN.VISIBLE_AREA_HEIGHT,
                     title="VisibleAreaHeight", name="visible_area_height",
                     checks=(CheckHexList(LEN.VISIBLE_AREA_HEIGHT // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.VISIBLE_AREA_HEIGHT) - 1),)),
        )

        VISIBLE_AREA_INFO_LENGTH = sum([field.length for field in FIELDS])
    # end class VisibleAreaInfo

    # noinspection DuplicatedCode
    class Image(BitFieldContainerMixin):
        """
        Define ``Image`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Image Format                  4
        Reserved                      4
        Image Location X              16
        Image Location Y              16
        Image Location Width          16
        Image Location Height         16
        Image Size                    24
        Image Payload                 Variable Length
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            IMAGE_FORMAT = RESERVED - 1
            IMAGE_LOCATION_X = IMAGE_FORMAT - 1
            IMAGE_LOCATION_Y = IMAGE_LOCATION_X - 1
            IMAGE_LOCATION_WIDTH = IMAGE_LOCATION_Y - 1
            IMAGE_LOCATION_HEIGHT = IMAGE_LOCATION_WIDTH - 1
            IMAGE_SIZE = IMAGE_LOCATION_HEIGHT - 1
            IMAGE_DATA = IMAGE_SIZE - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x4
            IMAGE_FORMAT = 0x4
            IMAGE_LOCATION_X = 0x10
            IMAGE_LOCATION_Y = 0x10
            IMAGE_LOCATION_WIDTH = 0x10
            IMAGE_LOCATION_HEIGHT = 0x10
            IMAGE_SIZE = 0x18
            HEADER = (RESERVED + IMAGE_FORMAT + IMAGE_LOCATION_X + IMAGE_LOCATION_Y + IMAGE_LOCATION_WIDTH +
                      IMAGE_LOCATION_HEIGHT + IMAGE_SIZE)
        # end class LEN

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=VlpMessage.DEFAULT.RESERVED),
            BitField(fid=FID.IMAGE_FORMAT, length=LEN.IMAGE_FORMAT,
                     title="ImageFormat", name="image_format",
                     checks=(CheckHexList(LEN.IMAGE_FORMAT // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.IMAGE_FORMAT) - 1),)),
            BitField(fid=FID.IMAGE_LOCATION_X, length=LEN.IMAGE_LOCATION_X,
                     title="ImageLocationX", name="image_location_x",
                     checks=(CheckHexList(LEN.IMAGE_LOCATION_X // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.IMAGE_LOCATION_X) - 1),)),
            BitField(fid=FID.IMAGE_LOCATION_Y, length=LEN.IMAGE_LOCATION_Y,
                     title="ImageLocationY", name="image_location_y",
                     checks=(CheckHexList(LEN.IMAGE_LOCATION_Y // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.IMAGE_LOCATION_Y) - 1),)),
            BitField(fid=FID.IMAGE_LOCATION_WIDTH, length=LEN.IMAGE_LOCATION_WIDTH,
                     title="ImageLocationWidth", name="image_location_width",
                     checks=(CheckHexList(LEN.IMAGE_LOCATION_WIDTH // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.IMAGE_LOCATION_WIDTH) - 1),)),
            BitField(fid=FID.IMAGE_LOCATION_HEIGHT, length=LEN.IMAGE_LOCATION_HEIGHT,
                     title="ImageLocationHeight", name="image_location_height",
                     checks=(CheckHexList(LEN.IMAGE_LOCATION_HEIGHT // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.IMAGE_LOCATION_HEIGHT) - 1),)),
            BitField(fid=FID.IMAGE_SIZE, length=LEN.IMAGE_SIZE,
                     title="ImageSize", name="image_size",
                     checks=(CheckHexList(LEN.IMAGE_SIZE // 8),
                             CheckInt(min_value=0, max_value=pow(2, LEN.IMAGE_SIZE) - 1),)),
            BitField(fid=FID.IMAGE_DATA,
                     title="ImageData",
                     name="image_data",
                     aliases=('image_payload',),
                     optional=True),
        )

        @classmethod
        def fromHexList(cls, *args, **kwargs):
            # See ``TimestampedBitFieldContainerMixin.fromHexList``
            data = None
            if 'data' in kwargs:
                data = kwargs['data']
            elif len(args) > 0:
                data = args[0]
            # end if
            inner_field_container_mixin = super().fromHexList(*args, **kwargs)
            inner_field_container_mixin.get_field_from_name('image_data').length = len(data) - cls.LEN.HEADER // 8
            inner_field_container_mixin.image_data = data[cls.LEN.HEADER // 8:]
            return inner_field_container_mixin
        # end def fromHexList
    # end class Image
# end class ContextualDisplay


# noinspection DuplicatedCode
class ContextualDisplayModel(FeatureModel):
    """
    Define ``ContextualDisplay`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_DISPLAY_INFO = 1
        SET_IMAGE = 2
        GET_SUPPORTED_DEVICE_STATES = 3
        SET_DEVICE_STATE = 4
        GET_DEVICE_STATE = 5
        SET_CONFIG = 6
        GET_CONFIG = 7

        # Event index
        BUTTON = 0
        DEVICE_STATE = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ContextualDisplay`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.GET_DISPLAY_INFO: {
                    "request": GetDisplayInfo,
                    "response": GetDisplayInfoResponse
                },
                cls.INDEX.SET_IMAGE: {
                    "request": SetImage,
                    "response": SetImageResponse
                },
                cls.INDEX.GET_SUPPORTED_DEVICE_STATES: {
                    "request": GetSupportedDeviceStates,
                    "response": GetSupportedDeviceStatesResponse
                },
                cls.INDEX.SET_DEVICE_STATE: {
                    "request": SetDeviceState,
                    "response": SetDeviceStateResponse
                },
                cls.INDEX.GET_DEVICE_STATE: {
                    "request": GetDeviceState,
                    "response": GetDeviceStateResponse
                },
                cls.INDEX.SET_CONFIG: {
                    "request": SetConfig,
                    "response": SetConfigResponse
                },
                cls.INDEX.GET_CONFIG: {
                    "request": GetConfig,
                    "response": GetConfigResponse
                }
            },
            "events": {
                cls.INDEX.BUTTON: {"report": ButtonEvent},
                cls.INDEX.DEVICE_STATE: {"report": DeviceStateEvent}
            }
        }

        return {
            "feature_base": ContextualDisplay,
            "versions": {
                ContextualDisplayV0.VERSION: {
                    "main_cls": ContextualDisplayV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class ContextualDisplayModel


class ContextualDisplayFactory(FeatureFactory):
    """
    Get ``ContextualDisplay`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ContextualDisplay`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``ContextualDisplayInterface``
        """
        return ContextualDisplayModel.get_main_cls(version)()
    # end def create
# end class ContextualDisplayFactory


class ContextualDisplayInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ContextualDisplay``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_display_info_cls = None
        self.set_image_cls = None
        self.get_supported_device_states_cls = None
        self.set_device_state_cls = None
        self.get_device_state_cls = None
        self.set_config_cls = None
        self.get_config_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_display_info_response_cls = None
        self.set_image_response_cls = None
        self.get_supported_device_states_response_cls = None
        self.set_device_state_response_cls = None
        self.get_device_state_response_cls = None
        self.set_config_response_cls = None
        self.get_config_response_cls = None

        # Events
        self.button_event_cls = None
        self.device_state_event_cls = None
    # end def __init__
# end class ContextualDisplayInterface


class ContextualDisplayV0(ContextualDisplayInterface):
    """
    Define ``ContextualDisplayV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> deviceScreenCount, maxImageSize, maxImageFps, deviceCapabilities

    [1] getDisplayInfo(displayIdx) -> displayShape, displayDimension, resHorizontal, resVertical, buttonCount,
    visibleAreaCount, button1, button2 ... buttonN, visibleArea1, visibleArea2 ... visibleAreaM

    [2] setImage(displayIdx, setImageFlags, imageCount, image1, image2 ... imageN) -> resultCode, count

    [3] getSupportedDeviceStates() -> deviceState

    [4] setDeviceState(deviceState) -> deviceState

    [5] getDeviceState() -> deviceState

    [6] setConfig(config) -> config

    [7] getConfig() -> config

    [Event 0] ButtonEvent -> displayIndex, buttonIndex

    [Event 1] DeviceStateEvent -> deviceState
    """
    VERSION = 0

    def __init__(self):
        # See ``ContextualDisplay.__init__``
        super().__init__()
        index = ContextualDisplayModel.INDEX

        # Requests
        self.get_capabilities_cls = ContextualDisplayModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_display_info_cls = ContextualDisplayModel.get_request_cls(
            self.VERSION, index.GET_DISPLAY_INFO)
        self.set_image_cls = ContextualDisplayModel.get_request_cls(
            self.VERSION, index.SET_IMAGE)
        self.get_supported_device_states_cls = ContextualDisplayModel.get_request_cls(
            self.VERSION, index.GET_SUPPORTED_DEVICE_STATES)
        self.set_device_state_cls = ContextualDisplayModel.get_request_cls(
            self.VERSION, index.SET_DEVICE_STATE)
        self.get_device_state_cls = ContextualDisplayModel.get_request_cls(
            self.VERSION, index.GET_DEVICE_STATE)
        self.set_config_cls = ContextualDisplayModel.get_request_cls(
            self.VERSION, index.SET_CONFIG)
        self.get_config_cls = ContextualDisplayModel.get_request_cls(
            self.VERSION, index.GET_CONFIG)

        # Responses
        self.get_capabilities_response_cls = ContextualDisplayModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_display_info_response_cls = ContextualDisplayModel.get_response_cls(
            self.VERSION, index.GET_DISPLAY_INFO)
        self.set_image_response_cls = ContextualDisplayModel.get_response_cls(
            self.VERSION, index.SET_IMAGE)
        self.get_supported_device_states_response_cls = ContextualDisplayModel.get_response_cls(
            self.VERSION, index.GET_SUPPORTED_DEVICE_STATES)
        self.set_device_state_response_cls = ContextualDisplayModel.get_response_cls(
            self.VERSION, index.SET_DEVICE_STATE)
        self.get_device_state_response_cls = ContextualDisplayModel.get_response_cls(
            self.VERSION, index.GET_DEVICE_STATE)
        self.set_config_response_cls = ContextualDisplayModel.get_response_cls(
            self.VERSION, index.SET_CONFIG)
        self.get_config_response_cls = ContextualDisplayModel.get_response_cls(
            self.VERSION, index.GET_CONFIG)

        # Events
        self.button_event_cls = ContextualDisplayModel.get_report_cls(
            self.VERSION, index.BUTTON)
        self.device_state_event_cls = ContextualDisplayModel.get_report_cls(
            self.VERSION, index.DEVICE_STATE)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``ContextualDisplayInterface.get_max_function_index``
        return ContextualDisplayModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class ContextualDisplayV0


# noinspection DuplicatedCode
class EmptyVLPPacketDataFormat(ContextualDisplay):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCapabilities
        - GetConfig
        - GetDeviceState
        - GetSupportedDeviceStates
        - SetImageResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       0
    ============================  ==========
    """

    FIELDS = ContextualDisplay.FIELDS
# end class EmptyVLPPacketDataFormat


class DeviceStateFormat(ContextualDisplay):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - DeviceStateEvent
        - GetDeviceStateResponse
        - GetSupportedDeviceStatesResponse
        - SetDeviceStateResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Device State                  8
    ============================  ==========
    """

    class FID(ContextualDisplay.FID):
        # See ``ContextualDisplay.FID``
        DEVICE_STATE = ContextualDisplay.FID.VLP_SEQUENCE_NUMBER - 1
    # end class FID

    class LEN(ContextualDisplay.LEN):
        # See ``ContextualDisplay.LEN``
        DEVICE_STATE = 0x8
    # end class LEN

    FIELDS = ContextualDisplay.FIELDS + (
        BitField(fid=FID.DEVICE_STATE, length=LEN.DEVICE_STATE,
                 title="DeviceState", name="device_state",
                 checks=(CheckHexList(LEN.DEVICE_STATE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_STATE) - 1))),
    )
# end class DeviceStateFormat


class ConfigFormat(ContextualDisplay):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetConfigResponse
        - SetConfigResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Config                        16
    ============================  ==========
    """

    class FID(ContextualDisplay.FID):
        # See ``ContextualDisplay.FID``
        RESERVED = ContextualDisplay.FID.VLP_SEQUENCE_NUMBER - 1
        DEVICE_ADOPTED = RESERVED - 1
    # end class FID

    class LEN(ContextualDisplay.LEN):
        # See ``ContextualDisplay.LEN``
        DEVICE_ADOPTED = 0x1
        RESERVED = 0xF
    # end class LEN

    class DEFAULT(ContextualDisplay.DEFAULT):
        # See ``ContextualDisplay.DEFAULT``
        RESERVED = 0
    # end class DEFAULT

    FIELDS = ContextualDisplay.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 default_value=DEFAULT.RESERVED,
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
        BitField(fid=FID.DEVICE_ADOPTED, length=LEN.DEVICE_ADOPTED,
                 title="Device Adopted", name="device_adopted",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_ADOPTED) - 1),)),
    )
# end class ConfigFormat


class GetCapabilities(EmptyVLPPacketDataFormat):
    """
    Define ``GetCapabilities`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetCapabilitiesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
    # end def __init__
# end class GetCapabilities


class GetDisplayInfo(ContextualDisplay):
    """
    Define ``GetDisplayInfo`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Display Index                 8
    ============================  ==========
    """

    class FID(ContextualDisplay.FID):
        # See ``ContextualDisplay.FID``
        DISPLAY_INDEX = ContextualDisplay.FID.VLP_SEQUENCE_NUMBER - 1
    # end class FID

    class LEN(ContextualDisplay.LEN):
        # See ``ContextualDisplay.LEN``
        DISPLAY_INDEX = 0x8
    # end class LEN

    class DEFAULT(ContextualDisplay.DEFAULT):
        # See ``ContextualDisplay.DEFAULT``
        DISPLAY_INDEX = 1
    # end class DEFAULT

    FIELDS = ContextualDisplay.FIELDS + (
        BitField(fid=FID.DISPLAY_INDEX, length=LEN.DISPLAY_INDEX,
                 title="DisplayIndex", name="display_index",
                 checks=(CheckHexList(LEN.DISPLAY_INDEX // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, display_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param display_index: Display Index
        :type display_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetDisplayInfoResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
        self.display_index = HexList(Numeral(display_index, self.LEN.DISPLAY_INDEX // 8))
    # end def __init__
# end class GetDisplayInfo


class SetImage(VlpMessageRawPayload):
    """
    Define ``SetImage`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    VLP Payload                   Variable length
    ============================  ==========
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         function_index=SetImageResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_EXTENDED_VLP_MESSAGE,
                         **kwargs)
    # end def __init__
# end class SetImage


class SetImagePayloadMixin(BitFieldContainerMixin):
    """
    Parse ``SetImage`` full VLP multi-packet payload

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Display Index                 8
    Reserved                      7
    Image Count                   8
    Image Data                    Variable Length
    ============================  ==========
    """

    class FID:
        """
        Field Lengths in bits
        """
        DISPLAY_INDEX = 0xFF
        RESERVED = DISPLAY_INDEX - 1
        DEFER_DISPLAY_UPDATE = RESERVED - 1
        IMAGE_COUNT = DEFER_DISPLAY_UPDATE - 1
    # end class FID

    class LEN:
        """
        Fields Default values
        """
        DISPLAY_INDEX = 0x8
        DEFER_DISPLAY_UPDATE = 0x1
        RESERVED = 0x7
        IMAGE_COUNT = 0x8
        HEADER = DISPLAY_INDEX + DEFER_DISPLAY_UPDATE + RESERVED + IMAGE_COUNT
    # end class LEN

    FIELDS = (
        BitField(fid=FID.DISPLAY_INDEX, length=LEN.DISPLAY_INDEX,
                 title="DisplayIndex", name="display_index",
                 checks=(CheckHexList(LEN.DISPLAY_INDEX // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ContextualDisplay.DEFAULT.RESERVED),
        BitField(fid=FID.DEFER_DISPLAY_UPDATE, length=LEN.DEFER_DISPLAY_UPDATE,
                 title="DeferDisplayUpdate", name="defer_display_update",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.DEFER_DISPLAY_UPDATE) - 1),),),
        BitField(fid=FID.IMAGE_COUNT, length=LEN.IMAGE_COUNT,
                 title="ImageCount", name="image_count",
                 checks=(CheckHexList(LEN.IMAGE_COUNT // 8), CheckByte(),)),
    )

    def __init__(self, display_index, defer_display_update, image_count, images):
        """
        :param display_index: The index of the display on the device on which this function should apply. 1-indexed,
                              e.g. first display is 0x01. Must be within the range returned by getCapabilities
        :type display_index: ``int|HexList``
        :param defer_display_update: 1: do not update the display. Store images in a buffer for later explicit update,
                                     0: update display immediately with the received images and any previous pending
                                     request
        :type defer_display_update: ``int|bool``
        :param image_count: Count of image records in request. Equals to N. A zero count is allowed.
        :type image_count: ``int|HexList``
        :param images: List of image records
        :type images: ``list[ContextualDisplay.Image]``
        """
        super().__init__(display_index=display_index,
                         defer_display_update=defer_display_update,
                         image_count=image_count)
        for index, image in enumerate(images):
            self.FIELDS += (BitField(fid=self.FID.IMAGE_COUNT - index - 1,
                                     length=len(HexList(image)),
                                     title=f"Image {index}",
                                     name=f"image_{index}",),)
            setattr(self, f"image_{index}", image)
        # end for
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``SetImage``
        """
        data = None
        if 'data' in kwargs:
            data = kwargs['data']
        elif len(args) > 0:
            data = args[0]
        # end if
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        images = data[cls.LEN.HEADER // 8:]

        start_index = 0
        for image_index in range(to_int(inner_field_container_mixin.image_count)):
            image = ContextualDisplay.Image.fromHexList(
                images[start_index:start_index + ContextualDisplay.Image.LEN.HEADER // 8])
            end_index = start_index + ContextualDisplay.Image.LEN.HEADER // 8 + to_int(image.image_size)
            image = ContextualDisplay.Image.fromHexList(images[start_index:end_index])
            inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS + (
                BitField(fid=(cls.FID.IMAGE_COUNT - (1 + image_index)),
                         length=ContextualDisplay.Image.LEN.HEADER + to_int(image.image_size) * 8,
                         title=f"Image {image_index}", name=f"image_{image_index}",
                         checks=(
                             CheckHexList(ContextualDisplay.Image.LEN.HEADER // 8 + to_int(image.image_size)),
                         )),
            )
            setattr(inner_field_container_mixin, f"image_{image_index}", image)
            start_index = end_index
        # end for
        return inner_field_container_mixin
    # end def fromHexList
# end class SetImagePayloadMixin


class GetSupportedDeviceStates(EmptyVLPPacketDataFormat):
    """
    Define ``GetSupportedDeviceStates`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetSupportedDeviceStatesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
    # end def __init__
# end class GetSupportedDeviceStates


class SetDeviceState(DeviceStateFormat):
    """
    Define ``SetDeviceState`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Device State                  8
    ============================  ==========
    """

    def __init__(self, device_index, feature_index, device_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param device_state: Device State
        :type device_state: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetDeviceStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)

        self.device_state = device_state
    # end def __init__
# end class SetDeviceState


class GetDeviceState(DeviceStateFormat):
    """
    Define ``GetDeviceState`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetDeviceStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
    # end def __init__
# end class GetDeviceState


class SetConfig(ConfigFormat):
    """
    Define ``SetConfig`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Config                        16
    ============================  ==========
    """

    def __init__(self, device_index, feature_index, device_adopted, reserved=0, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param device_adopted: Device Adopted
        :type device_adopted: ``bool | HexList``
        :param reserved: Reserved
        :type reserved: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetConfigResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
        self.device_adopted = device_adopted
        self.reserved = reserved
    # end def __init__
# end class SetConfig


class GetConfig(EmptyVLPPacketDataFormat):
    """
    Define ``GetConfig`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetConfigResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
                         **kwargs)
    # end def __init__
# end class GetConfig


class GetCapabilitiesResponse(ContextualDisplay):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Device Screen Count           8
    Max Image Size                16
    Max Image FPS                 8
    Device Capabilities           6
    Reserved                      25
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ContextualDisplay.FID):
        # See ``ContextualDisplay.FID``
        DEVICE_SCREEN_COUNT = ContextualDisplay.FID.VLP_SEQUENCE_NUMBER - 1
        MAX_IMAGE_SIZE = DEVICE_SCREEN_COUNT - 1
        MAX_IMAGE_FPS = MAX_IMAGE_SIZE - 1
        DEVICE_CAPABILITIES = MAX_IMAGE_FPS - 1
    # end class FID

    class LEN(ContextualDisplay.LEN):
        # See ``ContextualDisplay.LEN``
        DEVICE_SCREEN_COUNT = 0x8
        MAX_IMAGE_SIZE = 0x10
        MAX_IMAGE_FPS = 0x8
        DEVICE_CAPABILITIES = 0x20
    # end class LEN

    FIELDS = ContextualDisplay.FIELDS + (
        BitField(fid=FID.DEVICE_SCREEN_COUNT, length=LEN.DEVICE_SCREEN_COUNT,
                 title="DeviceScreenCount", name="device_screen_count",
                 checks=(CheckHexList(LEN.DEVICE_SCREEN_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.MAX_IMAGE_SIZE, length=LEN.MAX_IMAGE_SIZE,
                 title="MaxImageSize", name="max_image_size",
                 checks=(CheckHexList(LEN.MAX_IMAGE_SIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAX_IMAGE_SIZE) - 1),)),
        BitField(fid=FID.MAX_IMAGE_FPS, length=LEN.MAX_IMAGE_FPS,
                 title="MaxImageFps", name="max_image_fps",
                 checks=(CheckHexList(LEN.MAX_IMAGE_FPS // 8), CheckByte(),)),
        BitField(fid=FID.DEVICE_CAPABILITIES, length=LEN.DEVICE_CAPABILITIES,
                 title="DeviceCapabilities", name="device_capabilities",
                 checks=(CheckHexList(LEN.DEVICE_CAPABILITIES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_CAPABILITIES) - 1),)),
    )

    def __init__(self, device_index, feature_index, device_screen_count, max_image_size, max_image_fps,
                 deferrable_display_update_capability, rgb_565, rgb_888, jpeg, calibrated, origin, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param device_screen_count: Device Screen Count
        :type device_screen_count: ``int | HexList``
        :param max_image_size: Max Image Size
        :type max_image_size: ``HexList``
        :param max_image_fps: Max Image FPS
        :type max_image_fps: ``HexList``
        :param deferrable_display_update_capability: Deferrable Display Update Capability
        :type deferrable_display_update_capability: ``bool | HexList``
        :param rgb_565: RGB 565
        :type rgb_565: ``bool | HexList``
        :param rgb_888: RGB 888
        :type rgb_888: ``bool | HexList``
        :param jpeg: JPEG
        :type jpeg: ``bool | HexList``
        :param calibrated: calibrated
        :type calibrated: ``bool | HexList``
        :param origin: origin
        :type origin: ``bool | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_EXTENDED_VLP_MESSAGE,
                         **kwargs)
        self.device_screen_count = HexList(Numeral(device_screen_count, self.LEN.DEVICE_SCREEN_COUNT // 8))
        self.max_image_size = max_image_size
        self.max_image_fps = max_image_fps
        self.device_capabilities = self.DeviceCapabilities(
            deferrable_display_update_capability=deferrable_display_update_capability,
            rgb_565=rgb_565,
            rgb_888=rgb_888,
            jpeg=jpeg,
            calibrated=calibrated,
            origin=origin)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetCapabilitiesResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.device_capabilities = cls.DeviceCapabilities.fromHexList(
            inner_field_container_mixin.device_capabilities)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetCapabilitiesResponse


class GetDisplayInfoResponse(VlpMessageRawPayload):
    """
    Define ``GetDisplayInfoResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Variable payload              Variable length
    ============================  ==========
    """
    FEATURE_ID = ContextualDisplay.FEATURE_ID
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDisplayInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 1
# end class GetDisplayInfoResponse


class GetDisplayInfoResponsePayloadMixin(BitFieldContainerMixin):
    """
    Parse ``GetDisplayInfoResponse`` full multi-packet payload

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Display Shape                 8
    Display Dimension             16
    Horizontal Resolution         16
    Vertical Resolution           16
    Button Count                  8
    Visible Area Count            8
    Button Info 1...N             72 * N
    Visible Area Info 1...M       72 * M
    ============================  ==========
    """
    class FID(ContextualDisplay.FID):
        # See ``ContextualDisplay.FID``
        DISPLAY_SHAPE = 0xFF
        DISPLAY_DIMENSION = DISPLAY_SHAPE - 1
        HORIZONTAL_RESOLUTION = DISPLAY_DIMENSION - 1
        VERTICAL_RESOLUTION = HORIZONTAL_RESOLUTION - 1
        BUTTON_COUNT = VERTICAL_RESOLUTION - 1
        VISIBLE_AREA_COUNT = BUTTON_COUNT - 1
        BUTTON_AND_VISIBLE_AREA_INFO = VISIBLE_AREA_COUNT - 1
    # end class FID

    class LEN(ContextualDisplay.LEN):
        # See ``ContextualDisplay.LEN``
        DISPLAY_SHAPE = 0x8
        DISPLAY_DIMENSION = 0x10
        HORIZONTAL_RESOLUTION = 0x10
        VERTICAL_RESOLUTION = 0x10
        BUTTON_COUNT = 0x8
        VISIBLE_AREA_COUNT = 0x8
        BUTTON_INFO = 9 * 8
        VISIBLE_AREA_INFO = 9 * 8
    # end class LEN

    FIELDS = (
        BitField(fid=FID.DISPLAY_SHAPE, length=LEN.DISPLAY_SHAPE,
                 title="DisplayShape", name="display_shape",
                 checks=(CheckHexList(LEN.DISPLAY_SHAPE // 8), CheckByte(),)),
        BitField(fid=FID.DISPLAY_DIMENSION, length=LEN.DISPLAY_DIMENSION,
                 title="DisplayDimension", name="display_dimension",
                 checks=(CheckHexList(LEN.DISPLAY_DIMENSION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DISPLAY_DIMENSION) - 1),)),
        BitField(fid=FID.HORIZONTAL_RESOLUTION, length=LEN.HORIZONTAL_RESOLUTION,
                 title="HorizontalResolution", name="horizontal_resolution",
                 checks=(CheckHexList(LEN.HORIZONTAL_RESOLUTION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HORIZONTAL_RESOLUTION) - 1),)),
        BitField(fid=FID.VERTICAL_RESOLUTION, length=LEN.VERTICAL_RESOLUTION,
                 title="VerticalResolution", name="vertical_resolution",
                 checks=(CheckHexList(LEN.VERTICAL_RESOLUTION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.VERTICAL_RESOLUTION) - 1),)),
        BitField(fid=FID.BUTTON_COUNT, length=LEN.BUTTON_COUNT,
                 title="ButtonCount", name="button_count",
                 checks=(CheckHexList(LEN.BUTTON_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.VISIBLE_AREA_COUNT, length=LEN.VISIBLE_AREA_COUNT,
                 title="VisibleAreaCount", name="visible_area_count",
                 checks=(CheckHexList(LEN.VISIBLE_AREA_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.BUTTON_AND_VISIBLE_AREA_INFO,
                 title="ButtonAndVisibleAreaInfo",
                 name="button_and_visible_area_info",),
    )

    def __init__(self, display_shape, display_dimension, horizontal_resolution,
                 vertical_resolution, button_count, visible_area_count, **kwargs):
        """
        :param display_shape: Display Shape
        :type display_shape: ``HexList``
        :param display_dimension: Display Dimension
        :type display_dimension: ``HexList``
        :param horizontal_resolution: Horizontal Resolution
        :type horizontal_resolution: ``HexList``
        :param vertical_resolution: Vertical Resolution
        :type vertical_resolution: ``HexList``
        :param button_count: Button Count
        :type button_count: ``int | HexList``
        :param visible_area_count: Visible Area Count
        :type visible_area_count: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(**kwargs)

        self.display_shape = display_shape
        self.display_dimension = display_dimension
        self.horizontal_resolution = horizontal_resolution
        self.vertical_resolution = vertical_resolution
        self.button_count = HexList(Numeral(button_count, self.LEN.BUTTON_COUNT // 8))
        self.visible_area_count = HexList(Numeral(visible_area_count, self.LEN.VISIBLE_AREA_COUNT // 8))
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetDisplayInfoResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        button_count = int(Numeral(inner_field_container_mixin.button_count))
        visible_area_count = int(Numeral(inner_field_container_mixin.visible_area_count))
        inner_field_container_mixin.get_field_from_name('button_and_visible_area_info').length = (
                button_count * cls.LEN.BUTTON_INFO + visible_area_count * cls.LEN.VISIBLE_AREA_INFO)
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        button_and_visible_area_info = inner_field_container_mixin.button_and_visible_area_info.copy()
        # Delete the button_and_visible_area_info from FIELDS
        inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS[:-1]

        for button_index in range(button_count):
            inner_field_container_mixin.FIELDS += (
                BitField(fid=(cls.FID.VISIBLE_AREA_COUNT - (1 + button_index)),
                         length=ContextualDisplay.ButtonInfo.BUTTON_INFO_LENGTH,
                         title=f"Button Info {button_index}", name=f"button_info_{button_index}",
                         checks=(CheckHexList(ContextualDisplay.ButtonInfo.BUTTON_INFO_LENGTH // 8),)),
            )
            start_index = (button_index * int(ContextualDisplay.ButtonInfo.BUTTON_INFO_LENGTH)) // 8
            end_index = ((button_index + 1) * int(ContextualDisplay.ButtonInfo.BUTTON_INFO_LENGTH)) // 8
            value = ContextualDisplay.ButtonInfo.fromHexList(button_and_visible_area_info[start_index:end_index])
            setattr(inner_field_container_mixin, "button_info_" + str(button_index), value)
        # end for
        for visual_area_index in range(visible_area_count):
            inner_field_container_mixin.FIELDS += (
                BitField(fid=(cls.FID.VISIBLE_AREA_COUNT - (1 + button_count + visual_area_index)),
                         length=ContextualDisplay.VisibleAreaInfo.VISIBLE_AREA_INFO_LENGTH,
                         title=f"Visible Area Info {visual_area_index}", name=f"visible_area_info_{visual_area_index}",
                         checks=(CheckHexList(ContextualDisplay.VisibleAreaInfo.VISIBLE_AREA_INFO_LENGTH // 8),)),
            )
            start_index = ((button_count + int(ContextualDisplay.ButtonInfo.BUTTON_INFO_LENGTH)) +
                           (visual_area_index * int(ContextualDisplay.VisibleAreaInfo.VISIBLE_AREA_INFO_LENGTH))) // 8
            end_index = (((button_count + int(ContextualDisplay.ButtonInfo.BUTTON_INFO_LENGTH)) +
                         ((visual_area_index + 1) * int(ContextualDisplay.VisibleAreaInfo.VISIBLE_AREA_INFO_LENGTH)))
                         // 8)
            value = ContextualDisplay.VisibleAreaInfo.fromHexList(button_and_visible_area_info[start_index:end_index])
            setattr(inner_field_container_mixin, "visible_area_info_" + str(visual_area_index), value)
        # end for
        return inner_field_container_mixin
    # end def fromHexList
# end class GetDisplayInfoResponsePayloadMixin


class SetImageResponse(ContextualDisplay):
    """
    Define ``SetImageResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Result Code                   8
    Count                         8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetImage,)
    VERSION = (0,)
    FUNCTION_INDEX = 2
    # result codes
    DISPLAY_UPDATED = 0x00
    BUFFERED_NOT_VISIBLE = 0x01
    UNSUPPORTED_IMAGE_RESOLUTION = 0x80
    UNSUPPORTED_IMAGE_FORMAT = 0x81
    JPEG_PARSER_ERROR = 0x82
    EMPTY_BUFFER = 0x83
    UNSUPPORTED_DEVICE_STATE = 0x84

    class FID(ContextualDisplay.FID):
        # See ``ContextualDisplay.FID``
        RESULT_CODE = ContextualDisplay.FID.VLP_SEQUENCE_NUMBER - 1
        COUNT = RESULT_CODE - 1
    # end class FID

    class LEN(ContextualDisplay.LEN):
        # See ``ContextualDisplay.LEN``
        RESULT_CODE = 0x8
        COUNT = 0x8
    # end class LEN

    FIELDS = ContextualDisplay.FIELDS + (
        BitField(fid=FID.RESULT_CODE, length=LEN.RESULT_CODE,
                 title="ResultCode", name="result_code",
                 checks=(CheckHexList(LEN.RESULT_CODE // 8), CheckByte(),)),
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, result_code, count, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param result_code: Result Code
        :type result_code: ``HexList``
        :param count: Count
        :type count: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_EXTENDED_VLP_MESSAGE,
                         **kwargs)

        self.result_code = result_code
        self.count = count
    # end def __init__
# end class SetImageResponse


class GetSupportedDeviceStatesResponse(VlpMessageRawPayload):
    """
    Define ``GetSupportedDeviceStatesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Device State[N]               8 * N
    ============================  ==========
    """
    FEATURE_ID = ContextualDisplay.FEATURE_ID
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSupportedDeviceStates,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetSupportedDeviceStatesResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        device_state_list = inner_field_container_mixin.vlp_payload.copy()
        # Delete the device_state_list from FIELDS
        inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS[:-1]
        while device_state_list[-1] == 0:
            device_state_list = device_state_list[:-1]
        # end while
        for state_index in range(len(device_state_list)):
            inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS + (
                BitField(fid=(cls.FID.VLP_SEQUENCE_NUMBER - (1 + state_index)),
                         length=ContextualDisplay.DeviceStateInfo.LEN.DEVICE_STATE,
                         title=f"Device State {state_index}", name=f"device_state_{state_index}",
                         checks=(CheckHexList(ContextualDisplay.DeviceStateInfo.LEN.DEVICE_STATE // 8),)),
            )
            start_index = (state_index * int(ContextualDisplay.DeviceStateInfo.LEN.DEVICE_STATE)) // 8
            end_index = ((state_index + 1) * int(ContextualDisplay.DeviceStateInfo.LEN.DEVICE_STATE)) // 8
            value = ContextualDisplay.DeviceStateInfo.fromHexList(device_state_list[start_index:end_index])
            inner_field_container_mixin.__setattr__("device_state_" + str(state_index), value)
        # end for
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSupportedDeviceStatesResponse


class SetDeviceStateResponse(DeviceStateFormat):
    """
    Define ``SetDeviceStateResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Device State                  8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDeviceState,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, device_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param device_state: Device State
        :type device_state: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_EXTENDED_VLP_MESSAGE,
                         **kwargs)

        self.device_state = device_state
    # end def __init__
# end class SetDeviceStateResponse


class GetDeviceStateResponse(DeviceStateFormat):
    """
    Define ``GetDeviceStateResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Device State                  8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDeviceState,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, device_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param device_state: Device State
        :type device_state: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_EXTENDED_VLP_MESSAGE,
                         **kwargs)

        self.device_state = device_state
    # end def __init__
# end class GetDeviceStateResponse


class SetConfigResponse(ConfigFormat):
    """
    Define ``SetConfigResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Config                        16
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetConfig,)
    VERSION = (0,)
    FUNCTION_INDEX = 6

    def __init__(self, device_index, feature_index, device_adopted, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param device_adopted: Device Adopted
        :type device_adopted: ``bool | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_EXTENDED_VLP_MESSAGE,
                         **kwargs)
        self.device_adopted = device_adopted
    # end def __init__
# end class SetConfigResponse


class GetConfigResponse(ConfigFormat):
    """
    Define ``GetConfigResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Config                        16
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetConfig,)
    VERSION = (0,)
    FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index, device_adopted, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param device_adopted: Device Adopted
        :type device_adopted: ``bool | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_EXTENDED_VLP_MESSAGE,
                         **kwargs)
        self.device_adopted = device_adopted
    # end def __init__
# end class GetConfigResponse


class ButtonEvent(VlpMessageRawPayload):
    """
    Define ``ButtonEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Display Index                 8
    Button Index                  8
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FEATURE_ID = 0x19A1
    FUNCTION_INDEX = 0

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``ButtonEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        button_list = inner_field_container_mixin.vlp_payload.copy()
        # Delete the device_state_list from FIELDS
        inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS[:-1]
        while button_list[-1] == 0:
            button_list = button_list[:-1]
        # end while

        # add padding at the end to validate Break event
        button_list.append(0)
        inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS + (
            BitField(fid=(cls.FID.VLP_SEQUENCE_NUMBER - 1),
                     length=ContextualDisplay.ButtonEventInfo.LEN.DISPLAY_INDEX,
                     title="DisplayIndex", name="display_index",
                     checks=(CheckHexList(ContextualDisplay.ButtonEventInfo.LEN.DISPLAY_INDEX // 8),)),
        )

        # display index byte field
        display_index = button_list.pop(0)
        inner_field_container_mixin.__setattr__("display_index", HexList(display_index))

        for button_index in range(len(button_list)):
            inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS + (
                BitField(
                    fid=(cls.FID.VLP_SEQUENCE_NUMBER - (2 + button_index)),
                    length=int(ContextualDisplay.ButtonEventInfo.LEN.BUTTON_INDEX),
                    title=f"Button Index {button_index}", name=f"button_index_{button_index}",
                    checks=(CheckHexList(int(ContextualDisplay.ButtonEventInfo.LEN.BUTTON_INDEX) // 8),)),
            )
            start_index = (button_index * int(ContextualDisplay.ButtonEventInfo.LEN.BUTTON_INDEX)) // 8
            end_index = ((button_index + 1) * int(ContextualDisplay.ButtonEventInfo.LEN.BUTTON_INDEX)) // 8
            value = ContextualDisplay.ButtonEventInfo.fromHexList(button_list[start_index:end_index])
            inner_field_container_mixin.__setattr__("button_index_" + str(button_index), value)
        # end for
        return inner_field_container_mixin
    # end def fromHexList
# end class ButtonEvent


class DeviceStateEvent(DeviceStateFormat):
    """
    Define ``DeviceStateEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Device State                  8
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, device_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param device_state: Device State
        :type device_state: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_EXTENDED_VLP_MESSAGE,
                         **kwargs)

        self.device_state = device_state
    # end def __init__
# end class DeviceStateEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
