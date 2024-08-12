#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Kosmos Generator
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.kosmosio
:brief: Kosmos Input/Output hardware
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/03/17
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from enum import unique

from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_A
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_B
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_C
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_D
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_E
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_F
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_G
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_H


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosIO(object):
    """
    Kosmos Input/Output hardware allocation.
    """
    @unique
    class BUTTONS(IntEnum):
        """
        Kosmos Buttons identifiers
        """
        # Values of sliders identifiers and buttons identifiers must be different to facilitate the differentiation
        # between both on a list when using 'in'
        BUTTON_0 = 0
        BUTTON_1 = auto()
        BUTTON_2 = auto()
        BUTTON_3 = auto()
        BUTTON_4 = auto()
        BUTTON_5 = auto()
        BUTTON_6 = auto()
        BUTTON_7 = auto()
    # end class BUTTONS

    @unique
    class SLIDERS(IntEnum):
        """
        Kosmos Sliders identifiers
        """
        # Values of sliders identifiers and buttons identifiers must be different to facilitate the differentiation
        # between both on a list when using 'in'
        SLIDER_0 = 8
        SLIDER_1 = auto()
        SLIDER_2 = auto()
        SLIDER_3 = auto()
    # end class SLIDERS

    @unique
    class LEDS(IntEnum):
        """
        Kosmos LEDs identifiers
        """
        LED_0 = 0
        LED_1 = auto()
        LED_2 = auto()
        LED_3 = auto()
        LED_4 = auto()
        LED_5 = auto()
        LED_6 = auto()
        LED_7 = auto()
        LED_8 = auto()
        LED_9 = auto()
        LED_10 = auto()
        LED_11 = auto()
        LED_12 = auto()
        LED_13 = auto()
        LED_14 = auto()
        LED_15 = auto()
        LED_16 = auto()
        LED_17 = auto()
        LED_18 = auto()
        LED_19 = auto()
        LED_20 = auto()
        LED_21 = auto()
        LED_22 = auto()
        LED_23 = auto()
        LED_24 = auto()
        LED_25 = auto()
        LED_26 = auto()
        LED_27 = auto()
        LED_28 = auto()
        LED_29 = auto()
        LED_30 = auto()
        LED_31 = auto()
    # end class LEDS
# end class KosmosIO


# Mapping between Kosmos LEDs identifiers and DAC2 channels used as input voltage thresholds in Kosmos LED-spy module
KOSMOS_LEDS_TO_CHANNELS_DAC2_MAP = {
    KosmosIO.LEDS.LED_0: ADDA_DAC_CH_A,
    KosmosIO.LEDS.LED_1: ADDA_DAC_CH_A,
    KosmosIO.LEDS.LED_2: ADDA_DAC_CH_A,
    KosmosIO.LEDS.LED_3: ADDA_DAC_CH_A,
    KosmosIO.LEDS.LED_4: ADDA_DAC_CH_B,
    KosmosIO.LEDS.LED_5: ADDA_DAC_CH_B,
    KosmosIO.LEDS.LED_6: ADDA_DAC_CH_B,
    KosmosIO.LEDS.LED_7: ADDA_DAC_CH_B,
    KosmosIO.LEDS.LED_8: ADDA_DAC_CH_C,
    KosmosIO.LEDS.LED_9: ADDA_DAC_CH_C,
    KosmosIO.LEDS.LED_10: ADDA_DAC_CH_C,
    KosmosIO.LEDS.LED_11: ADDA_DAC_CH_C,
    KosmosIO.LEDS.LED_12: ADDA_DAC_CH_D,
    KosmosIO.LEDS.LED_13: ADDA_DAC_CH_D,
    KosmosIO.LEDS.LED_14: ADDA_DAC_CH_D,
    KosmosIO.LEDS.LED_15: ADDA_DAC_CH_D,
    KosmosIO.LEDS.LED_16: ADDA_DAC_CH_E,
    KosmosIO.LEDS.LED_17: ADDA_DAC_CH_E,
    KosmosIO.LEDS.LED_18: ADDA_DAC_CH_E,
    KosmosIO.LEDS.LED_19: ADDA_DAC_CH_E,
    KosmosIO.LEDS.LED_20: ADDA_DAC_CH_F,
    KosmosIO.LEDS.LED_21: ADDA_DAC_CH_F,
    KosmosIO.LEDS.LED_22: ADDA_DAC_CH_F,
    KosmosIO.LEDS.LED_23: ADDA_DAC_CH_F,
    KosmosIO.LEDS.LED_24: ADDA_DAC_CH_G,
    KosmosIO.LEDS.LED_25: ADDA_DAC_CH_G,
    KosmosIO.LEDS.LED_26: ADDA_DAC_CH_G,
    KosmosIO.LEDS.LED_27: ADDA_DAC_CH_G,
    KosmosIO.LEDS.LED_28: ADDA_DAC_CH_H,
    KosmosIO.LEDS.LED_29: ADDA_DAC_CH_H,
    KosmosIO.LEDS.LED_30: ADDA_DAC_CH_H,
    KosmosIO.LEDS.LED_31: ADDA_DAC_CH_H,
}
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
