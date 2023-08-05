from pathlib import Path

import numpy as np
import pandas as pd
from astropy.io import fits

import torch
from torch.utils.data import Dataset


class FITSDataset(Dataset):
    """Dataset from FITS files. Pre-caches FITS files as PyTorch tensors to
    improve data load speed while training."""

    def __init__(self, data_dir, size, label_col, filename_col="file_name",
                    channels=1, transform=None):
        """Instantiates a FITS dataset backed by a data directory. The data
        directory should have the following structure:

        path/to/data/
            info.csv
            cutouts/
                img1.fits
                img2.fits
                ...

        Parameters
        ----------
        data_dir : str
            The path to the data directory. This directory should contain an
            info.csv file and a subdirectory containing the FITS files titled
            cutouts/.
        label_col : str
            The name of the label column in info.csv.
        channels : int, optional
            The number of channels in the FITS images (default is 1).
        size : int or Tuple[int, int]
            The dimensions of each FITS image.
        transform : callable, optional
            Transform to apply on each input sample.

        Returns
        -------
        FITSDataset
            a PyTorch dataset
        """

        # Set data directory
        self.data_dir = Path(data_dir)
        if not self.data_dir.is_dir():
            raise OSError("{} is not a directory".format(data_dir))

        # Set cutouts shape
        shape = (size, size) if type(size) == int else size
        self.cutout_shape = (channels,) + shape

        # Set requested transforms
        self.transform = transform

        # Read the catalog CSV file
        catalog = self.data_dir / "info.csv"

        # Define paths
        self.data_info = pd.read_csv(catalog)
        self.cutouts_path = self.data_dir / "cutouts"
        self.tensors_path = self.data_dir / "tensors"
        self.tensors_path.mkdir(parents=True, exist_ok=True)

        # Retrieve labels & filenames
        self.labels = np.asarray(self.data_info[label_col])
        self.filenames = np.asarray(self.data_info[filename_col])

        # If we haven't already generated PyTorch tensor files, generate them
        for filename in self.filenames:
            filepath = self.tensors_path / (filename + ".pt")
            if not filepath.is_file():
                load_path = self.cutouts_path / filename
                t = FITSDataset.load_fits_as_tensor(load_path)
                torch.save(t, filepath)

        # Preload the tensors
        self.observations = [self.load_tensor(f) for f in self.filenames]

    def __getitem__(self, index):
        """Magic method to index into the dataset."""
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return [self[i] for i in range(start, stop, step)]
        elif isinstance(index, int):
            # Load image as tensor
            X = self.observations[index]

            # Get image label (make sure to cast to float!)
            y = torch.tensor(self.labels[index])
            y = y.unsqueeze(-1).float()

            # Transform and reshape X
            if self.transform:
                X = self.transform(X)
            X = X.view(self.cutout_shape).float()

            # Return X, y
            return X, y
        elif isinstance(index, tuple):
            raise NotImplementedError("Tuple as index")
        else:
            raise TypeError("Invalid argument type: {}".format(type(index)))

    def __len__(self):
        """Return the length of the dataset."""
        return len(self.labels)

    def load_tensor(self, filename):
        """Load a Torch tensor from disk."""
        return torch.load(self.tensors_path / (filename + ".pt"))

    @staticmethod
    def load_fits_as_tensor(filename):
        """Read a FITS file from disk and convert it to a Torch tensor."""
        fits_np = fits.getdata(filename, memmap=False)
        return torch.from_numpy(fits_np.astype(np.float32))
