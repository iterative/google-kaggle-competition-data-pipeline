import argparse
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
import yaml


def main(params):
    stage_params = yaml.safe_load(open(params.params))
    data_folder = Path(stage_params["data_folder"])
    input_folder = data_folder/Path(stage_params["split_dataset"]["output_folder"])
    output_file = data_folder/Path(stage_params["zip_dataset"]["output_file"])

    with ZipFile(output_file, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for file_path in input_folder.rglob("*"):
           archive.write(file_path, arcname=file_path.relative_to(input_folder))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=str, default="params.yaml")
    args = parser.parse_args()
    main(args)
