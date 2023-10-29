import datasets as ds
import pytest


@pytest.fixture
def dataset_path() -> str:
    return "Magazine.py"


def test_load_dataset(dataset_path: str):
    dataset = ds.load_dataset(
        path=dataset_path,
        token=True,
    )
