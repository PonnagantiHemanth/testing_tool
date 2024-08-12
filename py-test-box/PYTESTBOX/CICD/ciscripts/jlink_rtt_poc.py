# -*- coding: utf-8 -*-
import sys
import pylink
import time
import random
import threading
import _thread
import collections
from typing import Tuple
from dataclasses import dataclass
from statistics import mean

TAG_OFFSET = 0
TAG_SIZE = 2
CYCLES_OFFSET = 2
CYCLES_SIZE = 4
SEQ_NUMBER_OFFSET = 6
SEQ_NUMBER_SIZE = 2

MARKER_SIZE = 2
PAYLOAD_SIZE = TAG_SIZE + SEQ_NUMBER_SIZE + CYCLES_SIZE
HEADER = 0x1010
FOOTER = 0x2020
RECORD_SIZE = 2 * MARKER_SIZE + PAYLOAD_SIZE

@dataclass(frozen=True, eq=True)
class ProfilerRecord:
    tag: int
    seq_number : int
    cycles : int


@dataclass(frozen=True, eq=True)
class RelativeMeasure:
    start: int
    end: int


def counts_to_msec(counts : int) -> float:
    return counts / 64_000


class Profiler:
    def __init__(self, relative_measurements : Tuple[RelativeMeasure, ...]) -> None:
        self._relative = {key : [] for key in relative_measurements}
        self._in_records = [] # type : List[ProfilerRecord]
        self._mins = dict.fromkeys(relative_measurements, sys.maxsize)
        self._maxs = dict.fromkeys(relative_measurements, 0)
        self._average = dict.fromkeys(relative_measurements, 0)

    def add_data(self, profiler_records : Tuple[ProfilerRecord, ...]) -> None:
        self._in_records.extend(profiler_records)

    def process_data(self):
        # This builds a "list" of dictionaries where each dict's keys are
        # the tags in the records and the value is a list of indexes of the
        # records where the tag appears.
        # There is one dict for each contiguous section of seq_numbers, so
        # in the case that there are no missing seq_counters, the list of
        # dicts only contains one dict. The "list" of dicts is actually
        # implemented as a dict itself, so as to be able to use defaultdict()
        tags_index = collections.defaultdict(dict)
        tags_index_table_idx = 0
        seq_number = self._in_records[0].seq_number
        tags_index[0] = collections.defaultdict(list)
        for idx, record in enumerate(self._in_records):
            if record.seq_number != seq_number:
                print("missing counter, expected %u, actual:%u" % (seq_number, record.seq_number))
                tags_index_table_idx += 1
                seq_number = (record.seq_number + 1) if record.seq_number < 0xFFFF else 0
                tags_index[tags_index_table_idx] = collections.defaultdict(list)
            else:
                seq_number = (seq_number + 1) if seq_number < 0xFFFF else 0
            tags_index[tags_index_table_idx][record.tag].append(idx)

        for rel in self._relative.keys():
            for tags_dicts in tags_index.values():
                for idx_end in tags_dicts[rel.end]:
                    for idx_start in reversed(tags_dicts[rel.start]):
                        if idx_start < idx_end:
                            self._relative[rel].append((idx_start, idx_end))
                            break

        for rel in self._relative.keys():
            timestamps = [(self._in_records[start].cycles, self._in_records[end].cycles) for start, end in self._relative[rel]]
            self._mins[rel] = min((end_ts - start_ts) & 0xFFFFFFFF for start_ts, end_ts in timestamps)
            self._maxs[rel] = max((end_ts - start_ts) & 0xFFFFFFFF for start_ts, end_ts in timestamps)
            self._average[rel] = mean((end_ts - start_ts) & 0xFFFFFFFF for start_ts, end_ts in timestamps)

        for rel in self._relative.keys():
            print("tag pair:%s, min:%f, max:%f, ave:%f" % (rel,
                   counts_to_msec(self._mins[rel]),
                   counts_to_msec(self._maxs[rel]),
                   counts_to_msec(self._average[rel])))

        if self._in_records[0].seq_number == 0:
            startup_time = self._in_records[tags_index[0][393][0]].cycles
            print("start-up time:%f" % (counts_to_msec(startup_time)))
            assert startup_time == self._in_records[0].cycles

class Parser:
    def __init__(self):
        self._tmp_in_data = []
        self._prev_timestamp = 0

    def binary_stream_to_records(self, in_data) -> Tuple[tuple, ...]:
        self._tmp_in_data.extend(in_data)
        out_data = []
        while len(self._tmp_in_data) >= RECORD_SIZE:
            i = 0
            record_found = False
            for i in range(len(self._tmp_in_data) - MARKER_SIZE + 1):
                footer = int.from_bytes(self._tmp_in_data[i:i + MARKER_SIZE], byteorder='little', signed=False)
                if footer == FOOTER:
                    rec_limit = i + MARKER_SIZE
                    if rec_limit >= RECORD_SIZE:
                        header = int.from_bytes(self._tmp_in_data[rec_limit - RECORD_SIZE:rec_limit - (RECORD_SIZE - MARKER_SIZE)], byteorder='little', signed=False)
                        if header == HEADER:
                            record_found = True
                            payload_start = rec_limit - (RECORD_SIZE - MARKER_SIZE)
                            record = tuple(self._tmp_in_data[payload_start:payload_start + PAYLOAD_SIZE])
                            out_data.append(record)
                            # remove from buffer all the data that has been parsed
                            self._tmp_in_data = self._tmp_in_data[rec_limit:len(self._tmp_in_data)]
                        break # get out of the loop that looks for a footer
            if not record_found:
                # remove from buffer all bytes that are guaranteed no to form part of a partial record
                # Worst case is that only one byte is missing to have a complete record, so we can
                # safely remove data until we leave RECORD_SIZE - 1 bytes in the buffer.
                # Note that 'i' iterates up to buffer_size - MARKER_SIZE
                self._tmp_in_data = self._tmp_in_data[(i - (RECORD_SIZE - MARKER_SIZE - 1)):len(self._tmp_in_data)]
        return tuple(out_data)

    @staticmethod
    def parse_records(raw_records) -> Tuple[ProfilerRecord, ...]:
        out_data = []
        for rec in raw_records:
            tag = int.from_bytes(rec[TAG_OFFSET:TAG_OFFSET + TAG_SIZE], byteorder='little', signed=False)
            cycles = int.from_bytes(rec[CYCLES_OFFSET:CYCLES_OFFSET + CYCLES_SIZE], byteorder='little', signed=False)
            seq_number = int.from_bytes(rec[SEQ_NUMBER_OFFSET:SEQ_NUMBER_OFFSET + SEQ_NUMBER_SIZE], byteorder='little', signed=False)
            out_data.append(ProfilerRecord(tag=tag, seq_number=seq_number, cycles=cycles))
        return tuple(out_data)


class ProfilerExecutor(threading.Thread):
    def __init__(self, jlink, parser : Parser, profiler : Profiler):
        super(ProfilerExecutor, self).__init__()
        self._jlink = jlink
        self._stop_event = threading.Event()
        self._parser = parser
        self._profiler = profiler

    def stop_capture(self):
        self._stop_event.set()

    def stop_requested(self):
        return self._stop_event.is_set()

    def run(self):
        """
        This method is a polling loop against the connected JLink unit. If
        the JLink is disconnected, it will exit. Additionally, if any exceptions
        are raised, they will be caught and re-raised after interrupting the
        main thread.

        Raises:
          Exception on error.

        """
        try:

            while self._jlink.connected() and not self.stop_requested():
                in_data = self._jlink.rtt_read(1, 1024)
                parsed_data = self._parser.parse_records(self._parser.binary_stream_to_records(in_data))
                counters = tuple(record.seq_number for record in parsed_data)
                print(counters)
                if len(parsed_data) > 0:
                    self._profiler.add_data(parsed_data)
                time.sleep(0.01)
            self._profiler.process_data()
        except Exception:
            # this might require some rework as the exception must be catched by the main thread.
            print("IO read thread exception, exiting...")
            _thread.interrupt_main()
            raise

    def start_capture(self, rtt_block_address: int):
        """
        Returns:
          Always returns ``0`` or a JLinkException.

        Raises:
          JLinkException on error.
        """
        self._jlink.exec_command(f'SetRTTAddr {hex(rtt_block_address)}')
        while True:
            try:
                print("connected, starting RTT...")
                self._jlink.rtt_start()
                num_up = self._jlink.rtt_get_num_up_buffers()
                num_down = self._jlink.rtt_get_num_down_buffers()
                print("RTT started, %du p bufs, %d down bufs." % (num_up, num_down))
                break
            except pylink.errors.JLinkRTTException as e:
                print(e)
                time.sleep(0.01)

        if self._jlink.halted():
            print("CPU halted")
            while True:
                in_data = self._jlink.rtt_read(1, 1024)
                time.sleep(0.01)
                in_data = self._jlink.rtt_read(1, 1024)
                if len(in_data) == 0:
                    break
                if not self._jlink.connected() or self.stop_requested():
                    break
        else:
            total_length = 0
            while True:
                in_data = self._jlink.rtt_read(1, 1024)
                total_length += len(in_data)
                if total_length > 43:
                    break
                if not self._jlink.connected() or self.stop_requested():
                    break

        super(ProfilerExecutor, self).start()


def test_sample(parser : Parser, profiler : Profiler):
    pass
    # profiler.add_data(parser.parse_records(parser.binary_stream_to_records(in_data=raw_data)))
    # profiler.process_data()


def test_initial_draft():

    def delta10(in_record : ProfilerRecord):
        out_record = ProfilerRecord(tag=in_record.tag, seq_number=in_record.seq_number + 10, cycles=in_record.cycles)
        return out_record

    in_records1 = (ProfilerRecord(tag=393, seq_number=0, cycles=722940), ProfilerRecord(tag=787, seq_number=1, cycles=864254), ProfilerRecord(tag=393, seq_number=2, cycles=872227), ProfilerRecord(tag=787, seq_number=3, cycles=872880), ProfilerRecord(tag=393, seq_number=4, cycles=878001), ProfilerRecord(tag=787, seq_number=5, cycles=878619), ProfilerRecord(tag=393, seq_number=6, cycles=880657), ProfilerRecord(tag=787, seq_number=7, cycles=881274), ProfilerRecord(tag=393, seq_number=8, cycles=888420), ProfilerRecord(tag=787, seq_number=9, cycles=889030), ProfilerRecord(tag=393, seq_number=10, cycles=891726), ProfilerRecord(tag=787, seq_number=11, cycles=892345), ProfilerRecord(tag=393, seq_number=12, cycles=914229), ProfilerRecord(tag=787, seq_number=13, cycles=915316))
    in_records2 = tuple(map(delta10, in_records1))
    in_records = in_records1 + in_records2
    # relative_measurements = (RelativeMeasure(393, 787),RelativeMeasure(222, 333), RelativeMeasure(393, 393))
    relative_measurements = (RelativeMeasure(393, 787), RelativeMeasure(393, 393))
    profiler1 = Profiler(relative_measurements)
    profiler1.add_data(in_records)
    profiler1.process_data()


def tuple_to_profiler_record(t : Tuple[int, int, int]):
    return ProfilerRecord(tag=t[0], seq_number=t[1], cycles=t[2])

def test_unaligned_chunks_parsing(parser):

    in_data = [16, 16, 137, 1, 36, 104, 12, 0, 0, 0, 32, 32, 16, 16, 19, 3, 22, 141, 14, 0, 1, 0, 32, 32, 16, 16, 137, 1, 59, 172, 14, 0, 2, 0, 32, 32, 16, 16, 19, 3, 200, 174, 14, 0, 3, 0, 32, 32, 16, 16, 137, 1, 1, 186, 14, 0, 4, 0, 32, 32, 16, 16, 19, 3, 64, 190, 14, 0, 5, 0, 32, 32, 16, 16, 137, 1, 201, 194, 14, 0, 6, 0, 32, 32, 16, 16, 19, 3, 56, 197, 14, 0, 7, 0, 32, 32, 16, 16, 137, 1, 45, 205, 14, 0, 8, 0, 32, 32, 16, 16, 19, 3, 152, 207, 14, 0, 9, 0, 32, 32, 16, 16, 137, 1, 124, 235, 14, 0, 10, 0, 32, 32, 16, 16, 19, 3, 224, 237, 14, 0, 11, 0, 32, 32, 16, 16, 137, 1, 118, 248, 14, 0, 12, 0, 32, 32, 16, 16, 19, 3, 227, 250, 14, 0, 13, 0, 32, 32]
    pre_parsed_data = ((393, 0, 813092), (787, 1, 953622), (393, 2, 961595), (787, 3, 962248), (393, 4, 965121), (787, 5, 966208), (393, 6, 967369), (787, 7, 967992), (393, 8, 970029), (787, 9, 970648), (393, 10, 977788), (787, 11, 978400), (393, 12, 981110), (787, 13, 981731))
    expected_parsed_data = tuple(map(tuple_to_profiler_record, pre_parsed_data))

    for i in range(len(in_data)):
        in_data_bottom = in_data[0:i]
        in_data_top = in_data[i:len(in_data)]
        parsed_data_bottom = parser.parse_records(parser.binary_stream_to_records(in_data_bottom))
        parsed_data_top = parser.parse_records(parser.binary_stream_to_records(in_data_top))
        parsed_data = parsed_data_bottom + parsed_data_top
        assert parsed_data == expected_parsed_data


def test_random_invalid_data(parser):
    in_data = []
    for x in range(0, 128):
        in_data.append(random.randint(0, 255))
    empty_tuple = ()
    parsed_data = parser.binary_stream_to_records(in_data)
    assert parsed_data == empty_tuple


def test_repeated_footer(parser):
    in_data = []
    for x in range(0, 128):
        in_data.append(32)
    empty_tuple = ()
    parsed_data = parser.binary_stream_to_records(in_data)
    assert parsed_data == empty_tuple


def test_data_same_as_footer(parser):
    in_data = [16, 16, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 16, 16, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]
    pre_parsed_data = ((0x2020, 0x2020, 0x20202020), (0x2020, 0x2020, 0x20202020))
    expected_parsed_data = tuple(map(tuple_to_profiler_record, pre_parsed_data))
    parsed_data = parser.parse_records(parser.binary_stream_to_records(in_data))
    assert parsed_data == expected_parsed_data

def test_garbage_between_records(parser):

    in_data = [16, 16, 137, 1, 36, 104, 12, 0, 0, 0, 32, 32, 16, 16, 19, 3, 22, 141, 14, 0, 1, 0, 32, 32, 18, 54, 152, 190, 118, 212, 97, 80, 237, 109, 39, 35, 16, 16, 16, 32, 16, 16, 137, 1, 59, 172, 14, 0, 2, 0, 32, 32, 16, 16, 19, 3, 200, 174, 14, 0, 3, 0, 32, 32, 16, 16, 137, 1, 1, 186, 14, 0, 4, 0, 32, 32, 32, 32, 194, 249, 252, 207, 51, 16, 32, 32, 16, 16, 16, 16, 19, 3, 64, 190, 14, 0, 5, 0, 32, 32, 16, 16, 137, 1, 201, 194, 14, 0, 6, 0, 32, 32, 16, 16, 19, 3, 56, 197, 14, 0, 7, 0, 32, 32, 16, 16, 137, 1, 45, 205, 14, 0, 8, 0, 32, 32, 16, 16, 19, 3, 152, 207, 14, 0, 9, 0, 32, 32, 16, 16, 137, 1, 124, 235, 14, 0, 10, 0, 32, 32, 140, 16, 16, 19, 3, 224, 237, 14, 0, 11, 0, 32, 32, 16, 16, 137, 1, 118, 248, 14, 0, 12, 0, 32, 32, 16, 16, 19, 3, 227, 250, 14, 0, 13, 0, 32, 32, 11, 0, 32, 32, 16, 16, 137, 1, 12, 0, 32, 32, 15, 18, 19, 3, 13, 0, 32, 32 ]
    pre_parsed_data = ((393, 0, 813092), (787, 1, 953622), (393, 2, 961595), (787, 3, 962248), (393, 4, 965121), (787, 5, 966208), (393, 6, 967369), (787, 7, 967992), (393, 8, 970029), (787, 9, 970648), (393, 10, 977788), (787, 11, 978400), (393, 12, 981110), (787, 13, 981731))
    expected_parsed_data = tuple(map(tuple_to_profiler_record, pre_parsed_data))

    for i in range(len(in_data)):
        in_data_bottom = in_data[0:i]
        in_data_top = in_data[i:len(in_data)]
        parsed_data_bottom = parser.parse_records(parser.binary_stream_to_records(in_data_bottom))
        parsed_data_top = parser.parse_records(parser.binary_stream_to_records(in_data_top))
        parsed_data = parsed_data_bottom + parsed_data_top
        assert parsed_data == expected_parsed_data

if __name__ == "__main__":
    # test_initial_draft()
    parser_under_test = Parser()
    profiler = Profiler(relative_measurements=(RelativeMeasure(393, 787), RelativeMeasure(393, 393)))

    # test_sample(parser_under_test, profiler)

    test_unaligned_chunks_parsing(parser_under_test)
    test_random_invalid_data(parser_under_test)
    test_garbage_between_records(parser_under_test)
    test_repeated_footer(parser_under_test)
    test_data_same_as_footer(parser_under_test)

    target_device = 'NRF52840_XXAA'
    jlink = pylink.JLink()
    print("connecting to JLink...")
    jlink.open()
    print("connecting to %s..." % target_device)
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.set_speed(12000)
    jlink.connect(target_device)

    profiler_exec = ProfilerExecutor(jlink, parser_under_test, profiler)
    # jlink.reset(halt=True)
    profiler_exec.start_capture(0x20004858)
    # profiler_exec.start_capture(0x200041c8)
    # jlink.restart()

    try:
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        pass
    finally:
        profiler_exec.stop_capture()
        profiler_exec.join()
