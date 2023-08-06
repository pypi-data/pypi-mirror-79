import enum
from datetime import datetime
from typing import Optional, List, Union, Set, Type
from uuid import UUID


import attr

from hackgame.cli.identifier_cache import CacheItem


# conforms to signature needed to be a filter in attr.astuple
def _is_human_readable(attribute, value=None):
    return attribute.metadata.get("human_readable", True)


def _tuple_factory(values):
    if len(values) == 1:
        return values[0]
    else:
        return tuple(values)


def _ensure_class(cl):
    """If the attribute is an instance of cls, pass, else try constructing."""

    def converter(val):
        if isinstance(val, cl):
            return val
        elif val is None:
            return val
        else:
            return cl(**val)

    return converter


def _ensure_class_collection(cl):
    """If the attribute is an instance of cls, pass, else try constructing."""

    def converter(collection):
        results = []
        for val in collection:
            if isinstance(val, cl):
                results.append(val)
            elif val is None:
                results.append(val)
            else:
                results.append(cl(**val))
        return results

    return converter


_HIDE = attr.ib(metadata=dict(human_readable=False))


def _NESTED(klass, many=False, count=False, unknown=False):

    converter_func = _ensure_class_collection if many else _ensure_class
    converter = converter_func(klass)
    metadata = dict(count=count, unknown=unknown)
    return attr.ib(converter=converter, metadata=metadata)


@attr.s
class _HumanReadable(object):
    """
    Adapts Attr Classes, providing as_row - which is used to modify output for a nice
    summary view. Doing stuff like hiding non-useful fields, aggregating nested fields
    into a count instead, etc.
    """

    @classmethod
    def headers(cls) -> list:
        return [f.name.upper().replace("_", " ") for f in cls._fields()]

    @classmethod
    def _fields(cls) -> list:
        return [f for f in attr.fields(cls) if _is_human_readable(f)]

    def as_row(self) -> list:
        """
        Applies attr.astuple() to this instance, with certain modifications:

        - hide certain fields
        - if a field is a single nested object and only has one visible field,
          hide the nesting.
        - if a field is multiple nested objects, display a count instead

        :return: Tuple of values
        """

        fields = self._fields()
        values = attr.astuple(
            self,
            filter=_is_human_readable,
            tuple_factory=_tuple_factory,
            recurse=True,
            retain_collection_types=True,
        )
        output = []
        for field, value in zip(fields, values):
            if field.metadata.get("count", False):
                output.append(len(value))
            elif field.metadata.get("unknown", False):
                _value = "?" if value is None else value
                output.append(_value)
            else:
                output.append(value)

        return output


@attr.s(auto_attribs=True)
class ObjectSummary(_HumanReadable):
    """Used when an Object is referenced in the API Representation of another Object"""

    handle: str
    public_uuid: UUID = _HIDE


def object_summary_to_cache_item(summary, object_type) -> CacheItem:
    return CacheItem(
        public_uuid=summary.public_uuid,
        handle=summary.handle,
        object_type=object_type,
        added_at=datetime.now(),
    )


@attr.s(auto_attribs=True)
class AnonymousObjectSummary(_HumanReadable):
    """
    Used when an Anonymous Object is referenced in
    the API Representation of another Object
    """

    handle: str


class IceSide(enum.IntEnum):
    """Indicates which side of a Connection an Ice is attached to"""

    SOURCE = 1
    DESTINATION = 2


@attr.s(auto_attribs=True)
class IceSummary(ObjectSummary):
    """Like ObjectSummary, but also display the IceSide"""

    side: IceSide = attr.ib(converter=lambda v: IceSide(v).name)
    url: str = _HIDE


@attr.s(auto_attribs=True)
class HackgameObject(_HumanReadable, object):
    """Fields which all Hackgame Objects share"""

    public_uuid: UUID
    handle: str
    world: UUID = _HIDE

    def cacheables(self) -> Set[CacheItem]:
        return set()


@attr.s(auto_attribs=True)
class AccessToken(HackgameObject):
    """Authentication"""
    player: ObjectSummary = _NESTED(ObjectSummary)
    acting_as: ObjectSummary = _NESTED(ObjectSummary)
    url: str = _HIDE
    world: ObjectSummary = _NESTED(ObjectSummary)

    def cacheables(self) -> Set[CacheItem]:
        return {object_summary_to_cache_item(self.world, World)}


@attr.s(auto_attribs=True)
class World(_HumanReadable):
    """Game Server"""
    public_uuid: UUID
    handle: str


@attr.s(auto_attribs=True)
class Player(HackgameObject):
    """Real People"""
    public_uuid: UUID
    handle: str


@attr.s(auto_attribs=True)
class Account(HackgameObject):
    """Characters"""
    url: str = _HIDE
    router: ObjectSummary = _NESTED(ObjectSummary)
    parent: Optional[ObjectSummary] = _NESTED(ObjectSummary, unknown=True)

    def cacheables(self) -> Set[CacheItem]:
        return {object_summary_to_cache_item(self.router, Network)}


@attr.s(auto_attribs=True)
class Network(HackgameObject):
    """Location"""
    url: str = _HIDE
    clients: Optional[list] = _NESTED(AnonymousObjectSummary, many=True, count=True)
    parent: Optional[ObjectSummary] = _NESTED(ObjectSummary, unknown=True)
    router: Optional[ObjectSummary] = _NESTED(ObjectSummary, unknown=True)

    def cacheables(self) -> Set[CacheItem]:
        _cacheables = set()
        if self.router is not None:
            _cacheables.add(object_summary_to_cache_item(self.router, Network))
        return _cacheables


class ConnectionState(enum.Enum):
    open = "open"
    active = "active"
    closed = "closed"


@attr.s(auto_attribs=True)
class Connection(HackgameObject):
    """Links Objects"""
    url: str = _HIDE
    target: str
    state: ConnectionState = attr.ib(converter=lambda v: ConnectionState(v).name)
    source: ObjectSummary = _NESTED(ObjectSummary)
    destination: Optional[ObjectSummary] = _NESTED(ObjectSummary)
    ice: Optional[List[ObjectSummary]] = _NESTED(IceSummary, many=True, count=True)
    parent: Optional[ObjectSummary] = _NESTED(ObjectSummary, unknown=True)
    secure_source: bool
    secure_destination: bool
    ttl: Optional[int]

    def cacheables(self) -> Set[CacheItem]:
        return {object_summary_to_cache_item(i, Ice) for i in self.ice}


@attr.s(auto_attribs=True)
class Program(HackgameObject):
    """Equipment"""
    url: str = _HIDE
    memory: int
    installed: bool
    parent: Optional[ObjectSummary] = _NESTED(ObjectSummary)


@attr.s(auto_attribs=True)
class Ice(HackgameObject):
    """Defends against hacks"""
    connection: ObjectSummary = _NESTED(ObjectSummary)
    side: IceSide = attr.ib(converter=lambda v: IceSide(v).name)
    url: str = _HIDE
    active: bool
    parent: Optional[ObjectSummary] = _NESTED(ObjectSummary, unknown=True)

    def cacheables(self) -> Set[CacheItem]:
        return {object_summary_to_cache_item(self.connection, Connection)}


class ErrorCode(enum.IntEnum):
    """Structured reasons why an API Request might fail"""

    generic = 1
    target_action_combo_forbidden = 2
    access_level = 3
    no_change = 4
    out_of_memory = 5


@attr.s(auto_attribs=True)
class ActionError:
    code: ErrorCode
    message: str


@attr.s(auto_attribs=True)
class ActionResult:
    success: bool
    """Whether the Action had an effect or not."""

    status_code: int
    """The HTTP Status Code that the API Response was returned with."""

    data: dict = attr.ib(default=attr.Factory(dict))
    """
    Any data that the Object served if the Action was successful, empty if this
    Action failed.
    """

    messages: List[str] = attr.ib(default=attr.Factory(list))
    """
    Other Information about the Action, can be populated regardless of whether the
    Action succeeded or failed.
    """

    errors: List[ActionError] = attr.ib(
        default=attr.Factory(list), converter=_ensure_class_collection(ActionError)
    )
    """Anything that went wrong during the Action, empty if the Action succeeded."""


ObjectType = Union[
    Type[Account],
    Type[Player],
    Type[AccessToken],
    Type[World],
    Type[Network],
    Type[Connection],
    Type[Program],
    Type[Ice],
]
