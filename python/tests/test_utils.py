"""
Unit tests for ww3_tools.utils module.
"""

import pytest
import pandas as pd
from ww3_tools.utils import filter_by_bbox, format_datetime


def test_filter_by_bbox():
    data = {
        "latitude": [10.0, 20.0, 30.0, 40.0],
        "longitude": [-100.0, -80.0, -60.0, -40.0],
        "val": [1, 2, 3, 4],
    }
    df = pd.DataFrame(data)

    filtered = filter_by_bbox(df, min_lat=15.0, max_lat=35.0, min_lon=-85.0, max_lon=-55.0)

    assert len(filtered) == 2
    assert list(filtered["val"]) == [2, 3]


def test_filter_by_bbox_invalid_col():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    with pytest.raises(KeyError):
        filter_by_bbox(df, 0, 10, 0, 10)


def test_format_datetime():
    data = {
        "year": [2026, 2026],
        "month": [1, 2],
        "day": [15, 20],
        "hour": [12, 18],
        "minute": [0, 30],
    }
    df = pd.DataFrame(data)

    formatted = format_datetime(df)

    assert "time" in formatted.columns
    assert formatted["time"].iloc[0] == pd.Timestamp("2026-01-15 12:00:00")
    assert formatted["time"].iloc[1] == pd.Timestamp("2026-02-20 18:30:00")


def test_format_datetime_missing_cols():
    df = pd.DataFrame({"year": [2026], "month": [1]})
    with pytest.raises(KeyError):
        format_datetime(df)
