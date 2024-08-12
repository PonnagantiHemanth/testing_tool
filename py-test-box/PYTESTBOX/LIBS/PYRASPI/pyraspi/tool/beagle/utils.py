#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.tool.beagle.utils
:brief: Beagle 480 USB analyser utils classes
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyraspi.tool.beagle.beagle_py import array_u08


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
IDLE_THRESHOLD = 2000

# Packet groups
SOF = 0
IN_ACK = 1
IN_NAK = 2
PING_NAK = 3
SPLIT_IN_ACK = 4
SPLIT_IN_NYET = 5
SPLIT_IN_NAK = 6
SPLIT_OUT_NYET = 7
SPLIT_SETUP_NYET = 8
KEEP_ALIVE = 9

# States used in collapsing state machine
IDLE = 0
IN = 1
PING = 3
SPLIT = 4
SPLIT_IN = 5
SPLIT_OUT = 7
SPLIT_SETUP = 8

# Size of packet queue.  At most this many packets will need to be alive at the same time.
QUEUE_SIZE = 3

# Disable COMBINE_SPLITS by setting to False.  Disabling
# will show individual split counts for each group (such as
# SPLIT/IN/ACK, SPLIT/IN/NYET, ...).  Enabling will show all the
# collapsed split counts combined.
COMBINE_SPLITS = True


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PacketInfo:
    """
    Packet information structure extracted by the Beagle USB analyser
    """
    def __init__(self):
        self.data = array_u08(1024)
        self.time_sop = 0
        self.time_sop_ns = 0
        self.time_duration = 0
        self.time_dataoffset = 0
        self.status = 0
        self.events = 0
        self.length = 0
    # end def __init__
# end class PacketInfo


class PacketQueue:
    """
    Queue used to store the packets that are saved during the collapsing process.

    The tail of the queue is always used to store the current packet.
    """
    def __init__(self):
        self._tail = 0
        self._head = 0
        self.pkt = [PacketInfo() for _ in range(QUEUE_SIZE)]
    # end def __init__

    def __getattr__(self, attr):
        if attr == 'tail':
            return self.pkt[self._tail]
        elif attr == 'head':
            return self.pkt[self._head]
        else:
            raise AttributeError(f"{attr} not an attribute of PacketQueue")
        # end if
    # end def __getattr__

    def save_packet(self):
        self._tail = (self._tail + 1) % QUEUE_SIZE
    # end def save_packet

    def is_empty(self):
        return self._tail == self._head
    # end def is_empty

    def clear(self, dequeue=False):
        """
        Clear the queue. If requested, return the dequeued elements.

        :param dequeue: Flag indicating to return the dequeued elements. - OPTIONAL
        :type dequeue: ``bool``

        :return: List of the dequeued elements
        :rtype: ``list``
        """
        if not dequeue:
            self._head = self._tail
            return []
        # end if

        packets = []
        while self._head != self._tail:
            packets.append(self.pkt[self._head])
            self._head = (self._head + 1) % QUEUE_SIZE
        # end while
        return packets
    # end def clear
# end class PacketQueue


class CollapseInfo:
    def __init__(self):
        # Timestamp when collapsing begins
        self.time_sop = 0
        # The number of packets collapsed for each packet group
        self.count = {SOF: 0, PING_NAK: 0, IN_ACK: 0, IN_NAK: 0, SPLIT_IN_ACK: 0, SPLIT_IN_NYET: 0, SPLIT_IN_NAK: 0,
                      SPLIT_OUT_NYET: 0, SPLIT_SETUP_NYET: 0, KEEP_ALIVE: 0}
    # end def __init__

    def clear(self):
        self.time_sop = 0
        for k in self.count:
            self.count[k] = 0
        # end for
    # end def clear
# end class CollapseInfo


# ==========================================================================
# UTILITY FUNCTIONS
# ==========================================================================
def timestamp_to_ns(stamp, samplerate_khz):
    """
    Convert the timestamp to nanoseconds precision

    :param stamp: Packet timestamp
    :type stamp: ``int``
    :param samplerate_khz: The configured sampling rate in kHz
    :type samplerate_khz: ``int``

    :return: the converted timestamp in nanoseconds
    :rtype: ``int``
    """
    return (stamp * 1000) // (samplerate_khz // 1000)
# end def timestamp_to_ns


def collapse(group, collapse_info, pkt_q):
    """
    Collapse a group of packets.  This involves incrementing the group counter and clearing the queue.
    If this is the first group to be collapsed, the collapse time needs to be set, which marks
    when this collapsing began.

    :param group: Packet groups id (ex. KEEP_ALIVE, SOF, )
    :type group: ``int``
    :param collapse_info: Collapsing counts and timing
    :type collapse_info: ``CollapseInfo``
    :param pkt_q: The queue to get the packet from
    :type pkt_q: ``PacketQueue``
    """
    collapse_info.count[group] += 1

    if collapse_info.time_sop == 0:
        if not pkt_q.is_empty:
            collapse_info.time_sop = pkt_q.head.time_sop
        else:
            collapse_info.time_sop = pkt_q.tail.time_sop
        # end if
    # end if
    pkt_q.clear()
# end def collapse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
