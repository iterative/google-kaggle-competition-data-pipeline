# Data pipeline for Kaggle competition

## TLDR
Datasets in the repository:
```
coco17_25k - object detection and not image classification dataset -> not yet compatible with the workflow presented further
food_101_small - https://www.kaggle.com/datasets/kmader/food41?select=images
freiburg_groceries - https://paperswithcode.com/dataset/freiburg-groceries
google_landmarks_v2_micro - https://www.kaggle.com/datasets/confirm/google-landmark-dataset-v2-micro
kaggle_130k - https://www.kaggle.com/datasets/rhtsingh/google-universal-image-embeddings-128x128
kais_apparel - https://www.kaggle.com/datasets/kaiska/apparel-dataset?select=black_dress
triplets_dataset - manually created triplets from parts of food_101_small and kaggle_130k datasets
vision_furniture - https://www.kaggle.com/competitions/day-3-kaggle-competition/overview
```
Download with
```
dvc get https://github.com/iterative/google-kaggle-competition-data-pipeline datasets/<dataset_name> -o datasets/<dataset_name>
```


## Introduction

This repository contains various datasets for the [Kaggle competition](https://www.kaggle.com/competitions/google-universal-image-embedding). These datasets are further used in the:
- [ML pipeline](https://github.com/iterative/google-kaggle-competition)
- [Similarity index pipeline](https://github.com/mnrozhkov/google-universal-image-embedding)

The datasets are versioned with [DVC](https://dvc.org/) on a publicly available S3 bucket. You need no credentials to download the datasets.


## How to work with datasets

We have prepared Python package with functions for the most typical workflow with the dataset. You may install it together with other required packages in `requirements.txt` or separately with 

```
pip install git+https://github.com//iterative/google-kaggle-competition-data-pipeline.git#egg=dataset_utils\&subdirectory=dataset_utils_package
```
Note the [Voxel51](https://voxel51.com/) is a dependency for this package.

### Download dataset

Each dataset is split into 10 zip files, such that you can download even a portion of the dataset. The split is done in a way that the distribution of classes in each zip file is the same as for the whole dataset. You can download the whole dataset and unzip it with the following Python method.
```
from pathlib import Path
from dataset_utils.download_utils import prepare_dataset

prepare_dataset(dataset_name="vision_furniture", output_path=Path("../datasets/vision_furniture/"))
```
This creates the following folder structure
```
datasets/
    vision_furniture/
        data/
            <image_files>
        labels.json
```
For end-to-end example or downloading only a portion of dataset, please see [prepare_dataset_for_ML notebook](notebooks/prepare_dataset_for_ML.ipynb).

### Merge or share datasets

For instructions how to merge or share datasets, please see [merge_datasets notebook](notebooks/prepare_dataset_for_ML.ipynb) as it gives the end-to-end example.


### How to prepare a new dataset

You may get inspired by `prepare_data.ipynb` that is in the folder of each dataset. In general, the workflow for creating a new dataset is as follows:
1) Download the original dataset with labels.
2) Load the dataset with labels into Voxel51 and do some preprocessing if it is needed.
3) Export the dataset in `FiftyOneImageClassificationDataset` export format.
4) Do a stratified split of the dataset to multiple zip files if you want. Attach information about the partition into the `label.json` file.
5) Upload the zip files to the cloud storage.


### How to setup the local environment
Сreate and activate a virtual environment

```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
