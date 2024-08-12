#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.tools.hidppthreadutils
:brief: HID++ thread utils classes
:author: Stanislas Cottard
:date: 2021/08/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from collections import deque
from types import MethodType

from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1Model
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.tools.threadutils import QueueWithFilter
from pylibrary.tools.threadutils import RLockedDict
from pytransport.transportmessage import TransportMessage


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReceiverMultiHidppQueue(QueueWithFilter):
    """
    Queue for a receiver. It will have multiple queue inside. This implementation will lose the concept of blocking
    in put and get since the queues used inside will always be blocking.
    """
    DUMP_QUEUE_INDEX = -1

    def __init__(self, maxsize=0):
        # See ``QueueWithFilter.__init__``
        self._queue_order = None
        self.queues = None
        self._receiver_event_table = Hidpp1Model.get_available_events_map()
        super().__init__(maxsize=maxsize)
    # end def __init__

    def __del__(self):
        while len(self.queues) > 0:
            device_index = next(iter(self.queues))
            self._remove_device_index_queue(device_index=device_index)
        # end while
    # end def __del__

    def add_device_index_queue(self, device_index, associated_queue):
        """
        Add a new device index and its associated queue in the queues' dictionary. This is a thread safe method
        using a mutex. This will wrap the ``_get`` and ``_put`` methods to keep the order to the multiple queue, thus
        adding two more methods (``_official_get`` and ``_official_put``) as attributes to the given queue.

        :param device_index: The device index to add
        :type device_index: ``int``
        :param associated_queue: The queue for this device index
        :type associated_queue: ``QueueWithFilter``
        """
        with self.mutex:
            self._add_device_index_queue(device_index=device_index, associated_queue=associated_queue)
        # end with
    # end def add_device_index_queue

    def remove_device_index_queue(self, device_index):
        """
        Remove a device index and its associated queue in the queues' dictionary. The messages in the queue will be
        lost. The removed queue is returned. This is a thread safe method using a mutex. The wrap of the ``_get`` and
        ``_put`` methods will be removed, thus removing the two methods added in add_device_index_queue
        (``_official_get`` and ``_official_put``). This method cannot be used to remove the default queues:

        * ``ReceiverMultiHidppQueue.DUMP_QUEUE_INDEX``
        * ``Hidpp1Data.DeviceIndex.TRANSCEIVER``

        :param device_index: The device index to remove
        :type device_index: ``int``

        :return: Removed queue
        :rtype: ``QueueWithFilter``

        :raise ``AssertionError``: If ``device_index`` is not in the dictionary's keys
        """
        # Sanity check
        assert device_index not in [ReceiverMultiHidppQueue.DUMP_QUEUE_INDEX, Hidpp1Data.DeviceIndex.TRANSCEIVER], \
            f"Cannot remove the device index for the dump queue or the receiver"

        with self.mutex:
            return self._remove_device_index_queue(device_index=device_index)
        # end with
    # end def remove_device_index_queue

    # Initialize the queue representation, this will be called in ``QueueWithFilter.__init__``
    def _init(self, maxsize):
        """
        Initialize the dictionary of queues. This dictionary have the device indexes as keys. The receiver's device
        index (0xFF) and a dump index are automatically added. Use ``add_device_index_queue`` to add new device indexes.

        :param maxsize: Unused parameter inherited from ``QueueWithFilter``, it will be ignored in this method
        :type maxsize: ``object``
        """
        self.queues = RLockedDict()

        dump_queue = QueueWithFilter()
        receiver_queue = QueueWithFilter()
        self._queue_order = deque()

        self._add_device_index_queue(
            device_index=ReceiverMultiHidppQueue.DUMP_QUEUE_INDEX, associated_queue=dump_queue)
        self._add_device_index_queue(
            device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER, associated_queue=receiver_queue)
    # end def _init

    def _qsize(self):
        """
        Get the total number of elements in all queues.

        :return: The size of this multi-queue
        :rtype: ``int``
        """
        size = 0
        with self.queues:
            for device_index in self.queues:
                size += self.queues[device_index].qsize()
            # end for
        # end with
        return size
    # end def _qsize

    # Put a new item in the queue
    def _put(self, item):
        """
        Put a transport message to the associated queue based on the device index. If the device index in the message
        is not present in the queue dictionary's key, the receiver's queue (0xFF) will be used by default.

        :param item: Transport message to put in the associated queue
        :type item: ``TransportMessage``

        :raise ``AssertionError``: If the item is not a ``TransportMessage`` or the item's data is None
        """
        # Sanity check
        assert isinstance(item, TransportMessage), f"Cannot put a(n) {item.__class__.__name__} in the queue, " \
                                                   f"it should be a TransportMessage (or a child class)"
        assert item.data is not None, f"Cannot put an empty {item.__class__.__name__} in the queue"

        device_index = ReceiverMultiHidppQueue.DUMP_QUEUE_INDEX

        if len(item.data) >= Hidpp1Data.Offset.SUB_ID and \
                item.data[Hidpp1Data.Offset.SUB_ID] in self._receiver_event_table.keys():
            """
            According to https://sites.google.com/a/logitech.com/samarkand/appendix/hid-2-0-protocol-definition, some 
            feature_index can be send by the receiver in HID++ 1 with the index matching the device and not
            the receiver one (0xFF): 64 (0x40), 65 (0x41), 73 (0x49), 75 (0x4B), 143 (0x8F)
            """
            device_index = Hidpp1Data.DeviceIndex.TRANSCEIVER
        elif len(item.data) >= HidppMessage.OFFSET.DEVICE_INDEX:
            device_index = item.data[HidppMessage.OFFSET.DEVICE_INDEX]
        # end if

        with self.queues:
            if device_index not in self.queues.keys():
                # For now the default queue is the receiver one and not the dump queue
                # device_index = ReceiverMultiHidppQueue.DUMP_QUEUE_INDEX
                device_index = Hidpp1Data.DeviceIndex.TRANSCEIVER
            # end if

            self.queues[device_index].put(item)
        # end with
    # end def _put

    # Get an item from the queue
    def _get(self):
        """
        Get the next transport message according to the fifo arrival order.

        :return: The next transport message
        :rtype: ``TransportMessage``
        """
        # The value in the ``_queue_order`` will be removed in the get method of the queue (mechanism added in
        # ``add_device_index_queue``)
        with self.queues:
            return self.queues[self._queue_order[0]].get()
        # end with
    # end def _get

    def _add_device_index_queue(self, device_index, associated_queue):
        """
        Add a new device index and its associated queue in the queues' dictionary.

        :param device_index: The device index to add
        :type device_index: ``int``
        :param associated_queue: The queue for this device index
        :type associated_queue: ``QueueWithFilter``

        :raise ``AssertionError``: If ``device_index`` is already in the dictionary's keys
        """

        def sync_get(queue_self):
            """
            Method to synchronize the get method of the queue to add with this structure. It will permit to keep the
            right order for the messages in this structure while still being able to get a message directly from the
            added queue.

            :param queue_self: The self of the added queue
            :type queue_self: ``QueueWithFilter``

            :return: First item in the queue
            :rtype: ``object``
            """
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            item = queue_self._official_get()
            # Remove the first occurrence of this queue in the queue order
            self._queue_order.remove(device_index)
            return item
        # end def sync_get

        def sync_put(queue_self, item):
            """
            Method to synchronize the put method of the queue to add with this structure. It will permit to keep the
            right order for the messages in this structure while still being able to get a message directly from the
            added queue.

            :param queue_self: The self of the added queue
            :type queue_self: ``QueueWithFilter``
            :param item: Item to put in the queue
            :type item: ``object``
            """
            # noinspection PyUnresolvedReferences
            # noinspection PyProtectedMember
            queue_self._official_put(item=item)
            # Append this device_index to the ordered queue
            self._queue_order.append(device_index)
        # end def sync_put

        with self.queues:
            # Sanity check
            assert device_index not in self.queues, f"Cannot add the same device index ({device_index}) twice"

            # noinspection PyProtectedMember
            associated_queue._official_get = associated_queue._get
            associated_queue._get = MethodType(sync_get, associated_queue)
            # noinspection PyProtectedMember
            associated_queue._official_put = associated_queue._put
            associated_queue._put = MethodType(sync_put, associated_queue)
            self.queues[device_index] = associated_queue
        # end with
    # end def _add_device_index_queue

    def _remove_device_index_queue(self, device_index):
        """
        Remove a device index and its associated queue in the queues' dictionary. The messages in the queue will be
        lost. The removed queue is returned.

        :param device_index: The device index to remove
        :type device_index: ``int``

        :return: Removed queue
        :rtype: ``QueueWithFilter``

        :raise ``AssertionError``: If ``device_index`` is not in the dictionary's keys
        """
        with self.queues:
            # Sanity check
            assert device_index in self.queues, f"Cannot remove a device index ({device_index}) not present"

            removed_queue = self.queues.pop(device_index)
            # noinspection PyProtectedMember
            removed_queue._get = removed_queue._official_get
            delattr(removed_queue, "_official_get")
            # noinspection PyProtectedMember
            removed_queue._put = removed_queue._official_put
            delattr(removed_queue, "_official_put")
            self._queue_order = deque([x for x in self._queue_order if x != device_index])
        # end with

        return removed_queue
    # end def _remove_device_index_queue
# end class ReceiverMultiHidppQueue

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
