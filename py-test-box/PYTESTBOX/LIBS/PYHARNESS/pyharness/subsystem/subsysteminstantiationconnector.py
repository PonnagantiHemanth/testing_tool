#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.subsysteminstantiationconnector

@brief  Instantiation of a subsystem.

@author christophe.roquebert

@date   2018/10/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.subsystem.subsystemcomposite   import SubSystemComposite

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class AbstractSubSystemInstantiationImporter(object):
    '''
    Base class for SubSystemInstantiation importer classes
    '''
    def load(self, leafPath, moveUp = True):
        '''
        Loads a list of subsystem instantiations from a given file path.

        @param  leafPath [in] (str)  Path to the instantiations to load.
        @option moveUp   [in] (bool) If True, moves up in the variants until the
                                     full instantiations are gathered
        @return (list) List of SubSystemInstantiation instances
        '''
        raise NotImplementedError
    # end def load
# end class AbstractSubSystemInstantiationImporter

class AbstractSubSystemInstantiationExporter(object):
    '''
    Base class for SubSystemInstantiation exporter classes
    '''
    def save(self, rootPath, subSystemInstantiations):
        '''
        Saves a subsystem (and its children) to a given file path.

        @param  rootPath                [in] (str)  Path to the instantiations to save.
        @param  subSystemInstantiations [in] (dict) The subsystems to save. This is a dict of lists of SubSystemInstantiation.
                                             Each dict key is the PRODUCT/VARIANT relative path.
        '''
        raise NotImplementedError
    # end def save
# end class AbstractSubSystemInstantiationExporter

class SubSystemInstantiationImporterComposite(AbstractSubSystemInstantiationImporter, SubSystemComposite):
    '''
    SubSystem instantiation composite class

    This class can handle many SubSystem instantiation instances
    '''
    ClassReference = AbstractSubSystemInstantiationImporter

    def __init__(self):
        '''
        Constructor
        '''
        super(SubSystemInstantiationImporterComposite, self).__init__()

        self._childern = []
    # end def __init__

    def load(self, leafPath, moveUp = True):
        '''
        @copydoc pyharness.subsystem.subsysteminstantiationconnector.AbstractSubSystemInstantiationImporter.load
        '''
        if (self._childern == []):
            raise IndexError('No child defined, unable to load')
        # end if

        for child in self._childern:
            result = child.load(leafPath, moveUp)
            if (result is not None):
                break
            # end if
        # end for
        return result
    # end def load

# end class SubSystemInstantiationImporterComposite

class SubSystemInstantiationExporterComposite(AbstractSubSystemInstantiationExporter, SubSystemComposite):
    '''
    SubSystem instantiation composite class

    This class can handle many SubSystem instantiation instances
    '''
    ClassReference = AbstractSubSystemInstantiationExporter

    def __init__(self):
        '''
        Constructor
        '''
        super(SubSystemInstantiationExporterComposite, self).__init__()

        self._childern = []
    # end def __init__

    def save(self, rootPath, subSystemInstantiations):
        '''
        @copydoc pyharness.subsystem.subsysteminstantiationconnector.AbstractSubSystemInstantiationExporter.save
        '''
        if (self._childern == []):
            raise IndexError('No child defined, unable to save')
        # end if

        for child in self._childern:
            child.save(rootPath, subSystemInstantiations)
        # end for
    # end def save

# end class SubSystemInstantiationExporterComposite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
