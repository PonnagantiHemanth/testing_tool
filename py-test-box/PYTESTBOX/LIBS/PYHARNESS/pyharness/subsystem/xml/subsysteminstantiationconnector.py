#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.xml.subsysteminstantiationconnector

@brief  Importer/exporters for xml-instantiated subsystems

@author christophe Roquebert

@date   2018/06/05
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.subsystem.subsysteminstantiation          import SubSystemInstantiation
from pyharness.subsystem.subsysteminstantiationconnector import AbstractSubSystemInstantiationImporter
from os.path                                           import basename
from os.path                                           import dirname
from os.path                                           import isfile
from os.path                                           import join
from xml.dom.minidom                                   import Node
from xml.dom.minidom                                   import parse

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class XmlSubSystemInstantiationImporter(AbstractSubSystemInstantiationImporter):
    '''
    Imports a SubSystemInstantiation from:
    - @c PRODUCT.main.xml files
    - @c VARIANT.xml files
    .

    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(XmlSubSystemInstantiationImporter, self).__init__()

        self._normedSysPath = None
    # end def __init__

    TRANSLATION_MAP = {'True':  'true',
                       'False': 'false',
                       'None':  None,
                       }

    TRANSLATION_HINT_MAP = {'True':  'boolean',
                            'False': 'boolean',
                            'None':  'auto',
                            }

    ENCODING = "iso-8859-1"

    @classmethod
    def _loadFromXmlFile(cls, xmlFilePath):
        '''
        Loads from a .xml file

        @param  xmlFilePath [in] (str) Path to the .xml file to read

        @return list of SubSystemInstantiation, with absolute paths
        '''
        result = []

        doc = parse(xmlFilePath)

        subSystemElement = doc.documentElement
        encoding = doc.encoding or cls.ENCODING

        # Sub selection elements
        subSystemElements = [child for child in subSystemElement.childNodes
                                  if (    (child.nodeType == Node.ELEMENT_NODE)
                                      and (child.tagName == 'section'))]

        for subSystemInstantiationPath in subSystemElements:
            for child in subSystemInstantiationPath.childNodes:
                if (    (child.nodeType == Node.ELEMENT_NODE)
                    and (child.tagName == 'features')):
                    features = child
                # end if
            # end for
            featureInstantiations = []
            featureElements = [child for child in features.childNodes
                                      if (    (child.nodeType == Node.ELEMENT_NODE)
                                          and (child.tagName == 'feature'))]
            for feature in featureElements:
                # Add the feature value
                for child in feature.childNodes:
                    if (    (child.nodeType == Node.ELEMENT_NODE)
                        and (child.tagName == 'name')):
                        name = child.childNodes[0].wholeText
                    # end if
                    if (    (child.nodeType == Node.ELEMENT_NODE)
                        and (child.tagName == 'value')):
                        value = child.childNodes[0].wholeText
                    # end if
                    if (    (child.nodeType == Node.ELEMENT_NODE)
                        and (child.tagName == 'type')):
                        featureType = child.childNodes[0].wholeText
                    # end if
                # end for
                featureType = cls.TRANSLATION_HINT_MAP.get(value, featureType)
                value       = cls.TRANSLATION_MAP.get(value, value)

                featureInstantiations.append(SubSystemInstantiation.FeatureInstantiation(name,
                                                                                         value    = value,
                                                                                         location = xmlFilePath,
                                                                                         type     = featureType))

            # end for

            for child in subSystemInstantiationPath.childNodes:
                if (    (child.nodeType == Node.ELEMENT_NODE)
                    and (child.tagName == 'name')):
                    sectionName = child.childNodes[0].wholeText
                # end if
            # end for
            result.append(SubSystemInstantiation(sectionName,
                                                 features = featureInstantiations,
                                                 location = xmlFilePath))

        # end for

        return sorted(result,
                      key = lambda x: x.path)
    # end def _loadFromXmlFile

    def _loadFromPath(self, leafPath, moveUp = True):
        '''
        Loads from a path, looking for xxx.xml, and looking up until a PRODUCT.main.xml is found.

        The results are returned in reverse order: First product, then variant, then subvariant...

        This allow simple the building of the actual subSystem by applying each SubSystemInstantiation in turn.

        @param  leafPath [in] (str) The path to look in.
        @param  moveUp   [in] (boolean) Whether to move up in the path
        @return List of SubsystemInstantiation
        '''
        result = []

        # Load from the target .ini
        baseName = basename(leafPath)

        # Look for a VARIANT.ini file
        xmlFilePath = join(leafPath, baseName + '.xml')
        if (isfile(xmlFilePath)):
            if (moveUp):
                resultTmp = self._loadFromPath(dirname(leafPath))
                if (resultTmp is not None):
                    result.extend(resultTmp)
                else:
                    return None
                # end if
            # end if

            result.extend(self._loadFromXmlFile(xmlFilePath))
        else:
            xmlFilePath = join(leafPath, baseName + '.main.xml')
            if (isfile(xmlFilePath)):
                result.extend(self._loadFromXmlFile(xmlFilePath))
            else:
                return None
            # end if
        # end if

        return result
    # end def _loadFromPath

    def load(self, leafPath, moveUp = True):
        '''
        @copydoc pyharness.subsystem.subsysteminstantiationconnector.AbstractSubSystemInstantiationImporter.load
        '''
        return self._loadFromPath(leafPath, moveUp)
    # end def load
# end class XmlSubSystemInstantiationImporter

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
