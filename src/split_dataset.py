import argparse
import os
from pathlib import Path
import shutil
import splitfolders
import yaml


def split_data(params):
    stage_params = yaml.safe_load(open(params))
    data_folder = Path(stage_params["data_folder"])

    input_folder = data_folder/Path(stage_params["unzip_dataset"]['output_folder'])
    output_folder = data_folder/Path(stage_params["split_dataset"]['output_folder'])

    seed = stage_params["split_dataset"]['seed']
    train_ratio = stage_params["split_dataset"]['train_ratio']
    val_ratio = stage_params["split_dataset"]['val_ratio']
    test_ratio = stage_params["split_dataset"]['test_ratio']

    splitfolders.ratio(input_folder, output=output_folder, seed=seed, ratio=(train_ratio, val_ratio, test_ratio), move=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=str, default='params.yaml')
    args = parser.parse_args()

    split_data(args.params)