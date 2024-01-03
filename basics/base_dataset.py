import os

import numpy as np
from torch.utils.data import Dataset

from utils.hparams import hparams
from utils.indexed_datasets import IndexedDataset


class BaseDataset(Dataset):
    """
        Base class for datasets.
        1. *sizes*:
            clipped length if "max_frames" is set;
        2. *num_frames*:
            unclipped length.

        Subclasses should define:
        1. *collate*:
            take the longest data, pad other data to the same length;
        2. *__getitem__*:
            the index function.
    """

    def __init__(self, prefix):
        super().__init__()
        self.prefix = prefix
        self.data_dir = hparams['binary_data_dir']
        self.sizes = np.load(os.path.join(self.data_dir, f'{self.prefix}.lengths'))
        self.indexed_ds = IndexedDataset(self.data_dir, self.prefix)

    @property
    def _sizes(self):
        return self.sizes

    def __getitem__(self, index):
        return self.indexed_ds[index]

    def __len__(self):
        return len(self._sizes)

    def num_frames(self, index):
        return self.size(index)

    def size(self, index):
        """Return an example's size as a float or tuple. This value is used when
        filtering a dataset with ``--max-positions``."""
        return self._sizes[index]

    def collater(self, samples):
        return {
            'size': len(samples)
        }
