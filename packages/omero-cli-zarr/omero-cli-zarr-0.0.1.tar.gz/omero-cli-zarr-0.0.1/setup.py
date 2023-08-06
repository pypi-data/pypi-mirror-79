from setuptools import setup

setup(
    name="omero-cli-zarr",
    version="0.0.1",
    packages=["omero_zarr", "omero.plugins"],
    package_dir={"": "src"},
    description="Plugin for exporting images in zarr format.",
    url="https://github.com/ome/omero-cli-zarr",
    author="The Open Microscopy Team",
    author_email='ome-devel@lists.openmicroscopy.org.uk',
)
