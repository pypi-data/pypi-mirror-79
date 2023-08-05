import enum
import hashlib
import operator as op
from types import MappingProxyType
from typing import Any, Dict, List, Union

from cognite.air._api import BaseAPIClient
from cognite.air.constants import (
    AIR_EVENTS_FIELD_SUBTYPE,
    AIR_EVENTS_FIELD_TYPE,
    AIR_EVENTS_META_KEY_MODEL,
    AIR_EVENTS_META_KEY_MODEL_VERSION,
    AIR_EVENTS_META_KEY_SA_EXT_ID,
    EVENT_ASSET_IDS,
    EVENT_DATA_SET_ID,
    EVENT_DATA_SET_IDS,
    EVENT_EXT_ID,
    EVENT_METADATA,
    EVENT_SUBTYPE,
    EVENT_TYPE,
    SA_EXT_ID,
)
from cognite.air.utils import valfilter
from cognite.client.data_classes import Event, EventList
from cognite.client.exceptions import CogniteDuplicatedError


@enum.unique
class EventEndpoints(enum.Enum):
    LIST = enum.auto()
    CREATE_OR_UPDATE = enum.auto()


class AIREventsAPI(BaseAPIClient):
    RESERVED_AIR_EVENT_META_KEYS = set([AIR_EVENTS_META_KEY_MODEL, AIR_EVENTS_META_KEY_MODEL_VERSION, SA_EXT_ID])
    RESERVED_PARAMS_DCT = MappingProxyType(
        {
            EventEndpoints.LIST: set([EVENT_TYPE, EVENT_SUBTYPE, EVENT_ASSET_IDS, EVENT_DATA_SET_IDS]),
            EventEndpoints.CREATE_OR_UPDATE: set(
                [EVENT_EXT_ID, EVENT_TYPE, EVENT_SUBTYPE, EVENT_ASSET_IDS, EVENT_DATA_SET_ID]
            ),
        }
    )

    @property
    def air_event_required_meta(self):
        return {
            AIR_EVENTS_META_KEY_MODEL: self._config.model_name,
            AIR_EVENTS_META_KEY_MODEL_VERSION: self._config.model_version_stripped,
            AIR_EVENTS_META_KEY_SA_EXT_ID: self._config.schedule_asset_ext_id,
        }

    def _create_air_attr_dct(self, meta):
        return {
            EVENT_TYPE: AIR_EVENTS_FIELD_TYPE,
            EVENT_SUBTYPE: AIR_EVENTS_FIELD_SUBTYPE,
            EVENT_ASSET_IDS: [self._config.schedule_asset_id],
            EVENT_METADATA: {**meta, **self.air_event_required_meta},
        }

    def _verify_valid_air_event_query(self, endpoint: EventEndpoints, query_dct: Dict) -> None:
        reserved_params = self.RESERVED_PARAMS_DCT.get(endpoint)
        if reserved_params is None:
            raise TypeError(f"Expected 'endpoint' to be an {EventEndpoints}, not {type(endpoint)}")

        illegal_params = reserved_params.intersection(query_dct)
        if illegal_params:
            raise ValueError(f"Got one or more parameters reserved for AIR: {illegal_params}")

        kw_meta = query_dct.get(EVENT_METADATA, {})
        illegal_meta_keys = self.RESERVED_AIR_EVENT_META_KEYS.intersection(kw_meta)
        if illegal_meta_keys:
            raise ValueError(f"{EVENT_METADATA} contained one or more keys reserved for AIR: {illegal_meta_keys}")

    def _create_event_external_id(self, ev_dct: Dict[str, Any]) -> str:
        dcts = map(op.methodcaller("items"), (self.air_event_required_meta, ev_dct, ev_dct.get(EVENT_METADATA, {})))
        hash_input = "".join((f"{k}{v}" for d in dcts for k, v in d if isinstance(v, (str, int, float))))
        return hashlib.md5(hash_input.encode()).hexdigest()  # nosec

    def _make_events_air_compatible_inplace(self, events: List[Event]) -> None:
        for ev in events:
            param_dct = valfilter(lambda v: v is not None, vars(ev))
            self._verify_valid_air_event_query(EventEndpoints.CREATE_OR_UPDATE, param_dct)

            attr_dct = self._create_air_attr_dct(meta=ev.metadata or {})
            attr_dct.update(
                {EVENT_DATA_SET_ID: self._config.data_set_id, EVENT_EXT_ID: self._create_event_external_id(param_dct)}
            )
            for attr, val in attr_dct.items():
                setattr(ev, attr, val)

    def create(self, event: Union[Event, List[Event]]) -> Union[Event, EventList]:
        single_item = not isinstance(event, list)
        items = [event] if single_item else event
        if any(not isinstance(ev, Event) for ev in items):
            raise TypeError(f"Expected single (or list of) Event object(s) ({Event})")

        self._make_events_air_compatible_inplace(items)
        try:
            result = self.client.events.create(items[0] if single_item else items)
            return result
        except CogniteDuplicatedError as err:
            ev_fail = err.failed[0]
            existing_ev = self.client.events.retrieve(external_id=ev_fail.external_id)
            msg = (
                f"Event ext_id: '{ev_fail.external_id}' already exists.\nFailed event: {ev_fail}."
                f"\nExisting event: {existing_ev}"
            )
            raise CogniteDuplicatedError(msg) from None

    def update(self, event: Union[Event, List[Event]]) -> Union[Event, EventList]:
        # TODO: Support partial event updates using EventUpdate
        raise NotImplementedError("Soon... maybe")

    def list(self, **kwargs) -> EventList:
        self._verify_valid_air_event_query(EventEndpoints.LIST, kwargs)
        return self.client.events.list(
            **kwargs,
            **self._create_air_attr_dct(meta=kwargs.pop(EVENT_METADATA, {})),
            data_set_ids=[self._config.data_set_id],
        )
