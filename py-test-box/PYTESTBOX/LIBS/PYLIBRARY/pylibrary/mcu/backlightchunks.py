#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.backlightchunks
:brief: Backlight NVS chunk definition
:author: Anil Gadad <agadad@logitech.com>
:date: 2022/02/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckInt
from pyhid.field import CheckHexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BacklightChunk(BitFieldContainerMixin):
    """
    Define the format of the NVS_LEDBKLT_ID chunk
    {
        uint8_t status;
        uint8_t options;
        uint8_t level;
        uint8_t effect
    } bctrl_bkltCtrl_ts;
    """

    class LEN:
        """
        Field Lengths in bits
        """
        CONFIGURATION = 0x08
        OPTIONS = 0x08
        CURRENT_BACKLIGHT_LEVEL = 0x08
        BACKLIGHT_EFFECT = 0x08
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        CONFIGURATION = 0xFF
        OPTIONS = CONFIGURATION - 1
        CURRENT_BACKLIGHT_LEVEL = OPTIONS - 1
        BACKLIGHT_EFFECT = CURRENT_BACKLIGHT_LEVEL - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.CONFIGURATION,
            length=LEN.CONFIGURATION,
            title='Configuration',
            name='configuration',
            checks=(CheckHexList(LEN.CONFIGURATION // 8), CheckByte(),), ),
        BitField(
            fid=FID.OPTIONS,
            length=LEN.OPTIONS,
            title='Options',
            name='options',
            checks=(CheckHexList(LEN.OPTIONS // 8), CheckByte(),), ),
        BitField(
            fid=FID.CURRENT_BACKLIGHT_LEVEL,
            length=LEN.CURRENT_BACKLIGHT_LEVEL,
            title='CurrentBacklightLevel',
            name='current_backlight_level',
            checks=(CheckHexList(LEN.CURRENT_BACKLIGHT_LEVEL // 8), CheckByte(),), ),
        BitField(
            fid=FID.BACKLIGHT_EFFECT,
            length=LEN.BACKLIGHT_EFFECT,
            title='BacklightEffect',
            name='backlight_effect',
            checks=(CheckHexList(LEN.BACKLIGHT_EFFECT // 8), CheckByte(),), ),
    )

    def __init__(self, configuration, options, current_backlight_level, backlight_effect, ref=None, **kwargs):
        """
        :param configuration: Flag enabling the backlight
        :type configuration: ``int`` or ``HexList``
        :param options: Flag enabling pwrSave, crown and wow effect
        :type options: ``int`` or ``HexList``
        :param current_backlight_level: Backlight level
        :type current_backlight_level: ``int`` or ``HexList``
        :param backlight_effect: Setting up backlight effect
        :type backlight_effect: ``int`` or ``HexList``
        :param ref: Chunk object provided by the NvsParser
        :type ref: ``NvsChunk``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.configuration = configuration
        self.options = options
        self.current_backlight_level = current_backlight_level
        self.backlight_effect = backlight_effect
    # end def __init__
# end class BacklightChunk


class BacklightChunkV3(BacklightChunk):
    """
    Define the format of the NVS_LEDBKLT_ID chunk
    typedef struct
    {
        uint8_t  configuration;
        uint8_t  options;
        uint8_t  backlightEffect;
        uint8_t  currentBacklightLevel;
        uint16_t currDurationHandsOUT;
        uint16_t currDurationHandsIN;
        uint16_t currDurationPowered;
    } x1982_bkltNvmSettings_ts;
    """

    class LEN(BacklightChunk.LEN):
        # See ``BacklightChunk.LEN``
        CURR_DURATION_HANDS_OUT = 0x10
        CURR_DURATION_HANDS_IN = 0x10
        CURR_DURATION_POWERED = 0x10
    # end class LEN

    class FID(BacklightChunk.FID):
        # See ``BacklightChunk.FID``
        BACKLIGHT_EFFECT = BacklightChunk.FID.OPTIONS - 1
        CURRENT_BACKLIGHT_LEVEL = BACKLIGHT_EFFECT - 1
        CURR_DURATION_HANDS_OUT = CURRENT_BACKLIGHT_LEVEL - 1
        CURR_DURATION_HANDS_IN = CURR_DURATION_HANDS_OUT - 1
        CURR_DURATION_POWERED = CURR_DURATION_HANDS_IN - 1
    # end class FID

    FIELDS = BacklightChunk.FIELDS[:-2] + (
        BitField(fid=FID.BACKLIGHT_EFFECT, length=LEN.BACKLIGHT_EFFECT,
                 title='BacklightEffect', name='backlight_effect',
                 checks=(CheckHexList(LEN.BACKLIGHT_EFFECT // 8), CheckByte(),), ),
        BitField(fid=FID.CURRENT_BACKLIGHT_LEVEL, length=LEN.CURRENT_BACKLIGHT_LEVEL,
                 title='CurrentBacklightLevel', name='current_backlight_level',
                 checks=(CheckHexList(LEN.CURRENT_BACKLIGHT_LEVEL // 8), CheckByte(),), ),
        BitField(fid=FID.CURR_DURATION_HANDS_OUT, length=LEN.CURR_DURATION_HANDS_OUT,
                 title="CurrDurationHandsOut", name="curr_duration_hands_out",
                 checks=(CheckHexList(LEN.CURR_DURATION_HANDS_OUT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_HANDS_OUT) - 1),)),
        BitField(fid=FID.CURR_DURATION_HANDS_IN, length=LEN.CURR_DURATION_HANDS_IN,
                 title="CurrDurationHandsIn", name="curr_duration_hands_in",
                 checks=(CheckHexList(LEN.CURR_DURATION_HANDS_IN // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_HANDS_IN) - 1),)),
        BitField(fid=FID.CURR_DURATION_POWERED, length=LEN.CURR_DURATION_POWERED,
                 title="CurrDurationPowered", name="curr_duration_powered",
                 checks=(CheckHexList(LEN.CURR_DURATION_POWERED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_DURATION_POWERED) - 1),)),
    )

    def __init__(self, configuration, options, current_backlight_level, backlight_effect, curr_duration_hands_out,
                 curr_duration_hands_in, curr_duration_powered, ref=None, **kwargs):
        """
        :param configuration: Flag enabling the backlight
        :type configuration: ``int`` or ``HexList``
        :param options: Flag enabling pwrSave, crown and wow effect
        :type options: ``int`` or ``HexList``
        :param current_backlight_level: Backlight level
        :type current_backlight_level: ``int`` or ``HexList``
        :param backlight_effect: Setting up backlight effect
        :type backlight_effect: ``int`` or ``HexList``
        :param curr_duration_hands_out: The needed time to start the FADE-OUT effect after the last keystroke and
                                        no proximity detection.
        :type curr_duration_hands_out: ``int`` or ``HexList``
        :param curr_duration_hands_in: The needed time to start the FADE-OUT effect after the last interaction with
                                       the device while keeping the object/hands in the detection zone.
        :type curr_duration_hands_in: ``int`` or ``HexList``
        :param curr_duration_powered: The needed time to start the FADE-OUT effect after the last interaction with
                                      a device externally powered.
        :type curr_duration_powered: ``int`` or ``HexList``
        :param ref: Chunk object provided by the NvsParser
        :type ref: ``NvsChunk``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(configuration=configuration, options=options, current_backlight_level=current_backlight_level,
                         backlight_effect=backlight_effect, ref=ref, **kwargs)

        # Parameters initialization
        self.curr_duration_hands_out = curr_duration_hands_out
        self.curr_duration_hands_in = curr_duration_hands_in
        self.curr_duration_powered = curr_duration_powered
    # end def __init__
# end class BacklightChunkV3

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
