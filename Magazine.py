import datasets as ds

_CITATION = ""

_DESCRIPTION = ""

_HOMEPAGE = ""

_LICENSE = ""

_URLS = {
    "image": "https://huggingface.co/datasets/shunk031/Magazine-private/resolve/main/MagImage.zip",
    "layout": "https://huggingface.co/datasets/shunk031/Magazine-private/resolve/main/MagLayout.zip",
}


class MagazineDataset(ds.GeneratorBasedBuilder):
    VERSION = ds.Version("1.0.0")
    BUILDER_CONFIGS = [ds.BuilderConfig(version=VERSION)]

    def _info(self) -> ds.DatasetInfo:
        return ds.DatasetInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            features=ds.Features(),
        )

    def _split_generators(self, dl_manager: ds.DownloadManager):
        file_paths = dl_manager.download_and_extract(_URLS)
        breakpoint()
