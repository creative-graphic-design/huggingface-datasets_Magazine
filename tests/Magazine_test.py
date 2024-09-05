import os

import datasets as ds
import pytest


@pytest.fixture
def org_name() -> str:
    return "creative-graphic-design"


@pytest.fixture
def dataset_name() -> str:
    return "Magazine"


@pytest.fixture
def dataset_path(dataset_name: str) -> str:
    return f"{dataset_name}.py"


@pytest.fixture
def repo_id(org_name: str, dataset_name: str) -> str:
    return f"{org_name}/{dataset_name}"


@pytest.mark.skipif(
    condition=bool(os.environ.get("CI", False)),
    reason=(
        "Because this loading script downloads a large dataset, "
        "we will skip running it on CI."
    ),
)
@pytest.mark.parametrize(
    argnames=("expected_num_dataset",),
    argvalues=((3919,),),
)
def test_load_dataset(dataset_path: str, expected_num_dataset: int):
    dataset = ds.load_dataset(path=dataset_path, token=True)
    assert isinstance(dataset, ds.DatasetDict)

    assert dataset["train"].num_rows == expected_num_dataset


@pytest.mark.skipif(
    condition=bool(os.environ.get("CI", False)),
    reason=(
        "Because this loading script downloads a large dataset, "
        "we will skip running it on CI."
    ),
)
def test_push_to_hub(repo_id: str, dataset_path: str):
    dataset = ds.load_dataset(path=dataset_path, token=True)
    assert isinstance(dataset, ds.DatasetDict)

    # dataset.push_to_hub(repo_id=repo_id, private=True)
