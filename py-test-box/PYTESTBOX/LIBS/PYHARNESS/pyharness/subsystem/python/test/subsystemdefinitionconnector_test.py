#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.python.test.subsystemdefinitionconnectortest

@brief Abstract tests of SubSystemDefinitionConnector classes

@author christophe.roquebert

@date   2018/10/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.subsystem.python.subsystemdefinitionconnector   import PythonSubSystemDefinitionExporter
from pyharness.subsystem.python.subsystemdefinitionconnector   import PythonSubSystemDefinitionImporter
from pyharness.subsystem.test.subsystemdefinitionconnector_test import AbstractSubSystemDefinitionConnectorTestCase
# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class SubSystemDefinitionConnectorTestCase(AbstractSubSystemDefinitionConnectorTestCase):
    '''
    Tests the consistency between:
    - A SubSystemDefintionExporter
    - A SubSystemDefintionImporter
    .
    '''

    def _getBaseName(self):
        '''
        @copydoc pyharness.subsystem.test.subsystemdefinitionconnectortest.AbstractSubSystemDefinitionConnectorTestCase._getBaseName
        '''
        randomElement = self._tempDirPath[-4:]
        return "features%s_internal" % randomElement
    # end def _getBaseName

    @staticmethod
    def _createConnectors():
        '''
        @copydoc pyharness.subsystem.test.subsystemdefinitionconnectortest.AbstractSubSystemDefinitionConnectorTestCase._createConnectors
        '''
        return (PythonSubSystemDefinitionImporter(),
                PythonSubSystemDefinitionExporter())
    # end def _createConnectors
# end class SubSystemDefinitionConnectorTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
