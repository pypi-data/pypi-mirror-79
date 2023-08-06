import json
from typing import Any, Dict, List

from cognite.air._api import AIRClientError
from cognite.air._backfilling_api import AIRBackfillingAPI, NoBackfillAPI
from cognite.air._config import AIRClientConfig
from cognite.air._events_api import AIREventsAPI
from cognite.air._time_series_api import AIRTimeSeriesAPI
from cognite.air.constants import MA_FIELD_META_FIELDS, MA_FIELD_META_MODELVERSION, SA_EXT_ID, SA_FIELD_META_DATA
from cognite.air.utils import is_jsonable, is_string_truthy
from cognite.client import CogniteClient


class AIRClient:
    def __init__(self, data: Dict[str, Any], client: CogniteClient, secrets: Dict[str, Any], debug: bool = False):
        del secrets  # Unused for now (required in function signature)
        sa_ext_id = self._extract_and_validate_sa_ext_id(data)
        schedule_asset = self._retrieve_and_verify_schedule_asset(client, sa_ext_id)
        model_asset = self._retrieve_and_verify_model_asset(client, schedule_asset.parent_external_id)
        model_version = model_asset.metadata[MA_FIELD_META_MODELVERSION]
        # Retrieve backfilling asset if the model uses backfilling:
        backfilling_asset = None
        if is_string_truthy(model_asset.metadata.get("backfill")):
            backfilling_asset = self._retrieve_and_verify_backfill_asset(client, sa_ext_id, model_version)

        self._config = AIRClientConfig(
            client=client,
            data_set_id=schedule_asset.data_set_id,
            schedule_asset_id=schedule_asset.id,
            schedule_asset_ext_id=sa_ext_id,
            data_fields=json.loads(schedule_asset.metadata[SA_FIELD_META_DATA]),
            data_fields_defs=json.loads(model_asset.metadata[MA_FIELD_META_FIELDS]),
            model_name=model_asset.name,
            model_version=model_version,
        )
        self.events = AIREventsAPI(self._config)
        self.time_series = AIRTimeSeriesAPI(self._config)
        self.backfilling = NoBackfillAPI()
        if backfilling_asset:
            backfilling = AIRBackfillingAPI(self._config, backfilling_asset)
            if backfilling.in_progress:
                self.backfilling = backfilling  # type: ignore

        if debug:
            print(
                f"Tenant: {client.config.project}\nSchedule asset ext. ID: {self._config.schedule_asset_ext_id}\n"
                f"Model name: {self._config.model_name}\nModel version: {self._config.model_version}\n"
            )

    @property
    def config(self):
        return self._config

    @property
    def cognite_client(self):
        return self._config.client

    @property
    def schedule_asset_id(self):
        return self._config.schedule_asset_id

    @property
    def schedule_asset_ext_id(self):
        return self._config.schedule_asset_ext_id

    @property
    def model_name(self):
        return self._config.model_name

    @property
    def model_version(self):
        return self._config.model_version

    def retrieve_fields(self, field_names: List[str], ignore_unknown_field_names: bool = False) -> List[str]:
        if not isinstance(field_names, list) or not all(isinstance(s, str) for s in field_names):
            raise TypeError(f"Expected '{field_names}' to be a list of strings!")

        fields = list(map(self._config.data_fields.get, field_names))
        if not ignore_unknown_field_names and None in fields:
            err_field_names = [name for name, field in zip(field_names, fields) if field is None]
            raise ValueError(f"The following field names were not found: {err_field_names}")

        return list(map(lambda fld: json.loads(fld) if is_jsonable(fld) else fld, fields))  # type: ignore

    def retrieve_field(self, field_name: str) -> str:
        if not isinstance(field_name, str):
            raise TypeError(f"Expected 'field_name' to be of type {str}, not {type(field_name)}")
        return self.retrieve_fields([field_name])[0]

    @staticmethod
    def _extract_and_validate_sa_ext_id(data):
        sa_ext_id = data.get(SA_EXT_ID)
        if sa_ext_id is None:
            raise KeyError(f"Missing required input field '{SA_EXT_ID}'")
        if not isinstance(sa_ext_id, str):
            raise TypeError(f"Expected field '{SA_EXT_ID}' to be of type {str}, not {type(sa_ext_id)}")
        return sa_ext_id

    @staticmethod
    def _retrieve_and_verify_schedule_asset(client, sa_ext_id):
        schedule_asset = client.assets.retrieve(external_id=sa_ext_id)
        if schedule_asset is None:
            raise AIRClientError(f"Asset not found: No 'schedule asset' with external_id: '{sa_ext_id}'")
        return schedule_asset

    @staticmethod
    def _retrieve_and_verify_model_asset(client, model_ext_id):
        model_asset = client.assets.retrieve(external_id=model_ext_id)
        if model_asset is None:
            raise AIRClientError(f"Asset not found: No 'model asset' with external_id: '{model_ext_id}'")
        return model_asset

    @staticmethod
    def _retrieve_and_verify_backfill_asset(client, sa_ext_id, model_version):
        backfill_asset_list = client.assets.list(parent_external_ids=[sa_ext_id], metadata={"version": model_version})
        if len(backfill_asset_list) == 1:
            return backfill_asset_list[0]
        raise AIRClientError(
            f"{len(backfill_asset_list)} backfilling assets found. Expected to find exactly 1 backfilling asset"
        )
