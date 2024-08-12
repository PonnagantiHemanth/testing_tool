#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.transportmessage
:brief: Base definition of a raw transport message
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/12
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------
class TransportMessage:
    """
    Transport message base class
    """

    def __init__(self, message_class=None, data=None, timestamp=None):
        """
        Constructor

        :param message_class: The message class - OPTIONAL
        :type message_class: ``type`` or ``None``
        :param data: Binary data - OPTIONAL
        :type data: ``HexList`` or ``None``
        :param timestamp: Time stamp counter in us - OPTIONAL
        :type timestamp: ``int`` or ``None``
        """
        self.message_class = message_class
        self.data = data
        self.timestamp = timestamp
    # end def __init__

    @property
    def message_class(self):
        """
        Property getter of message_class.

        :return: message_class value
        :rtype: ``type`` or ``None``
        """
        return self._message_class
    # end def property getter message_class

    @message_class.setter
    def message_class(self, value):
        """
        Property setter of message_class.

        :param value: message_class value
        :type value: ``type`` or ``None``
        """
        assert value is None or isinstance(value, type), "message_class should be either None or a type"
        self._message_class = value
    # end def property setter message_class

    @property
    def data(self):
        """
        Property getter of data.

        :return: data value
        :rtype: ``HexList`` or ``None``
        """
        return self._data
    # end def property getter data

    @data.setter
    def data(self, value):
        """
        Property setter of data.

        :param value: data value
        :type value: ``HexList`` or ``None``
        """
        assert value is None or isinstance(value, HexList), "data should be either None or HexList"
        self._data = value
    # end def property setter data

    @property
    def timestamp(self):
        """
        Property getter of timestamp.

        :return: timestamp value
        :rtype: ``int`` or ``None``
        """
        return self._timestamp
    # end def property getter timestamp

    @timestamp.setter
    def timestamp(self, value):
        """
        Property setter of timestamp.

        :param value: timestamp value in us
        :type value: ``int`` or ``None``
        """
        assert value is None or isinstance(value, int), "timestamp should be either None or int"
        self._timestamp = value
    # end def property setter timestamp

    def __str__(self):
        to_str = ""

        if self.message_class is not None:
            to_str += f"{self.message_class.__name__} "
        # end if

        if self.data is not None:
            to_str += f"{self.data} "
        # end if

        if self.timestamp is not None:
            to_str += f"at {self.timestamp}ns "
        # end if

        if to_str == "":
            to_str = "Empty transport message"
        else:
            # Remove last space in the string
            to_str = to_str[:-1]
        # end if

        return to_str
    # end def __str__

    def __repr__(self):
        return str(self)
    # end def __repr__

    def __eq__(self, other):
        # The equality is not done over the timestamp because we can have two identical transport messages
        # at different times
        return type(self) == type(other) and \
               self.message_class == other.message_class and \
               self.data == other.data
    # end def __eq__

    def __len__(self):
        return len(self.data)
    # end def __len__
# end class TransportMessage

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
