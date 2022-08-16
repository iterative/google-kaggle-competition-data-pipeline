import argparse
from zipfile import ZipFile
from pathlib import Path
import yaml


def main(params):
    stage_params = yaml.safe_load(open(params.params))
    data_folder = Path(stage_params["data_folder"])
    input_file = Path(stage_params["unzip_dataset"]["input_file"])
    output_folder = Path(stage_params["unzip_dataset"]["output_folder"])

    data_archive_path = (data_folder/input_file).with_suffix(".zip")
    zipfile = ZipFile(data_archive_path)
    zipfile.extractall(path=data_folder/output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=str, default="params.yaml")
    args = parser.parse_args()
    main(args)
