#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pylibrary.tools.test.nvsparser_test

@brief NVS parser classes Tests

@author christophe.roquebert
@author nestor.lopez

@date   2019/11/27
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.rttprofiler import Parser
from pylibrary.tools.rttprofiler import Profiler
from pylibrary.tools.rttprofiler import RelativeMeasure
from pylibrary.tools.rttprofiler import ProfilerRecord
from unittest import TestCase
from typing import Tuple
import random


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def tuple_to_profiler_record(t: Tuple[int, int, int]):
    return ProfilerRecord(tag=t[0], seq_number=t[1], cycles=t[2])


class ParserTestCase(TestCase):
    '''
    Numeral test implementation.
    '''

    def setUp(self):
        '''
        Initialize test
        '''
        TestCase.setUp(self)

        self.parser_under_test = Parser()
    # end def setUp

    def test_initial_draft(self):

        def delta10(in_record: ProfilerRecord):
            out_record = ProfilerRecord(tag=in_record.tag, seq_number=in_record.seq_number + 10,
                                        cycles=in_record.cycles)
            return out_record

        in_records1 = (
        ProfilerRecord(tag=393, seq_number=0, cycles=722940), ProfilerRecord(tag=787, seq_number=1, cycles=864254),
        ProfilerRecord(tag=393, seq_number=2, cycles=872227), ProfilerRecord(tag=787, seq_number=3, cycles=872880),
        ProfilerRecord(tag=393, seq_number=4, cycles=878001), ProfilerRecord(tag=787, seq_number=5, cycles=878619),
        ProfilerRecord(tag=393, seq_number=6, cycles=880657), ProfilerRecord(tag=787, seq_number=7, cycles=881274),
        ProfilerRecord(tag=393, seq_number=8, cycles=888420), ProfilerRecord(tag=787, seq_number=9, cycles=889030),
        ProfilerRecord(tag=393, seq_number=10, cycles=891726), ProfilerRecord(tag=787, seq_number=11, cycles=892345),
        ProfilerRecord(tag=393, seq_number=12, cycles=914229), ProfilerRecord(tag=787, seq_number=13, cycles=915316))
        in_records2 = tuple(map(delta10, in_records1))
        in_records = in_records1 + in_records2
        # relative_measurements = (RelativeMeasure(393, 787),RelativeMeasure(222, 333), RelativeMeasure(393, 393))
        relative_measurements = (RelativeMeasure(393, 787), RelativeMeasure(393, 393))
        profiler1 = Profiler(
            startup_tag=444, startup_gap_idx=1)
        profiler1.add_data(in_records)
        profiler1.process_data()
    # end def test_initial_draft

    def test_unaligned_chunks_parsing(self):

        in_data = [16, 16, 137, 1, 36, 104, 12, 0, 0, 0, 32, 32, 16, 16, 19, 3, 22, 141, 14, 0, 1, 0, 32, 32, 16, 16,
                   137, 1, 59, 172, 14, 0, 2, 0, 32, 32, 16, 16, 19, 3, 200, 174, 14, 0, 3, 0, 32, 32, 16, 16, 137, 1,
                   1, 186, 14, 0, 4, 0, 32, 32, 16, 16, 19, 3, 64, 190, 14, 0, 5, 0, 32, 32, 16, 16, 137, 1, 201, 194,
                   14, 0, 6, 0, 32, 32, 16, 16, 19, 3, 56, 197, 14, 0, 7, 0, 32, 32, 16, 16, 137, 1, 45, 205, 14, 0, 8,
                   0, 32, 32, 16, 16, 19, 3, 152, 207, 14, 0, 9, 0, 32, 32, 16, 16, 137, 1, 124, 235, 14, 0, 10, 0, 32,
                   32, 16, 16, 19, 3, 224, 237, 14, 0, 11, 0, 32, 32, 16, 16, 137, 1, 118, 248, 14, 0, 12, 0, 32, 32,
                   16, 16, 19, 3, 227, 250, 14, 0, 13, 0, 32, 32]
        pre_parsed_data = (
        (393, 0, 813092), (787, 1, 953622), (393, 2, 961595), (787, 3, 962248), (393, 4, 965121), (787, 5, 966208),
        (393, 6, 967369), (787, 7, 967992), (393, 8, 970029), (787, 9, 970648), (393, 10, 977788), (787, 11, 978400),
        (393, 12, 981110), (787, 13, 981731))
        expected_parsed_data = tuple(map(tuple_to_profiler_record, pre_parsed_data))

        for i in range(len(in_data)):
            in_data_bottom = in_data[0:i]
            in_data_top = in_data[i:len(in_data)]
            parsed_data_bottom = self.parser_under_test.parse_records(
                self.parser_under_test.binary_stream_to_records(in_data_bottom))
            parsed_data_top = self.parser_under_test.parse_records(
                self.parser_under_test.binary_stream_to_records(in_data_top))
            parsed_data = parsed_data_bottom + parsed_data_top
            assert parsed_data == expected_parsed_data
        # end for
    # end def test_unaligned_chunks_parsing

    def test_random_invalid_data(self):
        in_data = []
        for x in range(0, 128):
            in_data.append(random.randint(0, 255))
        empty_tuple = ()
        parsed_data = self.parser_under_test.binary_stream_to_records(in_data)
        assert parsed_data == empty_tuple
    # end def test_random_invalid_data

    def test_repeated_footer(self):
        in_data = []
        for x in range(0, 128):
            in_data.append(32)
        empty_tuple = ()
        parsed_data = self.parser_under_test.binary_stream_to_records(in_data)
        assert parsed_data == empty_tuple
    # end def test_repeated_footer

    def test_data_same_as_footer(self):
        in_data = [16, 16, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 16, 16, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]
        pre_parsed_data = ((0x2020, 0x2020, 0x20202020), (0x2020, 0x2020, 0x20202020))
        expected_parsed_data = tuple(map(tuple_to_profiler_record, pre_parsed_data))
        parsed_data = self.parser_under_test.parse_records(
            self.parser_under_test.binary_stream_to_records(in_data))
        assert parsed_data == expected_parsed_data
    # end def test_data_same_as_footer

    def test_garbage_between_records(self):

        in_data = [16, 16, 137, 1, 36, 104, 12, 0, 0, 0, 32, 32, 16, 16, 19, 3, 22, 141, 14, 0, 1, 0, 32, 32, 18, 54,
                   152, 190, 118, 212, 97, 80, 237, 109, 39, 35, 16, 16, 16, 32, 16, 16, 137, 1, 59, 172, 14, 0, 2, 0,
                   32, 32, 16, 16, 19, 3, 200, 174, 14, 0, 3, 0, 32, 32, 16, 16, 137, 1, 1, 186, 14, 0, 4, 0, 32, 32,
                   32, 32, 194, 249, 252, 207, 51, 16, 32, 32, 16, 16, 16, 16, 19, 3, 64, 190, 14, 0, 5, 0, 32, 32, 16,
                   16, 137, 1, 201, 194, 14, 0, 6, 0, 32, 32, 16, 16, 19, 3, 56, 197, 14, 0, 7, 0, 32, 32, 16, 16, 137,
                   1, 45, 205, 14, 0, 8, 0, 32, 32, 16, 16, 19, 3, 152, 207, 14, 0, 9, 0, 32, 32, 16, 16, 137, 1, 124,
                   235, 14, 0, 10, 0, 32, 32, 140, 16, 16, 19, 3, 224, 237, 14, 0, 11, 0, 32, 32, 16, 16, 137, 1, 118,
                   248, 14, 0, 12, 0, 32, 32, 16, 16, 19, 3, 227, 250, 14, 0, 13, 0, 32, 32, 11, 0, 32, 32, 16, 16, 137,
                   1, 12, 0, 32, 32, 15, 18, 19, 3, 13, 0, 32, 32]
        pre_parsed_data = (
        (393, 0, 813092), (787, 1, 953622), (393, 2, 961595), (787, 3, 962248), (393, 4, 965121), (787, 5, 966208),
        (393, 6, 967369), (787, 7, 967992), (393, 8, 970029), (787, 9, 970648), (393, 10, 977788), (787, 11, 978400),
        (393, 12, 981110), (787, 13, 981731))
        expected_parsed_data = tuple(map(tuple_to_profiler_record, pre_parsed_data))

        for i in range(len(in_data)):
            in_data_bottom = in_data[0:i]
            in_data_top = in_data[i:len(in_data)]
            parsed_data_bottom = self.parser_under_test.parse_records(
                self.parser_under_test.binary_stream_to_records(in_data_bottom))
            parsed_data_top = self.parser_under_test.parse_records(
                self.parser_under_test.binary_stream_to_records(in_data_top))
            parsed_data = parsed_data_bottom + parsed_data_top
            assert parsed_data == expected_parsed_data
        # end for
    # end def test_garbage_between_records
# end class ParserTestCase
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
