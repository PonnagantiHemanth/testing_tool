#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.initools

@brief File tools

This module gives access to files utilities

@author christophe Roquebert

@date   2018/10/23
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from configparser           import ConfigParser
from os                     import R_OK
import os
# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class IniTool(object):
    '''
    A tool for accessing RsaKey ini files.

    This caches the access to the .ini files in memory as a performance enhancement.
    As this behaviour can be costly in memory, it can be disabled by setting
    the variable IniTool.iniCacheDepth to 0
    '''

    ## The number of ini files to keep in the cache.
    ## - The default is 1.
    ## - Set it to 0 to disable the cache mechanism.
    ## - Increase its value for greater performance (and memory consumption...)
    iniCacheDepth = 1

    ## The cached ini files
    ## This contains a list of tuples (stat, config)
    cachedIniFiles = {}
    cachedFifo     = []


    @staticmethod
    def _getConfig(filePath):
        '''
        Obtains and reads the ini file for the specified path.

        THIS IS NOT THREAD SAFE

        @param filePath [in] (str) The path to the ini file to load.
        @return The config read from the file or the cache, or an empty config if the file is not found.
        '''

        fileStat = os.stat(filePath)
        if (filePath in IniTool.cachedIniFiles):
            cachedStat, cachedConfig = IniTool.cachedIniFiles[filePath]

            # if the file was not modified, use the cache.
            if (fileStat == cachedStat):
                return cachedConfig
            # end if

            # Otherwise, invalidate the cache before proceeding further
            del IniTool.cachedIniFiles[filePath]

            # Remove the filePath from the cached FIFO, keeping the order
            IniTool.cachedFifo = [cachedPath for cachedPath in IniTool.cachedIniFiles if cachedPath != filePath]
        # end if

        # If there is not enough space left in the cache, truncate it
        for cachedPath in IniTool.cachedFifo[IniTool.iniCacheDepth:]:
            del IniTool.cachedIniFiles[cachedPath]
        # end for
        IniTool.cachedFifo = IniTool.cachedFifo[:IniTool.iniCacheDepth]

        # Read the config from the filePath
        config = ConfigParser()
        if (os.access(filePath, R_OK)):
            config.read(filePath)
        # end if

        # If there is still enough space in the cache, add the newly read
        # config to the cache
        if (len(IniTool.cachedFifo) < IniTool.iniCacheDepth):

            IniTool.cachedIniFiles[filePath] = (fileStat, config)
            IniTool.cachedFifo.insert(0, filePath)
        # end if

        # Finally, return the config
        return config
    # end def _getConfig


    @staticmethod
    def hasIniParameter(filename, section, parameter):
        '''
         Verify if parameter is present in ".ini" file

        @param  filename [in] (str) the filename
        @param  section [in] (str) the section within the file
        @param  parameter [in] (str) the parameter within the section

        @return True if parameter is present in file
        '''

        parsingFile = IniTool._getConfig(filename)

        result = False
        if parsingFile.has_section(section):
            if parsingFile.has_option(section, parameter):
                result = True
            # end if
        # end if
        return result
    # end def hasIniParameter


    @staticmethod
    def getIniParameter(filename, section, parameter):
        '''
        read a value from ".ini" file

        @param  filename [in] (str) source file
        @param  section [in] (str) section within the file
        @param  parameter [in] (str) parameter within the section

        @return  string containing read value
        @throws Exception if file error

        @note  this text file can be modified manually if you respect the following rule:
               ; comment line
               [SECTION]
               parameter = value
        '''

        if not os.access(filename, os.R_OK):
            raise Exception("IniTool - getIniParameter - file not exist")
        # end if

        if not IniTool.hasIniParameter(filename, section, parameter):
            raise Exception("IniTool - getIniParameter - parameter not found in file")
        # end if

        parsingFile = IniTool._getConfig(filename)
        return parsingFile.get(section, parameter)
    # end def getIniParameter


    @staticmethod
    def setIniParameter(filename, section, parameter, value):
        '''
        record a value into ".ini" file

        @param  filename [in] (str) destination file
        @param  section [in] (str) section within the file
        @param  parameter [in] (str) parameter within the section
        @param  value [in] (object) value to record

        @return  True if success, False otherwise
        '''

        parsingFile = IniTool._getConfig(filename)
        if not parsingFile.has_section(section):
            parsingFile.add_section(section)
        # end if
        parsingFile.set(section, parameter, value)
        result = True

        with open(filename, "r+") as writingFile:
            parsingFile.write(writingFile)
        # end with
        fileStat = os.stat(filename)

        if (filename in IniTool.cachedIniFiles):
            IniTool.cachedIniFiles[filename] = (fileStat, parsingFile)
        # end if

        return result
    # end def setIniParameter
# end class IniTool

# ------------------------------------------------------------------------------
#  END OF FILE
# ------------------------------------------------------------------------------
