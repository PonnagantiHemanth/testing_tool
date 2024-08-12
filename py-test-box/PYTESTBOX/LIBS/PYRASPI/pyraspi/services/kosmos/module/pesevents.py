#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Kosmos Generator
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.pesevents
:brief: Kosmos PES Action Events & Resume Events
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/02/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import fields
from itertools import count
from typing import Dict
from typing import Iterable
from typing import List
from typing import Type

from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.module.devicetree import DeviceTree
from pyraspi.services.kosmos.module.devicetree import DeviceTreeModuleBaseClass
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPERAND_BITS
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPERAND_MASK

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

# No-Operation events are special, and are identified via this name
NOP_EVENT_NAME = 'NOP_EVENT'

# LED PIN resume events name prefix
LED_PIN_EVENT_NAME = 'LED_PIN_'  # LED pin index is added as suffix


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

@dataclass(frozen=True)
class PesEventMapInterface(object, metaclass=ABCMeta):
    """
    PES Event Map Interface class
    """
    pass
# end class PesEventMapInterface


class PesEventModuleInterface(DeviceTreeModuleBaseClass, metaclass=ABCMeta):
    """
    Interface class that add the PES Action & Resume Events feature to a Kosmos module
    """

    # PES Event maps
    # Note: The type of these two attributes is expected to be overriden in the declaration of the final classes.
    #       After PES Events are initialized, the runtime type of these attribute conforms to what is defined below.
    #       This is a trick to get correct type hints and code suggestions while keeping the data structure API simple.
    action_event: PesEventMapInterface = None
    resume_event: PesEventMapInterface = None

    def init_pes_events(self, action_iter, resume_iter):
        """
        Initialize PES Events for the current module instance.

        :param action_iter: Iterator that is used to get the next available bit position for each event to create.
        :type action_iter: ``itertools.count``

        :param resume_iter: Iterator that is used to get the next available bit position for each event to create.
        :type resume_iter: ``itertools.count``
        """
        # noinspection PyTypeChecker
        self.action_event = self._init_pes_events(event_map_cls=self.action_event, event_iter=action_iter)
        # noinspection PyTypeChecker
        self.resume_event = self._init_pes_events(event_map_cls=self.resume_event, event_iter=resume_iter)
    # end def init_pes_events

    def _init_pes_events(self, event_map_cls, event_iter):
        """
        Compute all the PES Events for the current module and return an event map.

        :param event_map_cls: Event map class
        :type event_map_cls: ``Type[PesEventMapInterface]``
        :param event_iter: Iterator that is used to get the next available bit position for each newly created events.
        :type event_iter: ``itertools.count``

        :return: Event Map instance containing the PES Events related to the current module
        :rtype: ``PesEventMapInterface``

        :raise ``AssertionError``: invalid type for `event_map_cls`
        """
        # Before init: expect a class, not an instance
        # noinspection PyTypeChecker
        assert issubclass(event_map_cls, PesEventMapInterface), event_map_cls

        # Map of {event_name: PesEventBase(...)} used for dataclass initialization
        init_map = {f.name: f.type(name=f.name, module=self,
                                   value=(0 if f.name == NOP_EVENT_NAME else (1 << next(event_iter))))
                    for f in fields(event_map_cls)}

        # Create dataclass instance from dataclass type
        # noinspection PyCallingNonCallable
        event_map_obj = event_map_cls(**init_map)

        # After init: expect an instance, not a class
        assert isinstance(event_map_obj, PesEventMapInterface), event_map_obj
        return event_map_obj
    # end def _init_pes_events
# end class PesEventModuleInterface


@dataclass(frozen=True)
class PesEventBase(object):
    """
    Base dataclass representing a PES Event.
    This base class is not meant to be instantiated directly, except for verification purposes.
    """
    name: str
    value: int  # 16-bit unsigned integer

    @property
    def canonical_name(self):
        """
        Canonical name string; method to be overriden, returns `name` by default.

        Examples:
         - PesActionEventBase(TEST, 0xabcd)       --> 'TEST'

        :return: Canonical name of the PesEvent instance
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
        assert isinstance(self.value, int), self.value
        if self.name == NOP_EVENT_NAME:
            assert self.value == 0, self
        else:
            assert 0 < self.value <= PES_OPERAND_MASK, f'Out-of-bound value for event {self}.'
        # end if
    # end def __post_init__

    def __str__(self):
        """
        Short string representation of the PesEventBase instance.
        This is an adaptation of the code in dataclass._repr_fn() method.

        Examples:
         - "PesActionEventBase(TEST, 0xabcd)"

        :return: Short string representation of the PesEventBase instance
        :rtype: ``str``
        """
        return f'{self.__class__.__qualname__}({self.name}, {self.value:#06x})'
    # end def __str__

    def __call__(self):
        """
        Shorthand notation to set up a PES Events.
        """
        raise NotImplementedError(f'{self} base class cannot be called directly. '
                                  f'Only classes derived from {_PesEventMixin} support these feature.')
    # end def __call__
# end class PesEventBase


@dataclass(frozen=True)
class PesActionEventBase(PesEventBase):
    """
    PES Action Event Base class
    """
    pass
# end class PesActionEventBase


@dataclass(frozen=True)
class PesResumeEventBase(PesEventBase):
    """
    PES Resume Event Base class
    """
    pass
# end class PesResumeEventBase


@dataclass(frozen=True)
class _PesEventMixin(PesEventBase, metaclass=ABCMeta):
    """
    Data type representing a PES Event, also referencing the module instance it is related to.
    """
    module: PesEventModuleInterface

    @property
    def canonical_name(self):
        """
        Canonical name string, concatenating the module's canonical name and the PesEvent's name.
        The returned string is valid as a Python identifier as per the `str.isidentifier()` method.

        Examples:
         - PesActionEvent(PES, NOP_EVENT, 0x0000) --> 'PES_NOP_EVENT'
         - PesActionEvent(E7788_0, STOP, 0x0020)  --> 'E7788_0_STOP'
         - PesResumeEvent(BAS, READY, 0x0008)     --> 'BAS_READY'

        :return: Canonical name of the PesEvent instance
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
            assert isinstance(self.module, PesEventModuleInterface), self
        # end if
        assert self.canonical_name.isidentifier(), self.canonical_name
    # end def __post_init__

    def __str__(self):
        """
        Short string representation of the PesEvent instance.
        This is an adaptation of the code in dataclass._repr_fn() method.

        Examples:
         - "PesActionEvent(PES, NOP_EVENT, 0x0000)"
         - "PesActionEvent(E7788_0, STOP, 0x0020)"
         - "PesResumeEvent(BAS, READY, 0x0008)"
         - "PesActionEventBase(TEST, 0xabcd)"

        :return: Short string representation of the PesEvent instance
        :rtype: ``str``
        """
        return f'{self.__class__.__qualname__}({self.module.name}, {self.name}, {self.value:#06x})'
    # end def __str__

    @abstractmethod
    def __call__(self):
        """
        Shorthand notation to set up a PES Action or Resume Events.
        """
        raise NotImplementedAbstractMethodError()
    # end def __call__
# end class _PesEventMixin


@dataclass(frozen=True)
class PesActionEvent(_PesEventMixin, PesActionEventBase):
    """
    PES Action Event
    """
    def __call__(self):
        """
        Shorthand notation to set up a PES Action Event.

        Example:
        The following call using shorthand notation
            `self.kosmos.dt.pes.action_event.NOP_EVENT()`
        is equivalent to the standard pes.execute(...) notation
            `self.kosmos.dt.pes.execute(action=self.kosmos.dt.pes.action_event.NOP_EVENT)`
        """
        self.module.dt.pes.execute(action=self)
    # end def __call__
# end class PesActionEvent


@dataclass(frozen=True)
class PesResumeEvent(_PesEventMixin, PesResumeEventBase):
    """
    PES Resume Event
    """
    def __call__(self):
        """
        Shorthand notation to set up a PES Resume Event.

        Example:
        The following call using shorthand notation
            `self.kosmos.dt.pes.resume_event.NOP_EVENT()`
        is equivalent to the standard pes.wait(...) notation
            `self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.resume_event.NOP_EVENT)`
        """
        self.module.dt.pes.wait(action=self)
    # end def __call__
# end class PesResumeEvent


# Create special PesEvent objects for No-Operation events: no bit is set
PES_ACTION_EVENT_NOP = PesActionEventBase(name=NOP_EVENT_NAME, value=0)
PES_RESUME_EVENT_NOP = PesResumeEventBase(name=NOP_EVENT_NAME, value=0)


@dataclass(frozen=True, init=False)
class PesEvents(object):
    """
    Utility class for initialization of PES Action & Resume Events.
    Set PesEvent values depending on the Kosmos Device Tree configuration.
    """
    # Convenience lists that cross-reference all created PES Events
    action_event: List[PesActionEvent] = None
    resume_event: List[PesResumeEvent] = None

    # Mapping of the PES RESUME bits connected to LED pins
    # Pin mapping goes this way: LED_PIN[16-31] to PES_RESUME[0-15], depending on the available PES RESUME bits.
    led_pin_resume_events: Dict[int, PesResumeEvent] = None

    def __init__(self, dt):
        """
        :param dt: Kosmos Module Device Tree
        :type dt: ``DeviceTree``
        """
        # Loop through all `PesEventModuleInterface` modules in the Kosmos Device Tree and create `PesActionEvent` or
        # `PesResumeEvent` bitfields.
        action_list = []
        resume_list = []
        action_iter = count()  # iterator used to assign a value to each PesActionEvent
        resume_iter = count()  # iterator used to assign a value to each PesResumeEvent
        for instance in dt.flatmap.values():
            if isinstance(instance, PesEventModuleInterface):
                # Init all the PES Events for the selected module instance
                instance.init_pes_events(action_iter, resume_iter)
                # Reference the resulting events structures into global event lists, for convenient lookups
                action_list.extend(instance.action_event.__dict__.values())
                resume_list.extend(instance.resume_event.__dict__.values())
            # end if
        # end for

        # Connect the unused PES RESUME bits to LED pins
        # Pin mapping goes this way: LED_PIN[16-31] to PES_RESUME[0-15], depending on the available PES RESUME bits.
        led_pin_resume_events = {}
        for pes_resume_index in resume_iter:
            if pes_resume_index >= PES_OPERAND_BITS:
                break
            # end if
            led_pin_index = pes_resume_index + PES_OPERAND_BITS
            led_pin_resume_events[led_pin_index] = PesResumeEvent(name=f'{LED_PIN_EVENT_NAME}{led_pin_index:02}',
                                                                  value=1 << pes_resume_index,
                                                                  module=dt.pes)
        # end for
        resume_list.extend(led_pin_resume_events.values())

        # Force-set attributes, as dataclass is frozen
        object.__setattr__(self, 'action_event', action_list)
        object.__setattr__(self, 'resume_event', resume_list)
        object.__setattr__(self, 'led_pin_resume_events', led_pin_resume_events)
    # end def __init__
# end class PesEvents


def get_pes_events_combined_bitmask(events, event_type):
    """
    Returned the combined bitmask of all PES Events passed in arguments.

    :param events: A PES Event or a sequence of PES Events to compute the combined bitmask from
    :type events: ``PesEventBase or Iterable[PesEventBase]``
    :param event_type: The expected PES Event type(s)
    :type event_type: ``Type[PesEventBase] or tuple(Type[PesEventBase])``

    :return: Combined bitmask of all events passed in arguments.
    :rtype: ``int``

    :raise ``TypeError``: Unexpected event type
    :raise ``ValueError``: Resulting bitmask value is out-of-bound
    """
    bitmask = 0
    events = events if isinstance(events, Iterable) else [events]
    for event in events:
        if not isinstance(event, event_type):
            raise TypeError(f'Expected type {event_type}, got {type(event)} for events:\n\t'
                            + '\n\t'.join(str(e) for e in events))
        # end if
        bitmask |= event.value
    # end for

    if not 0 <= bitmask <= PES_OPERAND_MASK:
        raise ValueError(f'Out-of-bound bitmask value {bitmask:#06x} for events:\n\t'
                         + '\n\t'.join(str(e) for e in events))
    # end if
    return bitmask
# end def get_pes_events_combined_bitmask


def get_pes_action_events_combined_bitmask(events):
    """
    Returned the combined bitmask of all PES Action Events passed in arguments.

    :param events: A PES Action Event(s) to compute the combined bitmask from
    :type events: ``PesActionEventBase or Iterable[PesActionEventBase]``

    :return: Combined bitmask of all events passed in arguments.
    :rtype: ``int``
    """
    return get_pes_events_combined_bitmask(events, PesActionEventBase)
# end def get_pes_action_events_combined_bitmask


def get_pes_resume_events_combined_bitmask(events):
    """
    Returned the combined bitmask of all PES Resume Events passed in arguments.

    :param events: PES Resume Event(s) to compute the combined bitmask from
    :type events: ``PesResumeEventBase or Iterable[PesResumeEventBase]``

    :return: Combined bitmask of all events passed in arguments.
    :rtype: ``int``
    """
    return get_pes_events_combined_bitmask(events, PesResumeEventBase)
# end def get_pes_resume_events_combined_bitmask

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
