#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.config.keybaordlayout
:brief: Keyboard key layout definition per product
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.emulator.keybaordlayout import LAYOUT_MAX_COUNT
from pyraspi.services.kosmos.config.keymatrix.boston import BostonKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.boston import BostonMacKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.chengdu import ChengduJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.chengdu import ChengduKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.chengdu import ChengduUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.cinderellatkl import CinderellaJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.cinderellatkl import CinderellaKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.cinderellatkl import CinderellaUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.cortado import CortadoForAppleJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.cortado import CortadoForAppleKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.cortado import CortadoForAppleUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.cortado import CortadoJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.cortado import CortadoKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.cortado import CortadoUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.devboard import DevBoardIso104LayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.devboard import DevBoardIso105LayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.devboard import DevBoardIso107LayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.devboard import DevBoardJis109LayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.devboard import DevBoardKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.foster import FosterBLEPROKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.fostermini import FosterMiniForMacKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.fostermini import FosterMiniKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.fujian98 import Fujian98KeyMatrix
from pyraspi.services.kosmos.config.keymatrix.galvatrontkl import GalvatronTklBraLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.galvatrontkl import GalvatronTklJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.galvatrontkl import GalvatronTklKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.galvatrontkl import GalvatronTklRusLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.galvatrontkl import GalvatronTklUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.gansu import GansuBLEPROKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.harpy2 import Harpy2JpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.harpy2 import Harpy2KeyMatrix
from pyraspi.services.kosmos.config.keymatrix.honolulu import HonoluluBLEPROKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.hospoa import HospoaJpnLayoutMT8816SetupKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.hospoa import HospoaKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.hospoa import HospoaMT8816SetupKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.hospoa import HospoaUkLayoutMT8816SetupKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.inga import IngaJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.inga import IngaKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.inga import IngaUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.ingacs import IngaCSKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.ingacs import IngaCSMacJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.ingacs import IngaCSMacKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.ingacs import IngaCSMacUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.jilin import JilinWirelessKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nami import NamiForMacJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nami import NamiForMacKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nami import NamiForMacUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nami import NamiJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nami import NamiKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nami import NamiUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nerv import NervJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nerv import NervJpnLayoutMT8816SetupKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nerv import NervKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nerv import NervMT8816SetupKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nerv import NervRusLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nerv import NervRusLayoutMT8816SetupKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nerv import NervUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.nerv import NervUkLayoutMT8816SetupKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.norman import NormanForMacKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.norman import NormanKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.pamir import PamirJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.pamir import PamirKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.pamir import PamirUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.rangoon import RangoonBLEProKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.slim_plus import SlimPlusJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.slim_plus import SlimPlusKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.slim_plus import SlimPlusUkLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.topaztkl import TopazTklCordedKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.topaztkl import TopazTklKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.yoko import YokoBLEPROJpnLayoutKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.yoko import YokoBLEPROKeyMatrix
from pyraspi.services.kosmos.config.keymatrix.yoko import YokoBLEPROUkLayoutKeyMatrix

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
GET_KEYBOARD_LAYOUT_BY_ID = {
    'HAD02': [DevBoardKeyMatrix, DevBoardIso104LayoutKeyMatrix, DevBoardIso105LayoutKeyMatrix,
              DevBoardIso107LayoutKeyMatrix, DevBoardJis109LayoutKeyMatrix],
    'MPO03': [DevBoardKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'MPK17': [TopazTklKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'MPK20': [HospoaKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'MPK20_MT8816': [HospoaMT8816SetupKeyMatrix, HospoaMT8816SetupKeyMatrix, HospoaUkLayoutMT8816SetupKeyMatrix,
                     HospoaMT8816SetupKeyMatrix, HospoaJpnLayoutMT8816SetupKeyMatrix],
    'MPK22': [NervKeyMatrix, NervRusLayoutKeyMatrix, NervUkLayoutKeyMatrix, NervKeyMatrix, NervJpnLayoutKeyMatrix],
    'MPK22_MT8816': [NervMT8816SetupKeyMatrix, NervRusLayoutMT8816SetupKeyMatrix, NervUkLayoutMT8816SetupKeyMatrix,
                     NervMT8816SetupKeyMatrix, NervJpnLayoutMT8816SetupKeyMatrix],
    'MPK25': [CinderellaKeyMatrix, CinderellaKeyMatrix, CinderellaUkLayoutKeyMatrix, CinderellaKeyMatrix,
              CinderellaJpnLayoutKeyMatrix],
    'MPK26': [Harpy2KeyMatrix, Harpy2KeyMatrix, Harpy2KeyMatrix, Harpy2KeyMatrix, Harpy2JpnLayoutKeyMatrix],
    'RBK68': [FosterBLEPROKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK69': [GansuBLEPROKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK70': [HonoluluBLEPROKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK71': [IngaKeyMatrix, IngaKeyMatrix, IngaUkLayoutKeyMatrix, IngaKeyMatrix, IngaJpnLayoutKeyMatrix],
    'RBK72': [IngaCSKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK73': [FosterMiniKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK74': [FosterMiniForMacKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK75': [IngaCSMacKeyMatrix, IngaCSMacKeyMatrix, IngaCSMacUkLayoutKeyMatrix, IngaCSMacKeyMatrix,
              IngaCSMacJpnLayoutKeyMatrix],
    'RBK76': [RangoonBLEProKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK77': [JilinWirelessKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK78': [YokoBLEPROKeyMatrix, YokoBLEPROKeyMatrix, YokoBLEPROUkLayoutKeyMatrix, YokoBLEPROKeyMatrix,
              YokoBLEPROJpnLayoutKeyMatrix],
    'RBK81': [NormanKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK82': [NormanForMacKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK85': [PamirKeyMatrix, PamirKeyMatrix, PamirUkLayoutKeyMatrix, PamirKeyMatrix, PamirJpnLayoutKeyMatrix],
    'RBK88': [NamiKeyMatrix, NamiKeyMatrix, NamiUkLayoutKeyMatrix, NamiKeyMatrix, NamiJpnLayoutKeyMatrix],
    'RBK89': [NamiForMacKeyMatrix, NamiForMacKeyMatrix, NamiForMacUkLayoutKeyMatrix, NamiForMacKeyMatrix,
              NamiForMacJpnLayoutKeyMatrix],
    'RBK90': [SlimPlusKeyMatrix, SlimPlusKeyMatrix, SlimPlusUkLayoutKeyMatrix, SlimPlusKeyMatrix,
              SlimPlusJpnLayoutKeyMatrix],
    'RBK91': [BostonKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK92': [CortadoKeyMatrix, CortadoKeyMatrix, CortadoUkLayoutKeyMatrix, CortadoKeyMatrix,
              CortadoJpnLayoutKeyMatrix],
    'RBK93': [Fujian98KeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBK94': [CortadoForAppleKeyMatrix, CortadoForAppleKeyMatrix, CortadoForAppleUkLayoutKeyMatrix,
              CortadoForAppleKeyMatrix, CortadoForAppleJpnLayoutKeyMatrix],
    'RBK95': [ChengduKeyMatrix, ChengduKeyMatrix, ChengduUkLayoutKeyMatrix, ChengduKeyMatrix,
              ChengduJpnLayoutKeyMatrix],
    'RBK96': [BostonMacKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'RBO03': [IngaKeyMatrix, IngaKeyMatrix, IngaUkLayoutKeyMatrix, IngaKeyMatrix, IngaJpnLayoutKeyMatrix],
    'U158':  [TopazTklCordedKeyMatrix for _ in range(LAYOUT_MAX_COUNT)],
    'U170': [GalvatronTklKeyMatrix, GalvatronTklRusLayoutKeyMatrix, GalvatronTklUkLayoutKeyMatrix,
             GalvatronTklBraLayoutKeyMatrix, GalvatronTklJpnLayoutKeyMatrix],
}

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
