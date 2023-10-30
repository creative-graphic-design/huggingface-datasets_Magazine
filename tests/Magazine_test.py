import pytest

import datasets as ds


@pytest.fixture
def dataset_path() -> str:
    return "Magazine.py"


@pytest.mark.parametrize(
    argnames=("expected_num_dataset", "invalid_samples"),
    argvalues=((3919, 16),),
)
def test_load_dataset(
    dataset_path: str, expected_num_dataset: int, invalid_samples: int
):
    dataset = ds.load_dataset(
        path=dataset_path,
        # token=True,
        data_dir="./datasets",
    )

    assert dataset["train"].num_rows + invalid_samples == expected_num_dataset
