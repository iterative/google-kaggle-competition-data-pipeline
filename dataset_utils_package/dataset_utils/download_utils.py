import json
from pathlib import Path
from typing import List
import shutil
from subprocess import call


def prepare_dataset(dataset_name: str, output_path:Path, partitions: List[int]=list(range(0,10))):
    """Prepare and unzip dataset.

    Args:
        dataset_name (str): Name of the dataset from https://github.com/iterative/google-kaggle-competition-data-pipeline/tree/main/datasets
        output_path (Path): Folder where to save unzipped images and labels.json
        partitions (List[int], optional): Partitions to download. If left default, then it download the whole dataset.

    Example usage:
    prepare_dataset(dataset_name="vision_furniture", output_path=Path("../datasets/vision_furniture/"), partitions=[0])
    
    """

    (output_path/'data').mkdir(parents=True, exist_ok=True)

    # Remove old data
    shutil.rmtree(output_path/'data')

    download_and_unzip_dataset(dataset_name=dataset_name, output_path=output_path, partitions=partitions)
    get_labels(dataset_name=dataset_name, output_path=output_path, partitions=partitions)


def download_and_unzip_dataset(dataset_name: str, output_path: Path, partitions: List[int]):
    """Download and unzip a dataset .

    Args:
        dataset_name (str): Name of the dataset from https://github.com/iterative/google-kaggle-competition-data-pipeline/tree/main/datasets
        output_path (Path): Folder where to save unzipped images.
        partitions (List[int], optional): Partitions to download.
    """    

    partitions_in_output_path = {int(file.name.split("partition_")[1].split(".")[0]):file for file in output_path.iterdir() if file.name.startswith("partition_") and file.name.endswith(".zip")}

     # Download zip files
    for partition in partitions:
        zip_file_path = output_path/f"partition_{partition}.zip"
        
        print("path", zip_file_path)
        # Download zip file if not already present
        if partition not in partitions_in_output_path.keys():
            call(["dvc","get","https://github.com/iterative/google-kaggle-competition-data-pipeline",f"datasets/{dataset_name}/partition_{partition}.zip","-o",str(output_path)])            
        # Unzip all selected partitions as we have empty 'data'
        call(["unzip","-o",zip_file_path,"-d",output_path])


def get_labels(dataset_name: str, output_path: Path, partitions: List[int]):
    """Get labels from dataset .

    Args:
        dataset_name (str): Name of the dataset from https://github.com/iterative/google-kaggle-competition-data-pipeline/tree/main/datasets
        output_path (Path): Folder where to save labels.json.
        partitions (List[int], optional): Partitions which to extract from labels.json.
    """

    if (output_path/'labels.json').exists():
        (output_path/'labels.json').unlink()

    call(["dvc","get","https://github.com/iterative/google-kaggle-competition-data-pipeline",f"datasets/{dataset_name}/labels.json","-o",str(output_path)])

    with open(output_path/'labels.json', 'r') as file:
        labels = json.load(file)

    imgs_to_keep = [img for img,lbl in labels['labels'].items() if lbl['attributes']['partition'] in partitions]

    labels_to_keep = labels['labels'].copy()
    for img_name in labels['labels'].keys():
        if img_name not in imgs_to_keep:
                labels_to_keep.pop(img_name)
    labels['labels'] = labels_to_keep

    with open(output_path/"labels.json", "w") as outfile:
        json.dump(labels, outfile)
        