"""
Unit tests for ww3_tools.bufr_converter module.
"""

import os
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from ww3_tools.bufr_converter import (
    read_bufr,
    convert_bufr_to_dataframe,
    filter_bufr_data,
    convert_bufr_to_netcdf,
)


def test_read_bufr_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_bufr("non_existent_file.bufr")


@patch("ww3_tools.bufr_converter.pdbufr")
def test_read_bufr_mock(mock_pdbufr, tmp_path):
    bufr_file = tmp_path / "test.bufr"
    bufr_file.write_bytes(b"mock bufr content")

    mock_df = pd.DataFrame({
        "latitude": [20.0, 25.0],
        "longitude": [-70.0, -65.0],
        "significantWaveHeight": [2.5, 3.1]
    })
    mock_pdbufr.read_bufr.return_value = mock_df

    res = read_bufr(str(bufr_file))

    mock_pdbufr.read_bufr.assert_called_once_with(str(bufr_file), columns=None, filters=None)
    assert len(res) == 2
    assert res["significantWaveHeight"].iloc[0] == 2.5


def test_filter_bufr_data():
    df = pd.DataFrame({
        "latitude": [10.0, 25.0, 40.0],
        "longitude": [-80.0, -70.0, -60.0],
        "significantWaveHeight": [1.0, 3.5, 6.0],
    })

    # Test bbox filter
    filtered_bbox = filter_bufr_data(df, bbox=(20.0, 50.0, -75.0, -55.0))
    assert len(filtered_bbox) == 2
    assert list(filtered_bbox["latitude"]) == [25.0, 40.0]

    # Test wave height filters
    filtered_height = filter_bufr_data(df, min_wave_height=2.0, max_wave_height=5.0)
    assert len(filtered_height) == 1
    assert filtered_height["significantWaveHeight"].iloc[0] == 3.5


@patch("ww3_tools.bufr_converter.read_bufr")
def test_convert_bufr_to_netcdf(mock_read_bufr, tmp_path):
    bufr_file = tmp_path / "test.bufr"
    bufr_file.write_bytes(b"mock bufr")
    nc_out = tmp_path / "output.nc"

    mock_df = pd.DataFrame({
        "latitude": [20.0, 25.0],
        "longitude": [-70.0, -65.0],
        "significantWaveHeight": [2.5, 3.1]
    })
    mock_read_bufr.return_value = mock_df

    out_path = convert_bufr_to_netcdf(str(bufr_file), str(nc_out))

    assert os.path.exists(out_path)
    assert out_path == str(nc_out)


@patch("ww3_tools.bufr_converter.read_bufr")
def test_convert_bufr_to_netcdf_empty(mock_read_bufr, tmp_path):
    bufr_file = tmp_path / "test.bufr"
    bufr_file.write_bytes(b"mock bufr")
    nc_out = tmp_path / "output.nc"

    mock_read_bufr.return_value = pd.DataFrame()

    with pytest.raises(ValueError, match="Converted BUFR data is empty"):
        convert_bufr_to_netcdf(str(bufr_file), str(nc_out))
