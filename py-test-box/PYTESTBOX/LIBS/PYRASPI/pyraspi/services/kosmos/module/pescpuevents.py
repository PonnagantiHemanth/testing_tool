#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Kosmos Generator
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.pescpuevents
:brief: Kosmos PES CPU Events
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/03/01
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from dataclasses import dataclass
from dataclasses import fields
from dataclasses import replace
from typing import List
from typing import Type

from pyraspi.services.kosmos.module.devicetree import DeviceTree
from pyraspi.services.kosmos.module.module import ModuleBaseClass
from pyraspi.services.kosmos.module.pesevents import NOP_EVENT_NAME
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_BIT
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_PARAM_BIT


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class PesCpuEventMapInterface(object, metaclass=ABCMeta):
    """
    Interface class for PES-CPU Events
    """
    pass
# end class PesCpuEventMapInterface


class PesCpuEventModuleInterface(ModuleBaseClass, metaclass=ABCMeta):
    """
    Interface class for adding the PES CPU Events feature to a Kosmos module
    """

    # PES CPU Event maps
    # Note: The type of this attribute is expected to be overriden in the declaration of the final classes.
    #       After PES CPU Events are initialized, the runtime type of these attribute conforms to what is defined below.
    #       This is a trick to get correct type hints and code suggestions while keeping the data structure API simple.
    cpu_event: PesCpuEventMapInterface = None

    def init_pes_cpu_events(self):
        """
        Initialize PES CPU Events for the current module instance.
        """
        # noinspection PyTypeChecker
        self.cpu_event = self._init_pes_cpu_events(event_map_cls=self.cpu_event)
    # end def init_pes_cpu_events

    def _init_pes_cpu_events(self, event_map_cls):
        """
        Compute all the PES CPU Events for the current module and return an event map.

        :param event_map_cls: Event map class
        :type event_map_cls: ``Type[PesCpuEventMapInterface]``

        :return: Event Map instance containing the PES CPU Events related to the current module
        :rtype: ``PesCpuEventMapInterface``

        :raise ``AssertionError``: Invalid event map type
        """
        # Before init: expect a class, not an instance
        # noinspection PyTypeChecker
        assert issubclass(event_map_cls, PesCpuEventMapInterface), event_map_cls

        # Map of {event_name: PesCpuEventBase(...)} used for dataclass initialization
        init_map = {f.name: f.type(name=f.name, module=self, event=getattr(event_map_cls, f.name), param=0)
                    for f in fields(event_map_cls)}

        # Create dataclass instance from dataclass type
        # noinspection PyCallingNonCallable
        event_map_obj = event_map_cls(**init_map)

        # After init: expect an instance, not a class
        assert isinstance(event_map_obj, PesCpuEventMapInterface), event_map_obj
        return event_map_obj
    # end def _init_pes_cpu_events
# end class PesCpuEventModuleInterface


@dataclass(frozen=True)
class PesCpuEventBase(object):
    """
    Base dataclass representing a PES CPU Event.
    This base class is not meant to be instantiated directly, except for verification purposes.
    """
    name: str
    module_id: int  # 8-bit unsigned integer
    event: int      # 8-bit unsigned integer
    param: int      # 16-bit unsigned integer

    @property
    def canonical_name(self):
        """
        Canonical name string; method to be overriden, returns `name` by default.

        Examples:
         - PesCpuEventBase(TEST, 0xabcd)       --> 'TEST'

        :return: Canonical name of the PesCpuEvent instance
        :rtype: ``str``
        """
        return self.name
    # end def property getter canonical_name

    def __post_init__(self):
        """
        Sanity checks

        :raise ``AssertionError``:  a dataclass member value or type is invalid
        """
        assert self.name.isidentifier(), f'Module name must be a a valid identifier ' \
                                         f'([a-zA-Z0-9_] characters, without leading numbers), got "{self.name}".'
        assert isinstance(self.event, int), self.event
        if self.name == NOP_EVENT_NAME:
            assert self.event == 0, self
        else:
            assert 0 <= self.event <= (1 << PES_CPU_ACTION_BIT), f'Out-of-bounds value for {self}.'
        # end if

        assert isinstance(self.param, int), self.param
        assert 0 <= self.param <= (1 << PES_CPU_PARAM_BIT), f'Out-of-bounds param for {self}.'
    # end def __post_init__

    def with_param(self, param):
        """
        Return a copy of the current event, with a new `param` value.

        :param param: Value to be passed along the PES CPU Event (max `PES_CPU_PARAM_BIT` bits)
        :type param: ``int``

        :return: copy of the current event instance, with a new `param` value.
        :rtype: ``PesCpuEventBase``
        """
        return replace(self, param=param)
    # end def with_param

    def __str__(self):
        """
        Short string representation of the PesCpuEventBase instance.
        This is an adaptation of `dataclass._repr_fn()` method.

        Examples:
         - PesCpuEventBase(TEST, 0x42, 123456)

        :return: Short string representation of the PesCpuEventBase instance
        :rtype: ``str``
        """
        return f'{self.__class__.__qualname__}({self.name}, {self.event:#04x}, {self.param})'
    # end def __str__

    def __call__(self):
        """
        Shorthand notation to set up a PES CPU Events.
        """
        raise NotImplementedError(f'{self} base class cannot be called directly. '
                                  f'Only classes derived from {PesCpuEvent} support these feature.')
    # end def __call__
# end class PesCpuEventBase


@dataclass(frozen=True, init=False)
class PesCpuEvent(PesCpuEventBase):
    """
    Data type representing a PES CPU Event, also referencing the module instance it is related to.
    """
    module: PesCpuEventModuleInterface

    def __init__(self, name, module, event, param=0, module_id=None):
        """
        :param name: PES CPU Event name
        :type name: ``str``
        :param module: Module supporting the event
        :type module: ``PesCpuEventModuleInterface``
        :param event:  Event identifier for the given module, 8-bit positive integer
        :type event: ``int``
        :param param: Optional parameter to pass along the event, 16-bit positive integer, defaults to 0 - OPTIONAL
        :type param: ``int``
        :param module_id: Module ID, default to None (if not applicable) - OPTIONAL
        :type module_id: ``int or None``

        :raise ``AssertionError``: multiple source of error:
         - Invalid module type
         - Invalid module ID
        """
        assert isinstance(module, PesCpuEventModuleInterface), self
        assert module_id is None or module_id == module.settings.msg_id, (module_id, module.settings)
        object.__setattr__(self, 'module', module)
        super().__init__(name=name, module_id=module.settings.msg_id, event=event, param=param)
        # Note: Calling the base class __init__() will call __post__init__() on this class
    # end def __init__

    @property
    def canonical_name(self):
        """
        Canonical name string, concatenating the module's canonical name and the PesCpuEvent's name.
        The returned string is valid as a Python identifier as per the `str.isidentifier()` method.

        Examples:
         - PesCpuEvent(PES_CPU, NOP_EVENT, 0x00)     --> 'PES_CPU_NOP_EVENT'
         - PesCpuEvent(I2C_SPY_0, FLUSH_FIFO, 0x02)  --> 'I2C_SPY_0_FLUSH_FIFO'

        :return: Canonical name of the PesCpuEvent instance
        :rtype: ``str``
        """
        return f'{self.module.canonical_name}_{super().canonical_name}'
    # end def property getter canonical_name

    def __post_init__(self):
        """
        Sanity checks

        :raise ``AssertionError``:  a dataclass member value or type is invalid
        """
        super().__post_init__()
        if self.name != NOP_EVENT_NAME:
            assert isinstance(self.module, PesCpuEventModuleInterface), self
        # end if
        assert self.canonical_name.isidentifier(), self.canonical_name
    # end def __post_init__

    def __str__(self):
        """
        Short string representation of the PesCpuEvent instance.
        This is an adaptation of `dataclass._repr_fn()` method.

        Examples:
         - PesCpuEvent(PES_CPU, NOP_EVENT, 0x00, 0)
         - PesCpuEvent(I2C_SPY_0, FLUSH_FIFO, 0x02, 0)
         - PesCpuEventBase(TEST, 0x42, 123456)

        :return: Short string representation of the PesCpuEvent instance
        :rtype: ``str``
        """
        return f'{self.__class__.__qualname__}({self.module.canonical_name}, {self.name}, {self.event:#04x}, ' \
               f'{self.param})'
    # end def __str__

    def __call__(self, param=None):
        """
        Shorthand notation to set up a PES CPU Event.

        Example:
        The following call using shorthand notation
            `self.kosmos.dt.pes_cpu.cpu_event.NOP_EVENT()`
        is equivalent to the standard pes_cpu.action(...) notation
            `self.kosmos.dt.pes_cpu.action(cpu_event=self.kosmos.dt.pes_cpu.cpu_event.NOP_EVENT)`

        :param param: Value to be passed along the PES CPU Event (max `PES_CPU_PARAM_BIT` bits) - OPTIONAL
        :type param: ``int``
        """
        if param is None:
            self.module.dt.pes_cpu.action(cpu_event=self)
        else:
            self.module.dt.pes_cpu.action(cpu_event=self.with_param(param=param))
        # end if
    # end def __call__
# end class PesCpuEvent


@dataclass(frozen=True, init=False)
class PesCpuEvents(object):
    """
    Utility class for initialization of Pes Action & Resume Events.
    Set PesCpuEvent values depending on the Kosmos Device Tree configuration.
    """
    # Convenience list that cross-reference all created PES CPU Events
    cpu_event: List[PesCpuEvent] = None

    def __init__(self, dt):
        """
        :param dt: Kosmos Module Device Tree
        :type dt: ``DeviceTree``
        """
        # Loop through all `PesCpuEventModuleInterface` modules in the Kosmos Device Tree and create `PesCpuEvent`s.
        event_list = []
        for instance in dt.flatmap.values():
            if isinstance(instance, PesCpuEventModuleInterface):
                # Init all the PES Events for the selected module instance
                instance.init_pes_cpu_events()
                # Reference the resulting events structures into global event lists, for convenient lookups
                event_list.extend(instance.cpu_event.__dict__.values())
            # end if
        # end for

        # Force-set attribute, as dataclass is frozen
        object.__setattr__(self, 'cpu_event', event_list)
    # end def __init__
# end class PesCpuEvents

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
