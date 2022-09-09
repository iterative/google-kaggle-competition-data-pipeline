# Data pipeline for Kaggle competition

## TLDR
Available datasets:
```
freiburg_groceries - https://paperswithcode.com/dataset/freiburg-groceries
kaggle_130k - https://www.kaggle.com/datasets/rhtsingh/google-universal-image-embeddings-128x128
kais_apparel - https://www.kaggle.com/datasets/kaiska/apparel-dataset?select=black_dress
```
Download with
```
dvc get https://github.com/iterative/google-kaggle-competition-data-pipeline datasets/<dataset_name> -o datasets --rev <commit_hash>
```


## Introduction

This repository shall prepare data for the [Kaggle competition](https://www.kaggle.com/competitions/google-universal-image-embedding). This data is further used in the:
- [ML pipeline](https://github.com/iterative/google-kaggle-competition)
- [Similarity index pipeline](https://github.com/mnrozhkov/google-universal-image-embedding)

The data that is used in this repository comes from [Custom dataset](https://www.kaggle.com/datasets/odins0n/guie-custom-data?select=images_128). It covers all the nine classes that the competition mentions.

## DVC pipeline
The project is implemented in a DVC pipeline. The definition of the pipeline consists of two parts:

- `dvc.yaml` --- main file defining stages with: cli command, dependencies and outputs
- `params.yaml` --- parameters of the pipeline such as paths, split ratios etc.

Each stage is defined in a separate python file in `src` folder. At this moment there are two stages:
- `unzip_dataset` - unzips file with all data
- `split_dataset` - splits data to train/val/test datasets. The split ratio is defined in `params.yaml` file.
- `zip_dataset` - zips the train/val/test folders from the previous stage into one zip file.


### How to setup the local environment for this pipeline
Сreate and activate a virtual environment

```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Download the input data (`baseline.zip` file) into your local folder `data` with
```
dvc get https://github.com/iterative/google-kaggle-competition-data-pipeline data/baseline.zip -o data --rev v1.1
```
You also can prepare your own custom data. To do that, you need to make sure that the zip file contains the folder structure described in [Input to the pipeline](#Input-to-the-pipeline) section.

### How to run the project
The project can be run by running the DVC pipeline with
```
dvc repro
```

### Input to the pipeline
The input to the pipeline is a zip file that shall contain the following folder structure (the naming of the folder classes or images does not matter):
```
apparel/
    0.png
    1.png
    ...
artwork/
    0.png
    1.png
    ...
toys/
    ...
```

The filepath to the zip file is specified in `params.yaml` file, under the key `unzip_dataset.input_file`. The input zip file is in our case named `baseline.zip` 

If you are more interested how the `dvc` command works in this case, you may read more in [Data registry documentation](https://dvc.org/doc/use-cases/data-registry#data-registry).


### Output of the pipeline
The output of the pipeline is a zip file that contains split dataset with the following folder structure
```
train/
    apparel/
        1.png
        ...
    artwork/
        1.png
        ...
    ...
    toys/
        1.png
        ...
val/
    apparel/
        0.png
        ...
    artwork/
        0.png
        ...
    ...
    toys/
        0.png
        ...
test/
    apparel/
        6.png
        ...
    artwork/
        14.png
        ...
    ...
    toys/
        14.png
        ...
```
Note that the image names may differ if you use different seed. Also, note that if you use your custom dataset the names of the classes may differ. The filepath to the output zip file is specified in `params.yaml` file.

## How to setup local environment for a different pipeline
In case, you would like to use the output of this pipeline, you need to set up your local environment as follows

Сreate, activate a virtual environment, and install dvc package.
```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install dvc[s3]
```

Initialize the folder with `git` and `dvc` and download the prepared data (no credentials are required)
```
git init
dvc init
dvc get https://github.com/iterative/google-kaggle-competition-data-pipeline data/baseline_split.zip --rev v1.1
```

In the case, you would like to download the uncompressed split you run
```
dvc get https://github.com/iterative/google-kaggle-competition-data-pipeline data/baseline_split --rev v1.1
```

You can also download just some particular part of the data. In that case, you specify a folder to download. For example, like this
```
dvc get https://github.com/iterative/google-kaggle-competition-data-pipeline data/baseline_split/train/apparel --rev v1.1
```

You may also be interested in [`dvc import` command](https://dvc.org/doc/use-cases/data-registry#data-import-workflow) in case you would like to integrate this data into a DVC pipeline.