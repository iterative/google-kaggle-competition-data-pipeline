import fiftyone as fo
import fiftyone.utils.random as four
from pathlib import Path
from typing import List

from dataset_utils.fiftyone_export_utils import export_manifest

def load_dataset(dataset_name: str, dataset_path: Path=None, rewrite=False, print_test=False) -> fo.core.dataset.Dataset:
    """Loads dataset into Voxel51.

    Args:
        dataset_name (str): Dataset name.
        dataset_path (Path, optional): Where where to find images of the dataset.
        rewrite (bool, optional): Rewrite the dataset if it already exists. Defaults to False.
        print_test (bool, optional): Print total number of images and images per category for a quick check. Defaults to False.

    Returns:
        fo.core.dataset.Dataset: Loaded dataset
    """

    if dataset_path is None:
        dataset_path = Path(f"../datasets/{dataset_name}/")

    if rewrite and fo.dataset_exists(dataset_name):
        dataset = fo.load_dataset(dataset_name)
        dataset.delete()

    if not fo.dataset_exists(dataset_name):
        dataset = fo.Dataset.from_dir(
            dataset_dir=dataset_path,
            dataset_type=fo.types.FiftyOneImageClassificationDataset,
            name=dataset_name
        )
    else:
        dataset = fo.load_dataset(dataset_name)

    if print_test:
        print(dataset.count())
        print(dataset.count_values('ground_truth.label'))

    return dataset


def load_and_split_dataset(dataset_name: str, export_dir: Path, dataset_path: Path=None, split_ratio: List[int]=[0.6,0.2,0.2], seed: int=51):
    """Loads and splits dataset to train,val,test sets.

    Args:
        dataset_name (str): Dataset name.
        export_dir (Path): Path where to save labels.json and manifest.json file
        dataset_path (Path, optional): Where where to find images of the dataset.
        split_ratio (List[int], optional): Split ration [train, val, test]. Defaults to [0.6,0.2,0.2].
        seed (int, optional): Split seed. Defaults to 51.
    """    

    dataset = load_dataset(dataset_name=dataset_name,
                          dataset_path=dataset_path
                        )
    split_and_export_manifest(dataset=dataset,
                            export_dir=export_dir,
                            split_ratio=split_ratio,
                            seed=seed
                            )


def split_and_export_manifest(dataset: fo.core.dataset.Dataset, export_dir: Path, split_ratio: List[int]=[0.6,0.2,0.2], seed: int=51, relative=False):
    """Split dataset to train,val,test sets and exports it.

    Args:
        dataset (fo.core.dataset.Dataset): Dataset to be splited
        export_dir (Path): Path where to save labels.json and manifest.json file
        split_ratio (List[int], optional): Split ration [train, val, test]. Defaults to [0.6,0.2,0.2].
        seed (int, optional): Split seed. Defaults to 51.
    """    

    view_train,view_val,view_test = four.random_split(dataset, split_ratio, seed=seed)
    
    export_manifest(view_train, export_dir/'train',relative=relative)
    export_manifest(view_val, export_dir/'val',relative=relative )
    export_manifest(view_test, export_dir/'test',relative=relative)