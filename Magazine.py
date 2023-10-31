import os
import pathlib
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, TypedDict

from PIL import Image
from PIL.Image import Image as PilImage

import datasets as ds
from datasets.utils.logging import get_logger

logger = get_logger(__name__)

JsonDict = Dict[str, Any]

_DESCRIPTION = "A large-scale magazine layout dataset with fine-grained layout annotations and keyword labeling"

_CITATION = """\
@article{zheng2019content,
  title={Content-aware generative modeling of graphic design layouts},
  author={Zheng, Xinru and Qiao, Xiaotian and Cao, Ying and Lau, Rynson WH},
  journal={ACM Transactions on Graphics (TOG)},
  volume={38},
  number={4},
  pages={1--15},
  year={2019},
  publisher={ACM New York, NY, USA}
}
"""

_HOMEPAGE = "https://xtqiao.com/projects/content_aware_layout/"

_LICENSE = """\
Copyright (c) 2019, Xiaotian Qiao
All rights reserved.

This code is copyrighted by the authors and is for non-commercial research
purposes only.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


class URLs(TypedDict):
    image: str
    layout: str


_URLS: URLs = {
    # The author of this loading script has uploaded the image and layout annotation files to the HuggingFace's private repository to facilitate testing.
    # If you are using this loading script, please download the annotations from the appropriate channels, such as the OneDrive link provided by the Magazine dataset's author.
    # (To the author of Magazine dataset, if there are any issues regarding this matter, please contact us. We will address it promptly.)
    "image": "https://huggingface.co/datasets/shunk031/Magazine-private/resolve/main/MagImage.zip",
    "layout": "https://huggingface.co/datasets/shunk031/Magazine-private/resolve/main/MagLayout.zip",
}


@dataclass
class LayoutSize(object):
    width: int
    height: int


@dataclass
class LayoutElement(object):
    label: str
    polygon_x: List[int]
    polygon_y: List[int]

    @classmethod
    def parse_polygon(cls, polygon_str: str) -> List[float]:
        return list(map(lambda x: float(x), polygon_str.split()))

    @classmethod
    def parse_polygons(cls, json_dict: JsonDict) -> JsonDict:
        json_dict["polygon_x"] = cls.parse_polygon(json_dict["polygon_x"])
        json_dict["polygon_y"] = cls.parse_polygon(json_dict["polygon_y"])
        return json_dict

    @classmethod
    def from_dict(cls, json_dict: JsonDict) -> "LayoutElement":
        json_dict = cls.parse_polygons(json_dict)
        return cls(**json_dict)


def get_filename(annotation: ET.Element) -> str:
    filename = annotation.find("filename")
    assert filename is not None
    return filename.text


def get_layout_category(annotation: ET.Element) -> str:
    elem = annotation.find("category")
    assert elem is not None
    return elem.text


def get_layout_size(annotation: ET.Element) -> LayoutSize:
    size = annotation.find("size")
    assert size is not None

    h_elem = size.find("height")
    assert h_elem is not None

    w_elem = size.find("width")
    assert w_elem is not None

    return LayoutSize(width=int(w_elem.text), height=int(h_elem.text))


def get_layout_elements(annotation: ET.Element) -> List[LayoutElement]:
    layouts = annotation.find("layout")
    assert layouts is not None

    elements = layouts.findall("element")
    layout_elements = [LayoutElement.from_dict(element.attrib) for element in elements]
    return layout_elements


def get_keywords(annotation: ET.Element) -> List[str]:
    texts = annotation.find("text")
    assert texts is not None
    keywords = texts.findall("keyword")
    return [keyword.text for keyword in keywords]


def load_image(file_path: pathlib.Path) -> PilImage:
    return Image.open(file_path)


def load_images(
    image_base_dir: pathlib.Path, category: str, filename: str
) -> List[PilImage]:
    image_files = (image_base_dir / category).glob(f"{filename}_*")
    return [load_image(file_path) for file_path in image_files]


@dataclass
class LayoutAnnotation(object):
    filename: str
    category: str
    size: LayoutSize
    elements: List[LayoutElement]
    keywords: List[str]
    images: List[PilImage]

    @classmethod
    def get_annotation_from_xml(cls, xml_file: pathlib.Path) -> ET.Element:
        tree = ET.parse(xml_file)
        return tree.getroot()

    @classmethod
    def from_xml(
        cls, xml_file: pathlib.Path, image_base_dir: pathlib.Path
    ) -> "LayoutAnnotation":
        annotation = cls.get_annotation_from_xml(xml_file)
        filename = get_filename(
            annotation=annotation,
        )
        category = get_layout_category(
            annotation=annotation,
        )
        layout_size = get_layout_size(
            annotation=annotation,
        )
        layout_elements = get_layout_elements(
            annotation=annotation,
        )
        keywords = get_keywords(
            annotation=annotation,
        )
        images = load_images(
            image_base_dir=image_base_dir,
            category=category,
            filename=filename,
        )
        return cls(
            filename=filename,
            category=category,
            size=layout_size,
            elements=layout_elements,
            keywords=keywords,
            images=images,
        )


class MagazineDataset(ds.GeneratorBasedBuilder):
    VERSION = ds.Version("1.0.0")
    BUILDER_CONFIGS = [ds.BuilderConfig(version=VERSION, description=_DESCRIPTION)]

    @property
    def _manual_download_instructions(self) -> str:
        return (
            "To use Magazine dataset, you need to download the annotations "
            "from the OneDrive in the official webpage "
            "(https://portland-my.sharepoint.com/:f:/g/personal/xqiao6-c_my_cityu_edu_hk/EhmRh5SFoQ9Hjl_aRjCOltkBKFYefiSagR6QLJ7pWvs3Ww?e=y8HO5Q)."
        )

    def _info(self) -> ds.DatasetInfo:
        features = ds.Features(
            {
                "filename": ds.Value("string"),
                "category": ds.ClassLabel(
                    num_classes=6,
                    names=["fashion", "food", "news", "science", "travel", "wedding"],
                ),
                "size": {
                    "width": ds.Value("int64"),
                    "height": ds.Value("int64"),
                },
                "elements": ds.Sequence(
                    {
                        "label": ds.ClassLabel(
                            num_classes=5,
                            names=[
                                "text",
                                "image",
                                "headline",
                                "text-over-image",
                                "headline-over-image",
                            ],
                        ),
                        "polygon_x": ds.Sequence(ds.Value("float32")),
                        "polygon_y": ds.Sequence(ds.Value("float32")),
                    }
                ),
                "keywords": ds.Sequence(ds.Value("string")),
                "images": ds.Sequence(ds.Image()),
            }
        )
        return ds.DatasetInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            features=features,
        )

    def _download_from_hf(self, dl_manager: ds.DownloadManager) -> URLs:
        return dl_manager.download_and_extract(_URLS)

    def _download_from_local(self, dl_manager: ds.DownloadManager) -> URLs:
        assert dl_manager.manual_dir is not None, dl_manager.manual_dir
        dir_path = os.path.expanduser(dl_manager.manual_dir)

        if not os.path.exists(dir_path):
            raise FileNotFoundError()

        return dl_manager.extract(
            path_or_paths={
                "image": os.path.join(dir_path, "MagImage.zip"),
                "layout": os.path.join(dir_path, "MagLayout.zip"),
            }
        )

    def _split_generators(self, dl_manager: ds.DownloadManager):
        if dl_manager.download_config.token:
            file_paths = self._download_from_hf(dl_manager)
        else:
            file_paths = self._download_from_local(dl_manager)

        layout_xml_dir = (
            pathlib.Path(file_paths["layout"]) / "layoutdata" / "annotations"
        )
        image_base_dir = pathlib.Path(file_paths["image"]) / "images"

        return [
            ds.SplitGenerator(
                name=ds.Split.TRAIN,
                gen_kwargs={
                    "layout_xml_dir": layout_xml_dir,
                    "image_base_dir": image_base_dir,
                },
            )
        ]

    def _generate_examples(
        self, layout_xml_dir: pathlib.Path, image_base_dir: pathlib.Path
    ):
        xml_files = [f for f in layout_xml_dir.iterdir() if f.suffix == ".xml"]
        for i, xml_file in enumerate(xml_files):
            layout_annotation = LayoutAnnotation.from_xml(
                xml_file=xml_file,
                image_base_dir=image_base_dir,
            )
            yield i, asdict(layout_annotation)
