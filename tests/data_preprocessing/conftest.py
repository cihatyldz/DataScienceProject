import pytest

from src.data_preprocessing import DataPreprocessor, load_config
from pathlib import Path


@pytest.fixture
def preprocessor(config_path):
    return DataPreprocessor(config=load_config(config_path))