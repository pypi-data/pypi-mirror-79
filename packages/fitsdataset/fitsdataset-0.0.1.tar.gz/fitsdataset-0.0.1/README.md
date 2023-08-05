FITSDataset
===

This package contains a custom PyTorch Dataset for quick and easy training on FITS files, commonly used in astronomical data analysis. In particular, the `FITSDataset` class caches FITS files as PyTorch tensors for the purpose of increasing training speed.

Contributions and feedback are welcome; please open a pull request or an issue.

## Quickstart
Using Python 3.6+, install from source with
```bash
python -m pip install git+https://github.com/amritrau/fitsdataset.git
```

Create a toy dataset with samples from the
[Hyper Suprime-Cam survey](https://www.naoj.org/Projects/HSC/) with:
```python
>>> from fitsdataset import FITSDataset
>>> dataset = FITSDataset("path/to/examples/hsc/", size=101, label_col="target")
```

Notice that the cached tensors appear in `path/to/examples/hsc/tensors`.

## Documentation
```python
>>> from fitsdataset import FITSDataset
>>> help(FITSDataset)
```
