#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.deprecation

@brief  Deprecation warnings

@author christophe.roquebert

@date   2018/11/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.warning           import IgnoreWarning
import warnings

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

def deprecated(func, message = None, stackLevel=1, deadline=None):                                                      # pylint:disable=R0912
    '''
    This is a decorator which can be used to mark functions as deprecated
    It will result in a warning being emitted when the function is used.

    @param  func       [in] (callable) Deprecated function
    @option message    [in] (str)      Error message
    @option stackLevel [in] (int)      Stack level to remove
    @option deadline   [in] (str)      The deadline date, where the deprecation warning
                                       will be replaced by an exception. The deadline date
                                       has the format YYYY/MM/DD

    @return Warning

    Example:
    @code
    class MyClass(object):

      def getUpdated(self):
        return 0

      updated = property(getUpdated)

      @deprecated('Use getUpdated()')
      def getObsolete(self):
        return self.updated()

      obsolete = deprecated(updated, 'Use updated instead')
    @endcode
    '''
    deadlined = False
    if (deadline is not None):
        from datetime                   import date
        deadlineDate = date(*[int(x) for x in deadline.split('/')])
        deadlined = (date.today() > deadlineDate)
        deadlineWarning = ' (This will raise an exception on %s)' % deadline
    else:
        deadlineWarning = ''
    # end if


    if (isinstance(func, str)):
        return lambda f: deprecated(f, func, stackLevel+1, deadline)

    elif (isinstance(func, property)):
        class DeprecatedProperty(object):
            '''
            Prints a message on deprecated property access
            '''
            def __get__(self, cls, owner):                                                                              #pylint:disable=R0201
                '''
                Read access

                @param  cls   [in] (Type) target class
                @param  owner [in] (?) required argument

                @return The actual value.
                '''
                if (deadlined):
                    raise DeprecationWarning('Reading a property deprecated since %s\n%s' % (deadline, message))

                else:
                    warnings.warn("Reading deprecated property%s.\n%s" % (deadlineWarning, message),
                                  category   = DeprecationWarning,
                                  stacklevel = 3)
                # end if

                return func.__get__(cls, owner)
            # end def __get__

            def __set__(self, cls, value):                                                                              #pylint:disable=R0201
                '''
                Write access

                @param  cls   [in] (Type) target class
                @param  value [in] (?) required argument
                '''
                if (deadlined):
                    raise DeprecationWarning('Writing a property deprecated since %s\n%s' % (deadline, message))

                else:
                    warnings.warn("Writing deprecated property%s.\n%s" % (deadlineWarning, message),
                                  category   = DeprecationWarning,
                                  stacklevel = 3)
                # end if
                func.__set__(cls, value)
            # end def __set__
        # end class DeprecatedProperty

        return DeprecatedProperty()

    else:
        def newFunc(*args, **kwargs):
            '''
            Implementation of the warning

            This function triggers a warning before proceeding to the actual call.

            @option args   [in] (tuple) The function arguments
            @option kwargs [in] (dict) The function keyword arguments

            @return Warning
            '''
            if deadlined:
                raise DeprecationWarning('Calling function %s, deprecated since %s\n%s' % (func.__name__, deadline, (message or '')))
            else:
                warnings.warn("Call to deprecated function %(function)s%(warning)s.\n%(message)s"
                            % {"function": func.__name__,
                               'warning': deadlineWarning,
                               "message": message or "",
                              },
                              category   = DeprecationWarning,
                              stacklevel = stackLevel)
            # end if
            return func(*args, **kwargs)
        # end def newFunc

        newFunc.__name__ = func.__name__                                                                                #pylint:disable=W0621,W0622
        newFunc.__doc__  = func.__doc__                                                                                 #pylint:disable=W0621,W0622
        newFunc.__dict__.update(func.__dict__)
        return newFunc
    # end if
# end def deprecated

## The global level monitor. Its name should be ignored by pylint
ignoredeprecation = IgnoreWarning(DeprecationWarning)                                                                   #pylint:disable=C0103

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
