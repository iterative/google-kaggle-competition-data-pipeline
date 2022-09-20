import json
import numpy as np
from pathlib import Path
import shutil
from tqdm import tqdm
from typing import Tuple, Dict
from zipfile import ZipFile, ZIP_DEFLATED


def stratified_sample(path_data: Path, number_of_splits: int) -> Dict:
    """Sample the number of splits from the dataset .

    Args:
        path_data (Path): [description]
        number_of_splits (int): [description]

    Returns:
        Dict: [description]
    """    
    with open(path_data/'labels.json', 'r') as file:
        labels = json.load(file)
    
    classes = list(set(labels['labels'].values()))
    classes.sort()

    classes_images = {cl:[] for cl in classes}
    for img,cl in labels['labels'].items():
        classes_images[cl].append(img)

    classes_split = {cl:np.array_split(img_list, number_of_splits) for cl,img_list in classes_images.items()}
    return classes_split

def get_img_to_partition(classes_split: Dict) -> Tuple(Dict, Dict):
    """Convert dictionary (class -> list of partitioned images) to dictionary (image_name <-> partition).

    Args:
        classes_split (Dict): [description]
        Dict ([type]): [description]

    Returns:
        [type]: [description]
    """    

      
    img_to_partition = {}
    partition_to_img = {}

    for img_lists in classes_split.values():
        for split, img_list in enumerate(img_lists):
            for img in img_list:
                img_to_partition[str(img)] = split

    
    partition_to_img = {split:[] for split in set(img_to_partition.values())}
    for img,split in img_to_partition.items():
        partition_to_img[split].append(img)

    return img_to_partition, partition_to_img


def write_to_zip(path_data: Path, output_zip_folder: Path, partition_to_img, number_of_splits: int):
    img_to_ext = {Path(path).name.split(".")[0]:Path(path).name.split(".")[1] for path in glob.glob(str(path_data/"data"/f"*.*"))}

    output_zip_folder.mkdir(parents=True, exist_ok=True)
    temp_folder = Path(output_zip_folder/'temp'/'data')

    for split, img_list in partition_to_img.items():
        temp_folder.mkdir(parents=True, exist_ok=True)

        for img in tqdm(img_list):
            shutil.copy(path_data/"data"/f"{img}.{img_to_ext[img]}", temp_folder)

        with ZipFile(output_zip_folder/f'partition_{split}.zip', "w", ZIP_DEFLATED, compresslevel=9) as archive:
            for file in (temp_folder).rglob('*'):
                archive.write(file, file.relative_to((temp_folder).parent))      
        shutil.rmtree(temp_folder.parent)

