from cognite.air._api import AIRClientError, BaseAPIClient
from cognite.air._constants import AIR_META_BACKFILL_COMPLETE, AIR_META_BACKFILLED_UNTIL
from cognite.air.utils import is_string_truthy
from cognite.client.data_classes import Asset


class NoBackfillAPI:
    @property
    def in_progress(self):
        return False

    def __getattr__(self, attr):
        raise AttributeError(
            f"Can't call backfilling endpoint after it is done! Failed when trying to get/call '{attr}'!"
        )


class AIRBackfillingAPI(BaseAPIClient):
    def __init__(self, config, backfill_asset):
        super().__init__(config)
        if not isinstance(backfill_asset, Asset):
            raise AIRClientError(
                f"Could not find the required backfilling asset! Expected {Asset}, not {type(backfill_asset)}"
            )
        self._backfill_asset = backfill_asset

    @property
    def in_progress(self):
        return not is_string_truthy(self._backfill_asset.metadata[AIR_META_BACKFILL_COMPLETE])

    @property
    def latest_timestamp(self):
        backfilled_until = self._backfill_asset.metadata.get(AIR_META_BACKFILLED_UNTIL)
        if backfilled_until:
            return int(backfilled_until)

    def update_latest_timestamp(self, ts: int):
        if not isinstance(ts, int):
            raise TypeError(f"Expected input '{ts}' to be of type 'int' not '{type(ts)}'")
        self._backfill_asset.metadata[AIR_META_BACKFILLED_UNTIL] = ts
        self.client.assets.update(self._backfill_asset)

    def mark_as_completed(self):
        self._backfill_asset.metadata[AIR_META_BACKFILL_COMPLETE] = "True"
        self.client.assets.update(self._backfill_asset)
