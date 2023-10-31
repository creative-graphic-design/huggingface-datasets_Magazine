import pytest

import datasets as ds


@pytest.fixture
def dataset_path() -> str:
    return "Magazine.py"


@pytest.mark.parametrize(
    argnames=("expected_num_dataset",),
    argvalues=((3919,),),
)
def test_load_dataset(dataset_path: str, expected_num_dataset: int):
    dataset = ds.load_dataset(path=dataset_path, token=True)

    assert dataset["train"].num_rows == expected_num_dataset
