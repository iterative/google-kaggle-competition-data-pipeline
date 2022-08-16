import argparse
import os
from pathlib import Path
import splitfolders
import yaml


def split_for_train_and_test_teacher_model(params):
    stage_params = yaml.safe_load(open(params))
    data_folder = Path(stage_params["data_folder"])

    input_folder = data_folder/Path(stage_params["split_dataset"]['index_search']['output_folder'])/'train_ml'
    output_folder = data_folder/Path(stage_params["split_dataset"]['ML_model']['output_folder'])
    
    seed = stage_params["split_dataset"]['ML_model']['seed']
    test_ratio = stage_params["split_dataset"]['ML_model']['test_ratio']
    train_ratio = 1-test_ratio

    splitfolders.ratio(input_folder, output=output_folder, seed=seed, ratio=(train_ratio, test_ratio), move=False)
    

def split_for_train_and_index_search(params):
    stage_params = yaml.safe_load(open(params))
    data_folder = Path(stage_params["data_folder"])

    input_folder = data_folder/Path(stage_params["unzip_dataset"]['output_folder'])
    output_folder = data_folder/Path(stage_params["split_dataset"]['index_search']['output_folder'])
    
    seed = stage_params["split_dataset"]['index_search']['seed']
    index_search_ratio = stage_params["split_dataset"]['index_search']['index_search_ratio']
    train_ml_ratio = 1-index_search_ratio

    splitfolders.ratio(input_folder, output=output_folder, seed=seed, ratio=(train_ml_ratio, index_search_ratio), move=False)
    os.rename(output_folder/'train', output_folder/'train_ml')
    os.rename(output_folder/'val', output_folder/'index_search')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=str, default='params.yaml')
    args = parser.parse_args()

    split_for_train_and_index_search(args.params)
    split_for_train_and_test_teacher_model(args.params)