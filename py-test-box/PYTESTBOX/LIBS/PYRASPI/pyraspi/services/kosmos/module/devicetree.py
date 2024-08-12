#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Kosmos Generator
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.devicetree
:brief: Device Tree for Kosmos Modules
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/02/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Iterable as abc_Iterable
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from enum import auto
from enum import unique
from re import compile as re_compile
from re import sub
from types import MappingProxyType
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Set
from typing import TYPE_CHECKING

from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_DYN_BASE
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_DYN_END
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame
from pyraspi.services.kosmos.protocol.python.messagetable import MSG_TABLE_OPT_BASE
from pyraspi.services.kosmos.utils import AutoNameEnum

if TYPE_CHECKING:
    """
    This section is only visible to python static type checkers (`TYPE_CHECKING` is True),
    but not at python runtime (`TYPE_CHECKING` is False).

    Combined with `annotation` feature from `__future__` package, this satisfies the following requirements:
     - Solve python circular import dependencies between DeviceTree and Kosmos Modules,
     - Keep static type checking functional, to ease the development.

     Refer to:
      - <PEP 563 - Postponed Evaluation of Annotations> https://peps.python.org/pep-0563/,
      - <PEP 484 - Type Hints> https://peps.python.org/pep-0484/#runtime-or-type-checking,
      - this answer https://stackoverflow.com/a/39757388.
    """
    from pyraspi.services.kosmos.fpgatransport import FPGATransport
    from pyraspi.services.kosmos.module.adda import AddaModule
    from pyraspi.services.kosmos.module.bas import BasModule
    from pyraspi.services.kosmos.module.cmods6 import Cmods6Manager
    from pyraspi.services.kosmos.module.optemu_sensors import E7788Module
    from pyraspi.services.kosmos.module.optemu_sensors import E7790Module
    from pyraspi.services.kosmos.module.optemu_sensors import E7792Module
    from pyraspi.services.kosmos.module.optemu_sensors import Paw3266Module
    from pyraspi.services.kosmos.module.optemu_sensors import Pmw3816Module
    from pyraspi.services.kosmos.module.fpga import FpgaModule
    from pyraspi.services.kosmos.module.i2cspy import I2cSpyExtendedModule
    from pyraspi.services.kosmos.module.kbdmatrix import KbdMatrixModule
    from pyraspi.services.kosmos.module.kbdgtech import KbdGtechModule
    from pyraspi.services.kosmos.module.ledspy import LedSpyModule
    from pyraspi.services.kosmos.module.module import ModuleBaseClass
    from pyraspi.services.kosmos.module.pes import PesModule
    from pyraspi.services.kosmos.module.pescpu import PesCpuModule
    from pyraspi.services.kosmos.module.pestimer import PesTimersModule
    from pyraspi.services.kosmos.module.pio import PioModule
    from pyraspi.services.kosmos.module.sequencer import SequencerModule
# end if


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

# Regex matching the first characters in [_a-zA-Z0-9] of a string, excepted if it starts by a digit
_re_clean = re_compile(r'\W+|^(?=\d)')


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@unique
class DeviceName(AutoNameEnum):
    """
    List of Device Names present in the Kosmos DeviceTree.
    We ensure that all `DeviceName` enum values can be used as keys to address `DeviceTree` dataclass members.

    Note: There should be a 1:1 correspondence between `DeviceName` and `DeviceTree` members names
          (with a change of case), and members order.
          Each `DeviceName` enum members (in uppercase) must match a `DeviceTree` dataclass member name (in lowercase).
    """
    FPGA_TRANSPORT = auto()

    # --- Core FPGA Modules ---
    FPGA = auto()
    SEQUENCER = auto()
    PES = auto()
    PES_CPU = auto()
    TIMERS = auto()
    PIO = auto()
    ADDA = auto()
    CMODS6 = auto()

    # --- Optional FPGA Modules ---
    # /!\ NOTE: The optional module order must match the FPGA design. By convention let's always add newly designed
    # /!\        modules to the end of this dataclass: older first, newer last.
    KBD_MATRIX = auto()
    KBD_GTECH = auto()
    BAS = auto()
    LED_SPY = auto()
    I2C_SPY = auto()
    I2C_PER = auto()
    SPI_EM7770 = auto()
    SPI_E7788 = auto()
    SPI_E7790 = auto()
    SPI_E7792 = auto()
    SPI_PAW3266 = auto()
    SPI_PMW3816 = auto()
    SPI_MLX90393 = auto()
# end class DeviceName


@unique
class DeviceFamilyName(Set[DeviceName], Enum):
    """
    Regroups Device Names in Families of Devices of similar behavior or usage.
    """
    KBD_ANALOG = {DeviceName.KBD_GTECH}
    KBD_MATRIX = {DeviceName.KBD_MATRIX}
    KBD = KBD_ANALOG.union(KBD_MATRIX)
    AMBIENT_LIGHT_SENSOR = {DeviceName.ADDA}
    GENERIC_LED_SPY = {DeviceName.I2C_SPY,
                       DeviceName.LED_SPY}
    OPTICAL_SENSOR_12BITS = {DeviceName.SPI_E7792,
                             DeviceName.SPI_PAW3266}
    OPTICAL_SENSOR_16BITS = {DeviceName.SPI_E7788,
                             DeviceName.SPI_E7790,
                             DeviceName.SPI_PMW3816}
    OPTICAL_SENSOR = OPTICAL_SENSOR_12BITS.union(OPTICAL_SENSOR_16BITS)
    PROXIMITY_SENSOR = {DeviceName.BAS}
    WHEEL_SENSOR = {DeviceName.SPI_EM7770,
                    DeviceName.SPI_MLX90393}
# end class DeviceFamilyName


@dataclass(frozen=True)
class DeviceTree(Mapping):
    """
    Kosmos DeviceTree: Hold the Kosmos Modules instances.
    This represents the vertical integration FPGA module <-> Microblaze module <-> py-test-box module.

    Note 1: All module instances must be based on `DeviceTreeModuleBaseClass`.

    Note 2: All `DeviceTree` dataclass member names are guaranteed to be present in `DeviceName` Enum.
            That means all `DeviceName` Enum members can be used as keys to address this `DeviceTree`.
    """
    fpga_transport: FPGATransport

    # --- Core FPGA Modules ---
    fpga: FpgaModule
    sequencer: SequencerModule
    pes: PesModule
    pes_cpu: PesCpuModule
    timers: PesTimersModule
    pio: PioModule
    adda: AddaModule
    cmods6: Cmods6Manager

    # --- Optional FPGA Modules ---
    # /!\ NOTE: The optional module order must match the FPGA design. By convention let's always add newly designed
    # /!\        modules to the end of this dataclass: older first, newer last.
    kbd_matrix: KbdMatrixModule
    kbd_gtech: KbdGtechModule
    bas: BasModule
    led_spy: List[LedSpyModule]
    i2c_spy: List[I2cSpyExtendedModule]
    i2c_per: List[ModuleBaseClass]        # TODO
    spi_em7770: List[ModuleBaseClass]     # TODO
    spi_e7788: List[E7788Module]
    spi_e7790: List[E7790Module]
    spi_e7792: List[E7792Module]
    spi_paw3266: List[Paw3266Module]
    spi_pmw3816: List[Pmw3816Module]
    spi_mlx90393: List[ModuleBaseClass]   # TODO

    # --- Private attribute ---
    # Read-only mapping view of all module instances (not flattened)
    _map: MappingProxyType[str, DeviceTreeModuleBaseClass] = field(init=False)
    # Read-only mapping view of all module instances (flattened)
    _flatmap: MappingProxyType[str, DeviceTreeModuleBaseClass] = field(init=False)

    @property
    def flatmap(self):
        """
        Return a read-only view of the mapping <module.canonical_name : module> for each module present in the
        Device Tree. The mapping is based on a flattened list of modules from the Device Tree dataclass instance.

        Usage examples: (dt: DeviceTree)
         - dt.flatmap.len()
         - dt.flatmap.items(), dt.flatmap.keys(), dt.flatmap.values()
         - dt.flatmap[key], dt.flatmap.get(key, [default])
         - key in dt.flatmap
         - for key in dt.flatmap

         Refer to `types.MappingProxyType` class for complete usage documentation.

        :return: Read-only view of the mapping <module.canonical_name : module>
        :rtype: ``MappingProxyType[str, DeviceTreeModuleBaseClass]``
        """
        return self._flatmap
    # end def property getter flatmap

    def __post_init__(self):
        """
        Actions to perform after the instantiation of the DeviceTree.
        """
        self._init_map()
        self._init_flat_map()
        self._validate_device_names()
        self._set_device_tree()
        self._update_msg_table()
    # end def __post_init__

    def _init_map(self):
        """
        Create a read-only view of the mapping <device_name : module(s)> for each module present in the Device Tree.
        The dict is not flattened, so it contains modules AND list of modules from the Device Tree dataclass instance.
        The attributes with name prefixed by an underscore are private and thus are omitted from the created mapping.
        """
        devicemap = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

        # Force-set attribute, as dataclass is frozen
        object.__setattr__(self, '_map', MappingProxyType(devicemap))
    # end def _init_map

    def _init_flat_map(self):
        """
        Create a read-only view of the mapping <module.canonical_name : module> for each module present in the
        Device Tree. The mapping is based on a flattened list of modules from the Device Tree dataclass instance.

        :raise ``AssertionError``: One instance of the DeviceTree has invalid type
        """
        flatmap: Dict[str, DeviceTreeModuleBaseClass] = {}
        for name, instances in self.items():
            for instance in (instances if isinstance(instances, Iterable) else [instances]):
                assert isinstance(instance, DeviceTreeModuleBaseClass), (name, instance)
                flatmap[instance.canonical_name] = instance
            # end for
        # end for

        # Force-set attribute, as dataclass is frozen
        object.__setattr__(self, '_flatmap', MappingProxyType(flatmap))
    # end def _init_flat_map

    def _validate_device_names(self):
        """
        Validate that all members of `DeviceName` enum and `DeviceTree` dataclass match together.
        That ways we can ensure `DeviceName` enum values can be used as keys to address `DeviceTree` dataclass members.

        :raise ``AssertionError``: Kosmos DeviceName enum and DeviceTree dataclass do not match
        """
        dev_name_list = list(enum.value for enum in iter(DeviceName))
        dev_tree_list = list(self.keys())
        assert dev_name_list == dev_tree_list, f'Kosmos DeviceName enum and DeviceTree dataclass do not match:\n' \
                                               f'\tDeviceName: {dev_name_list}\n' \
                                               f'\tDeviceTree: {dev_tree_list}'
    # end def _validate_device_names

    def _set_device_tree(self):
        """
        Set reference to Device Tree recursively in DeviceTree entries.
        """
        for instance in self.flatmap.values():
            instance.init_device_tree(dt=self)
        # end for
    # end def _set_device_tree

    def _update_msg_table(self):
        """
        Update Message Table regarding Optional FPGA Modules.
        The original table is left intact, the update is performed on a copy.

        Note: Any exception

        :raise ``AssertionError``: multiple error source:
         - module instance shall not be optional
         - module instance message ID is out-of-range
        """
        extended_msg_table = deepcopy(MessageFrame.msg_table)
        for dev_name, dev_entry in self.items():
            instances = dev_entry if isinstance(dev_entry, Iterable) else [dev_entry]
            if any(instance.settings.optional for instance in instances):
                msg_ids = []
                for instance in instances:
                    assert instance.settings.optional, instance.settings
                    assert MSG_ID_DYN_BASE <= instance.settings.msg_id <= MSG_ID_DYN_END, instance.settings
                    msg_ids.append(instance.settings.msg_id)
                # end for
                optional_module_entry = MSG_TABLE_OPT_BASE[dev_name]
                if isinstance(optional_module_entry, Exception):
                    raise optional_module_entry
                # end if
                extended_msg_table[(min(msg_ids), max(msg_ids))] = deepcopy(optional_module_entry)
            # end if
        # end for
        MessageFrame.set_msg_table(extended_msg_table)
    # end def _update_msg_table

    def items(self):
        """
        Return a read-only Items View of all module instances (not flattened).

        Note: To get the items on a flattened view, call `self.flatmap.items()` instead.

        :return: items of `self._map`
        :rtype: ``ItemsView[str, DeviceTreeModuleBaseClass]``
        """
        return self._map.items()
    # end def items

    def keys(self):
        """
        Return a read-only Key View of all module instances (not flattened).

        Note: To get the keys on a flattened view, call `self.flatmap.keys()` instead.

        :return: keys of `self._map`
        :rtype: ``KeysView[str]``
        """
        return self._map.keys()
    # end def keys

    def values(self):
        """
        Return a read-only Values View of all module instances (not flattened).

        Note: To get the values on a flattened view, call `self.flatmap.values()` instead.

        :return: values of `self._map`
        :rtype: ``ValuesView[DeviceTreeModuleBaseClass]``
        """
        return self._map.values()
    # end def values

    def __iter__(self):
        """
        Return an iterator on the read-only mapping view of all module instances (not flattened).

        Note: To get an iterator on a flattened view, call `iter(self.flatmap)` instead.

        :return: iterator on `self._map`
        :rtype: ``Iterator[MappingProxyType[str, DeviceTreeModuleBaseClass]]``
        """
        return iter(self._map.values())
    # end def __iter__

    def __getitem__(self, device_name):
        """
        Return the module or list of module registered as `device_name` in the `DeviceTree` dataclass.
        This excludes private dataclass attributes, prefixed by an underscore.

        Note: To get a module by its canonical name, call `self.flatmap[canonical_name]` instead.

        Note: ``KeyError`` will be raised if `device_name` not found in the `DeviceTree`.

        :param device_name: name of the attributes of this dataclass
        :type device_name: ``str``

        :return: DeviceTree module(s)
        :rtype: ``DeviceTreeModuleBaseClass or List[DeviceTreeModuleBaseClass]``
        """
        return self._map[device_name]
    # end def __getitem__

    def __len__(self):
        """
        Return the count of instantiated DeviceTree modules, by device name

        Note: To get all modules instances count, call `len(self.flatmap)` instead.

        :return: Number of instantiated DeviceTree modules, by device name
        :rtype: ``int``
        """
        return len(self._map)
    # end def __len__
# end class DeviceTree


@dataclass(frozen=True)
class DeviceTreeModuleSettings(object):
    """
    Dataclass constructor arguments:
    ``name``: Module given name
    ``instance_id``: Module instance identifier number, None if singleton
    ``optional``: Is this module optional ?
                     If True, it can be instantiated depending on the Device Tree configuration.
                     If False, this module is always present.
    """
    name: str
    instance_id: Optional[int]
    optional: bool

    def __post_init__(self):
        """
        Dataclass initialization sanity checks.

        :raise ``AssertionError``: invalid dataclass member value
        """
        assert 0 < len(self.name) <= 20, \
            f'Module name must be 1 to 20 characters long, got "{self.name}".\n' \
            f'Please keep it short as it is often printed as prefix of log, warning, error messages.'
        assert self.instance_id is None or (isinstance(self.instance_id, int) and 0 <= self.instance_id), self
        assert isinstance(self.optional, bool), self.optional
    # end def __post_init__
# end class DeviceTreeModuleSettings


class DeviceTreeModuleBaseClass(object, metaclass=ABCMeta):
    """
    Kosmos Device Tree Module base class
    """
    _settings: DeviceTreeModuleSettings
    _dt: DeviceTree = None

    @abstractmethod
    def __init__(self, module_settings):
        """
        :param module_settings: Module settings dataclass object
        :type module_settings: ``DeviceTreeModuleSettings``

        :raise ``AssertionError``: invalid argument types
        """
        assert isinstance(module_settings, DeviceTreeModuleSettings), module_settings
        self._settings = module_settings
        assert self.canonical_name.isidentifier(), self.canonical_name
    # end def __init__

    @property
    def name(self):
        """
         Return Module's name concatenated to its instance number (if multiples).

         Examples:
            PES
            3DS
            I2C SPY [2]

        :return: Module's name
        :rtype: ``str``
        """
        return self.settings.name if self.settings.instance_id is None else \
            f'{self.settings.name} [{self.settings.instance_id}]'
    # end def property getter name

    @property
    def canonical_name(self):
        """
        Return Module's name concatenated to its instance number (if multiples).
        The returned string is sanitized to be valid for `str.isidentifier()` method.

         Examples:
            PES
            _3DS
            I2C_SPY_2

        :return: Module's name
        :rtype: ``str``
        """
        return to_identifier(self.settings.name) if self.settings.instance_id is None else \
            f'{to_identifier(self.settings.name)}_{self.settings.instance_id}'
    # end def property getter canonical_name

    @property
    def settings(self):
        """
        Return the module read-only setting dataclass.

        :return: Module read-only setting dataclass
        :rtype: ``DeviceTreeModuleSettings``
        """
        return self._settings
    # end def property getter settings

    @settings.setter
    def settings(self, _):
        """
        Prevent changing the module settings.

        :param _: Module Setting attribute (will fail to be set)
        :type _: ``Any``

        :raise ``AttributeError``: Module settings are read-only
        """
        raise AttributeError(f'{self.__class__.__name__} module settings are read-only.')
    # end def property setter settings

    @property
    def dt(self):
        """
        Return ``DeviceTree`` instance.

        :return: Kosmos Module Device Tree
        :rtype: ``DeviceTree``

        :raise ``AssertionError``: Device Tree was not initialized in the current module.
        """
        assert isinstance(self._dt, DeviceTree), f'Device Tree was not initialized in the current module {self}.'
        return self._dt
    # end def property getter dt

    @dt.setter
    def dt(self, _):
        """
        Prevent changing the module DeviceTree attribute.

        :param _: Module Device Tree attribute (will fail to be set)
        :type _: ``Any``

        :raise ``AttributeError``: Module DeviceTree attribute is read-only
        """
        raise AttributeError(f'{self.__class__.__name__} module DeviceTree attribute is read-only.')
    # end def property setter dt

    def init_device_tree(self, dt):
        """
        Link Device Tree to this module instance.

        :param dt: Kosmos Module Device Tree
        :type dt: ``DeviceTree``

        :raise ``AssertionError``: Device Tree type is wrong or was already set.
        """
        assert isinstance(dt, DeviceTree), dt
        assert self._dt is None, r'Device Tree cannot be changed after initialization.'
        self._dt = dt
        self.post_init_device_tree()
    # end def init_device_tree

    def post_init_device_tree(self):
        """
        Action to be done after Device Tree has been initialized.
        This method is meant to be overridden if needed.
        """
        pass
    # end def post_init_device_tree
# end class DeviceTreeModuleBaseClass


class DeviceTreeGenericModuleBaseClass(DeviceTreeModuleBaseClass, abc_Iterable, metaclass=ABCMeta):
    """
    Kosmos Device Tree Generic Module base class.
    This class allows to store and reference all instances derived from DeviceTreeModuleBaseClass in a Dictionary.
    This Dictionary stores class name as key and class instances as value.
    """

    # Class attribute
    _instances: Dict[str, List[DeviceTreeModuleBaseClass]] = {}

    @abstractmethod
    def __init__(self, module_settings):
        """
        :param module_settings: Module settings dataclass object
        :type module_settings: ``StatusResetModuleSettings``

        :raise ``AssertionError``: invalid argument types
        """
        # Let other subclasses initialize first
        super().__init__(module_settings=module_settings)

        # Sanity checks
        assert self.settings.optional, self.settings
        assert isinstance(self.__class__._instances, Dict), self.__class__._instances

        # Register current class instance in dictionary of instance
        if not self.settings.name in self.__class__._instances:
            # Add current class instance to a new class instance list
            self.__class__._instances[self.settings.name] = [self]
        else:
            # Add current class instance to an existing class instance list
            self.__class__._instances[self.settings.name].append(self)
        # end if
    # end def __init__

    @property
    def instances(self):
        """
        Return the list of instances of the Module.

        :return: list of instances of the Module
        :rtype: ``List[DeviceTreeModuleBaseClass]``
        """
        return self.__class__._instances[self.settings.name]
    # end def property getter instances

    def __iter__(self):
        """
        Iterator on the list of instances of the Module.

        :return: iterator on `self.instances`
        :rtype: ``Iterator[DeviceTreeModuleBaseClass]``
        """
        return iter(self.instances)
    # end def __iter__

    def __len__(self):
        """
        Length of the list of instances of the Module.

        :return: length of the list of instances of the Module
        :rtype: ``int``
        """
        return len(self.instances)
    # end def __len__

    def __getitem__(self, i):
        """
        Return an item from list of instances of the Module.

        Note: ``IndexError`` will be raised for invalid instance index

        :param i: instance index
        :type i: ``int``

        :return: instance
        :rtype: ``int``

        """
        return self.instances[i]
    # end def __getitem__
# end class DeviceTreeGenericModuleBaseClass


def to_identifier(string):
    """
    This substitution replaces any non-variable appropriate character with underscore
    and inserts underscore in front if the string starts with a digit.

    :param string: string to be sanitized
    :type string: ``str``

    :return: A string valid for `str.isidentifier()` method
    :rtype: ``str``
    """
    return sub(_re_clean, r'_', string)
# end def to_identifier

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
