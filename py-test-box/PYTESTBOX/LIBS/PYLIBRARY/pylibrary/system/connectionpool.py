#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.system.connectionpool

@brief  Connection pool

@author christophe.roquebert

@date   2018/11/26
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from threading                          import RLock
import socket
import sys

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
if (sys.platform == 'win32'):
    NON_BLOCKING_CODE = 10035
else:
    NON_BLOCKING_CODE = 11
# end if

SOCKET_POOL = {}
SOCKET_POOL_RLOCK = RLock()

class SocketDecorator(object):
    '''
    Socket instance that simulates the behavior of a socket, but
    actually redirects all calls to one instance.

    It handles a stack of open/close commands, only closing a connection when
    the last caller demands it.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.next  = socket.socket()
        self.count = 0
        self.lock  = RLock()
    # end def __init__

    def __getattr__(self, name):
        '''
        Get the attribute value of name

        @param  name [in] (str) Name of the attribute

        @return Value of the attribute
        '''
        return getattr(self.__next__, name)
    # end def __getattr__

    def __setattr__(self, name, value):
        '''
        Set the value of an attribute

        @param  name  [in] (str)    Name of the attribute
        @param  value [in] (object) Value of the attribute
        '''
        if (name in ('next', 'count', 'lock')):
            self.__dict__[name] = value
        else:
            setattr(self.__next__, name, value )
        # end if
    # end def __setattr__

    def connect(self, *args, **kwargs):
        '''
        Connection

        @option args   [in] (tuple) Arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        with self.lock:
            if (self.count <= 0):
                if (self.__next__ is not None):
                    timeout = self.gettimeout()
                else:
                    timeout = None
                # end if
                self.next  = socket.socket()
                self.next.settimeout(timeout)
                self.next.connect(*args, **kwargs)
                self.count = 0
            # end if
            self.count += 1
        # end with
    # end def connect

    def close(self, *args, **kwargs):
        '''
        Close

        @option args   [in] (tuple) Arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        with self.lock:
            self.count -= 1
            if (self.count <= 0):
                if (self.__next__ is not None):
                    self.next.close(*args, **kwargs)
                # end if
                self.count = 0

                with SOCKET_POOL_RLOCK:
                    keys = [k for k, v in SOCKET_POOL.items() if v is self]
                    for key in keys:
                        del SOCKET_POOL[key]
                    # end for
                # end with
            # end if
        # end with
    # end def close

    def send(self, *args, **kwargs):
        '''
        Send

        @option args   [in] (tuple) Arguments
        @option kwargs [in] (dict)  Keyword arguments

        @return Response of the command
        '''
        with self.lock:
            try:
                return self.next.send(*args, **kwargs)
            except socket.error:
                self.next = None
                self.close()
                raise
            # end try
        # end with
    # end def send

# end class SocketDecorator

def createPooledSocket(host, port, timeout = None):
    '''
    Socket

    @param  host    [in] (str) Host instance
    @param  port    [in] (int) Port of connection
    @option timeout [in] (int) Wait time in ms

    @return Result of the socket
    '''
    key = '%s:%d' % (host, port)
    with SOCKET_POOL_RLOCK:
        if (key in SOCKET_POOL):
            result = SOCKET_POOL[key]
        else:
            result = SocketDecorator()
            SOCKET_POOL[key] = result
        # end if
    # end with

    if (timeout is not None):
        try:
            result.settimeout(timeout)
        except Exception:                                                                                               # pylint:disable=W0703
            pass
        # end try
    # end if

    tempo = False
    try:
        try:
            result.connect((host, port))
        except socket.error as excp:
            import time
            # Append of tempo to wait deconnection process finalize
            tempo = True
            time.sleep(1)
            result.connect((host, port))
        # end try
    except socket.error as excp:
        if tempo:
            excp.strerror += ' Error even with 1 second wait before reconnection try'
        # end if
        raise socket.error(excp.errno, str(excp.strerror, errors='ignore'))
    # end try

    return result
# end def createPooledSocket

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
