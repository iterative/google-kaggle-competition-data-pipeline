import fiftyone as fo
import fiftyone.utils.random as four
from pathlib import Path
from typing import List


def split_dataset_and_export(dataset: fo.core.dataset.Dataset, output_dir: Path, split_ratio: List[int]=[0.6,0.2,0.2], seed: int=51):
    """Split the dataset and exports it.

    Args:
        dataset (fo.core.dataset.Dataset): Dataset to be splited
        output_dir (Path): Path where to save labels.json and manifest.json file
        split_ratio (List[int], optional): Split ration [train, val, test]. Defaults to [0.6,0.2,0.2].
        seed (int, optional): Split seed. Defaults to 51.
    """    
    
    view_train,view_val,view_test = four.random_split(dataset, split_ratio, seed=seed)
    
    view_train.export(export_dir=str(output_dir/'train'), 
                    dataset_type=fo.types.FiftyOneImageClassificationDataset,
                    label_field='ground_truth',
                    data_path='manifest.json',
                    labels_path='labels.json',
                    export_media='manifest',
                    overwrite=True
                    )

    view_val.export(export_dir=str(output_dir/'val'), 
                    dataset_type=fo.types.FiftyOneImageClassificationDataset,
                    label_field='ground_truth',
                    data_path='manifest.json',
                    labels_path='labels.json',
                    export_media='manifest',
                    overwrite=True
                    )

    view_test.export(export_dir=str(output_dir/'test'), 
                    dataset_type=fo.types.FiftyOneImageClassificationDataset,
                    label_field='ground_truth',
                    data_path='manifest.json',
                    labels_path='labels.json',
                    export_media='manifest',
                    overwrite=True
                    ) 