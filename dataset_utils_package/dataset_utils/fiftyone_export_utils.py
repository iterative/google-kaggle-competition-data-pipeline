import fiftyone as fo
import fiftyone.utils.random as four
import json

from pathlib import Path
from typing import List, Dict


def create_relative_paths_in_manifest(input_manifest_path: Path, output_manifest_path: Path=None):
    """Changes my absolute paths in manifest.json into relative paths

    Args:
        input_manifest_path (Path): Path to the manifest.
        output_manifest_path (Path, optional): Path where to save the changed manifest file. Defaults to 'manifest_relative.json'.
    """

    if output_manifest_path is None:
        manifest_path_parent = input_manifest_path.absolute().parent
        output_manifest_path = manifest_path_parent/'manifest_relative.json'

    with open(input_manifest_path) as json_file:
        manifest = json.load(json_file)

    # Relative path should look like as follows: "<dataset_name>/data/img_name_with_extension"
    manifest_relative = {img_name:"/".join(Path(abs_path).parts[-3:]) for img_name, abs_path in manifest.items()}

    with open(output_manifest_path, "w") as outfile:
        json.dump(manifest_relative, outfile)


def create_absolute_paths_in_manifest(dataset_path_dic: Dict, input_manifest_path: Path, output_manifest_path: Path=None):
    """Changes my relative paths in manifest.json into absolute paths

    Args:
        input_manifest_path (Path): Path to the manifest.
        dataset_path_dic (Dict): Should be dictionary with format: {"<dataset_name>: <absolute_path_to_the_folder>"}
            For example: {"food_101_small": "/workspaces/google-kaggle-competition/datasets/food_101_small"}
        output_manifest_path (Path, optional): Path where to save the changed manifest file. Defaults to 'manifest.json'.
    """

    if output_manifest_path is None:
        manifest_path_parent = input_manifest_path.absolute().parent
        output_manifest_path = manifest_path_parent/'manifest.json'

    with open(input_manifest_path) as json_file:
        manifest_relative = json.load(json_file)

    manifest_absolute = {}
    for img_name, rel_path in manifest_relative.items():
        rel_path = Path(rel_path)
        dataset_name = Path(rel_path).parts[0]
        abs_path = Path(dataset_path_dic[dataset_name])/rel_path.parts[1]/rel_path.parts[2]
        manifest_absolute[img_name] = str(abs_path)
    
    with open(output_manifest_path, "w") as outfile:
        json.dump(manifest_absolute, outfile)


def export_manifest(view: fo.core.view.DatasetView, export_dir: Path, relative: bool=False):
    """Exports view to the given path.

    Args:
        view (fo.core.view.DatasetView): View of the dataset to be exported.
        export_dir (Path): Path where to save labels.json and manifest.json file
        relative (bool): If true, rewrites the manifest.json paths to be in the format <dataset_name>/data/<image name with extension>
    """

    view.export(export_dir=str(export_dir), 
        dataset_type=fo.types.FiftyOneImageClassificationDataset,
        label_field='ground_truth',
        data_path='manifest.json',
        labels_path='labels.json',
        export_media='manifest',
        overwrite=True
        )
    
    if relative:
        create_relative_paths_in_manifest(
            input_manifest_path=export_dir/'manifest.json',
            output_manifest_path=export_dir/'manifest.json',
            )


def merge_datasets(datasets: List[fo.core.dataset.Dataset]) -> fo.core.dataset.Dataset:
    """Merges the given dataset into one dataset

    Args:
        datasets (List[fo.core.dataset.Dataset]): List of datasets to be merged

    Returns:
        fo.core.dataset.Dataset: Merged dataset
    """    
    if len(datasets) == 0:
        return

    dataset = datasets[0].clone()
    for ds in datasets[1:]:
        dataset.merge_samples(ds)
    return dataset