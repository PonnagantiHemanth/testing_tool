""" @package pylibrary.tools.chunkidmaps

@brief CRC classes

@author Stanislas Cottard

@date   2019/10/17
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Crc16ccitt:
    DEFAULT_PRESET = 0xFFFF
    DEFAULT_POLYNOMIAL = 0x1021

    def __init__(self, polynomial=DEFAULT_POLYNOMIAL, preset=DEFAULT_PRESET):
        self._tab = []  # This attribute will be set when self.polynomial is set on the next line
        self.polynomial = polynomial
        self.preset = preset
        self.crc = preset
    # end def __init__

    @property
    def polynomial(self):
        return self.__polynomial
    # end getter def polynomial

    @polynomial.setter
    def polynomial(self, value):
        self.__polynomial = value
        self._tab = [self._initial(i) for i in range(256)]
    # end setter def polynomial

    def _initial(self, c):
        crc = 0
        c = c << 8
        for j in range(8):
            if (crc ^ c) & 0x8000:
                crc = (crc << 1) ^ self.polynomial
            else:
                crc = crc << 1
            # end if
            c = c << 1
        # end for
        return crc
    # end setter def _initial

    def _compute_crc(self, array_to_parse):
        for c in array_to_parse:
            if isinstance(c, str):
                c = ord(c)
            # end if
            cc = 0xff & c

            tmp = (self.crc >> 8) ^ cc
            self.crc = (self.crc << 8) ^ self._tab[tmp & 0xff]
            self.crc = self.crc & 0xffff
        # end for
    # end def _compute_crc

    def start_crc(self, array_to_parse):
        self.crc = self.preset
        self._compute_crc(array_to_parse)
    # end def start_crc

    def continue_crc(self, array_to_parse):
        self._compute_crc(array_to_parse)
    # end def continue_crc
# end class Crc16ccitt


class Crc32Stm32:
    """
    Implement the CRC 32 algo integrated in the STM32 chipset
    """
    DEFAULT_POLYNOMIAL = 0x04C11DB7
    DEFAULT_INIT_VALUE = 0xFFFFFFFF
    INPUT_DATA_WORD_SIZE = 4  # Enter 32-bit input data to the CRC calculator

    def __init__(self, init_value=DEFAULT_INIT_VALUE, polynomial=DEFAULT_POLYNOMIAL):
        """
        :param init_value: Init value - OPTIONAL
        :type init_value: ``int``
        :param polynomial: Polynomial - OPTIONAL
        :type polynomial: ``int``
        """
        self.polynomial = polynomial
        self.init_value = init_value
        self.crc_table = {}
        self.generate_crc32_table()
    # end def __init__

    @classmethod
    def sort_data(cls, data):
        """
        Sort data in a list of reversed words

        :param data: Data to sort
        :type data: ``HexList``

        :return: Sorted data
        :rtype: ``list[HexList]``
        """
        return [data[i * cls.INPUT_DATA_WORD_SIZE:(i + 1) * cls.INPUT_DATA_WORD_SIZE:][::-1]
                for i in range(len(data) // cls.INPUT_DATA_WORD_SIZE)]
    # end def sort_data

    def generate_crc32_table(self):
        """
        Generate CRC32 table
        """
        for i in range(256):
            c = i << 24
            for _ in range(8):
                c = (c << 1) ^ self.polynomial if (c & 0x80000000) else c << 1
            # end for
            self.crc_table[i] = c & 0xffffffff
        # end for
    # end def generate_crc32_table

    def calculate_crc(self, data):
        """
        Calculate the CRC of data

        :param data: Input data
        :type data: ``HexList``

        :return: CRC value
        :rtype: ``HexList``
        """
        data = self.sort_data(data)
        return HexList(Numeral(self.crc32(data)))[::-1]
    # end def calculate_crc

    def crc32(self, data):
        """
        Get CRC32, as computed in STM32

        :param data: Input data
        :type data: ``list[HexList]``
        """
        crc = self.init_value
        for word in data:
            for byte in word:
                crc = ((crc << 8) & 0xffffffff) ^ self.crc_table[(crc >> 24) ^ byte]
            # end for
        # end for
        return crc
    # end def crc32
# end class Crc32Stm32
