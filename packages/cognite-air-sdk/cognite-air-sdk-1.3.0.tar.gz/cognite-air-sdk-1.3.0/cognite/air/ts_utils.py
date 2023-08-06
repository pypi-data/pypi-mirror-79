import numpy as np
import pandas as pd

from cognite.client import CogniteClient
from cognite.client._api.datapoints import DatapointsFetcher
from cognite.client.utils._time import granularity_to_ms


def get_outside_datapoint(client, external_id, start, end, *, before):
    dps = client.datapoints.retrieve(start=start, end=end, external_id=external_id, include_outside_points=True)
    if len(dps) == 2:
        return dps[0] if before else dps[1]

    elif len(dps) == 1:
        ts = dps[0].timestamp
        if before:
            if ts <= start:
                return dps[0]
        else:
            if ts >= end:
                return dps[0]


def get_complete_time_series(client: CogniteClient, external_id: str, start: int, end: int, granularity: str):
    start = DatapointsFetcher._align_with_granularity_unit(start, granularity)
    end = DatapointsFetcher._align_with_granularity_unit(end, granularity)
    series = (
        client.datapoints.retrieve_dataframe(
            external_id=external_id,
            start=start,
            end=end,
            aggregates=["average"],
            granularity=granularity,
            include_aggregate_name=False,
        )
        .squeeze(axis="columns")
        .reindex(
            np.arange(
                pd.Timestamp(start, unit="ms"),
                pd.Timestamp(end, unit="ms"),
                pd.Timedelta(milliseconds=granularity_to_ms(granularity)),
            ),
            copy=False,
        )
    )
    first_val, last_val = series.iloc[[0, -1]]
    extra_ffill_required, extra_bfill_required = False, False

    if np.isnan(first_val):  # API call is expensive, skip if not needed
        dp = get_outside_datapoint(client, external_id, start=start, end=start + 1, before=True)
        if dp:
            first_val = dp.value
        else:
            # No datapoints before start, have to backfill:
            idx = series.first_valid_index()
            if idx is not None:
                first_val = series[idx]
            else:
                # No data in series to use for backfill, wait for outside point:
                extra_bfill_required = True

    if np.isnan(last_val):
        dp = get_outside_datapoint(client, external_id, start=end - 1, end=end, before=False)
        if dp:
            last_val = dp.value
        else:
            # No datapoints after end, have to forward-fill:
            idx = series.last_valid_index()
            if idx is not None:
                last_val = series[idx]
            else:
                # No data in series to use for forward-fill, wait for outside point:
                extra_ffill_required = True

    series.iloc[[0, -1]] = first_val, last_val

    # Handle edge cases with missing outside data:
    if extra_ffill_required and extra_bfill_required:
        raise ValueError(f"Time series is completely empty! (ext.id: {external_id})")
    elif extra_ffill_required:
        return series.ffill()
    elif extra_bfill_required:
        return series.bfill()

    # Linearly interpolate all missing values:
    return series.interpolate(method="slinear")
