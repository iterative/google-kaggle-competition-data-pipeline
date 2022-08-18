### Data pipeline for Kaggle competition

This repository only purpose is to prepare data for the [Kaggle competition](https://www.kaggle.com/competitions/google-universal-image-embedding). This data is further used in the:
- [ML pipeline](https://github.com/iterative/google-kaggle-competition)
- [Similarity index pipeline](https://github.com/mnrozhkov/google-universal-image-embedding)


### Inputs and outputs
The input to the pipeline is `Benchmarks.zip` file which comes from [Custom dataset](https://www.kaggle.com/datasets/odins0n/guie-custom-data?select=images_128). It covers all the nine classes that the competition mentions. It can be either downloaded manually or with `dvc pull` command.

The output of the pipeline is a splitted dataset with the following folder structure
```
index_search/
    apparel/
        ...
    artwork/
        ...
    ...
    toys/
        ...
train_ml/
    apparel/
        ...
    artwork/
        ...
    ...
    toys/
        ...
```


which is done with [split-folders](https://github.com/jfilter/split-folders) Python package.

### How to setup local environment
Сreate and activate a virtual environment

```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Download benchmark data from [GUIE Custom data](https://www.kaggle.com/datasets/odins0n/guie-custom-data?select=images_128) (`images_128` directory). Or run `dvc pull` if you have AWS credentials.


### How to run the project
The project can be run by running the DVC pipeline with
```
dvc repro
```
or with
```
dvc exp run
```

### DVC pipeline
The project is implemented into a DVC pipeline. The definition of the pipeline consists of two parts:

- `dvc.yaml` --- main file defining stages with: cli command, dependencies and outputs
- `params.yaml` --- parameters of the pipeline such as paths, split ratios etc.

Each stage is defined in a separate python file in `src` folder. At this moment there are two stages:
- `unzip_dataset` - unzips file with all data
- `split_dataset` - splits data to *Similarity index pipeline* and to *ML pipeline*. And ML pipeline data further to *train* and *test* datasets.