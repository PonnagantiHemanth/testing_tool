#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pylibrary.system.tracelogger
:brief: Trace logger class
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from _io import TextIOWrapper
from enum import IntEnum
from enum import auto
from os import W_OK
from os import access
from os import path
from sys import stdout
from threading import RLock
from time import perf_counter_ns
from weakref import ref

from pylibrary.tools.threadutils import synchronize_with_object_inner_lock

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
# Unit to divider of the timestamp in nanosecond for all transport packet trace
TIMESTAMP_UNIT_DIVIDER_MAP = {
    's': 1e9,
    'ms': 1e6,
    'us': 1e3,
    'ns': 1
}
# This can the value 's', 'ms', 'us' or 'ns'
TIMESTAMP_UNIT = 'ms'


class TraceLevel(IntEnum):
    """
    Enumeration of the trace levels.
    """
    NO_TRACE = 0
    ERROR = auto()
    WARNING = auto()
    INFO = auto()
    DEBUG = auto()
    EXTRA_DEBUG = auto()

    RFU = auto()
# end class TraceLevel


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TraceLogger:
    """
    Trace logger. It is a subscription based logger, any object that wants to use it needs to subscribe to it.
    """
    class _SubscribedOwnerInfo:
        """
        Structure with an owner info.
        """
        def __init__(self):
            self.level = TraceLevel.NO_TRACE
            self.output = None
            self.name = None
            self.linked_owners_info = []
        # end def __init__
    # end class _SubscribedOwnerInfo

    _SINGLETON = None

    @staticmethod
    def get_instance():
        if TraceLogger._SINGLETON is None:
            TraceLogger._SINGLETON = TraceLogger()
        # end if

        return TraceLogger._SINGLETON
    # end def get_instance

    def __init__(self):
        self._lock = RLock()
        self._trace_table = {}
        self._setting_linked_trace_level = []
    # end def __init__

    def __del__(self):
        """
        Destroy the object.
        """
        self.unsubscribe_all()
    # end def __del__

    def _sanity_check(self, subscription_owner):
        """
        Perform a sanity check for a subscription owner.

        :param subscription_owner: Subscription owner to check
        :type subscription_owner: ``object``

        :return: Flag indicating the subscription_owner is good to be used
        :rtype: ``bool``
        """
        return subscription_owner is not None and ref(subscription_owner) in self._trace_table
    # end def _sanity_check

    def _set_trace_level(self, subscription_owner_info, trace_level=TraceLevel.NO_TRACE):
        """
        Set a trace level for a subscription owner. This is a private function and should only be used inside
        this class.

        :param subscription_owner_info: Weak reference to the subscription owner of the trace output
        :type subscription_owner_info: ``TraceLogger._SubscribedOwnerInfo``
        :param trace_level: The wanted trace level. Standard values can be found in
                            ``TraceLevel`` enumeration - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        """
        # This list mechanism is to avoid infinite recursive call
        if subscription_owner_info not in self._setting_linked_trace_level:
            trace_level = TraceLevel(trace_level)
            subscription_owner_info.level = trace_level
            self._setting_linked_trace_level.append(subscription_owner_info)
            for owner_info in subscription_owner_info.linked_owners_info:
                self._set_trace_level(subscription_owner_info=owner_info, trace_level=trace_level)
            # end for
        # end if
    # end def _set_trace_level

    @staticmethod
    def _set_trace_output(subscription_owner_info, trace_file_name=None):
        """
        Set a trace output for a subscription owner. This is a private function and should only be used inside
        this class.

        :param subscription_owner_info: Weak reference to the subscription owner of the trace output
        :type subscription_owner_info: ``TraceLogger._SubscribedOwnerInfo``
        :param trace_file_name: The wanted trace output as a file name. If ``None``, ``sys.stdout`` will be
                                used - OPTIONAL
        :type trace_file_name: ``str`` or ``None``

        :raise ``ValueError``: If ``trace_file_name`` is neither ``str`` nor ``None``, or if it is neither a writable
                               target nor accessible
        """
        if trace_file_name is None:
            trace_output = stdout
        elif path.exists(trace_file_name):
            if path.isfile(trace_file_name):
                # also works when file is a link and the target is writable
                if access(trace_file_name, W_OK):
                    trace_output = open(trace_file_name)
                else:
                    raise ValueError(f"The trace_file_name ({type(trace_file_name)}) parameter is not accessible")
                # end if
            else:
                raise ValueError(f"The trace_file_name ({type(trace_file_name)}) parameter is not a writable target")
            # end if
        else:
            raise ValueError(f"The trace_file_name ({type(trace_file_name)}) parameter should be a str or None")
        # end if
        subscription_owner_info.output = trace_output
    # end def _set_trace_output

    def _set_trace_name(self, subscription_owner, trace_name=None):
        """
        Set a trace name for a subscription owner. This is a private function and should only be used inside
        this class.

        :param subscription_owner: The subscription owner of the trace output
        :type subscription_owner: ``object``
        :param trace_name: The wanted trace name. If ``None``, the name of the class of ``subscription_owner`` will
                           be used - OPTIONAL
        :type trace_name: ``str`` or ``None``

        :raise ``ValueError``: If ``trace_name`` is neither ``str`` nor ``None``
        """
        if trace_name is None:
            trace_name = subscription_owner.__class__.__name__
        elif not isinstance(trace_name, str):
            raise ValueError(f"The trace_name parameter should be a str or None, {type(trace_name)} was given")
        # end if
        self._trace_table[ref(subscription_owner)].name = trace_name
    # end def _set_trace_name

    @synchronize_with_object_inner_lock("_lock")
    def subscribe(self, subscription_owner, trace_level=TraceLevel.NO_TRACE, trace_file_name=None, trace_name=None,
                  linked_owner=None):
        """
        Subscribe a new owner to the trace logger. It cannot already be subscribed.

        :param subscription_owner: Subscription owner to add
        :type subscription_owner: ``object``
        :param trace_level: The wanted trace level. Standard values can be found in
                            ``TraceLevel`` enumeration - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: The wanted trace output as a file name. If ``None``, ``sys.stdout`` will be
                                used - OPTIONAL
        :type trace_file_name: ``str`` or ``None``
        :param trace_name: The wanted trace name. If ``None``, the name of the class of ``subscription_owner`` will
                           be used - OPTIONAL
        :type trace_name: ``str`` or ``None``
        :param linked_owner: The potential owner that ``subscription_owner`` is linked to. ``linked_owner`` should have
                             already subscribed prior because it means that its level and the one of
                             ``subscription_owner`` are always the same. If it is not ``None``, ``trace_level`` will
                             then be ignored and the one from ``linked_owner`` will be used - OPTIONAL
        :type linked_owner: ``object`` or ``None``

        :raise ``AssertionError``: If ``subscription_owner`` is ``None``, it has already subscribed or if
                                   ``linked_owner`` is not ``None`` and it has not subscribe prior to this call
        :raise ``ValueError``: If ``trace_file_name`` is neither ``str`` nor ``None``, or if it is neither a writable
                               target nor accessible, or if ``trace_name`` is neither ``str`` nor ``None``
        """
        assert subscription_owner is not None, "There should be an owner to a subscription"
        ref_subscription_owner = ref(subscription_owner)

        new_subscription_info = TraceLogger._SubscribedOwnerInfo()

        assert ref_subscription_owner not in self._trace_table, "Cannot subscribe an owner multiple time"
        self._trace_table[ref_subscription_owner] = new_subscription_info

        if linked_owner is None:
            self._setting_linked_trace_level.clear()
            self._set_trace_level(subscription_owner_info=new_subscription_info, trace_level=trace_level)
        else:
            ref_linked_owner = ref(linked_owner)
            assert ref_linked_owner in self._trace_table, "Cannot link to an unsubscribed owner"
            linked_owner_info = self._trace_table[ref_linked_owner]

            new_subscription_info.linked_owners_info.append(linked_owner_info)
            linked_owner_info.linked_owners_info.append(new_subscription_info)
            new_subscription_info.level = linked_owner_info.level
        # end if

        self._set_trace_output(subscription_owner_info=new_subscription_info, trace_file_name=trace_file_name)
        self._set_trace_name(subscription_owner=subscription_owner, trace_name=trace_name)
    # end def subscribe

    @synchronize_with_object_inner_lock("_lock")
    def unsubscribe(self, subscription_owner):
        """
        Unsubscribe an owner.

        :param subscription_owner: Subscription owner to unsubscribe
        :type subscription_owner: ``object``
        """
        owner_info = self._trace_table.pop(ref(subscription_owner), None)
        if owner_info is not None:
            out_file = owner_info.output
            if out_file != stdout and hasattr(out_file, "close"):
                out_file.close()
            # end if

            for linked_owner_info in owner_info.linked_owners_info:
                try:
                    linked_owner_info.linked_owners_info.remove(owner_info)
                except ValueError:
                    # Pass if the link is already gone
                    pass
                # end try
            # end for
        # end if
    # end def unsubscribe

    @synchronize_with_object_inner_lock("_lock")
    def is_subscribe(self, subscription_owner):
        """
        Check is an owner is subscribed or not.

        :param subscription_owner: Subscription owner to check, can be ``None`` (False will be returned)
        :type subscription_owner: ``object`` or ``None``

        :return: Flag indicating if the owner is subscribed
        :rtype: ``bool``
        """
        if subscription_owner is None:
            return False
        # end if

        return ref(subscription_owner) in self._trace_table
    # end def is_subscribe

    @synchronize_with_object_inner_lock("_lock")
    def unsubscribe_all(self):
        """
        Unsubscribe all owners.
        """
        for owner_info in self._trace_table.values():
            out_file = owner_info.output
            if out_file != stdout and hasattr(out_file, "close"):
                out_file.close()
            # end if
        # end for
        self._trace_table.clear()
    # end def unsubscribe_all

    @synchronize_with_object_inner_lock("_lock")
    def update_trace_level(self, subscription_owner, trace_level=TraceLevel.NO_TRACE):
        """
        Update a trace level for a subscription owner.

        :param subscription_owner: Subscription owner of the trace level
        :type subscription_owner: ``object``
        :param trace_level: The wanted trace level. Standard values can be found in
                            ``TraceLevel`` enumeration - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        """
        if not self._sanity_check(subscription_owner=subscription_owner):
            return
        # end if
        self._setting_linked_trace_level.clear()
        self._set_trace_level(
            subscription_owner_info=self._trace_table[ref(subscription_owner)], trace_level=trace_level)
    # end def update_trace_level

    @synchronize_with_object_inner_lock("_lock")
    def get_trace_level(self, subscription_owner):
        """
        Get the trace level of an owner.

        :param subscription_owner: Subscription owner of the trace level
        :type subscription_owner: ``object``

        :return: The trace level of the owner or ``None`` if the sanity check on the owner fails
        :rtype: ``TraceLevel`` or ``int`` or ``None``
        """
        if not self._sanity_check(subscription_owner=subscription_owner):
            return
        # end if
        return self._trace_table[ref(subscription_owner)].level
    # end def update_trace_level

    @synchronize_with_object_inner_lock("_lock")
    def update_trace_output(self, subscription_owner, trace_file_name=None):
        """
        Update a trace output for a subscription owner.

        :param subscription_owner: Subscription owner of the trace output
        :type subscription_owner: ``object``
        :param trace_file_name: The wanted trace output as a file name. If ``None``, ``sys.stdout`` will be
                                used - OPTIONAL
        :type trace_file_name: ``str`` or ``None``

        :raise ``AssertionError``: If a sanity check fails
        :raise ``ValueError``: If ``trace_file_name`` is neither ``str`` nor ``None``, or if it is neither a writable
                               target nor accessible
        """
        if not self._sanity_check(subscription_owner=subscription_owner):
            return
        # end if
        self._set_trace_output(
            subscription_owner_info=self._trace_table[ref(subscription_owner)], trace_file_name=trace_file_name)
    # end def update_trace_output

    @synchronize_with_object_inner_lock("_lock")
    def get_trace_output(self, subscription_owner):
        """
        Get the trace output of an owner. This will not be a name or a ``str`` but the ``TextIOWrapper`` object itself.

        :param subscription_owner: Subscription owner of the trace output
        :type subscription_owner: ``object``

        :return: The output object of the owner
        :rtype: ``TextIOWrapper``

        :raise ``AssertionError``: If a sanity check fails
        """
        if not self._sanity_check(subscription_owner=subscription_owner):
            return
        # end if
        return self._trace_table[ref(subscription_owner)].output
    # end def update_trace_output

    @synchronize_with_object_inner_lock("_lock")
    def update_trace_name(self, subscription_owner, trace_name=None):
        """
        Update a trace name for a subscription owner.

        :param subscription_owner: Subscription owner of the trace name
        :type subscription_owner: ``object``
        :param trace_name: The wanted trace name. If ``None``, the name of the class of ``subscription_owner`` will
                           be used - OPTIONAL
        :type trace_name: ``str`` or ``None``

        :raise ``AssertionError``: If a sanity check fails
        :raise ``ValueError``: If ``trace_name`` is neither ``str`` nor ``None``
        """
        if not self._sanity_check(subscription_owner=subscription_owner):
            return
        # end if
        self._set_trace_name(subscription_owner=subscription_owner, trace_name=trace_name)
    # end def update_trace_name

    @synchronize_with_object_inner_lock("_lock")
    def get_trace_name(self, subscription_owner):
        """
        Get the trace name of an owner.

        :param subscription_owner: Subscription owner of the trace name
        :type subscription_owner: ``object``

        :return: The trace name of the owner
        :rtype: ``str``

        :raise ``AssertionError``: If a sanity check fails
        """
        if not self._sanity_check(subscription_owner=subscription_owner):
            return
        # end if
        return self._trace_table[ref(subscription_owner)].name
    # end def get_trace_name

    @synchronize_with_object_inner_lock("_lock")
    def log_trace(self, subscription_owner, message, trace_level=TraceLevel.NO_TRACE, end_line="\n"):
        """
        Write the wanted message on the owner output. The log format is:

        [owner trace name][trace_level] message+end_line

        If the trace level of the owner is ``TraceLevel.NO_TRACE``, the trace_level argument is NO_TRACE or
        ``trace_level`` is higher than the trace level of the owner, this message log is not done and ignored.

        :param subscription_owner: Subscription owner to use
        :type subscription_owner: ``object``
        :param message: Message to trace in the log
        :type message: ``str``
        :param trace_level: The trace level of this message - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param end_line: End line string, by default it is a new line character. If ``None``, no end line is
                         added - OPTIONAL
        :type end_line: ``str``

        :raise ``AssertionError``: If a sanity check fails or if writing all the message on the output failed
        """
        # The timestamp is computed before anything else to get the best value
        timestamp = perf_counter_ns()

        if not self._sanity_check(subscription_owner=subscription_owner):
            return
        # end if

        if self._trace_table[ref(subscription_owner)].level == TraceLevel.NO_TRACE or \
                trace_level == TraceLevel.NO_TRACE or \
                trace_level > self._trace_table[ref(subscription_owner)].level:
            return
        # end if

        if end_line is None:
            end_line = ""
        # end if

        if isinstance(trace_level, TraceLevel):
            trace_level_print = trace_level.name
        elif 0 <= trace_level < TraceLevel.RFU:
            trace_level_print = TraceLevel(trace_level).name
        else:
            trace_level_print = trace_level
        # end if

        str_to_write = f"[{self._trace_table[ref(subscription_owner)].name}]" \
                       f"[{trace_level_print}]" \
                       f"[{timestamp / TIMESTAMP_UNIT_DIVIDER_MAP[TIMESTAMP_UNIT]:.2f}{TIMESTAMP_UNIT}]" \
                       f" {message}{end_line}"
        len_written = self._trace_table[ref(subscription_owner)].output.write(str_to_write)

        assert len_written == len(str_to_write), f"Could not write the wanted number of character for the log. " \
                                                 f"Expected {len(str_to_write)}, obtained {len_written}"
    # end def log_trace
# end class TraceLogger


class DummyOwner:
    """
    The only purpose of this class is to be able to subscribe a dummy owner for small trace. For example, just for one
    method that will then unsubscribe at the end.
    """
    pass
# end class DummyOwner


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
