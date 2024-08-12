#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pylibrary.tools.test.nvsparser_test

@brief NVS parser classes Tests

@author Stanislas Cottard

@date   2019/10/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import os

from copy import deepcopy
from io import StringIO
from unittest import TestCase

from intelhex import diff_dumps
from intelhex import IntelHex

from pylibrary.tools.chunkidmaps import CHUNK_ID_MAP_NRF52
from pylibrary.tools.chunkidmaps import CHUNK_ID_MAP_QUARK
from pylibrary.tools.chunkidmaps import CHUNK_ID_MAP_STM32L052
from pylibrary.tools.nvsparser import NvsBank
from pylibrary.tools.nvsparser import NvsChunk
from pylibrary.tools.nvsparser import NvsParserInterface
from pylibrary.tools.nvsparser import IdBasedNvsParser
from pylibrary.tools.nvsparser import AddressBasedNvsParser
from pylibrary.tools.nvsparser import NvsZone


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class IdBasedNvsParserTestCase(TestCase):
    """
    NvsParser test implementation.
    """

    def test_interface_constructor(self):
        """
        Test that instantiating the interface raise an exception.
        """
        message_exception = "Can't instantiate abstract class NvsParserInterface"
        try:
            _ = NvsParserInterface(CHUNK_ID_MAP_NRF52)
        except TypeError as e:
            exception_str = str(e)
            self.assertEqual(message_exception,
                             exception_str[:len(message_exception)],
                             "Wrong exception")
        # end try
    # end def test_interface_constructor

    @staticmethod
    def test_class_constructor():
        """
        Test instantiating the NvsParser class.
        """
        _ = IdBasedNvsParser(CHUNK_ID_MAP_NRF52, [], None)
    # end def test_class_constructor

    @staticmethod
    def test_class_construction_by_parsing():
        """
        Test instantiating the NvsParser class by parsing a hex file from the path and from an IntelHex object.
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_herzog_test.hex")
        _ = IdBasedNvsParser.from_hex_file(test_file_path, 1024*4, CHUNK_ID_MAP_NRF52)

        tes_file_object = IntelHex(test_file_path)
        _ = IdBasedNvsParser.from_hex_file(tes_file_object, 1024*4, CHUNK_ID_MAP_NRF52)
    # end def test_class_construction_by_parsing

    def test_parsing_consistency(self):
        """
        Test instantiating the NvsParser class by parsing a hex file from the path and from an IntelHex object.
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_herzog_test.hex")
        tes_file_object = IntelHex(test_file_path)

        test_with_path = IdBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_QUARK)
        test_with_path_hex_file = test_with_path.to_hex_file()

        result_diff = StringIO()
        diff_dumps(tes_file_object, test_with_path_hex_file, result_diff)
        self.assertEqual(result_diff.tell(), 1, "Error parsing from path")

        test_with_hex_file_object = IdBasedNvsParser.from_hex_file(tes_file_object, 1024 * 4, CHUNK_ID_MAP_QUARK)
        test_with_hex_file_object_hex_file = test_with_hex_file_object.to_hex_file()

        result_diff = StringIO()
        diff_dumps(tes_file_object, test_with_hex_file_object_hex_file, result_diff)
        self.assertEqual(result_diff.tell(), 1, "Error parsing from IntelHex object")
    # end def test_parsing_consistency

    def test_add_get_chunk_no_padding_needed(self):
        """
        Test adding and getting a chunk that does not need padding: the length is dividable by 4 (word size in
        NRF52 flash).
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_herzog_test.hex")

        test_parser = IdBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_QUARK)

        test_parser.add_new_chunk(chunk_id="NVS_SERIAL_NB_ID", data=[1, 2, 3, 4])

        chunk_test = test_parser.get_chunk(chunk_id="NVS_SERIAL_NB_ID")

        self.assertEqual(list(chunk_test.chunk_data),
                         [1, 2, 3, 4],
                         "Wrong data")
    # end def test_add_get_chunk_no_padding_needed

    def test_add_get_chunk_padding_needed(self):
        """
        Test adding and getting a chunk that need padding: the length is not dividable by 4 (word size inNRF52 flash).
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_herzog_test.hex")

        test_parser = IdBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_QUARK)

        test_parser.add_new_chunk(chunk_id="NVS_SERIAL_NB_ID", data=[1, 2, 3, 4, 5])

        chunk_test = test_parser.get_chunk(chunk_id="NVS_SERIAL_NB_ID")

        self.assertEqual(list(chunk_test.chunk_data),
                         [1, 2, 3, 4, 5, 0, 0, 0],
                         "Wrong data")
    # end def test_add_get_chunk_padding_needed

    def test_delete_chunk_without_data(self):
        """
        Test deleting a chunk with using only the chunk_id, it should delete the last one in the chunk history.
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_herzog_test.hex")

        test_parser = IdBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_QUARK)

        test_parser.add_new_chunk(chunk_id="NVS_SERIAL_NB_ID", data=[1, 2, 3, 4])

        test_parser.delete_chunk("NVS_SERIAL_NB_ID")

        chunk_test = test_parser.get_chunk(chunk_id="NVS_INVALID_CHUNK_ID")

        self.assertEqual(list(chunk_test.chunk_data),
                         [1, 2, 3, 4],
                         "Wrong data")
    # end def test_delete_chunk_without_data

    def test_delete_chunk_with_data(self):
        """
        Test deleting a chunk using the chunk_id and chunk_data.
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_herzog_test.hex")

        test_parser = IdBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_QUARK)

        test_parser.add_new_chunk(chunk_id="NVS_SERIAL_NB_ID", data=[1, 2, 3, 4])

        test_parser.delete_chunk(chunk_id="NVS_SERIAL_NB_ID", data=[1, 2, 3, 4])

        chunk_test = test_parser.get_chunk(chunk_id="NVS_INVALID_CHUNK_ID")

        self.assertEqual(list(chunk_test.chunk_data),
                         [1, 2, 3, 4],
                         "Wrong data")
    # end def test_delete_chunk_with_data

    def test_diff(self):
        """
        Test NVS Parser diff
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_herzog_test.hex")
        test_parser_1 = IdBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_QUARK)
        test_parser_2 = IdBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_QUARK)
        test_parser_2.add_new_chunk(chunk_id="NVS_SERIAL_NB_ID", data=[1, 2, 3, 4])

        diff = test_parser_1.diff(test_parser_2)
        expected_diff = {
            "parsers": (test_parser_1, test_parser_2),
            "attrs": [],
            "zones": [
                {
                    "zones": (test_parser_1.zone_list[0], test_parser_2.zone_list[0]),
                    "attrs": [],
                    "banks": [
                        {
                            "banks": (test_parser_1.zone_list[0].banks[0], test_parser_2.zone_list[0].banks[0]),
                            "attrs": [],
                            "chunks": [
                                {
                                    "chunks": (test_parser_1.zone_list[0].banks[0].chunks[-1],
                                               test_parser_2.zone_list[0].banks[0].chunks[-2]),
                                    "attrs": ['chunk_id', 'chunk_length', 'chunk_crc', 'chunk_data', 'clear_data'],
                                },
                                {
                                    "chunks": (None, test_parser_2.zone_list[0].banks[0].chunks[-1]),
                                    "attrs": [],
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        self.assertEqual(diff, expected_diff, "Differences between NVS should be listed")
    # end def test_diff

    def test_no_diff(self):
        """
        Test NVS Parser no diff
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_herzog_test.hex")
        test_parser_1 = IdBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_QUARK)
        test_parser_2 = IdBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_QUARK)

        diff = test_parser_1.diff(test_parser_2)
        expected_diff = {}
        self.assertEqual(diff, expected_diff, "No difference should be found")
    # end def test_no_diff
# end class IdBasedNvsParserTestCase


class AddressBasedNvsParserTestCase(TestCase):
    """
    NvsParser test implementation.
    """

    def test_interface_constructor(self):
        """
        Test that instantiating the interface raise an exception.
        """
        message_exception = "Can't instantiate abstract class NvsParserInterface"
        try:
            _ = NvsParserInterface(CHUNK_ID_MAP_STM32L052)
        except TypeError as e:
            exception_str = str(e)
            self.assertEqual(message_exception,
                             exception_str[:len(message_exception)],
                             "Wrong exception")
        # end try
    # end def test_interface_constructor

    @staticmethod
    def test_class_constructor():
        """
        Test instantiating the NvsParser class.
        """
        _ = AddressBasedNvsParser(CHUNK_ID_MAP_STM32L052, [], None)
    # end def test_class_constructor

    @staticmethod
    def test_class_construction_by_parsing():
        """
        Test instantiating the NvsParser class by parsing a hex file from the path and from an IntelHex object.
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_drifter_test.hex")
        _ = AddressBasedNvsParser.from_hex_file(test_file_path, 1024*4, CHUNK_ID_MAP_STM32L052)

        tes_file_object = IntelHex(test_file_path)
        _ = AddressBasedNvsParser.from_hex_file(tes_file_object, 1024*4, CHUNK_ID_MAP_STM32L052)
    # end def test_class_construction_by_parsing

    def test_parsing_consistency(self):
        """
        Test instantiating the NvsParser class by parsing a hex file from the path and from an IntelHex object.
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_drifter_test.hex")
        test_file_object = IntelHex(test_file_path)

        test_with_path = AddressBasedNvsParser.from_hex_file(test_file_path, 2 * 1024, CHUNK_ID_MAP_STM32L052)
        test_with_path_hex_file = test_with_path.to_hex_file()

        result_diff = StringIO()
        diff_dumps(test_file_object, test_with_path_hex_file, result_diff)
        self.assertEqual(result_diff.tell(), 1, "Error parsing from path")

        test_with_hex_file_object = AddressBasedNvsParser.from_hex_file(test_file_object, 2 * 1024, CHUNK_ID_MAP_STM32L052)
        test_with_hex_file_object_hex_file = test_with_hex_file_object.to_hex_file()

        result_diff = StringIO()
        diff_dumps(test_file_object, test_with_hex_file_object_hex_file, result_diff)
        self.assertEqual(result_diff.tell(), 1, "Error parsing from IntelHex object")
    # end def test_parsing_consistency

    def test_add_get_chunk_no_padding_needed(self):
        """
        Test adding and getting a chunk that does not need padding: the length is dividable by 4 (word size in
        NRF52 flash).
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_drifter_test.hex")

        test_parser = AddressBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_STM32L052)

        test_parser.add_new_chunk(chunk_id="NVS_DFU_ID", data=[1, 2])

        chunk_test = test_parser.get_chunk(chunk_id="NVS_DFU_ID")

        self.assertEqual(list(chunk_test.chunk_data),
                         [1, 2],
                         "Wrong data")
    # end def test_add_get_chunk_no_padding_needed

    def test_add_get_chunk_padding_needed(self):
        """
        Test adding and getting a chunk that need padding: the length is not dividable by 4 (word size inNRF52 flash).
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_drifter_test.hex")

        test_parser = AddressBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_STM32L052)

        test_parser.add_new_chunk(chunk_id="NVS_REGULATORY_MODEL_NB_ID", data=[1, 2, 3, 4, 5])

        chunk_test = test_parser.get_chunk(chunk_id="NVS_REGULATORY_MODEL_NB_ID")

        self.assertEqual(list(chunk_test.chunk_data),
                         [1, 2, 3, 4, 5, 0],
                         "Wrong data")
    # end def test_add_get_chunk_padding_needed

    def test_delete_chunk_without_data(self):
        """
        Test deleting a chunk with using only the chunk_id, it should delete the last one in the chunk history.
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_drifter_test.hex")

        test_parser = AddressBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_STM32L052)

        test_parser.add_new_chunk(chunk_id="NVS_REGULATORY_MODEL_NB_ID", data=[1, 2, 3, 4, 5, 6])

        test_parser.delete_chunk("NVS_REGULATORY_MODEL_NB_ID")

        chunk_test = test_parser.get_chunk(chunk_id="NVS_REGULATORY_MODEL_NB_ID")

        self.assertEqual(list(chunk_test.chunk_data),
                         [0xFF] * 6,
                         "Wrong data")
    # end def test_delete_chunk_without_data

    def test_delete_chunk_with_data(self):
        """
        Test deleting a chunk using the chunk_id and chunk_data.
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_drifter_test.hex")

        test_parser = AddressBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_STM32L052)

        test_parser.add_new_chunk(chunk_id="NVS_REGULATORY_MODEL_NB_ID", data=[1, 2, 3, 4, 5, 6])

        test_parser.delete_chunk(chunk_id="NVS_REGULATORY_MODEL_NB_ID", data=[1, 2, 3, 4, 5, 6])

        chunk_test = test_parser.get_chunk(chunk_id="NVS_REGULATORY_MODEL_NB_ID")

        self.assertEqual(list(chunk_test.chunk_data),
                         [0xFF] * 6,
                         "Wrong data")
    # end def test_delete_chunk_with_data

    def test_diff(self):
        """
        Test NVS Parser diff
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_drifter_test.hex")
        test_parser_1 = AddressBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_STM32L052)
        test_parser_2 = AddressBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_STM32L052)
        test_parser_2.add_new_chunk(chunk_id="NVS_REGULATORY_MODEL_NB_ID", data=[1, 2, 3, 4, 5, 6])

        diff = test_parser_1.diff(test_parser_2)
        expected_diff = {
            "parsers": (test_parser_1, test_parser_2),
            "attrs": [],
            "zones": [
                {
                    "zones": (test_parser_1.zone_list[0], test_parser_2.zone_list[0]),
                    "attrs": [],
                    "banks": [
                        {
                            "banks": (test_parser_1.zone_list[0].banks[0], test_parser_2.zone_list[0].banks[0]),
                            "attrs": [],
                            "chunks": [
                                {
                                    "chunks": (test_parser_1.zone_list[0].banks[0].chunks[-1],
                                               test_parser_2.zone_list[0].banks[0].chunks[-2]),
                                    "attrs": ['chunk_id', 'chunk_length', 'chunk_crc', 'chunk_data', 'clear_data'],
                                },
                                {
                                    "chunks": (None, test_parser_2.zone_list[0].banks[0].chunks[-1]),
                                    "attrs": [],
                                }
                            ]
                        },
                        {
                            "banks": (None, None),
                            "attrs": [],
                            "chunks": []
                        },
                    ]
                }
            ]
        }
        self.assertEqual(diff, expected_diff, "Differences between NVS should be listed")
    # end def test_diff

    def test_no_diff(self):
        """
        Test NVS Parser no diff
        """
        test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nvs_drifter_test.hex")
        test_parser_1 = AddressBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_STM32L052)
        test_parser_2 = AddressBasedNvsParser.from_hex_file(test_file_path, 1024 * 4, CHUNK_ID_MAP_STM32L052)

        diff = test_parser_1.diff(test_parser_2)
        expected_diff = {'parsers': (test_parser_1, test_parser_2),
                         'attrs': [],
                         'zones': [{
                             'zones': (test_parser_1.zone_list[0], test_parser_2.zone_list[0]),
                             'attrs': [],
                             'banks': [{
                                 'banks': (None, None),
                                 'attrs': [],
                                 'chunks': []
                             }]
                         }]
                         }
        self.assertEqual(diff, expected_diff, "No difference should be found")
    # end def test_no_diff
# end class AddressBasedNvsParserTestCase


def chunk_from_hex_array(array_to_parse, chunk_id_map):
    """
    Parse the first chunk of a hex array.
    This function is done only for testing the NvsParser classes, it does not follow any specific format.

    :param array_to_parse: The hex array to parse to get a chunk
    :type array_to_parse: ``list`` or ``HexList`` or ``tuple`` or ``bytearray`` or ``bytes``
    :param chunk_id_map: Map of chunk ids which also defines the NVS_WORD_SIZE
    :type chunk_id_map: ``dict``

    :return: The chunk object and the array_to_parse minus the chunk
    :rtype: ``tuple``
    """
    chunk_id = array_to_parse[0]
    chunk_length = array_to_parse[1]
    chunk_crc = array_to_parse[2]
    chunk_data = array_to_parse[3:3+chunk_length]

    return NvsChunk(chunk_to_hex_array, chunk_id, chunk_length, chunk_crc, chunk_data), array_to_parse[3+chunk_length:]
# end def chunk_from_hex_array


def chunk_to_hex_array(chunk):
    """
    Format a chunk in a hex array.
    This function is done only for testing the NvsParser classes, it does not follow any specific format.

    :param chunk: The chunk to format
    :type chunk: ``NvsChunk``

    :return: The hex array
    :rtype: ``list``
    """
    if chunk.chunk_length != -1 and chunk.chunk_crc != -1:
        return [chunk.chunk_id, chunk.chunk_length, chunk.chunk_crc] + chunk.chunk_data
    else:
        return [chunk.chunk_id] + chunk.chunk_data
    # end if
# end def chunk_to_hex_array


TEST_CHUNK_ID_MAP = {
        "NVS_WORD_SIZE": 4,
        "NVS_CHUNK_METHOD": True,
        "NVS_INVALID_CHUNK_ID": 0x00,
        "NVS_ACTIVE_BANK_ID": 0x01,
        "NVS_EMPTY_CHUNK_ID": 0xFF,

        # Important headers: [chunkID, chunkLength, chunkCRC]
        "ACTIVE_BANK_HDR": [0x01, 0x00, 0x01],
        "TEMP_BANK_HDR": [0xFF, 0x00, 0x02],
        "INVALID_BANK_HDR": [0x00, 0x00, 0x0000],
    }


class NvsChunkTestCase(TestCase):
    """
    NvsChunk test implementation.
    """

    def test_constructor(self):
        """
        Test NvsChunk constructor.
        """
        test_chunk = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                              chunk_id=1,
                              chunk_length=2,
                              chunk_crc=3,
                              chunk_data=[4, 5])

        self.assertEqual(test_chunk.chunk_id, 1, "Wrong chunk_id")
        self.assertEqual(test_chunk.chunk_length, 2, "Wrong chunk_length")
        self.assertEqual(test_chunk.chunk_crc, 3, "Wrong chunk_crc")
        self.assertEqual(test_chunk.chunk_data, [4, 5], "Wrong chunk_data")
    # end def test_constructor

    def test_create_a_padding_chunk(self):
        """
        Test NvsChunk.create_a_padding_chunk(padding_length, to_hex_array_method).
        """
        test_padding_chunk = NvsChunk.create_a_padding_chunk(padding_length=5)

        self.assertEqual(test_padding_chunk.chunk_id, 0xFF, "Wrong chunk_id")
        self.assertEqual(test_padding_chunk.chunk_length, -1, "Wrong chunk_length")
        self.assertEqual(test_padding_chunk.chunk_crc, -1, "Wrong chunk_crc")
        self.assertEqual(test_padding_chunk.chunk_data, [0xFF] * 4, "Wrong chunk_data")

        self.assertEqual(test_padding_chunk.to_hex_array(), [0xFF] * 5, "Wrong hex array")
    # end def test_create_a_padding_chunk

    def test_chunk_to_hex_array(self):
        """
        Test NvsChunk.to_hex_array().
        """
        test_chunk = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                              chunk_id=1,
                              chunk_length=2,
                              chunk_crc=3,
                              chunk_data=[4, 5])

        self.assertEqual(test_chunk.to_hex_array(), [1, 2, 3, 4, 5], "Wrong hex array")
    # end def test_chunk_to_hex_array

    def test_chunk_to_hex_file(self):
        """
        Test NvsChunk.to_hex_file().
        """
        test_chunk = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                              chunk_id=1,
                              chunk_length=2,
                              chunk_crc=3,
                              chunk_data=[4, 5])

        hex_file = test_chunk.to_hex_file(address_in_memory=0x00)

        self.assertEqual(list(hex_file.addresses()), [0, 1, 2, 3, 4], "Wrong address_in_memory")
        self.assertEqual(list(hex_file.tobinarray()), [1, 2, 3, 4, 5], "Wrong chunk to hex file")
    # end def test_chunk_to_hex_file

    def test_chunk_equality(self):
        """
        Test NvsChunk equality.
        """
        test_chunk_1 = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                                chunk_id=1,
                                chunk_length=2,
                                chunk_crc=3,
                                chunk_data=[4, 5])
        test_chunk_2 = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                                chunk_id=1,
                                chunk_length=2,
                                chunk_crc=3,
                                chunk_data=[4, 5])

        self.assertEqual(test_chunk_1, test_chunk_2, "Chunks not equal when they should be")
    # end def test_chunk_equality

    def test_chunk_no_equality(self):
        """
        Test NvsChunk no equality.
        """
        test_chunk_1 = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                                chunk_id=1,
                                chunk_length=2,
                                chunk_crc=3,
                                chunk_data=[4, 5])
        test_chunk_2 = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                                chunk_id=1,
                                chunk_length=1,
                                chunk_crc=3,
                                chunk_data=[4])

        self.assertNotEqual(test_chunk_1, test_chunk_2, "Chunks equal when they should not be")
    # end def test_chunk_no_equality

    def test_chunk_diff(self):
        """
        Test NVS Chunk diff
        """
        test_chunk_1 = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                                chunk_id=2,
                                chunk_length=2,
                                chunk_crc=3,
                                chunk_data=[4, 5])
        test_chunk_2 = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                                chunk_id=1,
                                chunk_length=1,
                                chunk_crc=2,
                                chunk_data=[4])

        diff = test_chunk_1.diff(test_chunk_2)

        expected_diff = {
            "chunks": (test_chunk_1, test_chunk_2),
            "attrs": ["chunk_id", "chunk_length", "chunk_crc", "chunk_data", "clear_data"],
        }
        self.assertEqual(diff, expected_diff, "Chunks differences should be listed")
    # end def test_chunk_diff

    def test_chunk_no_diff(self):
        """
        Test NVS Chunk no diff
        """
        test_chunk_1 = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                                chunk_id=2,
                                chunk_length=2,
                                chunk_crc=3,
                                chunk_data=[4, 5])
        test_chunk_2 = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                                chunk_id=2,
                                chunk_length=2,
                                chunk_crc=3,
                                chunk_data=[4, 5])

        diff = test_chunk_1.diff(test_chunk_2)
        expected_diff = {}
        self.assertEqual(diff, expected_diff, "No difference between chunks should be found")
    # end def test_chunk_no_diff
# end class NvsChunkTestCase


class NvsBankTestCase(TestCase):
    """
    NvsBank test implementation.
    """

    def test_constructor(self):
        """
        Test NvsBank constructor.
        """
        test_chunk = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                              chunk_id=1,
                              chunk_length=2,
                              chunk_crc=3,
                              chunk_data=[4, 5])

        # If the length of array_to_test is equal to the bank length then no padding chunk will be added
        test_bank = NvsBank(active=True, start_address=0, bank_length=5, chunks=[test_chunk])

        self.assertTrue(test_bank.active, "Wrong active")
        self.assertEqual(test_bank.start_address, 0, "Wrong start_address")
        self.assertEqual(test_bank.bank_length, 5, "Wrong bank_length")
        self.assertEqual(len(test_bank.chunks), 1, "Wrong len(chunks)")
        self.assertEqual(test_bank.chunks[0], test_chunk, "Wrong chunks")

        # Else there will be a padding chunk added at the end
        test_bank = NvsBank(active=True, start_address=0, bank_length=7, chunks=[test_chunk])

        self.assertTrue(test_bank.active, "Wrong active")
        self.assertEqual(test_bank.start_address, 0, "Wrong start_address")
        self.assertEqual(test_bank.bank_length, 7, "Wrong bank_length")
        self.assertEqual(len(test_bank.chunks), 2, "Wrong len(chunks)")
        self.assertEqual(test_bank.chunks[0], test_chunk, "Wrong chunks")
        self.assertEqual(test_bank.chunks[1].to_hex_array(), [0xFF, 0xFF], "Wrong padding chunk")
    # end def test_constructor

    def test_bank_from_hex_array(self):
        """
        Test NvsBank.from_hex_array(array_to_parse, chunk_from_hex_array_method, start_address, bank_length,
        chunk_id_map).
        """
        # If the length of array_to_test is equal to the bank length then no padding chunk will be added
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_bank, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              start_address=0,
                                              bank_length=8,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertTrue(test_bank.active, "Wrong active")
        self.assertEqual(test_bank.start_address, 0, "Wrong start_address")
        self.assertEqual(test_bank.bank_length, 8, "Wrong bank_length")
        self.assertEqual(len(test_bank.chunks), 2, "Wrong len(chunks)")
        self.assertEqual(test_bank.chunks[0].to_hex_array(), TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"], "Wrong first chunk")
        self.assertEqual(test_bank.chunks[1].to_hex_array(), [1, 2, 3, 4, 5], "Wrong second chunk")

        # Else there will be a padding chunk added at the end
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_bank, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              start_address=0,
                                              bank_length=10,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertTrue(test_bank.active, "Wrong active")
        self.assertEqual(test_bank.start_address, 0, "Wrong start_address")
        self.assertEqual(test_bank.bank_length, 10, "Wrong bank_length")
        self.assertEqual(len(test_bank.chunks), 3, "Wrong len(chunks)")
        self.assertEqual(test_bank.chunks[0].to_hex_array(), TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"], "Wrong first chunk")
        self.assertEqual(test_bank.chunks[1].to_hex_array(), [1, 2, 3, 4, 5], "Wrong second chunk")
        self.assertEqual(test_bank.chunks[2].to_hex_array(), [0xFF, 0xFF], "Wrong padding chunk")
    # end def test_bank_from_hex_array

    def test_bank_to_hex_array_with_padding(self):
        """
        Test NvsBank.to_hex_array(no_padding=False). no_padding is an optional parameter that is False by default.
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_bank, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              start_address=0,
                                              bank_length=10,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_bank.to_hex_array(), array_to_test + [0xFF, 0xFF], "Wrong hex array result")
    # end def test_bank_to_hex_array_with_padding

    def test_bank_to_hex_array_without_padding(self):
        """
        Test NvsBank.to_hex_array(no_padding=True). no_padding is an optional parameter that is False by default.
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_bank, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              start_address=0,
                                              bank_length=10,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_bank.to_hex_array(no_padding=True), array_to_test, "Wrong hex array result")
    # end def test_bank_to_hex_array_without_padding

    def test_bank_to_hex_file_with_padding(self):
        """
        Test NvsBank.to_hex_file(no_padding=False). no_padding is an optional parameter that is False by default.
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_bank, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              start_address=0,
                                              bank_length=10,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        hex_file = test_bank.to_hex_file()

        self.assertEqual(list(hex_file.addresses()), [i for i in range(len(array_to_test) + 2)],
                         "Wrong address_in_memory")
        self.assertEqual(list(hex_file.tobinarray()), array_to_test + [0xFF, 0xFF], "Wrong bank to hex file")
    # end def test_bank_to_hex_file_with_padding

    def test_bank_to_hex_file_without_padding(self):
        """
        Test NvsBank.to_hex_file(no_padding=True). no_padding is an optional parameter that is False by default.
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_bank, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              start_address=0,
                                              bank_length=10,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        hex_file = test_bank.to_hex_file(no_padding=True)

        self.assertEqual(list(hex_file.addresses()), [i for i in range(len(array_to_test))], "Wrong address_in_memory")
        self.assertEqual(list(hex_file.tobinarray()), array_to_test, "Wrong bank to hex file")
    # end def test_bank_to_hex_file_without_padding

    def test_bank_add_chunk(self):
        """
        Test NvsBank.add_chunk(chunk_to_add).
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"]

        test_bank, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              start_address=0,
                                              bank_length=8,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        test_chunk = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                              chunk_id=1,
                              chunk_length=2,
                              chunk_crc=3,
                              chunk_data=[4, 5])

        test_bank.add_chunk(test_chunk)

        self.assertEqual(len(test_bank.chunks), 2, "Wrong len(chunks)")
        self.assertEqual(test_bank.chunks[1], test_chunk, "Wrong added chunk")
    # end def test_bank_add_chunk

    def test_bank_add_padding(self):
        """
        Test NvsBank.add_padding().
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"]

        test_bank, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              start_address=0,
                                              bank_length=8,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        # Remove automatic padding at creation to do the test
        if test_bank.chunks[-1].chunk_length == -1 and test_bank.chunks[-1].chunk_crc == -1:
            test_bank.chunks = test_bank.chunks[:-1]
        # end if

        test_bank.add_padding()

        expected_padding_chunk = NvsChunk(chunk_to_hex_array, chunk_id=0xFF, chunk_length=-1, chunk_crc=-1,
                                          chunk_data=[0xFF] * (8 - len(array_to_test) - 1))

        self.assertEqual(len(test_bank.chunks), 2, "Wrong len(chunks)")
        self.assertEqual(test_bank.chunks[1], expected_padding_chunk, "Wrong padding chunk")
    # end def test_bank_add_padding

    def test_bank_get_current_length(self):
        """
        Test NvsBank.get_current_length().
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"]

        test_bank, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              start_address=0,
                                              bank_length=8,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        test_current_length = test_bank.get_current_length()

        self.assertEqual(test_current_length, len(array_to_test), "Wrong current length")
    # end def test_bank_get_current_length

    def test_bank_equality(self):
        """
        Test NvsBank equality.
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"]

        # Equality for bank 1 without padding and bank 2 without padding
        test_bank_1, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test),
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        test_bank_2, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test),
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_bank_1, test_bank_2, "Banks not equal when they should be")

        # Equality for bank 1 with padding and bank 2 without padding
        test_bank_1, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test) + 1,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        test_bank_2, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test) + 1,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        # Remove automatic padding at creation to do the test
        if test_bank_2.chunks[-1].chunk_length == -1 and test_bank_2.chunks[-1].chunk_crc == -1:
            test_bank_2.chunks = test_bank_2.chunks[:-1]
        # end if

        self.assertEqual(test_bank_1, test_bank_2, "Banks not equal when they should be")

        # Equality for bank 1 without padding and bank 2 with padding
        test_bank_1, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test) + 1,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        # Remove automatic padding at creation to do the test
        if test_bank_1.chunks[-1].chunk_length == -1 and test_bank_1.chunks[-1].chunk_crc == -1:
            test_bank_1.chunks = test_bank_1.chunks[:-1]
        # end if

        test_bank_2, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test) + 1,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_bank_1, test_bank_2, "Banks not equal when they should be")

        # Equality for bank 1 with padding and bank 2 with padding
        test_bank_1, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test) + 1,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        test_bank_2, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test) + 1,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_bank_1, test_bank_2, "Banks not equal when they should be")
    # end def test_bank_equality

    def test_bank_no_equality(self):
        """
        Test NvsBank no equality.
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"]

        test_bank_1, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test),
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        array_to_test = TEST_CHUNK_ID_MAP["INVALID_BANK_HDR"]
        test_bank_2, _ = NvsBank.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test),
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertNotEqual(test_bank_1, test_bank_2, "Banks equal when they should not be")
    # end def test_bank_no_equality

    def test_bank_diff(self):
        """
        Test NVS bank diff
        """
        array_to_test_1 = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"]
        test_bank_1, _ = NvsBank.from_hex_array(array_to_parse=array_to_test_1,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test_1),
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        test_bank_2 = deepcopy(test_bank_1)
        test_bank_2.start_address += 1
        test_bank_2.bank_length += 4
        new_chunk = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                             chunk_id=1,
                             chunk_length=1,
                             chunk_crc=2,
                             chunk_data=[3])
        test_bank_2.add_chunk(new_chunk)

        diff = test_bank_1.diff(test_bank_2)
        expected_diff = {
            "banks": (test_bank_1, test_bank_2),
            "attrs": ["start_address", "bank_length"],
            "chunks": [{
                "chunks": (None, new_chunk),
                "attrs": []
            }]
        }
        self.assertEqual(diff, expected_diff, "Differences between banks should be listed")
    # end def test_bank_diff

    def test_bank_no_diff(self):
        """
        Test NVS bank no diff
        """
        array_to_test_1 = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"]
        test_bank_1, _ = NvsBank.from_hex_array(array_to_parse=array_to_test_1,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                start_address=0,
                                                bank_length=len(array_to_test_1),
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        test_bank_2 = deepcopy(test_bank_1)

        diff = test_bank_1.diff(test_bank_2)
        expected_diff = {}
        self.assertEqual(diff, expected_diff, "No difference between banks should be found")
    # end def test_bank_no_diff
# end class NvsBankTestCase


class NvsZoneTestCase(TestCase):
    """
    NvsZone test implementation.
    """

    def test_constructor(self):
        """
        Test NvsZone constructor.
        """
        test_chunk = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                              chunk_id=1,
                              chunk_length=2,
                              chunk_crc=3,
                              chunk_data=[4, 5])

        # If the the length of array_to_test is equal to the bank length then no padding chunk will be added
        test_bank_active = NvsBank(active=True, start_address=0, bank_length=5, chunks=[test_chunk])

        # If the the length of array_to_test is equal to the bank length then no padding chunk will be added
        test_bank_disabled = NvsBank(active=False, start_address=5, bank_length=5, chunks=[])

        test_zone = NvsZone(zone_number=0, banks=[test_bank_active, test_bank_disabled], start_address=0)

        self.assertEqual(test_zone.zone_number, 0, "Wrong zone_number")
        self.assertEqual(test_zone.start_address, 0, "Wrong start_address")
        self.assertEqual(len(test_zone.banks), 2, "Wrong len(banks)")
        self.assertEqual(test_zone.banks[0], test_bank_active, "Wrong first bank")
        self.assertEqual(test_zone.banks[1], test_bank_disabled, "Wrong second bank")
    # end def test_constructor

    def test_zone_from_hex_array(self):
        """
        Test NvsZone.from_hex_array(array_to_parse, chunk_from_hex_array_method, bank_length, zone_number,
        start_address, chunk_id_map).
        """
        # If the the length of array_to_test is bigger than the bank length then there will not be any bank only
        # full of padding
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5] + \
            TEST_CHUNK_ID_MAP["INVALID_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_zone, _ = NvsZone.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              bank_length=8,
                                              zone_number=0,
                                              start_address=0,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_zone.zone_number, 0, "Wrong zone_number")
        self.assertEqual(test_zone.start_address, 0, "Wrong start_address")
        self.assertEqual(len(test_zone.banks), 2, "Wrong len(banks)")
        self.assertEqual(test_zone.banks[0].to_hex_array(), array_to_test[:8], "Wrong first bank")
        self.assertEqual(test_zone.banks[1].to_hex_array(), array_to_test[8:], "Wrong second bank")

        # Else there will be a padding added at the end
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 1, 3, 4]

        test_zone, _ = NvsZone.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              bank_length=8,
                                              zone_number=0,
                                              start_address=0,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_zone.zone_number, 0, "Wrong zone_number")
        self.assertEqual(test_zone.start_address, 0, "Wrong start_address")
        self.assertEqual(len(test_zone.banks), 2, "Wrong len(banks)")
        self.assertEqual(test_zone.banks[0].to_hex_array(), array_to_test + [0xFF], "Wrong first bank")
        self.assertEqual(test_zone.banks[1].to_hex_array(), [0xFF] * 8, "Wrong second bank")
    # end def test_zone_from_hex_array

    def test_zone_to_hex_array(self):
        """
        Test NvsZone.to_hex_array().
        """
        # If the the length of array_to_test is bigger than the bank length then there will not be any bank only
        # full of padding
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5] + \
            TEST_CHUNK_ID_MAP["INVALID_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_zone, _ = NvsZone.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              bank_length=8,
                                              zone_number=0,
                                              start_address=0,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_zone.to_hex_array(), array_to_test, "Wrong zone_number")

        # Else there will be a padding added at the end
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 1, 3, 4]

        test_zone, _ = NvsZone.from_hex_array(array_to_parse=array_to_test,
                                              chunk_from_hex_array_method=chunk_from_hex_array,
                                              bank_length=8,
                                              zone_number=0,
                                              start_address=0,
                                              chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_zone.to_hex_array(), array_to_test + [0xFF]*9, "Wrong hex array result")
    # end def test_zone_to_hex_array

    def test_zone_get_active_bank(self):
        """
        Test NvsZone.get_active_bank().
        """
        test_chunk = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                              chunk_id=1,
                              chunk_length=2,
                              chunk_crc=3,
                              chunk_data=[4, 5])

        # If the length of array_to_test is equal to the bank length then no padding chunk will be added
        test_bank_active = NvsBank(active=True, start_address=0, bank_length=5, chunks=[test_chunk])

        # If the length of array_to_test is equal to the bank length then no padding chunk will be added
        test_bank_disabled = NvsBank(active=False, start_address=5, bank_length=5, chunks=[])

        test_zone = NvsZone(zone_number=0, banks=[test_bank_active, test_bank_disabled], start_address=0)

        self.assertEqual(test_zone.get_active_bank(), test_bank_active, "Wrong zone_number")
    # end def test_zone_get_active_bank

    def test_zone_get_disabled_bank(self):
        """
        Test NvsZone.get_disabled_bank().
        """
        test_chunk = NvsChunk(to_hex_array_method=chunk_to_hex_array,
                              chunk_id=1,
                              chunk_length=2,
                              chunk_crc=3,
                              chunk_data=[4, 5])

        # If the the length of array_to_test is equal to the bank length then no padding chunk will be added
        test_bank_active = NvsBank(active=True, start_address=0, bank_length=5, chunks=[test_chunk])

        # If the the length of array_to_test is equal to the bank length then no padding chunk will be added
        test_bank_disabled = NvsBank(active=False, start_address=5, bank_length=5, chunks=[])

        test_zone = NvsZone(zone_number=0, banks=[test_bank_active, test_bank_disabled], start_address=0)

        self.assertEqual(test_zone.get_disabled_bank(), test_bank_disabled, "Wrong zone_number")
    # end def test_zone_get_disabled_bank

    def test_zone_equality(self):
        """
        Test NvsZone equality.
        """
        # If the the length of array_to_test is bigger than the bank length then there will not be any bank only
        # full of padding
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5] + \
            TEST_CHUNK_ID_MAP["INVALID_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_zone_1, _ = NvsZone.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                bank_length=8,
                                                zone_number=0,
                                                start_address=0,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        test_zone_2, _ = NvsZone.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                bank_length=8,
                                                zone_number=0,
                                                start_address=0,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertEqual(test_zone_1, test_zone_2, "Zones not equal when they should be")
    # end def test_zone_equality

    def test_zone_no_equality(self):
        """
        Test NvsZone no equality.
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5] + \
            TEST_CHUNK_ID_MAP["INVALID_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_zone_1, _ = NvsZone.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                bank_length=8,
                                                zone_number=0,
                                                start_address=0,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 1, 3, 4]

        test_zone_2, _ = NvsZone.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                bank_length=8,
                                                zone_number=0,
                                                start_address=0,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        self.assertNotEqual(test_zone_1, test_zone_2, "Zones equal when they should not be")
    # end def test_zone_no_equality

    def test_zone_diff(self):
        """
        Test NVS Zone diff
        """
        array_to_test_1 = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5] + \
            TEST_CHUNK_ID_MAP["INVALID_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_zone_1, _ = NvsZone.from_hex_array(array_to_parse=array_to_test_1,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                bank_length=8,
                                                zone_number=0,
                                                start_address=0,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        array_to_test_2 = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 6] + \
            TEST_CHUNK_ID_MAP["INVALID_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_zone_2, _ = NvsZone.from_hex_array(array_to_parse=array_to_test_2,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                bank_length=8,
                                                zone_number=0,
                                                start_address=0,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        diff = test_zone_1.diff(test_zone_2)
        expected_diff = {
            "zones": (test_zone_1, test_zone_2),
            "attrs": [],
            "banks": [
                {
                    "banks": (test_zone_1.banks[0], test_zone_2.banks[0]),
                    "attrs": [],
                    "chunks": [
                        {
                            "chunks": (test_zone_1.banks[0].chunks[-1], test_zone_2.banks[0].chunks[-1]),
                            "attrs": ["chunk_data", "clear_data"],
                        }
                    ]
                }
            ]
        }
        self.assertEqual(diff, expected_diff, "Differences between zones should be listed")
    # end def test_zone_diff

    def test_zone_no_diff(self):
        """
        Test NVS Zone no diff
        """
        array_to_test = TEST_CHUNK_ID_MAP["ACTIVE_BANK_HDR"] + [1, 2, 3, 4, 5] + \
            TEST_CHUNK_ID_MAP["INVALID_BANK_HDR"] + [1, 2, 3, 4, 5]

        test_zone_1, _ = NvsZone.from_hex_array(array_to_parse=array_to_test,
                                                chunk_from_hex_array_method=chunk_from_hex_array,
                                                bank_length=8,
                                                zone_number=0,
                                                start_address=0,
                                                chunk_id_map=TEST_CHUNK_ID_MAP)

        test_zone_2 = deepcopy(test_zone_1)

        diff = test_zone_1.diff(test_zone_2)
        expected_diff = {}
        self.assertEqual(diff, expected_diff, "No difference between banks should be found")
    # end def test_zone_no_diff
# end class NvsZoneTestCase
