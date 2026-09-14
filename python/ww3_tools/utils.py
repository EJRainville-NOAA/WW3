"""
Utilities for geospatial bounding box filtering and time formatting.
"""

from typing import Union
import pandas as pd


def filter_by_bbox(
    df: pd.DataFrame,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
) -> pd.DataFrame:
    """
    Filter DataFrame records within specified latitude/longitude bounding box.
    """
    if lat_col not in df.columns or lon_col not in df.columns:
        raise KeyError(f"Columns '{lat_col}' and '{lon_col}' must be present in DataFrame.")

    mask = (
        (df[lat_col] >= min_lat)
        & (df[lat_col] <= max_lat)
        & (df[lon_col] >= min_lon)
        & (df[lon_col] <= max_lon)
    )
    return df[mask].reset_index(drop=True)


def format_datetime(
    df: pd.DataFrame,
    year_col: str = "year",
    month_col: str = "month",
    day_col: str = "day",
    hour_col: str = "hour",
    minute_col: str = "minute",
    output_col: str = "time",
) -> pd.DataFrame:
    """
    Combine date and time component columns into a pandas datetime column.
    """
    required_cols = [year_col, month_col, day_col, hour_col]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required time columns: {missing}")

    df_out = df.copy()
    if minute_col in df_out.columns:
        dt_dict = {
            "year": df_out[year_col],
            "month": df_out[month_col],
            "day": df_out[day_col],
            "hour": df_out[hour_col],
            "minute": df_out[minute_col],
        }
    else:
        dt_dict = {
            "year": df_out[year_col],
            "month": df_out[month_col],
            "day": df_out[day_col],
            "hour": df_out[hour_col],
        }

    df_out[output_col] = pd.to_datetime(dt_dict)
    return df_out
