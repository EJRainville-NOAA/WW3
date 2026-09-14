"""
BUFR file converter module for WAVEWATCH III observations.
Handles reading BUFR files, converting to DataFrames, filtering, and exporting to NetCDF.
"""

import os
from typing import List, Optional, Dict, Union, Any
import pandas as pd
import numpy as np

try:
    import pdbufr
except ImportError:
    pdbufr = None

try:
    import xarray as xr
except ImportError:
    xr = None

from .utils import filter_by_bbox, format_datetime


def read_bufr(
    filepath: str,
    columns: Optional[List[str]] = None,
    filters: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Read a BUFR file and return a pandas DataFrame using pdbufr.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"BUFR file not found: {filepath}")

    if pdbufr is None:
        raise ImportError(
            "pdbufr package is required to read BUFR files. "
            "Please install it using 'pip install pdbufr'."
        )

    return pdbufr.read_bufr(filepath, columns=columns, filters=filters)


def convert_bufr_to_dataframe(
    bufr_filepath: str,
    columns: Optional[List[str]] = None,
    filters: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Convert BUFR file into a cleaned pandas DataFrame.
    """
    df = read_bufr(bufr_filepath, columns=columns, filters=filters)
    df = df.dropna(how="all")
    return df.reset_index(drop=True)


def filter_bufr_data(
    df: pd.DataFrame,
    bbox: Optional[tuple] = None,
    min_wave_height: Optional[float] = None,
    max_wave_height: Optional[float] = None,
    wave_height_col: str = "significantWaveHeight",
) -> pd.DataFrame:
    """
    Filter converted BUFR DataFrame by bounding box and/or wave height ranges.

    bbox format: (min_lat, max_lat, min_lon, max_lon)
    """
    filtered = df.copy()

    if bbox is not None:
        min_lat, max_lat, min_lon, max_lon = bbox
        filtered = filter_by_bbox(
            filtered, min_lat, max_lat, min_lon, max_lon
        )

    if min_wave_height is not None and wave_height_col in filtered.columns:
        filtered = filtered[filtered[wave_height_col] >= min_wave_height]

    if max_wave_height is not None and wave_height_col in filtered.columns:
        filtered = filtered[filtered[wave_height_col] <= max_wave_height]

    return filtered.reset_index(drop=True)


def convert_bufr_to_netcdf(
    bufr_filepath: str,
    output_netcdf_path: str,
    columns: Optional[List[str]] = None,
    filters: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Convert a BUFR file directly to NetCDF output format using xarray.
    """
    df = convert_bufr_to_dataframe(bufr_filepath, columns=columns, filters=filters)

    if df.empty:
        raise ValueError("Converted BUFR data is empty, cannot generate NetCDF.")

    if xr is None:
        raise ImportError("xarray package is required to export to NetCDF.")

    # Convert DataFrame to xarray Dataset
    ds = df.to_xarray()

    # Add global metadata
    ds.attrs["title"] = "WAVEWATCH III converted BUFR observation data"
    ds.attrs["source"] = f"Converted from BUFR file: {os.path.basename(bufr_filepath)}"

    ds.to_netcdf(output_netcdf_path)
    return output_netcdf_path
