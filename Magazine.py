import pathlib
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

import datasets as ds
from datasets.utils.logging import get_logger
from PIL import Image
from PIL.Image import Image as PilImage

logger = get_logger(__name__)

JsonDict = Dict[str, Any]

_CITATION = ""

_DESCRIPTION = ""

_HOMEPAGE = ""

_LICENSE = ""

_URLS = {
    "image": "https://huggingface.co/datasets/shunk031/Magazine-private/resolve/main/MagImage.zip",
    "layout": "https://huggingface.co/datasets/shunk031/Magazine-private/resolve/main/MagLayout.zip",
}


class MagazineException(Exception):
    pass


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
    def parse_polygon(cls, polygon_str: str) -> List[int]:
        return list(map(lambda x: int(x), polygon_str.split()))

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
        try:
            layout_elements = get_layout_elements(
                annotation=annotation,
            )
        except ValueError as err:
            raise MagazineException(f"Invalid xml file: {xml_file}") from err

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
    BUILDER_CONFIGS = [ds.BuilderConfig(version=VERSION)]

    def _info(self) -> ds.DatasetInfo:
        features = ds.Features(
            {
                "filename": ds.Value("string"),
                "category": ds.Value("string"),
                "size": {
                    "width": ds.Value("int64"),
                    "height": ds.Value("int64"),
                },
                "elements": ds.Sequence(
                    {
                        "label": ds.Value("string"),
                        "polygon_x": ds.Sequence(ds.Value("int64")),
                        "polygon_y": ds.Sequence(ds.Value("int64")),
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

    def _split_generators(self, dl_manager: ds.DownloadManager):
        file_paths = dl_manager.download_and_extract(_URLS)

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
            try:
                layout_annotation = LayoutAnnotation.from_xml(
                    xml_file=xml_file,
                    image_base_dir=image_base_dir,
                )
            except MagazineException as err:
                logger.warning(err)
                continue

            yield i, asdict(layout_annotation)
