---
annotations_creators:
- machine-generated
language:
- en
language_creators:
- found
license:
- unknown
multilinguality:
- monolingual
pretty_name: Magazine
size_categories: []
source_datasets:
- original
tags:
- graphic design
- layout
- content-aware
task_categories:
- image-to-image
- text-to-image
- unconditional-image-generation
task_ids: []
---

# Dataset Card for Magazine dataset

## Table of Contents
- [Dataset Card Creation Guide](#dataset-card-creation-guide)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
    - [Languages](#languages)
  - [Dataset Structure](#dataset-structure)
    - [Data Instances](#data-instances)
    - [Data Fields](#data-fields)
    - [Data Splits](#data-splits)
  - [Dataset Creation](#dataset-creation)
    - [Curation Rationale](#curation-rationale)
    - [Source Data](#source-data)
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
    - [Personal and Sensitive Information](#personal-and-sensitive-information)
  - [Considerations for Using the Data](#considerations-for-using-the-data)
    - [Social Impact of Dataset](#social-impact-of-dataset)
    - [Discussion of Biases](#discussion-of-biases)
    - [Other Known Limitations](#other-known-limitations)
  - [Additional Information](#additional-information)
    - [Dataset Curators](#dataset-curators)
    - [Licensing Information](#licensing-information)
    - [Citation Information](#citation-information)
    - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://xtqiao.com/projects/content_aware_layout/
- **Repository:** https://github.com/shunk031/huggingface-datasets_Magazine
- **Paper (SIGGRAPH2019):** https://dl.acm.org/doi/10.1145/3306346.3322971

### Dataset Summary

A large-scale magazine layout dataset with fine-grained layout annotations and keyword labeling.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

To use Magazine dataset, you need to download the image and layout annotations from the [OneDrive](https://portland-my.sharepoint.com/:f:/g/personal/xqiao6-c_my_cityu_edu_hk/EhmRh5SFoQ9Hjl_aRjCOltkBKFYefiSagR6QLJ7pWvs3Ww?e=y8HO5Q) in the official page. 
Then place the downloaded files in the following structure and specify its path.

```shell
/path/to/datasets
├── MagImage.zip
└── MagLayout.zip
```

```python
import datasets as ds

dataset = ds.load_dataset(
    path="shunk031/Magazine",
    data_dir="/path/to/datasets/", # Specify the path of the downloaded directory.
)
```

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

```bibtex
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
```

### Contributions

Thanks to [Xinru Zheng and Xiaotian Qiao*](https://xtqiao.com/projects/content_aware_layout/) for creating this dataset.
