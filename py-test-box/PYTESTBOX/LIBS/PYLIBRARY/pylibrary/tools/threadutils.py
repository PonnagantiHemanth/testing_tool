#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.tools.threadutils
:brief: Various threading utilities
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/06/06
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import threading
from atexit import register
from collections import deque
from contextlib import contextmanager
from ctypes import c_long
from ctypes import py_object
from ctypes import pythonapi
from functools import wraps
from inspect import signature
from queue import Empty
from queue import Full
from queue import Queue
from sys import getswitchinterval
from sys import maxsize as sys_maxsize
from sys import setswitchinterval
from threading import Event
from threading import Lock
from threading import RLock
from threading import Thread
from threading import currentThread
from time import sleep
from time import time
from traceback import extract_stack
from traceback import format_exc
from traceback import format_list
from types import ClassMethodDescriptorType
from types import FunctionType
from types import MethodDescriptorType
from types import MethodType
from types import MethodWrapperType
from types import WrapperDescriptorType
from weakref import proxy

from locked_dict.locked_dict import LockedDict

from pylibrary.tools.docutils import DocUtils

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
GLOBAL_SYNCHRONIZATION_LOCKS = {}
GLOBAL_SYNCHRONIZATION_LOCK = Lock()


def synchronized(lock=None):
    """
    This is a decorator function.

    This function is used as a decorator for handling the synchronization of
    function/method access.

    It can be used without any argument, or with a Lock/RLock instance as an argument.

    If a lock is specified, it is used as a MUTEX for the function access.

    In the following example, @c myFunction and @c myOtherFunction cannot be
    called at the same time by different threads.
    @code
    myLock = RLock()

    @@synchronized(myLock)
    def myFunction():
        pass
    # end def myFunction

    @@synchronized(myLock)
    def myOtherFunction():
        pass
    # end def myOtherFunction
    @endcode

    In the following example, @c myFunction and @c myOtherFunction can be called
    at the same time by different threads. However, @c myFunction cannot be called
    at the same time by different threads, the same is true for @c myOtherFunction.

    @code
    @@synchronized
    def myFunction():
        pass
    # end def myFunction

    @@synchronized
    def myOtherFunction():
        pass
    # end def myOtherFunction
    @endcode

    :param lock: The lock that is used as a MUTEX (if not given, it will be the decorated function) - OPTIONAL
    :type lock: ``Lock`` or ``callable type``

    :return: An inner decorator that will handle the MUTEX
    :rtype: ``callable type``
    """

    if callable(lock):
        function = lock
        lock = None
    else:
        function = None
    # end if

    def wrapper(function_to_wrap):
        """
        Wrapper around the given function.

        :param function_to_wrap: The function to decorate
        :type function_to_wrap: ``callable type``

        :return: An inner decorator on the function
        :rtype: ``callable type``
        """
        assert callable(function_to_wrap), f"Can only wrap a callable type, {function_to_wrap}"

        inner_lock = lock

        # If no lock is specified, create a lock for the specified function.
        key = id(function_to_wrap)
        with GLOBAL_SYNCHRONIZATION_LOCK:
            if key not in GLOBAL_SYNCHRONIZATION_LOCKS:
                GLOBAL_SYNCHRONIZATION_LOCKS[key] = inner_lock if inner_lock is not None else RLock()
            # end if

            inner_lock = GLOBAL_SYNCHRONIZATION_LOCKS[key]
        # end with

        # Define the actual synchronization decorator
        def __caller__(*args, **kwargs):
            """
            The locking caller on the decorated function.

            :param args: The decorated function arguments
            :type args: ``tuple``
            :param kwargs: The decorated function keyword arguments
            :type kwargs: ``dict``

            :return: The decorated function return value
            :rtype: ``object`` or ``None``
            """
            with inner_lock:
                return function_to_wrap(*args, **kwargs)
            # end with
        # end def __caller__

        __caller__.__name__ = function_to_wrap.__name__                   # pylint:disable=W0621,W0622
        __caller__.__doc__ = function_to_wrap.__doc__                     # pylint:disable=W0621,W0622
        __caller__.__dict__.update(function_to_wrap.__dict__)

        return __caller__
    # end def wrapper

    # If no lock is specified, the wrapper will create one based on the function id.
    if function is not None:
        return wrapper(function)
    # end if

    return wrapper
# end def synchronized


def synchronize_with_object_inner_lock(inner_lock_attribute_name):
    """
    ONLY ON OBJECT METHODS

    Decorator to synchronize an object method with an inner object lock. The inner_lock_attribute_name parameter should
    be the name as a string of the lock attribute in the object.

    For example, it can be used to make a property thread safe:

    class LockedPropertyObject:
        def __init__(self, property_1):
            self._lock_property_1 = RLock()
            self.property_1 = property_1
        # end def __init__

        @property
        @synchronize_with_object_inner_lock("_lock_property_1")
        def property_1(self):
            return self.__property_1
        # end def property getter property_1

        @property_1.setter
        @synchronize_with_object_inner_lock("_lock_property_1")
        def property_1(self, value):
            self.__property_1 = value
        # end def property setter property_1
    # end class LockedPropertyObject

    :param inner_lock_attribute_name: The name as a string of the lock attribute in the object to use
    :type inner_lock_attribute_name: ``str``

    :return: An inner decorator that will handle the lock
    :rtype: ``callable type``
    """

    def synchronize(wrapped):
        """
        Wrapper around the given function

        :param wrapped: The function to decorate
        :type wrapped: ``callable type``

        :return: An inner decorator on the function
        :rtype: ``callable type``
        """
        @wraps(wrapped)
        def wrapper(*args, **kwargs):
            """
            The locking caller on the decorated function

            :param args: The decorated function arguments. Since this decorator is to use on an object method,
                         the first one will be self
            :type args: ``tuple``
            :param kwargs: The decorated function keyword arguments
            :type kwargs: ``dict``

            :return: The decorated function return value
            :rtype: ``object`` or ``None``
            """
            # Sanity checks
            assert args is not None and len(args) > 0 and isinstance(args[0], object), \
                "This decorator should only be called for methods in a class (not classmethod, nor staticmethod)"
            assert hasattr(args[0], inner_lock_attribute_name), \
                f"Inner lock does not exist: {inner_lock_attribute_name}"

            lock = getattr(args[0], inner_lock_attribute_name)
            with lock:
                return wrapped(*args, **kwargs)
            # end with
        # end def wrapper

        try:
            # Copy signature of the source method to the wrapper one
            wrapper.__signature__ = signature(wrapped)
        except ValueError:
            # Value error is raised when source_method signature does not exist, it should therefore not be a problem
            pass
        # end try
        return wrapper
    # end def synchronize
    return synchronize
# end def synchronize_with_object_inner_lock


def wait_for_any_lock(locks, timeout=None):
    """
    This method will attempt to acquire any of the Lock object in the given
    sequence, and return the lock that could be acquired.

    :param locks: The sequence of locks to monitor
    :type locks: ``tuple of Lock``
    :param timeout: A timeout value, in seconds, or None if no timeout is expected - OPTIONAL
    :type timeout: ``float``

    :return: The acquired Lock
    :rtype: ``Lock``
    """

    result = None
    time_quanta = 0.05

    # Only monitor existing locks
    if len(locks) > 0:
        # Iterate until a lock was acquired
        while result is None or (timeout is not None and timeout > 0):
            # Loop on all locks, and wait at the end of the loop.
            # Break as soon as ONE lock has been acquired
            for lock in locks:
                if lock.acquire(False):
                    result = lock
                    break
                # end if
            else:
                # Should decrement thread priority not to block other threads.
                # But this is not supported in Python <=2.5
                sleep(time_quanta)
                if timeout is not None:
                    timeout -= time_quanta
                # end if
            # end for
        # end while
    # end if
    return result
# end def wait_for_any_lock


@contextmanager
def acquire_timeout(lock, timeout):
    """
    Context manager to be used in a with statement to be able to acquire a lock with a timeout.

    :param lock: Lock to acquire
    :type lock: ``Lock``
    :param timeout: A timeout value, in seconds
    :type timeout: ``float``
    """
    result = lock.acquire(timeout=timeout)
    yield result
    if result:
        lock.release()
    # end if
# end def acquire_timeout


@contextmanager
def atomic_action():
    """
    Do an atomic action in a with statement.

    !! WARNING !! An atomic action is not truly possible in python 3.7 for threading. This atomic action is a hack that
    change the context switch count to an absurdly long value and then change it back to its initial value when the
    wanted action is done. This permit to avoid the context switch from periodic counting but if another action that
    trigger a context switch (like I/O (print for example), sleep, wait on a queue, etc...) is done inside the atomic
    action it will create a very bad behavior because it will still make a context switch and the counter will not be
    changed before we come back on the thread that called this.
    """
    current_count_interval = getswitchinterval()
    setswitchinterval(sys_maxsize)
    try:
        yield current_count_interval
    finally:
        setswitchinterval(current_count_interval)
    # end try
# end def atomic_action


def atomic_decorator(func):
    """
    Decorator to call the context management atomic_action.

    :return: An inner decorator that will handle the atomic action
    :rtype: ``callable type``
    """
    def wrapped_func(*args, **kwargs):
        """
        The atomic caller on the decorated function

        :param args: The decorated function arguments
        :type args: ``tuple``
        :param kwargs: The decorated function keyword arguments
        :type kwargs: ``dict``

        :return: The decorated function return value
        :rtype: ``object`` or ``None``
        """
        with atomic_action():
            return func(*args, **kwargs)
        # end with
    # end def wrapped_func
    return wrapped_func
# end def atomic_decorator


def synchronize_all_methods_of_a_class(class_to_use):
    """
    Create a new class inheriting from the one given in parameter and make all its methods synchronized on one inner
    lock. It creates an overhead of 20-30us on raspberry pi.

    :param class_to_use: Class to use to create the new class
    :type class_to_use: ``type``

    :return: New synchronized class
    :rtype: ``type``
    """
    class SynchronizedClass(class_to_use):
        def __init__(self, *args, **kwargs):
            self._inner_lock = RLock()
            super().__init__(*args, **kwargs)
        # end def __init__
    # end class SynchronizedClass

    all_method_types = (FunctionType,
                        WrapperDescriptorType,
                        MethodWrapperType,
                        MethodDescriptorType,
                        ClassMethodDescriptorType,
                        MethodType)
    for attribute_name in dir(SynchronizedClass):
        if attribute_name == "__init__" or attribute_name == "__getattribute__" or attribute_name == "__setattr__":
            continue
        elif isinstance(getattr(SynchronizedClass, attribute_name), all_method_types):
            setattr(SynchronizedClass,
                    attribute_name,
                    (synchronize_with_object_inner_lock('_inner_lock'))(getattr(SynchronizedClass, attribute_name)))
        # end if
    # end for

    return SynchronizedClass
# end def synchronize_all_methods_of_a_class


class DLock:
    """
    Debug implementation of a RLock
    """

    def __init__(self, name=None):
        """
        Constructor. Creates the RLock.

        :param name: A name for this lock - OPTIONAL
        :type name: ``str``
        """
        self.lock = RLock()
        self.name = name
        self.counter = 0
        self.tracebacks = []
        self.tid = None
    # end def __init__

    def acquire(self, blocking=True):
        """
        Proxy Acquire method

        :param blocking: Whether to block or not - OPTIONAL
        :type blocking: ``bool``

        :return: Whether the lock was acquired
        :rtype: ``bool``
        """
        result = self.lock.acquire(blocking)
        if result:
            self.counter += 1
            self.tid = id(currentThread())
            # Create a fake exception to capture the trace
            tb = "\n".join(format_list(extract_stack()))
            self.tracebacks.append(tb)
        # end if
        return result
    # end def acquire

    def release(self):
        """
        Releases the internal lock.
        """
        # Create a fake exception to capture the trace
        # noinspection PyBroadException
        try:
            raise Exception("Called release on DLock")
        except Exception:                                    # pylint:disable=W0703
            self.tracebacks.append(format_exc())
        # end try

        if self.counter <= 0:
            raise Exception("Release of un-acquired lock\n{}".format(
                '\n'.join(['NEW CALL: ' + tb for tb in self.tracebacks])))
        # end if
        self.counter -= 1

        assert (self.tid == id(currentThread())), "Lock released from other thread."

        try:
            self.lock.release()
        except AssertionError:
            raise AssertionError(f"Attempting to release un-acquired lock: {str(self)}")
        # end try
    # end def release

    def __str__(self):
        """
        Obtains a string representation of the current object.

        :return: The current object, as a string
        :rtype: ``str``
        """
        return self.name
    # end def __str__
# end class DLock


class LockingProxy:
    """
    Defines a proxy for an object to lock.

    The purpose of this class is to allow only one use of proxied object per run.

    Using this class and a global lock, an object provider will be able to serve
    an object to various threads based on a lock.

    Usage:
    @code
    myLock = Lock()

    class Printer(object):
        def __call__(self, text):
            print text
        # end def __call__
    # end class Printer

    def printerProvider()
        return LockingProxy(Printer(), myLock)
    # end def printerProvider

    # In thread 1, thread2, thread x...
    for i in xrange(0, 100):
        printer = printerProvider()
        printer("Hello")
    # end for
    @endcode
    """

    def __init__(self, next_object, lock, is_locked=False):
        """
        Constructor.

        This acquires the lock on the object.

        :param next_object: The object to wrap in the proxy
        :type next_object: ``object``
        :param lock: The lock to use for controlling access to this object
        :type lock: ``Lock``
        :param is_locked: Whether the lock is already locked or not - OPTIONAL
        :type is_locked: ``bool``
        """
        self.next = next_object
        self.__lock = lock

        if not is_locked:
            self.__lock.acquire()
        # end if
    # end def __init__

    def __del__(self):
        """
        Destructor.

        This releases the lock on the object.

        Note that in some cases, the release may fail, and is therefore
        protected with an absorbing @c try / @c catch clause.

        This strange behavior is 'normal', but quite complicated, and can occur when
        - Thread_A has created the lock
        - Thread_B has created the @c LockingProxy, and acquired the lock
        - Thread_B terminates, and the instance on the @c LockingProxy is lost
        - Thread_A garbage collects the @c LockingProxy.
          (Why is it Thread_A and not Thread_B that performs the garbage
          collection is still a mystery...)
        - As Thread_B has already been terminated, its link to the lock is
          implicitly released.
        - So, when Thread_A executes the destructor of the @c LockingProxy, the
          release is done on a lock that is not acquired anymore, even though
          no call to @c release has been done.
        """
        # noinspection PyBroadException
        try:
            self.__lock.release()
        except Exception:                                          # pylint:disable=W0703
            pass
        # end try
    # end def __del__

    def __getattr__(self, name):
        """
        Obtains the attribute of the next wrapped object

        :param name: The name of the attribute to obtain
        :type name: ``str``

        :return: The attribute of the proxied object
        :rtype: ``object``
        """
        return getattr(self.next, name)
    # end def __getattr__

    def __setattr__(self, name, value):
        """
        Sets the value of the specified attribute.

        :param name: The name of the attribute to set
        :type name: ``str``
        :param  value: The value of the attribute
        """
        if name in ("next", "_LockingProxy__lock"):
            self.__dict__[name] = value
        else:
            setattr(self.__next__, name, value)
        # end if
    # end def __setattr__

    def __str__(self):
        """
        Converts the current object to a string.

        :return: The current object, as a string
        :rtype: ``str``
        """
        return str(self.__next__)
    # end def __str__
# end class LockingProxy


class WeakMethod:
    """
    ONLY ON OBJECT METHODS

    A callable object to change an object method to a weak referenced one.

    For example:

    class WeakMethodObject:
        def __init__(self):
            self.method_to_make_weak = WeakMethod(self.method_to_make_weak)
        # end def __init__

        def method_to_make_weak(self):
            return self.__property_1
        # end def property getter property_1
    # end class LockedPropertyObject

    """
    def __init__(self, object_method):
        """
        Constructor

        :param object_method: Object method to use
        :type object_method: ``callable type``
        """
        self.target = proxy(object_method.__self__)
        self.method = proxy(object_method.__func__)
    # end def __init__

    def __call__(self, *args, **kwargs):
        """
        Call the weak method with args and kwargs as needed
        """
        return self.method(self.target, *args, **kwargs)
    # end def __call__
# end class WeakMethod


class RLockedDict(LockedDict):
    """
    Overriding LockedDict to have its lock as a RLock and not a Lock. It also adds a contextmanager method to try
    locking and still doing the action anyway if the locking failed.
    """

    def __init__(self, mapping=(), **kwargs):
        super().__init__(mapping=mapping, **kwargs)
        self._lock = RLock()
    # end def __init__

    @contextmanager
    def try_lock_do_anyway(self):
        """
        Try to acquire the lock and do the wanted action even if the acquisition failed. It will release the lock
        after the action only if the acquisition succeeded.
        """
        successfully_acquired = self._lock.acquire(blocking=False)
        try:
            yield
        finally:
            if successfully_acquired:
                self._lock.release()
            # end if
        # end try
    # end def try_lock_do_anyway
# end class RLockedDict


class QueueEmpty(Empty):
    """
    Exception thrown by QueueWithEvents when .
    """
    pass
# end class QueueEmpty


class QueueWithEvents(Queue):
    """
    Queue object, adding events for empty and not empty.
    """

    def __init__(self, maxsize=0):
        # See ``Queue.__init__``
        # Events to avoid using get to wait for the queue to be empty or not
        self.event_not_empty = Event()
        self.event_empty = Event()
        # Queue empty at the beginning
        self.event_empty.set()

        super().__init__(maxsize=maxsize)
    # end def __init__

    def put(self, item, block=True, timeout=None):
        # See ``Queue.put``
        with self.not_full:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() >= self.maxsize:
                        raise Full
                    # end if
                elif timeout is None:
                    while self._qsize() >= self.maxsize:
                        self.not_full.wait()
                    # end while
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    end_time = time() + timeout
                    while self._qsize() >= self.maxsize:
                        remaining = end_time - time()
                        if remaining <= 0.0:
                            raise Full
                        # end if
                        self.not_full.wait(remaining)
                    # end while
                # end if
            # end if
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
            self._update_event_not_empty()
        # end with
    # end def put

    def get(self, block=True, timeout=None):
        # See ``Queue.get``
        with self.not_empty:
            if not block:
                if not self._qsize():
                    raise QueueEmpty(f"Queue still empty after {timeout} seconds")
                # end if
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
                # end while
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                end_time = time() + timeout
                while not self._qsize():
                    remaining = end_time - time()
                    if remaining <= 0.0:
                        raise QueueEmpty(f"Queue still empty after {timeout} seconds")
                    # end if
                    self.not_empty.wait(remaining)
                # end while
            # end if
            item = self._get()
            self.not_full.notify()
            self._update_event_not_empty()
            return item
        # end with
    # end def get

    def _update_event_not_empty(self):
        """
        Update the empty and not empty events if needed. This method is an addon to the class Queue.
        """
        if self._qsize() != 0 and self.event_empty.is_set():
            self.event_not_empty.set()
            self.event_empty.clear()
        elif self._qsize() == 0 and self.event_not_empty.is_set():
            self.event_not_empty.clear()
            self.event_empty.set()
        # end if
    # end def _update_event_not_empty
# end class QueueWithEvents


class QueueWithFilter(QueueWithEvents):
    """
    QueueWithEvents object, adding a method to get with filter.
    """
    def get_first_message_filter(self, timeout=2, filter_method=None, skip_error=False):
        """
        Get the first object from the queue that matches the given filter method. If no filter method is given, the
        first object in the queue is returned (if any). If no parameter is given this method acts like the method
        ``get``.

        :param timeout: The timeout of this action in seconds (``None`` disables it) - OPTIONAL
        :type timeout: ``float`` or ``None``
        :param filter_method: The method used to test an object to know if it is the expected one. It should return
                              a ``bool`` - OPTIONAL
        :type filter_method: ``callable type`` or ``None``
        :param skip_error: Flag to enable (default) / disable exception when the requested object is not
                           found - OPTIONAL
        :type skip_error: ``bool``

        :return: Expected object or ``None`` if not found and ``skip_error`` is ``True``
        :rtype: ``object`` or ``None``

        :raise ``QueueEmpty``: If no expected message is found and ``skip_error`` is ``False``
        """
        unwanted_objects = []
        returned_message = None

        if timeout is None:
            end_time = None
        else:
            end_time = time() + timeout
        # end if
        remaining_time = timeout

        try:
            while returned_message is None:
                returned_message = self.get(block=timeout is not None, timeout=remaining_time)
                if filter_method is not None and not filter_method(returned_message):
                    unwanted_objects.append(returned_message)
                    returned_message = None
                # end if

                if remaining_time is not None:
                    remaining_time = end_time - time()
                    if remaining_time <= 0 and returned_message is None:
                        raise QueueEmpty(f"Message filtered still not in queue after {timeout} seconds")
                    # end if
                # end if
            # end while
        except QueueEmpty:
            if not skip_error:
                raise
            # end if
        finally:
            self._post_processing_unwanted_objects(unwanted_objects=unwanted_objects)
        # end try

        return returned_message
    # end def get_first_message_filter

    def get_no_wait_first_message_filter(self, filter_method=None, skip_error=False):
        """
        Get the first object from the queue that matches the given filter method with no wait period. If no filter
        method is given, the first object in the queue is returned (if any). If no parameter is given this method acts
        like the method ``get_nowait``.

        :param filter_method: The method used to test an object to know if it is the expected one. It should return
                              a ``bool`` - OPTIONAL
        :type filter_method: ``callable type`` or ``None``
        :param skip_error: Flag to enable (default) / disable exception when the requested object in not
                           found - OPTIONAL
        :type skip_error: ``bool``

        :return: Expected object or ``None`` if not found and ``skip_error`` is ``True``
        :rtype: ``object`` or ``None``

        :raise ``QueueEmpty``: If no expected message is found and ``skip_error`` is ``False``
        """
        unwanted_objects = []
        returned_message = None

        try:
            while returned_message is None:
                # get an item from the queue without blocking
                returned_message = self.get_nowait()
                if filter_method is not None and not filter_method(returned_message):
                    unwanted_objects.append(returned_message)
                    returned_message = None
                # end if
            # end while
        except QueueEmpty:
            if not skip_error:
                raise
            # end if
        finally:
            self._post_processing_unwanted_objects(unwanted_objects=unwanted_objects)
        # end try

        return returned_message
    # end def get_no_wait_first_message_filter

    def _post_processing_unwanted_objects(self, unwanted_objects):
        """
        Post-processing that has to be done on the temporary queue to put back all the unwanted object in the
        right order.

        :param unwanted_objects: List of the objects that were popped and unwanted
        :type unwanted_objects: ``list``
        """
        if len(unwanted_objects) == 0:
            return
        # end if

        # Empty the queue and keep the messages that are not to be returned in a temporary queue
        while not self.event_empty.is_set():
            # get an item from the queue without blocking
            unwanted_objects.append(self.get_nowait())
        # end while

        # Put back the unused messages into the initial queue
        while len(unwanted_objects) > 0:
            self.put(unwanted_objects.pop(0))
        # end while
    # end def _post_processing_unwanted_objects
# end class QueueWithFilter


class OrEventFactory:
    """
    Class to use to create Event objects that are triggered by at least one Event of a list
    """
    @staticmethod
    def _or_set(self):
        """
        Method to give to all Event objects instead of Event.set. This will permit to change the or event value with it.

        :param self: Since this method will replace an object method we need the self argument
        :type self: ``Event passed through _make_or``
        """
        self._set()
        self._changed()
    # end def _or_set

    @staticmethod
    def _or_clear(self):
        """
        Method to give to all Event objects instead of Event.clear. This will permit to change the or event value
        with it.

        :param self: Since this method will replace an object method we need the self argument
        :type self: ``Event passed through _make_or``
        """
        self._clear()
        self._changed()
    # end def _or_clear

    @staticmethod
    def _make_or(e, changed_callback):
        """
        This is the method to call to change an Event set and clear method to be able to be used on an OR event.

        :param e: Event to add to OR event
        :type e: ``Event``
        :param changed_callback: The callback to change the value of the OR event
        :type changed_callback: ``callable type``
        """
        assert callable(changed_callback), f"changed_callback must be callable, {changed_callback}"

        if all(elem in dir(e) for elem in ['_changed', '_set', '_clear']):
            # Event already used in another OR event
            if '_changed_callbacks' in dir(e):
                # noinspection PyUnresolvedReferences
                # noinspection PyProtectedMember
                e._changed_callbacks.append(changed_callback)
            else:
                # noinspection PyUnresolvedReferences
                # noinspection PyProtectedMember
                e._changed_callbacks = [e._changed, changed_callback]
            # end if

            def multiple_changed():
                # noinspection PyUnresolvedReferences
                # noinspection PyProtectedMember
                for callback in e._changed_callbacks:
                    callback()
                # end for
            # end def multiple_changed

            e._changed = multiple_changed
        else:
            e._set = e.set
            e._clear = e.clear
            e._changed = changed_callback
            e.set = lambda: OrEventFactory._or_set(e)
            e.clear = lambda: OrEventFactory._or_clear(e)
        # end if
    # end def _make_or

    @staticmethod
    def create_or_event(events):
        """
        Call this method to create an OR event based on a tuple of Event objects

        :param events: Event objects to use to make the OR event
        :type events: ``tuple of Event`` or ``list of Event``

        :return: OR event
        :rtype: ``Event``
        """
        or_event = Event()

        def changed():
            bool_value = [ev.is_set() for ev in events]
            if any(bool_value):
                or_event.set()
            else:
                or_event.clear()
            # end if
        # end def changed

        for e in events:
            OrEventFactory._make_or(e, changed)
        # end for

        changed()
        return or_event
    # end def create_or_event
# end class OrEventFactory


class Task:
    """
    The base class for tasks.

    A task is a unit of work that is run an executor.

    The Task interface defines only one method: work, with no arguments, that performs
    the task operation.
    This method returns a sequence of tasks that are to be processed later.
    When no other tasks are returned, the task is considered to be finished.
    """
    def __init__(self, function, *args, **kwargs):
        """
        Constructor

        :param function: The function to call for the task
        :type function: ``callable type``
        :param args: The arguments of the function to call for the task
        :type args: ``tuple``
        :param kwargs: The keyword arguments of the function to call for the task
        :type kwargs: ``dict``
        """
        assert callable(function), f"function must be callable, {function}"
        self.function = function
        self.args = args
        self.kwargs = kwargs
    # end def __init__

    def __call__(self):
        """
        Performs the work unit for this task.

        :return: A sequence of further tasks to perform
        :rtype: ``object`` or ``None``
        """
        return self.function(*self.args, **self.kwargs)
    # end def __call__
# end class Task


class Executor:
    """
    The interface definition of an Executor.

    An executor is object that executes a series of tasks, implemented by
    callable objects, that each return a sequence of callable objects.

    Note: This occurrence of an Executor is not thread-safe: it is up to
    specialized executors to provide thread safety.

    Example 1: Define a function that increments a counter, and execute 10 times
    this function in the executor.
    @code
    counter = 0
    def incrementCounter():
        global counter += 1
    # end def incrementCounter

    # Prepare the tasks
    tasks = []
    for i in xrange(10):
        tasks.append(incrementCounter)
    # end for

    # Create the executor
    executor = Executor(tasks)

    # Run the tasks
    executor.execute()
    @endcode

    Example 2: Define a function that increments a counter with different values,
    from 0 to 9.
    @code
    counter = 0
    def incrementCounter(step):
        global counter += step
    # end def incrementCounter

    # Prepare the tasks
    tasks = []
    for i in xrange(10):
        # The parameters following the name of the function will be
        # passed as function arguments in the executor.
        tasks.append(incrementCounter, i)
    # end for

    # Create the executor
    executor = Executor(tasks)

    # Run the tasks
    executor.execute()
    @endcode
    """

    def __init__(self,
                 tasks,
                 on_start=lambda: None,
                 on_suspend=lambda: None,
                 on_resume=lambda: None,
                 on_stop=lambda: None):
        """
        Constructor.

        The internal Queue object used to store the tasks is thread-safe.

        :param tasks: The default sequence of callable objects for this executor
        :type tasks: ``tuple of callable type``
        :param on_start: A callback used to notify a global executor start - OPTIONAL
        :type on_start: ``callable type``
        :param on_suspend: A callback used to notify a global executor suspend - OPTIONAL
        :type on_suspend: ``callable type``
        :param on_resume: A callback used to notify a global executor resume - OPTIONAL
        :type on_resume: ``callable type``
        :param on_stop: A callback used to notify a global executor stop - OPTIONAL
        :type on_stop: ``callable type``
        """
        assert callable(on_start), f"on_start must be callable, {on_start}"
        assert callable(on_suspend), f"on_suspend must be callable, {on_suspend}"
        assert callable(on_resume), f"on_resume must be callable, {on_resume}"
        assert callable(on_stop), f"on_stop must be callable, {on_stop}"
        self.tasks = QueueWithEvents()
        for i in range(len(tasks)):
            assert callable(tasks[i]), f"task[{i}] must be callable, {tasks[i]}"
            self.tasks.put(tasks[i])
        # end for

        self._on_start = on_start
        self._on_suspend = on_suspend
        self._on_resume = on_resume
        self._on_stop = on_stop
    # end def __init__

    def __del__(self):
        self.stop()
    # end def __del__

    def add_task(self, task, *args, **kwargs):
        """
        Adds a task to the list.

        :param task: The task to execute, as a callable.
        :type task: ``callable type``
        :param args: The arguments of the task to execute.
        :type args: ``tuple``
        :param kwargs: The keyword arguments of the task to execute.
        :type kwargs: ``dict``
        """
        assert callable(task), f"task must be callable, {task}"

        if isinstance(task, Task):
            assert len(args) == 0, "no arguments should be specified when a Task instance is used."
            assert len(kwargs) == 0, "no arguments should be specified when a Task instance is used."
        else:
            task = Task(task, *args, **kwargs)
        # end if

        self.tasks.put(task)
    # end def add_task

    def execute(self):
        """
        Start running tasks, and wait for their completion.
        """
        raise NotImplementedError
    # end def execute

    def pause(self):
        """
        Pauses the execution of tasks.
        This will NOT pause threads, but will block the worker threads
        between tasks.

        Note also that only ONE pause is active, successive calls to @c pause will
        be ignored.
        """
        raise NotImplementedError
    # end def pause

    def stop(self):
        """
        Stops the execution of tasks.

        This will NOT stop, but will block the worker threads
        between tasks, and exit before the tasks have been completed.
        """
        raise NotImplementedError
    # end def stop

    def resume(self):
        """
        Resumes the execution of tasks.

        This will NOT start a run, but will unblock the worker threads
        that have been paused between tasks.

        Note also that, as only ONE pause is active, successive calls to @c resume
        will be ignored.
        """
        raise NotImplementedError
    # end def resume
# end class Executor


class BasicExecutor(Executor):
    """
    Basic implementation of an executor.

    This executor is mono-threaded, and not thread safe: the @c start method
    blocks until all tasks have run, the add_task method is not synchronized.
    """

    @DocUtils.copy_doc(Executor.__init__)
    def __init__(self, tasks,
                 on_start=lambda: None,
                 on_suspend=lambda: None,
                 on_resume=lambda: None,
                 on_stop=lambda: None):
        """
        See `Executor.__init__`
        """
        super().__init__(tasks=tasks, on_start=on_start, on_suspend=on_suspend, on_resume=on_resume, on_stop=on_stop)

        self._pause = False
        self._stop = False
        self._lock = RLock()
    # end def __init__

    @DocUtils.copy_doc(Executor.pause)
    def pause(self):
        """
        See `Executor.pause`
        """
        self._lock.acquire()
        self._pause = True
    # end def pause

    @DocUtils.copy_doc(Executor.stop)
    def stop(self):
        """
        See `Executor.stop`
        """
        self._stop = True
        if self._pause:
            self.resume()
        # end if
    # end def stop

    @DocUtils.copy_doc(Executor.resume)
    def resume(self):
        """
        See `Executor.resume`
        """
        self._pause = False
        self._lock.release()
    # end def resume

    @DocUtils.copy_doc(Executor.execute)
    def execute(self):
        """
        See `Executor.execute`
        """

        self._on_start()

        # Loop until no more tasks are left to run.
        while self.tasks.event_not_empty.is_set() and not self._stop:
            # Obtain the next task
            task = self.tasks.get()

            # Execute the task, and obtain its children
            child_tasks = task()

            # Append its children to the remaining tasks
            if child_tasks is not None:
                for childTask in child_tasks:
                    self.tasks.put(childTask)
                # end for
            # end if

            if self._pause:
                # FIXME This may not be thread-safe, check it
                self._on_suspend()

                self._lock.acquire()
                self._lock.release()

                self._on_resume()
            # end if
        # end while

        self._on_stop()
    # end def execute
# end class BasicExecutor


class ThreadedExecutor(Executor):
    """
    Executes a series of tasks, distributing them to a maximum number of threads.

    This implementation is not very efficient, as it will create a thread for each new task.
    A better implementation would use a real ThreadPool: a list of available thread objects.
    """

    def __init__(self, tasks,
                 on_start=lambda: None,
                 on_suspend=lambda: None,
                 on_resume=lambda: None,
                 on_stop=lambda: None,
                 max_threads=10,
                 name='Executor',
                 pre_execute_thread=lambda: None,
                 post_execute_thread=lambda: None,
                 run_until_stop=False):
        """
        Constructs the new executor.

        This only initializes the maximum number of threads, and does not allocate them.

        The preExecute and postExecute functions are optional, and are used to
        perform thread-specific initialization. (For instance, COM initialization)

        :param tasks: The default sequence of callable objects for this executor - OPTIONAL
        :type tasks: ``tuple of callable type``
        :param on_start: A callback used to notify a global executor start - OPTIONAL
        :type on_start: ``callable type``
        :param on_suspend: A callback used to notify a global executor suspend - OPTIONAL
        :type on_suspend: ``callable type``
        :param on_resume: A callback used to notify a global executor resume - OPTIONAL
        :type on_resume: ``callable type``
        :param on_stop: A callback used to notify a global executor stop - OPTIONAL
        :type on_stop: ``callable type``
        :param max_threads: The maximum number of Threads to run concurrently. Defaults to 10 - OPTIONAL
        :type max_threads: ``int``
        :param name: A name for this executor - OPTIONAL
        :type name: ``str``
        :param pre_execute_thread: A function that will be called at the beginning of each thread - OPTIONAL
        :type pre_execute_thread: ``callable type``
        :param post_execute_thread: A function that will be called at the end of each thread - OPTIONAL
        :type post_execute_thread: ``callable type``
        :param run_until_stop: Flag to indicate that the executor should run until a stop is called and not just when
                               no task is in the pipe - OPTIONAL
        :type run_until_stop: ``callable type``
        """
        assert callable(pre_execute_thread), f"pre_execute_thread must be callable, {pre_execute_thread}"
        assert callable(post_execute_thread), f"post_execute_thread must be callable, {post_execute_thread}"

        super(ThreadedExecutor, self).__init__(
            tasks, on_start=on_start, on_suspend=on_suspend, on_resume=on_resume, on_stop=on_stop)

        self._maxThreads = max_threads
        self._name = name
        self._stop = Event()
        self._started = False

        self._preExecute = pre_execute_thread
        self._postExecute = post_execute_thread

        # self._pause is an inverted event:
        # When set, the executor is running
        # When unset, the executor is paused
        self._pause = Event()
        self._pause.set()

        self._pendingTasks = QueueWithEvents()  # Temporary queue, used to pause/resume

        self.threads = []

        self._run_until_stop = run_until_stop
        self._stop_or_task_event = OrEventFactory.create_or_event((self._stop, self.tasks.event_not_empty))
        self._stop_or_no_task_event = OrEventFactory.create_or_event((self._stop, self.tasks.event_empty))

        # atexit register
        register(self.clean_up)
    # end def __init__

    def clean_up(self):
        """
        Clean up callback for when python is exiting
        """
        self.stop()
    # end def clean_up

    def __del__(self):
        self.clean_up()
    # end def __del__

    @DocUtils.copy_doc(Executor.pause)
    def pause(self):
        """
        See `Executor.pause`
        """

        # Do not block: The _pause is not a RLock, and re-entrance is not handled
        # The purpose here is to acquire the lock and test for pause, NOT to
        # block the caller.
        self._pause.clear()
        # Consume all remaining tasks, and place them in the pending queue.
        # The main loop will then wait for the completion of working tasks
        # before notifying the on_suspend callback
        try:
            while True:
                task = self.tasks.get(False)
                self._pendingTasks.put(task)
                self.tasks.task_done()
            # end while
        except Empty:
            pass
        # end try
    # end def pause

    @DocUtils.copy_doc(Executor.stop)
    def stop(self):
        """
        See `Executor.stop`
        """
        if not self._stop.is_set():
            self._stop.set()
            for _ in range(len(self.threads)):
                self.tasks.put(None)
            # end for
            self.resume()
        # end if
    # end def stop

    @DocUtils.copy_doc(Executor.resume)
    def resume(self):
        """
        See `Executor.resume`
        """
        # Only resume if already paused
        if not self._pause.is_set():
            # Release the _pause lock, allowing the tasks
            # to continue their execution
            self._pause.set()

            # Consume all remaining tasks, and place them in the pending queue.
            # The main loop will then wait for the completion of working tasks
            # before notifying the on_suspend callback
            try:
                while True:
                    task = self._pendingTasks.get(False)
                    self.tasks.put(task)
                    self._pendingTasks.task_done()
                # end while
            except Empty:
                pass
            # end try
        # end if
    # end def resume

    @DocUtils.copy_doc(Executor.add_task)
    def add_task(self, task, *args, **kwargs):
        """
        See `Executor.add_task`
        """
        super().add_task(task, *args, **kwargs)
    # end def add_task

    def execute(self):                                                                  # pylint:disable=R0912
        """
        Starts the executor.

        This starts the threads, up to the maximum number defined in the constructor,
        and distributes the tasks to each thread.
        """

        self._on_start()
        self._started = True

        def worker():
            """
            Worker function for the threads

            This function consumes tasks, and appends child tasks to the queue.
            """

            self._preExecute()

            try:
                try:
                    # Loop until the executor has stopped
                    while not self._stop.is_set():
                        # Wait for either a task or stop event
                        self._stop_or_task_event.wait()

                        # It is needed to test again because when just one task is added, all threads will have
                        # the not_empty event
                        if not self._stop.is_set() and self.tasks.event_not_empty.is_set():
                            # Consume a task
                            task = self.tasks.get()

                            try:
                                if task is not None and callable(task):
                                    # Execute the task, and append its children to the queue
                                    sub_tasks = task()
                                    # Do not add the children task if executor.stop() called
                                    if sub_tasks is not None and not self._stop.is_set():
                                        for subTask in sub_tasks:
                                            self.tasks.put(subTask)
                                        # end for
                                    # end if
                                # end if
                            finally:
                                # Signal that the processing is done on this task
                                self.tasks.task_done()
                            # end try

                            # Pause if necessary
                            if not self._stop.is_set():
                                self._pause.wait()
                            # end if
                        # end if
                    # end while
                except StopIteration:
                    pass
                # end try
            finally:
                self._postExecute()
            # end try
        # end def worker

        # Start the threads that will process tasks
        for i in range(self._maxThreads):
            # The thread to start
            thread = Thread(target=worker, name="%s thread %d" % (self._name, i))
            # The thread is a daemon: It will NOT prevent the main thread from dying
            thread.setDaemon(True)
            thread.start()
            self.threads.append(thread)
        # end for

        loop = True
        # Wait for the tasks to be run, and handle pause/resume through the
        while loop:
            # Detect a pause
            if self._pendingTasks.event_not_empty.is_set():
                # Notify the callback
                self._on_suspend()

                # Wait for pending tasks (the executor has been paused)
                self._pendingTasks.join()

                # Notify the callback
                self._on_resume()
            # end if

            if self._run_until_stop:
                # Wait for new tasks (or stop)
                self._stop_or_task_event.wait()
            # end if
            # Wait for them to be done (or stop)
            self._stop_or_no_task_event.wait()

            loop = self._pendingTasks.event_not_empty.is_set() or (self._run_until_stop and not self._stop.is_set())
        # end while

        # Signal all waiting threads that the run has ended.
        self.stop()

        # As the threads are not daemon threads, the main thread will have to
        # wait for the threads to properly terminate before dying.
        # The current thread will _also_ wait for the worker threads termination.
        for thread in self.threads:
            thread.join()
        # end for

        self._on_stop()
    # end def execute

    def force_kill_all_threads(self):
        self.stop()
        for thread in self.threads:
            if not thread.is_alive():
                continue
            # end if

            result = pythonapi.PyThreadState_SetAsyncExc(c_long(thread.ident), py_object(SystemExit))
            if result > 1:
                # Failure, there is not that much more to try
                pythonapi.PyThreadState_SetAsyncExc(c_long(thread.ident), 0)
            # end if
        # end for
    # end def force_kill_all_threads
# end class ThreadedExecutor


class StoppableThread(threading.Thread):
    """
    Thread class with a stop() method. The target function itself has to check
    regularly for the stopped() condition.
    """

    def __init__(self, target, name=None, *args, **kwargs):
        """
        :param target: is the callable object to be invoked by the run() method,
            need to support passing the thread object as a named parameter 'thread'
        :type target: ``Callable[..., StoppableThread]``
        :param name: is the thread name. By default, a unique name is constructed of the form "Thread-N"
            where N is a small decimal number
        :type name: ``str`` or ``None``
        :param args: arguments for the target invocation. Defaults to () - OPTIONAL
        :type args: ``list`` or ``tuple``
        :param kwargs: dictionary of keyword arguments for the target Defaults to {} - OPTIONAL
        :type kwargs: ``dict``
        """
        kwargs["thread"] = self
        super().__init__(target=target, name=name, args=args, kwargs=kwargs)
        self._stop_event = threading.Event()
    # end def __init__

    def stop(self):
        """
        Ask to stop the thread
        """
        self._stop_event.set()
    # end def stop

    def stopped(self):
        """
        Return ``True`` if the thread was stopped otherwise ``False``

        :return: flag indicating the stop request status
        :rtype: ``bool``
        """
        return self._stop_event.is_set()
    # end def stopped
# end class StoppableThread
class UniqueInstanceDeque(deque):
    """
    A Queue object where there can each instance can only appear once.

    Multiple instances of the same classes are allowed
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor

        :param args: The arguments
        :type args: ``tuple``
        :param kwargs: The keyword arguments
        :type kwargs: ``dict``
        """
        super().__init__(self, *args, **kwargs)

        self._lock = Lock()
    # end def __init__

    def append(self, x):
        """
        Append a value to the right of the queue

        :param x: The value to append
        :type x: ``object``
        """
        with self._lock:
            try:
                deque.remove(self, x)
            except ValueError:
                pass
            # end try

            deque.append(self, x)
        # end with
    # end def append

    def appendleft(self, x):
        """
        Append a value to the left of the queue

        :param x: The value to append
        :type x: ``object``
        """
        with self._lock:
            try:
                deque.remove(self, x)
            except ValueError:
                pass
            # end try

            deque.appendleft(self, x)
        # end with
    # end def appendleft

    def extend(self, iterable):
        """
        Extend a value to the right of the queue

        :param iterable: The value to append
        :type iterable: ``iterable``
        """
        with self._lock:
            for x in iterable:
                try:
                    deque.remove(self, x)
                except ValueError:
                    pass
                # end try
            # end for

            deque.extend(self, iterable)
        # end with
    # end def extend

    def extendleft(self, iterable):
        """
        Extend a value to the right of the queue

        :param iterable: The value to append
        :type iterable: ``iterable``
        """
        with self._lock:
            for x in iterable:
                try:
                    deque.remove(self, x)
                except ValueError:
                    pass
                # end try
            # end for

            deque.extendleft(self, iterable)
        # end with
    # end def extendleft

    def clear(self):
        """
        clear proxy
        """
        with self._lock:
            deque.clear(self)
        # end with
    # end def clear

    def pop(self):
        """
        pop proxy

        :return: The popped value
        :rtype: ``object``
        """
        with self._lock:
            return deque.pop(self)
        # end with
    # end def pop

    def popleft(self):
        """
        popleft proxy

        :return: The popped value
        :rtype: ``object``
        """
        with self._lock:
            return deque.popleft(self)
        # end with
    # end def popleft

    def remove(self, value):
        """
        popleft proxy

        :param value: The value to remove
        :type value: ``object``
        """
        with self._lock:
            deque.remove(self, value)
        # end with
    # end def remove

    def rotate(self, *args, **kwargs):                                            # pylint:disable=W0221
        """
        rotate proxy
        """
        with self._lock:
            deque.rotate(self, *args, **kwargs)                                     # pylint:disable=E1120
        # end with
    # end def rotate
# end class UniqueInstanceDeque


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
