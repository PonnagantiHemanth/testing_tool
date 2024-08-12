#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.subsystemcomposite

@brief  Composite definition for all SubSystem classes

@author christophe Roquebert

@date   2018/06/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class SubSystemComposite(object):
    '''
    SubSystem composite class

    This class can handle many SubSystem instances
    '''

    ClassReference = None

    def __init__(self):
        '''
        Constructor
        '''
        self._childern = []
    # end def __init__

    def add(self, child):
        '''
        Append of a SubSystem importer instance

        @param  child [in] (object) Child to add
        '''
        if not isinstance(child, self.ClassReference):
            raise TypeError('Wrong child type: %s. Should be %s instead'
                            % (type(child).__name__, type(self.ClassReference).__name__))
        # end if

        self._childern.append(child)

    # end def add

    def remove(self, child):
        '''
        Remove a child of the list

        @param  child [in] (object) Child to remove
        '''
        if child in self._childern:
            self._childern.remove(child)
        else:
            raise IndexError('%s not present in composite' % child)
        # end if
    # end def remove

    def getChild(self, index):
        '''
        Get a child from the list

        @param  index [in] (int) Index of the child in the list

        @return (object) Child instance
        '''
        return self._childern[index]
    # end def getChild

# end class SubSystemComposite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
