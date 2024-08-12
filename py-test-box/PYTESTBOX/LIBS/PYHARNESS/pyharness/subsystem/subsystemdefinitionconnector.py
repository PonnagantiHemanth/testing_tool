#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.subsystemdefinitionconnector

@brief  Definition of a subsystem.

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
class AbstractSubSystemDefinitionImporter(object):
    '''
    Base class for SubSystemDefinition importer classes
    '''
    def load(self, rootPath):
        '''
        Loads a list of subsystem definitions from a given file path.

        @param  rootPath [in] (str) path to the definitions to load.

        @return (list) List of SubSystemDefinition instances
        '''
        raise NotImplementedError
    # end def load
# end class AbstractSubSystemDefinitionImporter

class AbstractSubSystemDefinitionExporter(object):
    '''
    Base class for SubSystemDefinition exporter classes
    '''
    def save(self, rootPath, subSystemDefinition, baseName = None):
        '''
        Saves a subsystem (and its children) to a given file path.

        @param  rootPath            [in] (str) path to the definitions to save.
        @param  subSystemDefinition [in] (SubSystemDefinition) The subsystem to save
        @option baseName            [in] (str) base name of the serialized file, without extension.
        '''
        raise NotImplementedError
    # end def save
# end class AbstractSubSystemDefinitionExporter

class SubSystemDefinitionImporterComposite(AbstractSubSystemDefinitionImporter, SubSystemComposite):
    '''
    SubSystem definition composite class

    This class can handle many SubSystem definition instances
    '''

    ClassReference = AbstractSubSystemDefinitionImporter

    def __init__(self):
        '''
        Constructor
        '''
        super(SubSystemDefinitionImporterComposite, self).__init__()

        self._childern = []
    # end def __init__

    def load(self, rootPath):
        '''
        @copydoc pyharness.subsystem.subsystemdefinitionconnector.AbstractSubSystemDefinitionImporter.load
        '''
        if (self._childern == []):
            raise IndexError('No child defined, unable to load')
        # end if

        for child in self._childern:
            result = child.load(rootPath)
            if (result is not None):
                break
            # end if
        # end for
        return result
    # end def load

# end class SubSystemDefinitionImporterComposite

class SubSystemDefinitionExporterComposite(AbstractSubSystemDefinitionExporter, SubSystemComposite):
    '''
    SubSystem definition composite class

    This class can handle many SubSystem definition instances
    '''

    ClassReference = AbstractSubSystemDefinitionExporter

    def __init__(self):
        '''
        Constructor
        '''
        super(SubSystemDefinitionExporterComposite, self).__init__()

        self._childern = []
    # end def __init__

    def save(self, rootPath, subSystemDefinition, baseName = None):
        '''
        @copydoc pyharness.subsystem.subsystemdefinitionconnector.AbstractSubSystemDefinitionExporter.save
        '''
        if (self._childern == []):
            raise IndexError('No child defined, unable to save')
        # end if

        for child in self._childern:
            child.save(rootPath, subSystemDefinition, baseName)
        # end for
    # end def save

# end class SubSystemDefinitionExporterComposite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
