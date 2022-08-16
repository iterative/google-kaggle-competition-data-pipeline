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