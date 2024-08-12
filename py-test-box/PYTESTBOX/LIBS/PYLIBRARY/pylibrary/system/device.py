#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.system.device
    :brief: Base definition of a Device interface
    :author: Christophe Roquebert
    :date: 2018/10/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import synchronized
from threading import RLock


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReadOnlyDeviceCacheMetaClass(type):
    """
    This class is used as a metaclass to create a read-only class property for thread safe device cache
    """
    # Thread safe cache of device available from config file, private in class
    _DEVICE_CACHE = []

    # This is a read only property, therefore there is no setter
    @property
    def device_cache(cls):
        return cls._DEVICE_CACHE.copy()
    # end def property getter device_cache
# end class ReadOnlyDeviceCacheMetaClass


class DeviceProvider(object):
    """
    Interface implemented by objects able of provide an instance of a BaseSmartDevice
    """

    def getDevice(self, indexOrPredicate=0, keepForTestduration=False):
        """
        Obtains an instance of a BaseSmartDevice.

        @option indexOrPredicate    [in] (int,callable) Either:
                                         - An index identifying a unique device.
                                         - A predicate, taking a BaseSmartDevice
                                           instance as a parameter, and able to
                                           test whether the device is acceptable

        @option keepForTestduration [in] (bool) Whether to NOT autocollect the object
        """
        raise NotImplementedError()
    # end def getDevice
# end class DeviceProvider


class BaseSmartDevice(object):                                        # pylint:disable=R0922
    """
    This is the base definition of the SmartDevice interface.

    Implementors of SmartDevice instances should follow this interface definition
    in order to implement a consistent behaviour between instances.

    Do not forget to run the associated test case, in test/basedevicetestcase_test.py

    A SmartDevice allows the manipulation of one device.

    Declaration:
    @code
    sc = SmartDeviceDerivedClass(device, *options)
    @endcode
    where:
     - device : index of the device in this device types (greater than 0, the
       maximum number may vary).
     - *options: optional parameters, specific to the specialized class.
       Such parameters MUST be OPTIONAL to follow this interface's contract.
    """
    def __init__(self, device_number):
        """
        Initializes a smartdevice instance.

        @param  device_number [in]  (int) Local device's number (greater than 0)
        """
        self.number = device_number
    # end def __init__

    def __del__(self):
        """
        Close a smartdevice instance.
        """
        pass
    # end def __del__

# ------------------------------------------------------------------------------
#                           Public interface
# ------------------------------------------------------------------------------
    @classmethod
    def configure(cls, **kwargs):
        """
        Configures this smartdevice type.

        @option kwargs [in] (dict) Keyword arguments used as configuration parameters.
        """
        pass
    # end def configure

    def is_allocated(self):
        """
        Obtains the allocation status of the smart device.
        """
        raise NotImplementedError
    # end def is_allocated

    def allocate(self):
        """
        Connection to the real reader.
        """
        raise NotImplementedError
    # end def allocate

    def unallocate(self):
        """
        Deconnection from the real reader.
        """
        raise NotImplementedError
    # end def unallocate

    def powerUp(self):
        """
        Power up the device inserted in the reader.
        """
        raise NotImplementedError
    # end def powerUp

    def isPoweredUp(self):
        """
        Returns the logical state of the powerUp

        Depending on the implementation, this may be either the real state
        of the device, or the logical state
        where the user could powerDown a device through the GUI without python
        being notified)

        @return (bool) True if the device has been powered up
        """
        raise NotImplementedError
    # end def isPoweredUp

    def reset(self):
        """
        Reset an already device inserted in the connected reader.
        """
        raise NotImplementedError
    # end def reset

    def powerDown(self):
        """
        Power down the device inserted in the reader.
        """
        raise NotImplementedError
    # end def powerDown

    def getDriverInfo(self):                                                                                            #pylint:disable=R0201
        """
        Obtains driver information.

        The obtained driver information is dependent on the actual driver connection method.
        By default, no info is returned

        @return Driver info, if any.
        """
        result = {'NAME':    'Unknown',
                  'VERSION': 'Unknown'}

        return result
    # end def getDriverInfo

    def setTearing(self, tearing_time):
        """
        Set the tearing time to use

        @param  tearing_time [in] (int) tearing time in micro-s (time=500 for 5ms)

        @return None
        """
        raise NotImplementedError
    # end def setTearing

    def sendRaw(self, *data):
        """
        Sends raw data to this device.

        @option data [in] (tuple,HexList) The data to send.

        @return Device response in HeBuf form.
        """
        raise NotImplementedError
    # end def sendRaw

    def getElapsedTime(self):
        """
        Get the processing time of the last APDU or reset.

        @return Processing time in ms
        """
        raise NotImplementedError
    # end def getElapsedTime
# end class BaseSmartDevice


class SmartDeviceException(Exception):
    """
    Common class for smart device exceptions
    """

    CAUSE_UNKNOWN = None
    CAUSE_MUTE = 0
    CAUSE_CONNECTION = 1
    CAUSE_CONFIGURATION = 2
    CAUSE_INTERNAL = 3
    CAUSE_MUTE_RESET = 4
    CAUSE_TEARING = 5
    CAUSE_INTERRUPT = 6
    CAUSE_INVALID_ACK = 7

    def __init__(self, *options):
        """
        Constructor.

        The constructor takes its parameters from the list of
        CAUSE_XXX constants, and may optionally provide a message.

        @param options [in] (tuple) Arguments passed to the parent constructor
        """
        super(SmartDeviceException, self).__init__(*options)
    # end def __init__

    def getCause(self):
        """
        Obtains the exception cause.

        This is the first int argument.

        @return The exception cause, as an int from SmartDeviceException
        """
        causes = [x for x in self.args if isinstance(x, int)]
        if len(causes) > 0:
            return causes[0]
        # end if
        return SmartDeviceException.CAUSE_UNKNOWN
    # end def getCause

    def getMessage(self):
        """
        Obtains the messages for this exception

        @return The message embedded within this exception.
        """
        string_messages = [x for x in self if isinstance(x, str)]
        return ', '.join(string_messages)
    # end def getMessage
# end class SmartDeviceException


class DummySmartDevice(BaseSmartDevice):
    """
    A dummy object, that serves as an empty smartDevice.

    This object is useful in some very specific cases, for:
    - Implementing Generic tests.
    - Validation, when a mock object is required in the current configuration.
    """

    def is_allocated(self):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.is_allocated
        """
        return False
    # end def is_allocated

    def allocate(self):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.allocate
        """
        pass
    # end def allocate

    def unallocate(self):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.unallocate
        """
        pass
    # end def unallocate

    def powerUp(self):
        """
        Power up the device inserted in the reader.

        @return The device unique identification
        """
        return None
    # end def powerUp

    def isPoweredUp(self):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.isPoweredUp
        """
        return False
    # end def isPoweredUp

    def reset(self):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.reset
        """
        return HexList()
    # end def reset

    def powerDown(self):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.powerDown
        """
        pass
    # end def powerDown

    def setTearing(self, tearing_time):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.setTearing
        """
        pass
    # end def setTearing

    def sendRaw(self, *data):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.sendRaw
        """
        return HexList(*data)
    # end def sendRaw

    def getElapsedTime(self):
        """
        @copydoc pylibrary.system.device.BaseSmartDevice.getElapsedTime
        """
        return 1000
    # end def getElapsedTime
# end class DummySmartDevice


class SmartDeviceFactory(object):
    """
    A factory class for the creation of singleton SmartDevice objects.
    """

    SYNCHRONIZATION_LOCK = RLock()

    def __init__(self, smartDeviceClass):
        """
        Constructor.

        @param  smartDeviceClass [in] (BaseSmartDevice) The class used for instantiation
        """
        self._SMARTCARD_CACHE = {}
        self._isConfigured = False
        self._smartDeviceClass = smartDeviceClass
    # end def __init__

    @synchronized(SYNCHRONIZATION_LOCK)                            # pylint:disable=E0602
    def configure(self, **kwargs):
        """
        Proxy for the SmartDevice.configure method

        @option kwargs [in] (dict) the keyword arguments of the SmartDevice.configure method.
        """
        if not self._isConfigured:
            self._smartDeviceClass.configure(**kwargs)
            self._isConfigured = True
        # end if
    # end def configure

    @synchronized(SYNCHRONIZATION_LOCK)                                                        # pylint:disable=E0602
    def __call__(self, *args):
        """
        Factory providing a singleton for the specified parameters.

        @option args [in] (tuple) The arguments passed to the SmartDevice constructor

        @return (SmartDevice) A SmartDevice-derived instance
        """
        key = args
        if key not in self._SMARTCARD_CACHE:
            self._SMARTCARD_CACHE[key] = self._smartDeviceClass(*args)
        # end if

        return self._SMARTCARD_CACHE[key]
    # end def __call__
# end class SmartDeviceFactory


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
