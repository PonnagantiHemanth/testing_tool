#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.tools.hidppthreadutils
:brief: HID++ thread utils classes unit tests
:author: Stanislas Cottard
:date: 2021/08/25
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from random import randint
from unittest import TestCase

from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1NotificationMap
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.tools.hidppthreadutils import ReceiverMultiHidppQueue
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import QueueEmpty
from pylibrary.tools.threadutils import QueueWithFilter
from pytransport.transportmessage import TransportMessage

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
DEVICE_INDEX_FOR_TEST = 1
MAX_DEVICE_INDEX_FOR_TEST = 6


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReceiverMultiHidppQueueTestCase(TestCase):
    """
    Tests of the ``ReceiverMultiHidppQueue`` class
    """
    def test_creation_business(self):
        """
        Test creation of a ``ReceiverMultiHidppQueue`` object
        """
        test_object = ReceiverMultiHidppQueue()

        self.assertIsNotNone(obj=test_object.queues.get(ReceiverMultiHidppQueue.DUMP_QUEUE_INDEX, None),
                             msg="The dump queue should be added during creation")
        self.assertIsNotNone(obj=test_object.queues.get(Hidpp1Data.DeviceIndex.TRANSCEIVER, None),
                             msg="The receiver device index queue should be added during creation")
        self.assertIsInstance(obj=test_object.queues[ReceiverMultiHidppQueue.DUMP_QUEUE_INDEX],
                              cls=QueueWithFilter,
                              msg="The dump queue should be a QueueWithFilter object (or a child class)")
        self.assertIsInstance(
            obj=test_object.queues[Hidpp1Data.DeviceIndex.TRANSCEIVER],
            cls=QueueWithFilter,
            msg="The receiver device index queue should be a QueueWithFilter object (or a child class)")
    # end def test_creation_business

    def test_add_device_index_queue_business(self):
        """
        Test add_device_index_queue method of a ``ReceiverMultiHidppQueue`` object
        """
        queue_to_add = QueueWithFilter()
        test_object = ReceiverMultiHidppQueue()
        test_object.add_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST, associated_queue=queue_to_add)

        self.assertIsNotNone(obj=test_object.queues.get(DEVICE_INDEX_FOR_TEST, None),
                             msg=f"The device_index {DEVICE_INDEX_FOR_TEST} queue had not been added")
        self.assertEqual(first=queue_to_add,
                         second=test_object.queues[DEVICE_INDEX_FOR_TEST],
                         msg="The device_index {device_index} queue is not the expected one")
        self.assertTrue(expr=hasattr(queue_to_add, "_official_get"),
                        msg="The added queue should have the method _official_get added to its attribute")
        self.assertTrue(expr=hasattr(queue_to_add, "_official_put"),
                        msg="The added queue should have the method _official_put added to its attribute")
    # end def test_add_device_index_queue_business

    def test_remove_device_index_queue_business(self):
        """
        Test remove_device_index_queue method of a ``ReceiverMultiHidppQueue`` object
        """
        queue_to_add = QueueWithFilter()
        test_object = ReceiverMultiHidppQueue()
        test_object.add_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST, associated_queue=queue_to_add)
        queue_removed = test_object.remove_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST)

        self.assertEqual(first=queue_to_add,
                         second=queue_removed,
                         msg="Removed queue is not the one added")
        self.assertIsNone(obj=test_object.queues.get(DEVICE_INDEX_FOR_TEST, None),
                          msg=f"The device_index {DEVICE_INDEX_FOR_TEST} queue had not been removed")
        self.assertFalse(expr=hasattr(queue_to_add, "_official_get"),
                         msg="The removed queue should not have the method _official_get in its attribute list")
        self.assertFalse(expr=hasattr(queue_to_add, "_official_put"),
                         msg="The removed queue should not have the method _official_put in its attribute list")
    # end def test_remove_device_index_queue_business

    def test_put_business(self):
        """
        Test put method of a ``ReceiverMultiHidppQueue`` object
        """
        test_object = ReceiverMultiHidppQueue()
        # Create message with device index to the receiver
        item_to_put = self._create_transport_message()
        test_object.put(item=item_to_put)

        self.assertEqual(
            first=test_object.queues[Hidpp1Data.DeviceIndex.TRANSCEIVER].get(block=False),
            second=item_to_put, msg="The object is not in the expected queue")
    # end def test_put_business

    def test_get_business(self):
        """
        Test get method of a ``ReceiverMultiHidppQueue`` object
        """
        test_object = ReceiverMultiHidppQueue()
        item_to_put = self._create_transport_message()
        test_object.put(item=item_to_put)
        item_in_queue = test_object.get(block=False)

        self.assertEqual(first=item_in_queue,
                         second=item_to_put,
                         msg="The object is not in the queue")
    # end def test_get_business

    def test_qsize_business(self):
        """
        Test qsize method of a ``ReceiverMultiHidppQueue`` object
        """
        test_object = ReceiverMultiHidppQueue()
        # Create message with device index to the receiver
        item_to_put = self._create_transport_message()
        test_object.put(item=item_to_put)

        self.assertEqual(first=test_object.qsize(),
                         second=1,
                         msg="The measured length is not the expected one")
    # end def test_qsize_business

    def test_put_to_an_added_queue(self):
        """
        Test that the transport message goes in the right queue in a ``ReceiverMultiHidppQueue`` object
        """
        test_object = ReceiverMultiHidppQueue()
        test_object.add_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST, associated_queue=QueueWithFilter())
        item_to_put = self._create_transport_message(device_index=DEVICE_INDEX_FOR_TEST)
        test_object.put(item=item_to_put)

        self.assertEqual(first=test_object.queues[DEVICE_INDEX_FOR_TEST].get(block=False),
                         second=item_to_put,
                         msg="The object is not in the expected queue")
    # end def test_put_to_an_added_queue

    def test_put_to_an_unknown_queue(self):
        """
        Test that the transport message goes in the transceiver queue in a ``ReceiverMultiHidppQueue`` object is it
        has an unknown device index
        """
        test_object = ReceiverMultiHidppQueue()
        item_to_put = self._create_transport_message(device_index=DEVICE_INDEX_FOR_TEST)
        test_object.put(item=item_to_put)

        self.assertEqual(
            first=test_object.queues[Hidpp1Data.DeviceIndex.TRANSCEIVER].get(block=False),
            second=item_to_put, msg="The object is not in the expected queue")
    # end def test_put_to_an_unknown_queue

    def test_order_in_queue(self):
        """
        Test that the order in a ``ReceiverMultiHidppQueue`` object is respected
        """
        test_object = ReceiverMultiHidppQueue()
        self._create_put_get_and_check_order(test_object=test_object)
    # end def test_order_in_queue

    def test_add_device_index_keep_order_in_queue(self):
        """
        Test that the order in a ``ReceiverMultiHidppQueue`` object is respected even with an added queue in it
        """
        test_object = ReceiverMultiHidppQueue()
        test_object.add_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST, associated_queue=QueueWithFilter())
        self._create_put_get_and_check_order(test_object=test_object, different_device_index=True)
    # end def test_add_device_index_keep_order_in_queue

    def test_add_then_remove_device_index_keep_order_in_queue(self):
        """
        Test that the order in a ``ReceiverMultiHidppQueue`` object is respected even with an added queue in it
        is removed
        """
        queue_to_add = QueueWithFilter()
        test_object = ReceiverMultiHidppQueue()
        test_object.add_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST, associated_queue=queue_to_add)
        self._create_put_get_and_check_order(test_object=test_object, different_device_index=True)
        item_to_put_1 = self._create_transport_message(device_index=DEVICE_INDEX_FOR_TEST)
        item_to_put_2 = self._create_transport_message()
        test_object.put(item=item_to_put_1)
        test_object.put(item=item_to_put_2)
        queue_removed = test_object.remove_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST)
        item_in_queue_1 = test_object.get(block=False)

        self.assertEqual(first=queue_removed.get(block=False),
                         second=item_to_put_1,
                         msg="The first object put in the removed queue is not in the first one gotten from this queue")
        self.assertEqual(first=item_in_queue_1,
                         second=item_to_put_2,
                         msg="The second object put in the queue is not in the first one gotten from the multi queue")
    # end def test_add_then_remove_device_index_keep_order_in_queue

    def test_order_in_multi_queue_when_get_from_inside_queue(self):
        """
        Test that the order in a ``ReceiverMultiHidppQueue`` object is respected
        """
        test_object = ReceiverMultiHidppQueue()
        test_object.add_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST, associated_queue=QueueWithFilter())
        self._create_put_get_and_check_order(test_object=test_object, get_from_inside_queue=True)
    # end def test_order_in_multi_queue_when_get_from_inside_queue

    def test_multiple_add_same_device_index_queue_error(self):
        """
        Test multiple call of add_device_index_queue method of a ``ReceiverMultiHidppQueue`` object on the same device
        index raise an error
        """
        queue_to_add = QueueWithFilter()
        test_object = ReceiverMultiHidppQueue()
        test_object.add_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST, associated_queue=queue_to_add)

        exception = None
        try:
            test_object.add_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST, associated_queue=queue_to_add)
        except AssertionError as e:
            exception = e
        # end try

        self.assertIsNotNone(
            obj=exception,
            msg=f"No exception was risen when trying to add device index = {DEVICE_INDEX_FOR_TEST} the second time")
        self.assertEqual(first=str(exception),
                         second=f"Cannot add the same device index ({DEVICE_INDEX_FOR_TEST}) twice",
                         msg="Message of the exception is not the expected one when trying to add device "
                             f"index = {DEVICE_INDEX_FOR_TEST} the second time")
    # end def test_multiple_add_same_device_index_queue_error

    def test_remove_default_device_index_error(self):
        """
        Test remove_device_index_queue method of a ``ReceiverMultiHidppQueue`` object assert when device index is one
        of the default one
        """
        test_object = ReceiverMultiHidppQueue()
        for device_index in [ReceiverMultiHidppQueue.DUMP_QUEUE_INDEX, Hidpp1Data.DeviceIndex.TRANSCEIVER]:
            exception = None
            try:
                test_object.remove_device_index_queue(device_index=device_index)
            except AssertionError as e:
                exception = e
            # end try

            self.assertIsNotNone(
                obj=exception,
                msg=f"No exception was risen when trying to remove default device index = {device_index}")
            self.assertEqual(first=str(exception),
                             second="Cannot remove the device index for the dump queue or the receiver",
                             msg="Message of the exception is not the expected one when trying to remove default "
                                 f"device index = {device_index}")
        # end for
    # end def test_remove_default_device_index_error

    def test_remove_unknown_device_index_queue_error(self):
        """
        Test call of remove_device_index_queue method of a ``ReceiverMultiHidppQueue`` object on an unknown device
        index raise an error
        """
        test_object = ReceiverMultiHidppQueue()

        exception = None
        try:
            test_object.remove_device_index_queue(device_index=DEVICE_INDEX_FOR_TEST)
        except AssertionError as e:
            exception = e
        # end try

        self.assertIsNotNone(
            obj=exception,
            msg=f"No exception was risen when trying to remove unknown device index = {DEVICE_INDEX_FOR_TEST}")
        self.assertEqual(first=str(exception),
                         second=f"Cannot remove a device index ({DEVICE_INDEX_FOR_TEST}) not present",
                         msg="Message of the exception is not the expected one when trying to remove unknown "
                             f"device index = {DEVICE_INDEX_FOR_TEST}")
    # end def test_remove_unknown_device_index_queue_error

    def test_put_not_a_transport_message_error(self):
        """
        Test put method of a ``ReceiverMultiHidppQueue`` object raise an error if the item is not a ``TransportMessage``
        """
        test_object = ReceiverMultiHidppQueue()
        # Create an ``int`` instead of a ``TransportMessage``
        item_to_put = 1

        self._put_wrong_item_check_exception(test_object=test_object, wrong_item_to_put=item_to_put)
    # end def test_put_not_a_transport_message_error

    def test_put_an_empty_transport_message_error(self):
        """
        Test put method of a ``ReceiverMultiHidppQueue`` object raise an error if the item is an
        empty ``TransportMessage``
        """
        test_object = ReceiverMultiHidppQueue()
        # Create an empty ``TransportMessage``
        item_to_put = TransportMessage()

        self._put_wrong_item_check_exception(test_object=test_object, wrong_item_to_put=item_to_put)
    # end def test_put_an_empty_transport_message_error

    def test_put_a_hidpp1_notification_in_queue_ignore_device_index(self):
        """
        Test that the transport message goes in the right queue in a ``ReceiverMultiHidppQueue`` object
        """
        test_object = ReceiverMultiHidppQueue()
        for device_index in range(1, MAX_DEVICE_INDEX_FOR_TEST + 1):
            test_object.add_device_index_queue(device_index=device_index, associated_queue=QueueWithFilter())
        # end for

        for device_index in range(1, MAX_DEVICE_INDEX_FOR_TEST + 1):
            for sub_id in Hidpp1NotificationMap.get_available_events_map().keys():
                item_to_put = self._create_transport_message(device_index=device_index, hidpp1_sub_id=sub_id)
                test_object.put(item=item_to_put)

                with self.assertRaises(expected_exception=QueueEmpty):
                    test_object.queues[device_index].get(block=False)
                # end with
                self.assertEqual(
                    first=test_object.queues[Hidpp1Data.DeviceIndex.TRANSCEIVER].get(block=False),
                    second=item_to_put,
                    msg="The object put in the multi queue should be in the transceiver queue")
            # end for
        # end for
    # end def test_put_to_an_added_queue

    @staticmethod
    def _create_transport_message(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER, hidpp1_sub_id=0x00):
        """
        Create a transport message of short size (see ``HidppMessage.SHORT_MSG_SIZE``).

        :param device_index: The device index to use in the transport message - OPTIONAL
        :type device_index: ``int``
        :param hidpp1_sub_id: The Sub ID for a HID++ 1.0 message, by default it is 0 to avoid triggering an automatic
                              put in the transceiver queue - OPTIONAL
        :type hidpp1_sub_id: ``int``

        :return: The created transport message
        :rtype: ``TransportMessage``
        """
        transport_message = [randint(0x00, 0xFF)]*HidppMessage.SHORT_MSG_SIZE
        transport_message[Hidpp1Data.Offset.SUB_ID] = hidpp1_sub_id
        transport_message[HidppMessage.OFFSET.DEVICE_INDEX] = device_index
        return TransportMessage(data=HexList(transport_message))
    # end def _create_transport_message

    def _create_put_get_and_check_order(self, test_object, different_device_index=False, get_from_inside_queue=False):
        """
        Create two transport message, put them in the test object, get the first two element of the multi queue and
        then check if they are in the right order.

        :param test_object: The multi queue object to test
        :type test_object: ``ReceiverMultiHidppQueue``
        :param different_device_index: Flag indicating if the first transport message should have a different device
                                       index (``DEVICE_INDEX_FOR_TEST``) than the second one - OPTIONAL
        :type different_device_index: ``bool``
        :param get_from_inside_queue: Flag indicating if the first transport message should be gotten directly from
                                      its inside queue, this will automatically consider ``different_device_index``
                                      to True - OPTIONAL
        :type get_from_inside_queue: ``bool``
        """
        item_to_put_1 = self._create_transport_message(
            device_index=DEVICE_INDEX_FOR_TEST if different_device_index or get_from_inside_queue else None)
        item_to_put_2 = self._create_transport_message()
        test_object.put(item=item_to_put_1)
        test_object.put(item=item_to_put_2)
        if get_from_inside_queue:
            item_in_queue_1 = test_object.queues[DEVICE_INDEX_FOR_TEST].get(block=False)
        else:
            item_in_queue_1 = test_object.get(block=False)
        # end if
        item_in_queue_2 = test_object.get(block=False)

        self.assertEqual(first=item_in_queue_1,
                         second=item_to_put_1,
                         msg="The first object put in the queue is not in the first one gotten from the multi queue")
        self.assertEqual(first=item_in_queue_2,
                         second=item_to_put_2,
                         msg="The second object put in the queue is not in the second one gotten from the multi queue")
    # end def _create_put_get_and_check_order

    def _put_wrong_item_check_exception(self, test_object, wrong_item_to_put):
        """
        Put a wrong item in the test object and check that the right exception is risen.

        :param test_object: The multi queue object to test
        :type test_object: ``ReceiverMultiHidppQueue``
        :param wrong_item_to_put: Wrong item to put in the
        """
        exception = None
        try:
            test_object.put(item=wrong_item_to_put)
        except AssertionError as e:
            exception = e
        # end try

        self.assertIsNotNone(
            obj=exception,
            msg=f"No exception was risen when trying to put a wrong item in the multi queue: {wrong_item_to_put}")
        if isinstance(wrong_item_to_put, TransportMessage):
            self.assertEqual(first=str(exception),
                             second=f"Cannot put an empty {wrong_item_to_put.__class__.__name__} in the queue",
                             msg="Message of the exception is not the expected one when trying to put a wrong item "
                                 f"in the multi queue: {wrong_item_to_put}")
        else:
            self.assertEqual(first=str(exception),
                             second=f"Cannot put a(n) {wrong_item_to_put.__class__.__name__} in the queue, it should "
                                    "be a TransportMessage (or a child class)",
                             msg="Message of the exception is not the expected one when trying to put a wrong item "
                                 f"in the multi queue: {wrong_item_to_put}")
        # end if
    # end def _create_put_get_and_check_order
# end class ReceiverMultiHidppQueueTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
