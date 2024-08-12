#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.ui.configuration

@brief  Configuration registry for the GUI

@author christophe Roquebert

@date   2018/01/21
'''
# ------------------------------------------------------------------------------
# pylint:disable=E0611,C8101
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.config            import ConfigParser
from pyharness.arguments                 import KeywordArguments
from pyharness.consts                    import DEFAULT_OUTPUT_DIRECTORY
from pyharness.output.xmlhttpui          import XmlHttpClient
from os                                 import F_OK
from os                                 import access
from os.path                            import join
import urllib.request, urllib.parse, urllib.error
import wx

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PyHarnessConfiguration(object):
    '''
    Configuration interface
    '''
    AVAILABLE_OPTIONS = ()

    def __init__(self):
        '''
        Constructor
        '''
        self._fullPathToConfigFile  = None
        self._repeatSynchronization = True
        self._instances             = {}

    # end def __init__

    def _getFullPathToConfigFile(self, iniFile,
                                       kwArgs):
        '''
        Create path to access an PyHarness ini file

        @param  iniFile [in] (str)  INI file name
        @param  kwArgs  [in] (dict) Keywords arguments

        @return (str) Full ini path
        '''
        attrNameAndOverridePrefixes = [(key.lower(), '%s.value=' % key.upper()) for key in ('product', 'variant', 'target', 'mode')]
        for (attrName, _) in attrNameAndOverridePrefixes:
            setattr(self, attrName, None)
        # end for

        if KeywordArguments.KEY_OVERRIDES in kwArgs:
            for override in kwArgs[KeywordArguments.KEY_OVERRIDES]:
                for (attrName, overridePrefix) in attrNameAndOverridePrefixes:
                    if override.startswith(overridePrefix):
                        setattr(self, attrName, override[len(overridePrefix):])
                    # end if
                # end for
            # end for
        # end if

        return join(kwArgs[KeywordArguments.KEY_ROOT],
                    DEFAULT_OUTPUT_DIRECTORY,
                    iniFile)

    # end def _getFullPathToConfigFile

    def create(self, *args,
                     **kwargs):
        '''
        Factory method for creating the Configuration.

        @option args   [in] (tuple) The arguments of the constructor
        @option kwargs [in] (dict)  The keyword arguments of the constructor.

        @return (Configuration) The instance of the configuration
        '''
        if (self.__class__ not in self._instances):
            self._instances[self.__class__] = self.__class__(*args, **kwargs)
        # end if
        return self._instances[self.__class__]

    # end def create

    def hasOption(self, name):
        '''
        Check if an option is supported by the configuration

        @param  name [in] (str) Name of an option

        @return (bool) True if option supported by the configuration
        '''
        return name in self.AVAILABLE_OPTIONS
    # end def hasOption

    def getOption(self, name,
                        defaultValue,
                        section):
        '''
        Obtains an option from the configuration file.

        @param  name         [in] (str)    The name of the option
        @param  defaultValue [in] (object) The value of the option, if it is not
                                           found in the configuration file
        @param  section      [in] (str)    The section of the option

        @return The value of the option.
        '''
        config = ConfigParser()
        if (access(self._fullPathToConfigFile, F_OK)):
            config.load(self._fullPathToConfigFile)
            result = config.get(section, name, defaultValue)
        else:
            result = defaultValue
        # end if

        return result
    # end def getOption

    def setOption(self, name,
                        value,
                        section):
        '''
        Sets the value for a configuration option.

        @param  name    [in] (str)    The name of the option to obtain.
        @param  value   [in] (object) The value of the option to obtain
        @param  section [in] (str)    The section of the option to obtain
        '''
        config = ConfigParser()
        if (access(self._fullPathToConfigFile, F_OK)):
            config.load(self._fullPathToConfigFile)
        # end if
        config.set(section, name, value)
        config.write(self._fullPathToConfigFile)
    # end def setOption

# end class PyHarnessConfiguration


class ConfigurationChain(PyHarnessConfiguration):
    '''
    Handle a chain of configurations
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(ConfigurationChain, self).__init__()

        self.runs = {}

        self.runConfig              = None
        self._connectionHash        = None
        self._connection            = None
        self._synchronized          = False

        self._chain = []
    # end def __init__

    def addConfig(self, config):
        '''
        Append of an PyHarnessConfiguration instance

        @param  config [in] (PyHarnessConfiguration) Configuration to add
        '''
        self._chain.append(config)
    # end def addConfig

    def getOption(self, name,
                        defaultValue,
                        section = None):
        '''
        @copydoc pyharness.ui.configuration.PyHarnessConfiguration.getOption
        '''
        result = None
        for config in self._chain:
            if config.hasOption(name):
                result = config.getOption(name, defaultValue)
                break
            # end if
        else:
            raise ValueError('Unable to find a config supporting option: %s'
                             % name)
        # end for
        return result
    # end def getOption

    def setOption(self, name,
                        value,
                        section = None):
        '''
        @copydoc pyharness.ui.configuration.PyHarnessConfiguration.setOption
        '''
        result = None
        for config in self._chain:
            if config.hasOption(name):
                result = config.setOption(name, value)
                break
            # end if
        else:
            raise ValueError('Unable to find a config supporting option: %s'
                             % name)
        # end for
        return result
    # end def setOption

    reservedAttr = ('_chain',
                    '_instances',
                    'runs',
                    'runConfig',
                    '_connectionHash',
                    '_connection',
                    '_synchronized',
                    '_fullPathToConfigFile',
                    '_repeatSynchronization')

    def __getattr__(self, name):
        '''
        Get attribute value

        @param  name [in] (str) Name of the attribute to get

        @return (object) Value of the attribute
        '''
        result = None
        if (name in self.reservedAttr):
            result = self.__dict__[name]
        else:
            for config in self._chain:
                if hasattr(config, name):
                    result = getattr(config, name)
                    break
                # end if
            else:
                raise AttributeError('Unable to find a config supporting attribute: %s'
                                   % name)
            # end for
        # end if
        return result
    # end def __getattr__

    def __setattr__(self, name,
                          value):
        '''
        Set attribute value

        @param  name  [in] (str) Name of the attribute to get
        @param  value [in] (any) Value of the Attribute
        '''
        if (name in self.reservedAttr):
            self.__dict__[name] = value
        else:
            for config in self._chain:
                if hasattr(config, name):
                    setattr(config, name, value)
                    break
                # end if
            else:
                raise AttributeError('Unable to find a config supporting attribute: %s'
                                   % name)
            # end for
        # end if
    # end def __setattr__

    def _connect(self, url        = None,
                       name       = None,
                       user       = None,
                       password   = None,
                       clientName = None):
        '''
        Connects to the server

        @option url        [in] (str) The server url
        @option name       [in] (str) The DB name
        @option user       [in] (str) The server user
        @option password   [in] (str) The server password
        @option clientName [in] (str) Client name

        @return (XmlHttpClient) A connection to the database
        '''
        url        = url        is not None and url        or self.dbUrl
        name       = name       is not None and name       or self.dbName
        user       = user       is not None and user       or self.dbUser
        password   = password   is not None and password   or self.dbPassword
        clientName = clientName is not None and clientName or self.dbClientName

        from hashlib                    import md5
        connectionHash = md5('/'.join((url, name, user, password))).digest()                                            # pylint:disable=E1101,E1121
        if (self._connectionHash != connectionHash):
            connection = XmlHttpClient(url        = url,
                                       name       = name,
                                       user       = user,
                                       password   = password,
                                       clientName = clientName)
            self._connection = connection
            self._connectionHash = connectionHash
        else:
            connection = self._connection
        # end if

        # This attempts sends a ping request, and validates the connection.
        connection.ping()

        return connection
    # end def _connect

    def validateConnection(self, url,
                                 name,
                                 user,
                                 password):
        '''
        Tests the connection to the server

        @param  url      [in] (str) The server url
        @param  name     [in] (str) The DB name
        @param  user     [in] (str) The server user
        @param  password [in] (str) The server password
        '''
        self._connect(url, name, user, password)
    # end def validateConnection

    def synchronize(self, force = False):
        '''
        Synchronizes the run and config list with the server

        @option force [in] (bool) Force the synchronization
        '''
        if (force or self._repeatSynchronization):
            runs = {}
            try:
                connection = self._connect()
                runs = connection.getRunsAndRunConfigs(('runnable', 'initializable'))
                connection.close()
                self._synchronized = True

            except Exception as excp:                                                                                   # pylint:disable=W0703
                message = excp.args[-1] if len(excp.args) else excp
                wx.MessageBox("Unable to synchronize with server:\n%s" % message,
                              caption = 'PyHarness distributed client')

            # end try

            self.runs = runs
        # end if
        self._repeatSynchronization = False
    # end def synchronize

    def isSynchronized(self):
        '''
        Test if the run and config list with the server are synchronized

        @return (bool) Synchronization status
        '''
        return self._synchronized
    # end def isSynchronized

    def buildRunAddressFromRunConfigId(self, runConfigId):
        '''
        Build the address to the selected run page

        @param  runConfigId [in] (str) Run config identifier

        @return (None,str) Address to the run page
        '''
        if (self.runConfig is None):
            return
        # end if

        runId = [x for x, y in self.runs.items() if (runConfigId in y['runConfigs'])][0]

        return self.buildRunAddress(eval(runId))

    # end def buildRunAddressFromRunConfigId

    def buildRunAddress(self, runIdOrName):
        '''
        Build the address to the selected run page

        @param  runIdOrName [in] (int/str) Run identifier

        @return (None,str) Address to the run page
        '''
        if isinstance(runIdOrName, str):
            runIdOrName = [x for x, y in self.runs.items() if (runIdOrName == y['name'])][0]
        # end if

        params = urllib.parse.urlencode({'db': self.dbName, 'runid': runIdOrName})
        return '%suser_run.php?%s' % (self._dbUrl, params)

    # end def buildRunAddress

# end class ConfigurationChain

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
