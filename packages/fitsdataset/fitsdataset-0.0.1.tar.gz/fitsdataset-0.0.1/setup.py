import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fitsdataset",
    version="0.0.1",
    author="Amrit Rau",
    description="A PyTorch Dataset for the FITS file format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amritrau/fits-dataset",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['numpy', 'pandas', 'torch', 'astropy']
)
